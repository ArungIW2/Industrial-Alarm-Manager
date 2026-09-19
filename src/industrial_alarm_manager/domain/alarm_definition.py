"""Alarm definition domain model."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.enums import AlarmPriority
from industrial_alarm_manager.exceptions import DomainValidationError


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _is_timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


@dataclass(frozen=True, slots=True)
class AlarmDefinition:
    """Configuration describing what an alarm represents.

    A definition is intentionally separate from an occurrence. Configuration can
    evolve while historical occurrences preserve the values captured when they
    were created.
    """

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
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        required_text = {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "source": self.source,
            "category": self.category,
        }

        for field_name, value in required_text.items():
            if not value or not value.strip():
                raise DomainValidationError(f"{field_name} must not be empty")

        if not isinstance(self.default_priority, AlarmPriority):
            raise DomainValidationError("default_priority must be an AlarmPriority")

        if not _is_timezone_aware(self.created_at):
            raise DomainValidationError("created_at must be timezone-aware")
