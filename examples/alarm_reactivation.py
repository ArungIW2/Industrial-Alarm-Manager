"""A cleared fault returns before reset, so the occurrence is reused."""

from industrial_alarm_manager import (
    AlarmDefinition,
    AlarmManager,
    AlarmPriority,
    InMemoryAlarmRepository,
)

repository = InMemoryAlarmRepository()
manager = AlarmManager(repository)
definition = AlarmDefinition(
    code="COMM_FAILURE",
    name="Controller Communication Failure",
    description="Connection to the controller was lost",
    source="PLC_01",
    default_priority=AlarmPriority.HIGH,
)
manager.register_definition(definition)
alarm = manager.trigger_alarm(definition.code, definition.source)
manager.clear_alarm(alarm.occurrence_id)
reactivated = manager.trigger_alarm(definition.code, definition.source)

print("same occurrence:", alarm.occurrence_id == reactivated.occurrence_id)
print("activation count:", reactivated.activation_count)
