"""Persist and query alarm history with SQLite."""

from industrial_alarm_manager import (
    AlarmDefinition,
    AlarmManager,
    AlarmPriority,
    EventQuery,
    HistoryQueryService,
    SQLiteAlarmRepository,
)

with SQLiteAlarmRepository("alarm_history.sqlite3") as repository:
    manager = AlarmManager(repository)
    manager.register_definition(
        AlarmDefinition(
            code="LOW_MATERIAL",
            name="Low Material",
            description="Material hopper level is low",
            source="HOPPER_01",
            default_priority=AlarmPriority.LOW,
        )
    )
    manager.trigger_alarm("LOW_MATERIAL", "HOPPER_01")
    for event in HistoryQueryService(repository).events(EventQuery(code="LOW_MATERIAL")):
        print(event.timestamp.isoformat(), event.event_type.value)
