from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from libs.domain.entities.article import Article


class ArticleRepository(ABC):
    @abstractmethod
    async def save(self, article: Article) -> None:
        """Saves or updates an article."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, article_id: UUID) -> Optional[Article]:
        """Finds an article by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_link(self, link: str) -> Optional[Article]:
        """Finds an article by its link."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_source_id(self, source_id: UUID, limit: int = 20) -> list[Article]:
        """Finds articles by source ID."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_group_id(self, group_id: UUID) -> list[Article]:
        """Finds articles by group ID."""
        raise NotImplementedError

