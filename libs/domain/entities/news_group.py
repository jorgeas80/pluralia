from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from libs.domain.value_objects.topic_hash import TopicHash
from libs.domain.errors.domain_error import InvalidDomainError


@dataclass(frozen=True)
class NewsGroup:
    id: UUID
    topic_hash: TopicHash
    summary: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    embedding: Optional[list[float]] = field(default=None, compare=False, hash=False)

    def __post_init__(self) -> None:
        self._validate_id()
        self._validate_summary()
        if self.created_at.utcoffset() is None:
            raise InvalidDomainError("NewsGroup created_at must have timezone information")
        object.__setattr__(self, "created_at", self.created_at.astimezone(timezone.utc))

    @classmethod
    def new(
        cls,
        topic_hash: TopicHash,
        summary: Optional[str] = None,
        id: Optional[UUID] = None,
        embedding: Optional[list[float]] = None,
    ) -> "NewsGroup":
        if id is None:
            id = uuid4()
        return cls(
            id=id,
            topic_hash=topic_hash,
            summary=summary,
            created_at=datetime.now(timezone.utc),
            embedding=embedding,
        )

    @classmethod
    def build(
        cls,
        id: UUID,
        topic_hash: TopicHash,
        summary: Optional[str],
        created_at: datetime,
        embedding: Optional[list[float]] = None,
    ) -> "NewsGroup":
        return cls(
            id=id,
            topic_hash=topic_hash,
            summary=summary,
            created_at=created_at,
            embedding=embedding,
        )

    def _validate_id(self) -> None:
        if not isinstance(self.id, UUID):
            raise InvalidDomainError("NewsGroup id must be a UUID")

    def _validate_summary(self) -> None:
        if self.summary and len(self.summary) > 2000:
            raise InvalidDomainError("NewsGroup summary must be less than 2000 characters")
