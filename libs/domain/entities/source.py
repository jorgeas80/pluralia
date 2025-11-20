from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from libs.domain.value_objects.bias import Bias
from libs.domain.errors.domain_error import InvalidDomainError


@dataclass(frozen=True)
class Source:
    id: UUID
    name: str
    url: Optional[str]
    bias: Bias

    def __post_init__(self) -> None:
        self._validate_id()
        self._validate_name()

    @classmethod
    def new(
        cls,
        name: str,
        url: Optional[str],
        bias: Bias,
        id: Optional[UUID] = None,
    ) -> "Source":
        if id is None:
            id = uuid4()
        return cls(id=id, name=name, url=url, bias=bias)

    @classmethod
    def build(
        cls,
        id: UUID,
        name: str,
        url: Optional[str],
        bias: Bias,
    ) -> "Source":
        return cls(id=id, name=name, url=url, bias=bias)

    def _validate_id(self) -> None:
        if not isinstance(self.id, UUID):
            raise InvalidDomainError("Source id must be a UUID")

    def _validate_name(self) -> None:
        if not self.name or len(self.name) > 200:
            raise InvalidDomainError("Source name must be between 1 and 200 characters")

