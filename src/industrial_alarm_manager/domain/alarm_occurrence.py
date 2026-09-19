"""Alarm occurrence domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.alarm_definition import AlarmDefinition
from industrial_alarm_manager.domain.enums import AlarmPriority, AlarmState
from industrial_alarm_manager.exceptions import DomainValidationError


def _is_timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


@dataclass(slots=True)
class AlarmOccurrence:
    """A single lifecycle instance of an alarm definition."""

    definition_id: UUID
    code: str
    source: str
    priority: AlarmPriority

    occurrence_id: UUID = field(default_factory=uuid4)
    state: AlarmState = AlarmState.INACTIVE

    first_active_at: datetime | None = None
    last_active_at: datetime | None = None
    acknowledged_at: datetime | None = None
    acknowledged_by: str | None = None
    cleared_at: datetime | None = None
    reset_at: datetime | None = None

    activation_count: int = 0
    duplicate_count: int = 0

    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise DomainValidationError("code must not be empty")

        if not self.source or not self.source.strip():
            raise DomainValidationError("source must not be empty")

        if not isinstance(self.priority, AlarmPriority):
            raise DomainValidationError("priority must be an AlarmPriority")

        if not isinstance(self.state, AlarmState):
            raise DomainValidationError("state must be an AlarmState")

        if self.activation_count < 0:
            raise DomainValidationError("activation_count cannot be negative")

        if self.duplicate_count < 0:
            raise DomainValidationError("duplicate_count cannot be negative")

        timestamp_fields = {
            "first_active_at": self.first_active_at,
            "last_active_at": self.last_active_at,
            "acknowledged_at": self.acknowledged_at,
            "cleared_at": self.cleared_at,
            "reset_at": self.reset_at,
        }

        for field_name, value in timestamp_fields.items():
            if value is not None and not _is_timezone_aware(value):
                raise DomainValidationError(f"{field_name} must be timezone-aware")

    @classmethod
    def from_definition(cls, definition: AlarmDefinition) -> "AlarmOccurrence":
        """Create an inactive occurrence with a snapshot of definition data."""

        return cls(
            definition_id=definition.definition_id,
            code=definition.code,
            source=definition.source,
            priority=definition.default_priority,
        )

    @property
    def identity_key(self) -> str:
        """Logical key used later by duplicate-alarm handling."""

        return f"{self.code}:{self.source}"
