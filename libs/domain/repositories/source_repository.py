from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from libs.domain.entities.source import Source


class SourceRepository(ABC):
    @abstractmethod
    async def save(self, source: Source) -> None:
        """Saves or updates a source."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, source_id: UUID) -> Optional[Source]:
        """Finds a source by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Source]:
        """Finds a source by its name."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[Source]:
        """Finds all sources."""
        raise NotImplementedError

