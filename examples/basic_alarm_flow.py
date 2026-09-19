"""Run with: python examples/basic_alarm_flow.py"""

from industrial_alarm_manager import (
    AlarmDefinition,
    AlarmManager,
    AlarmPriority,
    InMemoryAlarmRepository,
)

repository = InMemoryAlarmRepository()
manager = AlarmManager(repository)
definition = AlarmDefinition(
    code="MOTOR_OVERLOAD",
    name="Motor 01 Overload",
    description="Motor protection detected an overload condition",
    source="MOTOR_01",
    default_priority=AlarmPriority.HIGH,
    category="MOTOR",
)
manager.register_definition(definition)

alarm = manager.trigger_alarm(definition.code, definition.source, message="Current above limit")
manager.acknowledge_alarm(alarm.occurrence_id, actor="operator-01")
manager.clear_alarm(alarm.occurrence_id)
manager.reset_alarm(alarm.occurrence_id, actor="operator-01")

for event in repository.list_events(occurrence_id=alarm.occurrence_id):
    print(event.timestamp.isoformat(), event.code, event.event_type.value, event.state.value)
