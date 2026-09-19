"""Immutable sequence-of-events record."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4

from industrial_alarm_manager.domain.alarm_definition import ensure_aware, utc_now
from industrial_alarm_manager.domain.enums import AlarmEventType, AlarmPriority, AlarmState


@dataclass(frozen=True, slots=True)
class AlarmEvent:
    occurrence_id: UUID
    definition_id: UUID
    code: str
    source: str
    priority: AlarmPriority
    event_type: AlarmEventType
    state: AlarmState
    timestamp: datetime = field(default_factory=utc_now)
    actor: str | None = None
    details: Mapping[str, Any] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        ensure_aware(self.timestamp, "timestamp")
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))
