"""Run one service's real repositories in an isolated SQLModel registry."""
import asyncio
from datetime import datetime, timedelta, timezone
from importlib import import_module
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from uuid import UUID, uuid4

from sqlmodel import Session, create_engine

from libs.domain.entities.article import Article


async def main(service):
    base = f"services.{service}.src"
    models = import_module(f"{base}.infrastructure.database.models")
    repository = import_module(f"{base}.infrastructure.repositories.sqlmodel_article_repository")
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        if service == "ingest":
            groups = import_module(f"{base}.infrastructure.repositories.sqlmodel_news_group_repository")
            group_repo = groups.SqlModelNewsGroupRepository(session)
            # Regression for the exact query that failed in GitHub Actions.
            assert await group_repo.find_recent(days=1) == []

        group_id, source_id = str(uuid4()), str(uuid4())
        session.add(models.SourceModel(id=source_id, name="Example", bias="center"))
        # Exercise the model's creation-time default, not a supplied test value.
        session.add(models.NewsGroupModel(id=group_id, topic_hash="0123456789abcdef"))
        session.commit()
        group = session.get(models.NewsGroupModel, group_id)
        assert group.created_at.utcoffset() == timedelta(0)
        if service == "ingest":
            old_id = str(uuid4())
            session.add(models.NewsGroupModel(
                id=old_id, topic_hash="fedcba9876543210",
                created_at=datetime.now(timezone.utc) - timedelta(days=2),
            ))
            session.commit()
            assert [str(g.id) for g in await group_repo.find_recent(days=1)] == [group_id]

        article_repo = repository.SqlModelArticleRepository(session)
        article = Article.new(
            "Story", "https://example.com/story", UUID(source_id), group_id=UUID(group_id),
            published_at=datetime(2026, 9, 27, 10, tzinfo=timezone(timedelta(hours=2))),
        )
        await article_repo.save(article)
        restored = await article_repo.find_by_id(article.id)
        assert restored.published_at.isoformat() == "2026-09-27T08:00:00+00:00"
        undated = Article.new(
            "Undated story", "https://example.com/undated", UUID(source_id),
            group_id=UUID(group_id),
        )
        await article_repo.save(undated)
        assert (await article_repo.find_by_id(undated.id)).published_at is None

        if service == "api":
            from contextlib import contextmanager
            from fastapi.testclient import TestClient
            from services.api.src.main import app
            from services.api.src.infrastructure.api import routes

            @contextmanager
            def test_session():
                yield session

            routes.get_session = test_session
            with TestClient(app) as client:
                news = client.get("/news").json()["news"]
                grouped = client.get("/groups").json()["groups"]
        else:
            static = import_module(f"{base}.generate_static_data")
            with TemporaryDirectory() as directory:
                os.environ["GITHUB_WORKSPACE"] = directory
                static.main()
                news = json.loads((Path(directory) / "services/web/public/data/news.json").read_text())["news"]
                grouped = json.loads((Path(directory) / "services/web/public/data/groups.json").read_text())["groups"]

        news_by_id = {item["id"]: item for item in news}
        assert news_by_id[str(article.id)]["published"] == "2026-09-27T08:00:00+00:00"
        assert news_by_id[str(undated.id)]["published"] is None
        assert grouped[0]["created_at"].endswith("+00:00")
        group_articles = {item["id"]: item for item in grouped[0]["articles"]}
        assert group_articles[str(article.id)]["published"] == "2026-09-27T08:00:00+00:00"
        assert group_articles[str(undated.id)]["published"] is None
    engine.dispose()


asyncio.run(main(sys.argv[1]))
