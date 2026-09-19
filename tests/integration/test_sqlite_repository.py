from industrial_alarm_manager import AlarmDefinition, AlarmPriority, AlarmState
from industrial_alarm_manager.application import AlarmManager
from industrial_alarm_manager.storage import SQLiteAlarmRepository


def test_full_lifecycle_survives_sqlite_round_trip(tmp_path, clock) -> None:
    path = tmp_path / "alarms.sqlite3"
    definition = AlarmDefinition(
        code="ESTOP",
        name="Emergency Stop",
        description="Emergency stop is active",
        source="LINE_01",
        default_priority=AlarmPriority.CRITICAL,
    )
    with SQLiteAlarmRepository(path) as repository:
        manager = AlarmManager(repository, clock)
        manager.register_definition(definition)
        alarm = manager.trigger_alarm("ESTOP", "LINE_01", metadata={"station": 4})
        manager.acknowledge_alarm(alarm.occurrence_id, "operator")
        manager.clear_alarm(alarm.occurrence_id)
        manager.reset_alarm(alarm.occurrence_id)

    with SQLiteAlarmRepository(path) as repository:
        restored = repository.get_occurrence(alarm.occurrence_id)
        assert restored is not None
        assert restored.state is AlarmState.RESET
        assert restored.metadata == {"station": 4}
        assert len(repository.list_events(occurrence_id=alarm.occurrence_id)) == 4
