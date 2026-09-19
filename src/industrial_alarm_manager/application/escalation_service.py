"""Timeout-driven escalation evaluation."""

from datetime import datetime

from industrial_alarm_manager.clock import Clock, SystemClock
from industrial_alarm_manager.domain import (
    AlarmEvent,
    AlarmEventType,
    AlarmState,
    EscalationPolicy,
)
from industrial_alarm_manager.storage.repository import AlarmRepository


class EscalationService:
    def __init__(
        self,
        repository: AlarmRepository,
        policies: list[EscalationPolicy],
        clock: Clock | None = None,
    ) -> None:
        self.repository = repository
        self.policies = {policy.priority: policy for policy in policies}
        self.clock = clock or SystemClock()

    def process(self) -> list[AlarmEvent]:
        now = self.clock.now()
        generated: list[AlarmEvent] = []
        for priority, policy in self.policies.items():
            alarms = self.repository.list_occurrences(priority=priority, state=AlarmState.ACTIVE)
            for alarm in alarms:
                if alarm.is_suppressed or alarm.first_active_at is None:
                    continue
                if alarm.escalation_count >= policy.max_escalations:
                    continue
                if now - alarm.first_active_at < policy.acknowledgement_timeout:
                    continue
                alarm.escalation_count += 1
                self.repository.save_occurrence(alarm)
                event = AlarmEvent(
                    occurrence_id=alarm.occurrence_id,
                    definition_id=alarm.definition_id,
                    code=alarm.code,
                    source=alarm.source,
                    priority=alarm.priority,
                    event_type=AlarmEventType.ESCALATED,
                    state=alarm.state,
                    timestamp=now,
                    details={
                        "level": alarm.escalation_count,
                        "unacknowledged_seconds": self._elapsed(now, alarm.first_active_at),
                    },
                )
                self.repository.append_event(event)
                generated.append(event)
        return generated

    @staticmethod
    def _elapsed(now: datetime, started: datetime) -> int:
        return int((now - started).total_seconds())
