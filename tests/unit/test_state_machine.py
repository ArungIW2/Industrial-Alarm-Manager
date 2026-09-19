import pytest

from industrial_alarm_manager.domain import AlarmAction, AlarmState, AlarmStateMachine
from industrial_alarm_manager.exceptions import InvalidAlarmTransitionError


@pytest.mark.parametrize(
    ("current", "action", "expected"),
    [
        (AlarmState.INACTIVE, AlarmAction.TRIGGER, AlarmState.ACTIVE),
        (AlarmState.ACTIVE, AlarmAction.ACKNOWLEDGE, AlarmState.ACKNOWLEDGED),
        (AlarmState.ACTIVE, AlarmAction.CLEAR, AlarmState.CLEARED),
        (AlarmState.ACKNOWLEDGED, AlarmAction.CLEAR, AlarmState.CLEARED),
        (AlarmState.CLEARED, AlarmAction.ACKNOWLEDGE, AlarmState.CLEARED),
        (AlarmState.CLEARED, AlarmAction.TRIGGER, AlarmState.ACTIVE),
        (AlarmState.CLEARED, AlarmAction.RESET, AlarmState.RESET),
        (AlarmState.RESET, AlarmAction.FINALIZE, AlarmState.INACTIVE),
    ],
)
def test_valid_transition(current: AlarmState, action: AlarmAction, expected: AlarmState) -> None:
    assert AlarmStateMachine.transition(current, action) is expected


@pytest.mark.parametrize(
    ("current", "action"),
    [
        (AlarmState.INACTIVE, AlarmAction.ACKNOWLEDGE),
        (AlarmState.ACTIVE, AlarmAction.RESET),
        (AlarmState.ACKNOWLEDGED, AlarmAction.TRIGGER),
        (AlarmState.RESET, AlarmAction.CLEAR),
    ],
)
def test_invalid_transition_is_rejected(current: AlarmState, action: AlarmAction) -> None:
    with pytest.raises(InvalidAlarmTransitionError, match="Invalid alarm transition"):
        AlarmStateMachine.transition(current, action)
