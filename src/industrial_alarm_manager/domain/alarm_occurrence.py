"""Mutable alarm occurrence aggregate."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.alarm_definition import AlarmDefinition, ensure_aware
from industrial_alarm_manager.domain.enums import AlarmPriority, AlarmState
from industrial_alarm_manager.exceptions import DomainValidationError


@dataclass(slots=True)
class AlarmOccurrence:
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
    escalation_count: int = 0
    is_suppressed: bool = False
    suppression_reason: str | None = None
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
        for name in ("activation_count", "duplicate_count", "escalation_count"):
            if getattr(self, name) < 0:
                raise DomainValidationError(f"{name} cannot be negative")
        for name in (
            "first_active_at",
            "last_active_at",
            "acknowledged_at",
            "cleared_at",
            "reset_at",
        ):
            value = getattr(self, name)
            if value is not None:
                ensure_aware(value, name)

    @classmethod
    def from_definition(cls, definition: AlarmDefinition) -> "AlarmOccurrence":
        return cls(
            definition_id=definition.definition_id,
            code=definition.code,
            source=definition.source,
            priority=definition.default_priority,
        )

    @property
    def identity_key(self) -> str:
        return f"{self.code}:{self.source}"

    @property
    def is_active(self) -> bool:
        return self.state in {AlarmState.ACTIVE, AlarmState.ACKNOWLEDGED}
