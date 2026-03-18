import json
import os
from pathlib import Path

from sqlmodel import select
from services.ingest.src.infrastructure.database.db import get_session
from services.ingest.src.infrastructure.database.models import (
    ArticleModel, NewsGroupModel, SourceModel,
)

NEWS_LIMIT = 100
GROUPS_LIMIT = 50
MIN_ARTICLES = 2


def generate_news(session) -> dict:
    rows = session.exec(
        select(ArticleModel, SourceModel)
        .join(SourceModel, ArticleModel.source_id == SourceModel.id, isouter=True)
        .order_by(ArticleModel.published_at.desc())
        .limit(NEWS_LIMIT)
    ).all()
    news = []
    for article, source in rows:
        news.append({
            "id": article.id,
            "title": article.title,
            "link": article.link,
            "description": article.description,
            "published": article.published_at.isoformat() if article.published_at else None,
            "source": source.name if source else "Desconocido",
            "bias": source.bias if source else "center",
            "sensationalism_score": article.sensationalism_score,
            "sensationalism_explanation": article.sensationalism_explanation,
        })
    return {"news": news}


def generate_groups(session) -> dict:
    rows = session.exec(
        select(ArticleModel, SourceModel)
        .join(SourceModel, ArticleModel.source_id == SourceModel.id, isouter=True)
        .where(ArticleModel.group_id.is_not(None))
    ).all()

    groups_dict: dict[str, list[dict]] = {}
    for article, source in rows:
        gid = article.group_id
        if gid not in groups_dict:
            groups_dict[gid] = []
        groups_dict[gid].append({
            "id": article.id,
            "title": article.title,
            "link": article.link,
            "description": article.description,
            "published": article.published_at.isoformat() if article.published_at else None,
            "source": source.name if source else "Desconocido",
            "bias": source.bias if source else "center",
            "sensationalism_score": article.sensationalism_score,
            "sensationalism_explanation": article.sensationalism_explanation,
        })

    qualifying_ids = [gid for gid, arts in groups_dict.items() if len(arts) >= MIN_ARTICLES]
    newsgroups = session.exec(
        select(NewsGroupModel.id, NewsGroupModel.created_at)
        .where(NewsGroupModel.id.in_(qualifying_ids))
    ).all()
    newsgroup_map = {ng.id: ng for ng in newsgroups}

    output = [
        {
            "id": gid,
            "created_at": newsgroup_map[gid].created_at.isoformat() if gid in newsgroup_map else None,
            "articles": groups_dict[gid],
        }
        for gid in qualifying_ids
    ]
    output.sort(key=lambda g: len(g["articles"]), reverse=True)
    return {"groups": output[:GROUPS_LIMIT]}


def main():
    # parents[3] sube 3 niveles desde services/ingest/src/ hasta la raíz del repo
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", str(Path(__file__).resolve().parents[3])))
    output_dir = repo_root / "services" / "web" / "public" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    with get_session() as session:
        news_data = generate_news(session)
        groups_data = generate_groups(session)

    (output_dir / "news.json").write_text(
        json.dumps(news_data, ensure_ascii=False, default=str), encoding="utf-8"
    )
    (output_dir / "groups.json").write_text(
        json.dumps(groups_data, ensure_ascii=False, default=str), encoding="utf-8"
    )
    print(f"Written {len(news_data['news'])} articles and {len(groups_data['groups'])} groups")


if __name__ == "__main__":
    main()
