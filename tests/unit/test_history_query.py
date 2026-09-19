from industrial_alarm_manager import AlarmEventType, AlarmPriority, AlarmState
from industrial_alarm_manager.application import AlarmQuery, EventQuery, HistoryQueryService


def test_occurrences_filter_by_priority_and_state(manager, repository, definition) -> None:
    manager.register_definition(definition)
    manager.trigger_alarm(definition.code, definition.source)
    service = HistoryQueryService(repository)

    result = service.occurrences(AlarmQuery(priority=AlarmPriority.HIGH, state=AlarmState.ACTIVE))

    assert len(result) == 1
    assert service.occurrences(AlarmQuery(priority=AlarmPriority.LOW)) == []


def test_event_history_filters_by_type(manager, repository, definition) -> None:
    manager.register_definition(definition)
    manager.trigger_alarm(definition.code, definition.source)
    manager.trigger_alarm(definition.code, definition.source)
    service = HistoryQueryService(repository)

    duplicates = service.events(EventQuery(event_type=AlarmEventType.DUPLICATE_DETECTED))

    assert len(duplicates) == 1
