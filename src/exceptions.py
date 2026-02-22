"""Custom exceptions for the reservation system."""


class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""


class ValidationError(Exception):
    """Raised when validation fails."""


class ReservationError(Exception):
    """Raised when reservation operations fail."""
