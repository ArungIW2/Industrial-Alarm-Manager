"""Auditable suppression rule."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.alarm_definition import ensure_aware, utc_now
from industrial_alarm_manager.exceptions import DomainValidationError


@dataclass(slots=True)
class AlarmSuppression:
    definition_id: UUID
    reason: str
    created_by: str
    created_at: datetime = field(default_factory=utc_now)
    expires_at: datetime | None = None
    active: bool = True
    suppression_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise DomainValidationError("suppression reason must not be empty")
        if not self.created_by.strip():
            raise DomainValidationError("created_by must not be empty")
        ensure_aware(self.created_at, "created_at")
        if self.expires_at is not None:
            ensure_aware(self.expires_at, "expires_at")
            if self.expires_at <= self.created_at:
                raise DomainValidationError("expires_at must be after created_at")

    def applies_at(self, timestamp: datetime) -> bool:
        return self.active and (self.expires_at is None or timestamp < self.expires_at)
