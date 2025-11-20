from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.api.src.application.get_news import GetNews
from services.api.src.infrastructure.database.db import get_session
from services.api.src.infrastructure.repositories.sqlmodel_article_repository import SqlModelArticleRepository
from services.api.src.infrastructure.repositories.sqlmodel_source_repository import SqlModelSourceRepository

router = APIRouter()


def get_article_repository() -> SqlModelArticleRepository:
    with get_session() as session:
        return SqlModelArticleRepository(session)


def get_source_repository() -> SqlModelSourceRepository:
    with get_session() as session:
        return SqlModelSourceRepository(session)


@router.get("/news")
async def get_news(limit: int = 20):
    """Returns recent news from multiple sources."""
    with get_session() as session:
        article_repository = SqlModelArticleRepository(session)
        source_repository = SqlModelSourceRepository(session)
        use_case = GetNews(
            article_repository=article_repository,
            source_repository=source_repository,
        )
        news = await use_case.execute(limit=limit)
        return {"news": news}

