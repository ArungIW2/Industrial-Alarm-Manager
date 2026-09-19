"""Fast in-memory repository for unit tests and examples."""

from datetime import UTC, datetime
from uuid import UUID

from industrial_alarm_manager.domain import (
    AlarmDefinition,
    AlarmEvent,
    AlarmOccurrence,
    AlarmPriority,
    AlarmState,
    AlarmSuppression,
)


class InMemoryAlarmRepository:
    def __init__(self) -> None:
        self.definitions: dict[UUID, AlarmDefinition] = {}
        self.occurrences: dict[UUID, AlarmOccurrence] = {}
        self.events: list[AlarmEvent] = []
        self.suppressions: dict[UUID, AlarmSuppression] = {}

    def save_definition(self, definition: AlarmDefinition) -> None:
        self.definitions[definition.definition_id] = definition

    def get_definition(self, definition_id: UUID) -> AlarmDefinition | None:
        return self.definitions.get(definition_id)

    def find_definition(self, code: str, source: str) -> AlarmDefinition | None:
        return next(
            (d for d in self.definitions.values() if d.code == code and d.source == source), None
        )

    def list_definitions(self) -> list[AlarmDefinition]:
        return sorted(self.definitions.values(), key=lambda d: (d.code, d.source))

    def save_occurrence(self, occurrence: AlarmOccurrence) -> None:
        self.occurrences[occurrence.occurrence_id] = occurrence

    def get_occurrence(self, occurrence_id: UUID) -> AlarmOccurrence | None:
        return self.occurrences.get(occurrence_id)

    def find_open_occurrence(self, code: str, source: str) -> AlarmOccurrence | None:
        open_states = {AlarmState.ACTIVE, AlarmState.ACKNOWLEDGED, AlarmState.CLEARED}
        matches = [
            o
            for o in self.occurrences.values()
            if o.code == code and o.source == source and o.state in open_states
        ]
        if not matches:
            return None
        earliest = datetime.min.replace(tzinfo=UTC)
        return max(matches, key=lambda o: o.last_active_at or o.first_active_at or earliest)

    def list_occurrences(
        self,
        *,
        priority: AlarmPriority | None = None,
        state: AlarmState | None = None,
        code: str | None = None,
        source: str | None = None,
        suppressed: bool | None = None,
    ) -> list[AlarmOccurrence]:
        result = list(self.occurrences.values())
        if priority is not None:
            result = [o for o in result if o.priority is priority]
        if state is not None:
            result = [o for o in result if o.state is state]
        if code is not None:
            result = [o for o in result if o.code == code]
        if source is not None:
            result = [o for o in result if o.source == source]
        if suppressed is not None:
            result = [o for o in result if o.is_suppressed is suppressed]
        earliest = datetime.min.replace(tzinfo=UTC)
        return sorted(result, key=lambda o: o.first_active_at or earliest)

    def append_event(self, event: AlarmEvent) -> None:
        self.events.append(event)

    def list_events(
        self,
        *,
        occurrence_id: UUID | None = None,
        event_type: str | None = None,
        code: str | None = None,
        source: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[AlarmEvent]:
        result = list(self.events)
        if occurrence_id is not None:
            result = [e for e in result if e.occurrence_id == occurrence_id]
        if event_type is not None:
            result = [e for e in result if e.event_type.value == event_type]
        if code is not None:
            result = [e for e in result if e.code == code]
        if source is not None:
            result = [e for e in result if e.source == source]
        if start_time is not None:
            result = [e for e in result if e.timestamp >= start_time]
        if end_time is not None:
            result = [e for e in result if e.timestamp <= end_time]
        return sorted(result, key=lambda e: e.timestamp)

    def save_suppression(self, suppression: AlarmSuppression) -> None:
        self.suppressions[suppression.suppression_id] = suppression

    def get_active_suppression(self, definition_id: UUID, at: datetime) -> AlarmSuppression | None:
        return next(
            (
                s
                for s in self.suppressions.values()
                if s.definition_id == definition_id and s.applies_at(at)
            ),
            None,
        )

    def deactivate_suppression(self, suppression_id: UUID) -> None:
        self.suppressions[suppression_id].active = False
