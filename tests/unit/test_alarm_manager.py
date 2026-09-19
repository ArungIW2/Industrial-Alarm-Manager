from industrial_alarm_manager import AlarmEventType, AlarmState


def test_complete_acknowledged_lifecycle(manager, repository, definition) -> None:
    manager.register_definition(definition)

    alarm = manager.trigger_alarm(definition.code, definition.source)
    assert alarm.state is AlarmState.ACTIVE
    assert alarm.activation_count == 1

    manager.acknowledge_alarm(alarm.occurrence_id, "operator-a")
    manager.clear_alarm(alarm.occurrence_id)
    manager.reset_alarm(alarm.occurrence_id, "operator-a")
    manager.finalize_alarm(alarm.occurrence_id)

    assert alarm.state is AlarmState.INACTIVE
    assert [event.event_type for event in repository.events] == [
        AlarmEventType.ACTIVATED,
        AlarmEventType.ACKNOWLEDGED,
        AlarmEventType.CLEARED,
        AlarmEventType.RESET,
        AlarmEventType.FINALIZED,
    ]


def test_clear_before_acknowledgement_then_ack_and_reset(manager, definition) -> None:
    manager.register_definition(definition)
    alarm = manager.trigger_alarm(definition.code, definition.source)
    manager.clear_alarm(alarm.occurrence_id)
    assert alarm.state is AlarmState.CLEARED

    manager.acknowledge_alarm(alarm.occurrence_id, "operator-b")
    assert alarm.state is AlarmState.CLEARED
    manager.reset_alarm(alarm.occurrence_id)
    assert alarm.state is AlarmState.RESET


def test_active_alarm_query_excludes_suppressed_by_default(manager, definition) -> None:
    manager.register_definition(definition)
    alarm = manager.trigger_alarm(definition.code, definition.source)
    manager.suppress_alarm(
        definition.code, definition.source, reason="Maintenance", created_by="tech"
    )

    assert manager.get_active_alarms() == []
    assert manager.get_active_alarms(include_suppressed=True) == [alarm]
