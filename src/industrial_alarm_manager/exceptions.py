"""Domain-specific exceptions."""


class AlarmError(Exception):
    """Base exception for alarm-domain errors."""


class DomainValidationError(AlarmError, ValueError):
    """Raised when a domain object contains invalid data."""


class InvalidAlarmTransitionError(AlarmError):
    """Raised when a lifecycle transition is not permitted."""


class AlarmNotFoundError(AlarmError):
    """Raised when an occurrence cannot be found."""


class AlarmDefinitionNotFoundError(AlarmError):
    """Raised when an alarm definition cannot be found."""


class AlarmDefinitionDisabledError(AlarmError):
    """Raised when a disabled definition is triggered."""


class AlarmAlreadyAcknowledgedError(AlarmError):
    """Raised when an occurrence has already been acknowledged."""


class AlarmAcknowledgementRequiredError(AlarmError):
    """Raised when reset is requested before required acknowledgement."""


class SuppressionNotFoundError(AlarmError):
    """Raised when no active suppression exists for a definition."""
