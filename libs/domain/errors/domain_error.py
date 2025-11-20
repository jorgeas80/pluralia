class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class InvalidDomainError(DomainError):
    """Raised when domain validation fails."""
    pass


class ResourceNotFound(DomainError):
    """Raised when a requested resource is not found."""
    pass

