import hashlib
from dataclasses import dataclass
from libs.domain.errors.domain_error import InvalidDomainError


@dataclass(frozen=True)
class TopicHash:
    value: str

    def __post_init__(self) -> None:
        self._validate_value()

    @classmethod
    def from_title(cls, title: str) -> "TopicHash":
        """Creates a topic hash from a normalized title."""
        normalized = title.lower().strip()
        hash_value = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
        return cls(value=hash_value)

    def _validate_value(self) -> None:
        if not self.value or len(self.value) != 16:
            raise InvalidDomainError("TopicHash must be exactly 16 characters")

