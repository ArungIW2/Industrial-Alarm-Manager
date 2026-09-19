"""Domain-specific exceptions for Industrial Alarm Manager."""


class AlarmError(Exception):
    """Base exception for alarm-domain errors."""


class DomainValidationError(AlarmError, ValueError):
    """Raised when a domain object is constructed with invalid data."""


class InvalidAlarmTransitionError(AlarmError):
    """Raised when an alarm lifecycle transition is not permitted."""


class AlarmNotFoundError(AlarmError):
    """Raised when an alarm occurrence cannot be found."""
