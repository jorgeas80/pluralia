from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from libs.domain.errors.domain_error import InvalidDomainError


@dataclass(frozen=True)
class Article:
    id: UUID
    title: str
    link: str
    description: Optional[str]
    published_at: Optional[datetime]
    source_id: UUID
    group_id: Optional[UUID] = None
    sensationalism_score: Optional[float] = None
    sensationalism_explanation: Optional[str] = None
    analysis_metadata: Optional[dict] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_id()
        self._validate_title()
        self._validate_link()
        self._validate_source_id()
        self._validate_sensationalism_score()

    @classmethod
    def new(
        cls,
        title: str,
        link: str,
        source_id: UUID,
        description: Optional[str] = None,
        published_at: Optional[datetime] = None,
        group_id: Optional[UUID] = None,
        sensationalism_score: Optional[float] = None,
        sensationalism_explanation: Optional[str] = None,
        analysis_metadata: Optional[dict] = None,
        id: Optional[UUID] = None,
    ) -> "Article":
        if id is None:
            id = uuid4()
        return cls(
            id=id,
            title=title,
            link=link,
            description=description,
            published_at=published_at,
            source_id=source_id,
            group_id=group_id,
            sensationalism_score=sensationalism_score,
            sensationalism_explanation=sensationalism_explanation,
            analysis_metadata=analysis_metadata or {},
        )

    @classmethod
    def build(
        cls,
        id: UUID,
        title: str,
        link: str,
        source_id: UUID,
        description: Optional[str],
        published_at: Optional[datetime],
        group_id: Optional[UUID],
        sensationalism_score: Optional[float] = None,
        sensationalism_explanation: Optional[str] = None,
        analysis_metadata: Optional[dict] = None,
    ) -> "Article":
        return cls(
            id=id,
            title=title,
            link=link,
            description=description,
            published_at=published_at,
            source_id=source_id,
            group_id=group_id,
            sensationalism_score=sensationalism_score,
            sensationalism_explanation=sensationalism_explanation,
            analysis_metadata=analysis_metadata or {},
        )

    def assign_to_group(self, group_id: UUID) -> "Article":
        """Assigns the article to a news group."""
        return self.__class__(
            id=self.id,
            title=self.title,
            link=self.link,
            description=self.description,
            published_at=self.published_at,
            source_id=self.source_id,
            group_id=group_id,
            sensationalism_score=self.sensationalism_score,
            sensationalism_explanation=self.sensationalism_explanation,
            analysis_metadata=self.analysis_metadata,
        )

    def _validate_id(self) -> None:
        if not isinstance(self.id, UUID):
            raise InvalidDomainError("Article id must be a UUID")

    def _validate_title(self) -> None:
        if not self.title or len(self.title) > 500:
            raise InvalidDomainError("Article title must be between 1 and 500 characters")

    def _validate_link(self) -> None:
        if not self.link or len(self.link) > 1000:
            raise InvalidDomainError("Article link must be between 1 and 1000 characters")
        if not self.link.startswith(("http://", "https://")):
            raise InvalidDomainError("Article link must be a valid URL")

    def _validate_source_id(self) -> None:
        if not isinstance(self.source_id, UUID):
            raise InvalidDomainError("Article source_id must be a UUID")

    def _validate_sensationalism_score(self) -> None:
        if self.sensationalism_score is not None:
            if not isinstance(self.sensationalism_score, float):
                 raise InvalidDomainError("Sensationalism score must be a float")
            if not (0.0 <= self.sensationalism_score <= 1.0):
                raise InvalidDomainError("Sensationalism score must be between 0.0 and 1.0")
