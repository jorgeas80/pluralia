from typing import Optional
from uuid import UUID, uuid5, NAMESPACE_DNS
from sqlmodel import Session, select

from libs.domain.entities.article import Article
from libs.domain.repositories.article_repository import ArticleRepository
from services.ingest.src.infrastructure.database.models import ArticleModel


class SqlModelArticleRepository(ArticleRepository):
    def __init__(self, session: Session):
        self._session = session

    async def save(self, article: Article) -> None:
        article_model = self._to_model(article)
        self._session.add(article_model)
        self._session.commit()
        self._session.refresh(article_model)

    async def find_by_id(self, article_id: UUID) -> Optional[Article]:
        result = self._session.exec(select(ArticleModel).where(ArticleModel.id == str(article_id))).first()
        return self._to_entity(result) if result else None

    async def find_by_link(self, link: str) -> Optional[Article]:
        result = self._session.exec(select(ArticleModel).where(ArticleModel.link == link)).first()
        return self._to_entity(result) if result else None

    async def find_by_source_id(self, source_id: UUID, limit: int = 20) -> list[Article]:
        results = self._session.exec(
            select(ArticleModel).where(ArticleModel.source_id == str(source_id)).limit(limit)
        ).all()
        return [self._to_entity(model) for model in results]

    async def find_by_group_id(self, group_id: UUID) -> list[Article]:
        results = self._session.exec(select(ArticleModel).where(ArticleModel.group_id == str(group_id))).all()
        return [self._to_entity(model) for model in results]

    def _to_model(self, article: Article) -> ArticleModel:
        return ArticleModel(
            id=str(article.id),
            title=article.title,
            link=article.link,
            description=article.description,
            published_at=article.published_at,
            source_id=str(article.source_id),
            group_id=str(article.group_id) if article.group_id else None,
        )

    def _to_entity(self, model: ArticleModel) -> Article:
        # Handle both int (from existing DB stored as string) and str (UUID) IDs
        def _to_uuid(value: str, prefix: str) -> UUID:
            if not value:
                raise ValueError("Value cannot be None")
            try:
                # Try to parse as int first (for existing data)
                int_id = int(value)
                return uuid5(NAMESPACE_DNS, f"{prefix}-{int_id}")
            except (ValueError, TypeError):
                # Not an int, try to parse as UUID
                try:
                    return UUID(value)
                except (ValueError, AttributeError):
                    # Fallback: generate UUID from string
                    return uuid5(NAMESPACE_DNS, f"{prefix}-{value}")
        
        model_id = _to_uuid(model.id, "article")
        source_id = _to_uuid(model.source_id, "source") if model.source_id else None
        group_id = _to_uuid(model.group_id, "newsgroup") if model.group_id else None
        
        return Article.build(
            id=model_id,
            title=model.title,
            link=model.link,
            description=model.description,
            published_at=model.published_at,
            source_id=source_id,
            group_id=group_id,
        )

