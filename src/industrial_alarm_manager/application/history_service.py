"""Read-side filtering for occurrences and sequence-of-events history."""

from dataclasses import dataclass
from datetime import datetime

from industrial_alarm_manager.domain import (
    AlarmEvent,
    AlarmEventType,
    AlarmOccurrence,
    AlarmPriority,
    AlarmState,
)
from industrial_alarm_manager.storage.repository import AlarmRepository


@dataclass(frozen=True, slots=True)
class AlarmQuery:
    priority: AlarmPriority | None = None
    state: AlarmState | None = None
    code: str | None = None
    source: str | None = None
    suppressed: bool | None = None


@dataclass(frozen=True, slots=True)
class EventQuery:
    event_type: AlarmEventType | None = None
    code: str | None = None
    source: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class HistoryQueryService:
    def __init__(self, repository: AlarmRepository) -> None:
        self.repository = repository

    def occurrences(self, query: AlarmQuery | None = None) -> list[AlarmOccurrence]:
        query = query or AlarmQuery()
        return self.repository.list_occurrences(
            priority=query.priority,
            state=query.state,
            code=query.code,
            source=query.source,
            suppressed=query.suppressed,
        )

    def events(self, query: EventQuery | None = None) -> list[AlarmEvent]:
        query = query or EventQuery()
        return self.repository.list_events(
            event_type=query.event_type.value if query.event_type else None,
            code=query.code,
            source=query.source,
            start_time=query.start_time,
            end_time=query.end_time,
        )

    def most_frequent(self, limit: int = 10) -> list[AlarmOccurrence]:
        return sorted(
            self.repository.list_occurrences(),
            key=lambda alarm: alarm.activation_count + alarm.duplicate_count,
            reverse=True,
        )[:limit]
