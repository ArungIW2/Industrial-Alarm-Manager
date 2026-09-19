from datetime import timedelta

from industrial_alarm_manager import AlarmEventType, AlarmPriority, EscalationPolicy
from industrial_alarm_manager.application import EscalationService


def test_unacknowledged_alarm_escalates_after_threshold(
    manager, repository, definition, clock
) -> None:
    manager.register_definition(definition)
    alarm = manager.trigger_alarm(definition.code, definition.source)
    clock.value += timedelta(seconds=31)
    service = EscalationService(
        repository, [EscalationPolicy(AlarmPriority.HIGH, timedelta(seconds=30))], clock
    )

    events = service.process()

    assert len(events) == 1
    assert events[0].event_type is AlarmEventType.ESCALATED
    assert alarm.escalation_count == 1
    assert service.process() == []


def test_acknowledged_or_suppressed_alarm_does_not_escalate(
    manager, repository, definition, clock
) -> None:
    manager.register_definition(definition)
    alarm = manager.trigger_alarm(definition.code, definition.source)
    manager.acknowledge_alarm(alarm.occurrence_id, "operator")
    clock.value += timedelta(minutes=2)
    service = EscalationService(
        repository, [EscalationPolicy(AlarmPriority.HIGH, timedelta(seconds=30))], clock
    )
    assert service.process() == []
