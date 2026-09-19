"""Core alarm-domain API."""

from industrial_alarm_manager.domain.alarm_definition import AlarmDefinition
from industrial_alarm_manager.domain.alarm_event import AlarmEvent
from industrial_alarm_manager.domain.alarm_occurrence import AlarmOccurrence
from industrial_alarm_manager.domain.enums import (
    AlarmAction,
    AlarmEventType,
    AlarmPriority,
    AlarmState,
)
from industrial_alarm_manager.domain.escalation import EscalationPolicy
from industrial_alarm_manager.domain.state_machine import AlarmStateMachine
from industrial_alarm_manager.domain.suppression import AlarmSuppression

__all__ = [
    "AlarmAction",
    "AlarmDefinition",
    "AlarmEvent",
    "AlarmEventType",
    "AlarmOccurrence",
    "AlarmPriority",
    "AlarmState",
    "AlarmStateMachine",
    "AlarmSuppression",
    "EscalationPolicy",
]
