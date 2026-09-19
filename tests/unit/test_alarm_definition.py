from datetime import datetime

import pytest

from industrial_alarm_manager import AlarmDefinition, AlarmPriority
from industrial_alarm_manager.exceptions import DomainValidationError


def make_definition() -> AlarmDefinition:
    return AlarmDefinition(
        code="MOTOR_01_OVERLOAD",
        name="Motor 01 Overload",
        description="Motor protection detected an overload condition.",
        source="MOTOR_01",
        default_priority=AlarmPriority.HIGH,
        category="MOTOR",
    )


def test_alarm_definition_is_created_with_utc_timestamp() -> None:
    definition = make_definition()
    assert definition.code == "MOTOR_01_OVERLOAD"
    assert definition.created_at.tzinfo is not None


def test_alarm_definition_rejects_blank_required_text() -> None:
    with pytest.raises(DomainValidationError, match="code must not be empty"):
        AlarmDefinition(
            code=" ",
            name="Motor Overload",
            description="Overload condition.",
            source="MOTOR_01",
            default_priority=AlarmPriority.HIGH,
        )


def test_alarm_definition_rejects_naive_timestamp() -> None:
    with pytest.raises(DomainValidationError, match="created_at must be timezone-aware"):
        AlarmDefinition(
            code="MOTOR_01_OVERLOAD",
            name="Motor 01 Overload",
            description="Overload condition.",
            source="MOTOR_01",
            default_priority=AlarmPriority.HIGH,
            created_at=datetime(2026, 9, 19),
        )
