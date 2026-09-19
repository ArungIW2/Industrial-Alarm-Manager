"""Persistence ports owned by the application/domain boundary."""

from datetime import datetime
from typing import Protocol
from uuid import UUID

from industrial_alarm_manager.domain import (
    AlarmDefinition,
    AlarmEvent,
    AlarmOccurrence,
    AlarmPriority,
    AlarmState,
    AlarmSuppression,
)


class AlarmRepository(Protocol):
    def save_definition(self, definition: AlarmDefinition) -> None: ...
    def get_definition(self, definition_id: UUID) -> AlarmDefinition | None: ...
    def find_definition(self, code: str, source: str) -> AlarmDefinition | None: ...
    def list_definitions(self) -> list[AlarmDefinition]: ...

    def save_occurrence(self, occurrence: AlarmOccurrence) -> None: ...
    def get_occurrence(self, occurrence_id: UUID) -> AlarmOccurrence | None: ...
    def find_open_occurrence(self, code: str, source: str) -> AlarmOccurrence | None: ...
    def list_occurrences(
        self,
        *,
        priority: AlarmPriority | None = None,
        state: AlarmState | None = None,
        code: str | None = None,
        source: str | None = None,
        suppressed: bool | None = None,
    ) -> list[AlarmOccurrence]: ...

    def append_event(self, event: AlarmEvent) -> None: ...
    def list_events(
        self,
        *,
        occurrence_id: UUID | None = None,
        event_type: str | None = None,
        code: str | None = None,
        source: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[AlarmEvent]: ...

    def save_suppression(self, suppression: AlarmSuppression) -> None: ...
    def get_active_suppression(
        self, definition_id: UUID, at: datetime
    ) -> AlarmSuppression | None: ...
    def deactivate_suppression(self, suppression_id: UUID) -> None: ...


class ClosableRepository(Protocol):
    def close(self) -> None: ...
