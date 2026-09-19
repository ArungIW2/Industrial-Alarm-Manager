"""Alarm definition domain model."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.enums import AlarmPriority
from industrial_alarm_manager.exceptions import DomainValidationError


def utc_now() -> datetime:
    return datetime.now(UTC)


def ensure_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class AlarmDefinition:
    """Configuration describing what an alarm represents."""

    code: str
    name: str
    description: str
    source: str
    default_priority: AlarmPriority
    category: str = "GENERAL"
    ack_required: bool = True
    reset_required: bool = True
    enabled: bool = True
    definition_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        for name in ("code", "name", "description", "source", "category"):
            value = getattr(self, name)
            if not value or not value.strip():
                raise DomainValidationError(f"{name} must not be empty")
        if not isinstance(self.default_priority, AlarmPriority):
            raise DomainValidationError("default_priority must be an AlarmPriority")
        ensure_aware(self.created_at, "created_at")

    @property
    def identity_key(self) -> str:
        return f"{self.code}:{self.source}"
