from datetime import datetime

from sqlmodel import Session, delete, select

from libs.domain.news_policy import news_retention_cutoff
from services.ingest.src.infrastructure.database.models import ArticleModel, NewsGroupModel


def cleanup_old_news(session: Session, now: datetime | None = None) -> tuple[int, int]:
    """Delete articles outside the live window and groups left without articles."""
    cutoff = news_retention_cutoff(now)
    deleted_articles = session.exec(
        delete(ArticleModel).where(
            ArticleModel.published_at.is_(None) | (ArticleModel.published_at < cutoff)
        )
    ).rowcount or 0
    deleted_groups = session.exec(
        delete(NewsGroupModel).where(
            ~NewsGroupModel.id.in_(
                select(ArticleModel.group_id).where(ArticleModel.group_id.is_not(None))
            )
        )
    ).rowcount or 0
    session.commit()
    return deleted_articles, deleted_groups
