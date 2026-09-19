from datetime import datetime

import pytest

from industrial_alarm_manager.domain.alarm_definition import AlarmDefinition
from industrial_alarm_manager.domain.alarm_occurrence import AlarmOccurrence
from industrial_alarm_manager.domain.enums import AlarmPriority, AlarmState
from industrial_alarm_manager.exceptions import DomainValidationError


def make_definition() -> AlarmDefinition:
    return AlarmDefinition(
        code="COMM_FAILURE_PLC_01",
        name="PLC 01 Communication Failure",
        description="Communication to PLC 01 is unavailable.",
        source="PLC_01",
        default_priority=AlarmPriority.HIGH,
        category="COMMUNICATION",
    )


def test_occurrence_is_created_from_definition() -> None:
    definition = make_definition()

    occurrence = AlarmOccurrence.from_definition(definition)

    assert occurrence.definition_id == definition.definition_id
    assert occurrence.code == definition.code
    assert occurrence.source == definition.source
    assert occurrence.priority is AlarmPriority.HIGH
    assert occurrence.state is AlarmState.INACTIVE
    assert occurrence.activation_count == 0
    assert occurrence.duplicate_count == 0


def test_occurrence_has_logical_identity_key() -> None:
    occurrence = AlarmOccurrence.from_definition(make_definition())

    assert occurrence.identity_key == "COMM_FAILURE_PLC_01:PLC_01"


def test_metadata_is_not_shared_between_occurrences() -> None:
    definition = make_definition()
    first = AlarmOccurrence.from_definition(definition)
    second = AlarmOccurrence.from_definition(definition)

    first.metadata["diagnostic_code"] = "TIMEOUT"

    assert second.metadata == {}


def test_occurrence_rejects_negative_duplicate_count() -> None:
    definition = make_definition()

    with pytest.raises(DomainValidationError, match="duplicate_count cannot be negative"):
        AlarmOccurrence(
            definition_id=definition.definition_id,
            code=definition.code,
            source=definition.source,
            priority=definition.default_priority,
            duplicate_count=-1,
        )


def test_occurrence_rejects_naive_timestamps() -> None:
    definition = make_definition()

    with pytest.raises(DomainValidationError, match="first_active_at must be timezone-aware"):
        AlarmOccurrence(
            definition_id=definition.definition_id,
            code=definition.code,
            source=definition.source,
            priority=definition.default_priority,
            first_active_at=datetime(2026, 9, 19, 0, 0, 0),
        )
