from industrial_alarm_manager.domain.enums import AlarmPriority, AlarmState


def test_alarm_priorities_are_explicit_and_stable() -> None:
    assert [priority.value for priority in AlarmPriority] == [
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW",
    ]


def test_alarm_states_match_designed_lifecycle() -> None:
    assert [state.value for state in AlarmState] == [
        "INACTIVE",
        "ACTIVE",
        "ACKNOWLEDGED",
        "CLEARED",
        "RESET",
    ]
