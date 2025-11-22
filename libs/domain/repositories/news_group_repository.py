from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from libs.domain.entities.news_group import NewsGroup
from libs.domain.value_objects.topic_hash import TopicHash


class NewsGroupRepository(ABC):
    @abstractmethod
    async def save(self, group: NewsGroup) -> None:
        """Saves or updates a news group."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, group_id: UUID) -> Optional[NewsGroup]:
        """Finds a news group by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_topic_hash(self, topic_hash: TopicHash) -> Optional[NewsGroup]:
        """Finds a news group by its topic hash."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[NewsGroup]:
        """Finds all news groups."""
        raise NotImplementedError

