from datetime import datetime, timedelta, timezone

from sqlmodel import Session, SQLModel, create_engine

from services.ingest.src.application.cleanup_old_news import cleanup_old_news
from services.ingest.src.generate_static_data import generate_groups, generate_news
from services.ingest.src.infrastructure.database.models import ArticleModel, NewsGroupModel


def add_group(session, group_id, created_at):
    session.add(NewsGroupModel(id=group_id, topic_hash=group_id, created_at=created_at))


def add_article(session, article_id, group_id, published_at):
    session.add(ArticleModel(
        id=article_id,
        group_id=group_id,
        title=article_id,
        link=f"https://example.com/{article_id}",
        published_at=published_at,
    ))


def test_generation(session, now):
    add_group(session, "old", now - timedelta(days=10))
    for i in range(4):
        add_article(session, f"old-{i}", "old", now - timedelta(days=10))

    add_group(session, "recent", now - timedelta(days=1))
    add_article(session, "recent-a", "recent", now - timedelta(hours=3))
    add_article(session, "recent-b", "recent", now - timedelta(hours=2))

    add_group(session, "latest", now - timedelta(hours=1))
    add_article(session, "latest-a", "latest", now - timedelta(minutes=30))
    add_article(session, "latest-b", "latest", now - timedelta(minutes=20))

    add_group(session, "single", now - timedelta(hours=1))
    add_article(session, "single-a", "single", now - timedelta(hours=1))
    session.commit()

    groups = generate_groups(session, now=now)
    news = generate_news(session, now=now)
    assert [group["id"] for group in groups["groups"]] == ["latest", "recent"]
    assert {article["id"] for article in news["news"]} == {
        "recent-a", "recent-b", "latest-a", "latest-b", "single-a"
    }


def test_cleanup(session, now):
    add_group(session, "expired", now - timedelta(days=8))
    add_article(session, "expired-a", "expired", now - timedelta(days=8))
    add_group(session, "live", now - timedelta(days=1))
    add_article(session, "live-a", "live", now - timedelta(days=1))
    session.commit()

    deleted_articles, deleted_groups = cleanup_old_news(session, now=now)

    assert session.get(ArticleModel, "expired-a") is None
    assert session.get(ArticleModel, "live-a") is not None
    assert session.get(NewsGroupModel, "expired") is None
    assert session.get(NewsGroupModel, "live") is not None
    assert (deleted_articles, deleted_groups) == (1, 1)


def main():
    assert not ArticleModel.__table__.c.published_at.nullable
    now = datetime(2026, 9, 29, 12, tzinfo=timezone.utc)
    for test in (test_generation, test_cleanup):
        engine = create_engine("sqlite://")
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            test(session, now)
        engine.dispose()


if __name__ == "__main__":
    main()
