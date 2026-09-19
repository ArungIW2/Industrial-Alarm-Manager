"""Pure alarm lifecycle transition rules."""

from industrial_alarm_manager.domain.enums import AlarmAction, AlarmState
from industrial_alarm_manager.exceptions import InvalidAlarmTransitionError


class AlarmStateMachine:
    _TRANSITIONS = {
        (AlarmState.INACTIVE, AlarmAction.TRIGGER): AlarmState.ACTIVE,
        (AlarmState.ACTIVE, AlarmAction.ACKNOWLEDGE): AlarmState.ACKNOWLEDGED,
        (AlarmState.ACTIVE, AlarmAction.CLEAR): AlarmState.CLEARED,
        (AlarmState.ACKNOWLEDGED, AlarmAction.CLEAR): AlarmState.CLEARED,
        (AlarmState.CLEARED, AlarmAction.ACKNOWLEDGE): AlarmState.CLEARED,
        (AlarmState.CLEARED, AlarmAction.TRIGGER): AlarmState.ACTIVE,
        (AlarmState.CLEARED, AlarmAction.RESET): AlarmState.RESET,
        (AlarmState.RESET, AlarmAction.FINALIZE): AlarmState.INACTIVE,
    }

    @classmethod
    def transition(cls, current: AlarmState, action: AlarmAction) -> AlarmState:
        try:
            return cls._TRANSITIONS[(current, action)]
        except KeyError as exc:
            raise InvalidAlarmTransitionError(
                f"Invalid alarm transition: {current.value} + {action.value}"
            ) from exc

    @classmethod
    def can_transition(cls, current: AlarmState, action: AlarmAction) -> bool:
        return (current, action) in cls._TRANSITIONS
