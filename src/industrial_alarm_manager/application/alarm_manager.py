"""Application service coordinating lifecycle, persistence, and audit events."""

from datetime import datetime
from typing import Any
from uuid import UUID

from industrial_alarm_manager.clock import Clock, SystemClock
from industrial_alarm_manager.domain import (
    AlarmAction,
    AlarmDefinition,
    AlarmEvent,
    AlarmEventType,
    AlarmOccurrence,
    AlarmPriority,
    AlarmState,
    AlarmStateMachine,
    AlarmSuppression,
)
from industrial_alarm_manager.exceptions import (
    AlarmAcknowledgementRequiredError,
    AlarmAlreadyAcknowledgedError,
    AlarmDefinitionDisabledError,
    AlarmDefinitionNotFoundError,
    AlarmNotFoundError,
    SuppressionNotFoundError,
)
from industrial_alarm_manager.storage.repository import AlarmRepository


class AlarmManager:
    def __init__(self, repository: AlarmRepository, clock: Clock | None = None) -> None:
        self.repository = repository
        self.clock = clock or SystemClock()

    def register_definition(self, definition: AlarmDefinition) -> None:
        self.repository.save_definition(definition)

    def trigger_alarm(
        self,
        code: str,
        source: str,
        *,
        message: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AlarmOccurrence:
        definition = self._definition(code, source)
        if not definition.enabled:
            raise AlarmDefinitionDisabledError(
                f"Alarm definition {definition.identity_key} is disabled"
            )
        now = self.clock.now()
        occurrence = self.repository.find_open_occurrence(code, source)

        if occurrence and occurrence.state in {AlarmState.ACTIVE, AlarmState.ACKNOWLEDGED}:
            occurrence.duplicate_count += 1
            occurrence.last_active_at = now
            if message is not None:
                occurrence.message = message
            if metadata:
                occurrence.metadata.update(metadata)
            self.repository.save_occurrence(occurrence)
            self._record(
                occurrence,
                AlarmEventType.DUPLICATE_DETECTED,
                now,
                details={"duplicate_count": occurrence.duplicate_count},
            )
            return occurrence

        if occurrence and occurrence.state is AlarmState.CLEARED:
            occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.TRIGGER)
            occurrence.last_active_at = now
            occurrence.cleared_at = None
            occurrence.acknowledged_at = None
            occurrence.acknowledged_by = None
            occurrence.escalation_count = 0
            occurrence.activation_count += 1
            occurrence.message = message or occurrence.message
            if metadata:
                occurrence.metadata.update(metadata)
            event_type = AlarmEventType.REACTIVATED
        else:
            occurrence = AlarmOccurrence.from_definition(definition)
            occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.TRIGGER)
            occurrence.first_active_at = now
            occurrence.last_active_at = now
            occurrence.activation_count = 1
            occurrence.message = message
            occurrence.metadata = dict(metadata or {})
            event_type = AlarmEventType.ACTIVATED

        suppression = self.repository.get_active_suppression(definition.definition_id, now)
        if suppression:
            occurrence.is_suppressed = True
            occurrence.suppression_reason = suppression.reason
        self.repository.save_occurrence(occurrence)
        self._record(occurrence, event_type, now)
        if suppression:
            self._record(
                occurrence,
                AlarmEventType.SUPPRESSED,
                now,
                actor=suppression.created_by,
                details={"reason": suppression.reason},
            )
        return occurrence

    def acknowledge_alarm(self, occurrence_id: UUID, actor: str) -> AlarmOccurrence:
        occurrence = self._occurrence(occurrence_id)
        if occurrence.acknowledged_at is not None:
            raise AlarmAlreadyAcknowledgedError(f"Alarm {occurrence_id} is already acknowledged")
        now = self.clock.now()
        occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.ACKNOWLEDGE)
        occurrence.acknowledged_at = now
        occurrence.acknowledged_by = actor
        self.repository.save_occurrence(occurrence)
        self._record(occurrence, AlarmEventType.ACKNOWLEDGED, now, actor=actor)
        return occurrence

    def clear_alarm(self, occurrence_id: UUID) -> AlarmOccurrence:
        occurrence = self._occurrence(occurrence_id)
        now = self.clock.now()
        occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.CLEAR)
        occurrence.cleared_at = now
        self.repository.save_occurrence(occurrence)
        self._record(occurrence, AlarmEventType.CLEARED, now)
        return occurrence

    def reset_alarm(self, occurrence_id: UUID, actor: str | None = None) -> AlarmOccurrence:
        occurrence = self._occurrence(occurrence_id)
        definition = self.repository.get_definition(occurrence.definition_id)
        if definition is None:
            raise AlarmDefinitionNotFoundError(str(occurrence.definition_id))
        if definition.ack_required and occurrence.acknowledged_at is None:
            raise AlarmAcknowledgementRequiredError(
                f"Alarm {occurrence_id} must be acknowledged before reset"
            )
        now = self.clock.now()
        occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.RESET)
        occurrence.reset_at = now
        self.repository.save_occurrence(occurrence)
        self._record(occurrence, AlarmEventType.RESET, now, actor=actor)
        return occurrence

    def finalize_alarm(self, occurrence_id: UUID) -> AlarmOccurrence:
        occurrence = self._occurrence(occurrence_id)
        now = self.clock.now()
        occurrence.state = AlarmStateMachine.transition(occurrence.state, AlarmAction.FINALIZE)
        self.repository.save_occurrence(occurrence)
        self._record(occurrence, AlarmEventType.FINALIZED, now)
        return occurrence

    def suppress_alarm(
        self,
        code: str,
        source: str,
        *,
        reason: str,
        created_by: str,
        expires_at: datetime | None = None,
    ) -> AlarmSuppression:
        definition = self._definition(code, source)
        now = self.clock.now()
        suppression = AlarmSuppression(
            definition_id=definition.definition_id,
            reason=reason,
            created_by=created_by,
            created_at=now,
            expires_at=expires_at,
        )
        self.repository.save_suppression(suppression)
        occurrence = self.repository.find_open_occurrence(code, source)
        if occurrence and occurrence.is_active:
            occurrence.is_suppressed = True
            occurrence.suppression_reason = reason
            self.repository.save_occurrence(occurrence)
            self._record(
                occurrence,
                AlarmEventType.SUPPRESSED,
                now,
                actor=created_by,
                details={"reason": reason},
            )
        return suppression

    def unsuppress_alarm(self, code: str, source: str, *, actor: str) -> None:
        definition = self._definition(code, source)
        now = self.clock.now()
        suppression = self.repository.get_active_suppression(definition.definition_id, now)
        if suppression is None:
            raise SuppressionNotFoundError(f"No active suppression for {definition.identity_key}")
        self.repository.deactivate_suppression(suppression.suppression_id)
        occurrence = self.repository.find_open_occurrence(code, source)
        if occurrence:
            occurrence.is_suppressed = False
            occurrence.suppression_reason = None
            self.repository.save_occurrence(occurrence)
            self._record(occurrence, AlarmEventType.UNSUPPRESSED, now, actor=actor)

    def get_active_alarms(
        self, *, priority: AlarmPriority | None = None, include_suppressed: bool = False
    ) -> list[AlarmOccurrence]:
        alarms = [
            *self.repository.list_occurrences(priority=priority, state=AlarmState.ACTIVE),
            *self.repository.list_occurrences(priority=priority, state=AlarmState.ACKNOWLEDGED),
        ]
        if not include_suppressed:
            alarms = [alarm for alarm in alarms if not alarm.is_suppressed]
        return sorted(alarms, key=lambda alarm: alarm.first_active_at or self.clock.now())

    def _definition(self, code: str, source: str) -> AlarmDefinition:
        definition = self.repository.find_definition(code, source)
        if definition is None:
            raise AlarmDefinitionNotFoundError(f"Alarm definition not found: {code}:{source}")
        return definition

    def _occurrence(self, occurrence_id: UUID) -> AlarmOccurrence:
        occurrence = self.repository.get_occurrence(occurrence_id)
        if occurrence is None:
            raise AlarmNotFoundError(f"Alarm occurrence not found: {occurrence_id}")
        return occurrence

    def _record(
        self,
        occurrence: AlarmOccurrence,
        event_type: AlarmEventType,
        timestamp: datetime,
        *,
        actor: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.repository.append_event(
            AlarmEvent(
                occurrence_id=occurrence.occurrence_id,
                definition_id=occurrence.definition_id,
                code=occurrence.code,
                source=occurrence.source,
                priority=occurrence.priority,
                event_type=event_type,
                state=occurrence.state,
                timestamp=timestamp,
                actor=actor,
                details=details or {},
            )
        )
