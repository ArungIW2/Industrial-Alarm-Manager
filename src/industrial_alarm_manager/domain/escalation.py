"""Priority-based escalation policy."""

from dataclasses import dataclass
from datetime import timedelta

from industrial_alarm_manager.domain.enums import AlarmPriority
from industrial_alarm_manager.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class EscalationPolicy:
    priority: AlarmPriority
    acknowledgement_timeout: timedelta
    max_escalations: int = 1

    def __post_init__(self) -> None:
        if self.acknowledgement_timeout.total_seconds() <= 0:
            raise DomainValidationError("acknowledgement_timeout must be positive")
        if self.max_escalations < 1:
            raise DomainValidationError("max_escalations must be at least one")
