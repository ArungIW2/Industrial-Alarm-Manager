"""Suppression blocks escalation but preserves the audit trail."""

from datetime import timedelta

from industrial_alarm_manager import (
    AlarmDefinition,
    AlarmManager,
    AlarmPriority,
    EscalationPolicy,
    EscalationService,
    InMemoryAlarmRepository,
)

repository = InMemoryAlarmRepository()
manager = AlarmManager(repository)
definition = AlarmDefinition(
    code="HIGH_TEMPERATURE",
    name="High Temperature",
    description="Process temperature exceeded the configured limit",
    source="OVEN_01",
    default_priority=AlarmPriority.CRITICAL,
)
manager.register_definition(definition)
manager.suppress_alarm(
    definition.code,
    definition.source,
    reason="Planned hot commissioning",
    created_by="commissioning-engineer",
)
manager.trigger_alarm(definition.code, definition.source)

service = EscalationService(
    repository,
    [EscalationPolicy(AlarmPriority.CRITICAL, timedelta(seconds=30))],
)
print("escalations:", service.process())
print("audit events:", [event.event_type.value for event in repository.events])
