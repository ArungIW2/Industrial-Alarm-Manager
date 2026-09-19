from industrial_alarm_manager import AlarmEventType, AlarmState


def test_repeated_signal_is_duplicate_not_new_occurrence(manager, repository, definition) -> None:
    manager.register_definition(definition)
    first = manager.trigger_alarm(definition.code, definition.source)
    second = manager.trigger_alarm(definition.code, definition.source)

    assert first.occurrence_id == second.occurrence_id
    assert second.duplicate_count == 1
    assert len(repository.occurrences) == 1
    assert repository.events[-1].event_type is AlarmEventType.DUPLICATE_DETECTED


def test_fault_return_before_reset_reactivates_same_occurrence(
    manager, repository, definition
) -> None:
    manager.register_definition(definition)
    alarm = manager.trigger_alarm(definition.code, definition.source)
    manager.acknowledge_alarm(alarm.occurrence_id, "operator")
    manager.clear_alarm(alarm.occurrence_id)

    reactivated = manager.trigger_alarm(definition.code, definition.source)

    assert reactivated.occurrence_id == alarm.occurrence_id
    assert reactivated.state is AlarmState.ACTIVE
    assert reactivated.activation_count == 2
    assert reactivated.acknowledged_at is None
    assert repository.events[-1].event_type is AlarmEventType.REACTIVATED
