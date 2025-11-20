from dataclasses import dataclass
from libs.domain.errors.domain_error import InvalidDomainError


@dataclass(frozen=True)
class Bias:
    value: str

    def __post_init__(self) -> None:
        self._validate_value()

    @classmethod
    def left(cls) -> "Bias":
        return cls(value="left")

    @classmethod
    def center(cls) -> "Bias":
        return cls(value="center")

    @classmethod
    def right(cls) -> "Bias":
        return cls(value="right")

    def _validate_value(self) -> None:
        valid_values = {"left", "center", "right"}
        if self.value not in valid_values:
            raise InvalidDomainError(f"Bias must be one of {valid_values}, got: {self.value}")

