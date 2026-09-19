from datetime import timedelta

import pytest

from industrial_alarm_manager import AlarmEventType
from industrial_alarm_manager.exceptions import SuppressionNotFoundError


def test_suppression_is_audited_and_applied_to_new_alarm(
    manager, repository, definition, clock
) -> None:
    manager.register_definition(definition)
    manager.suppress_alarm(
        definition.code,
        definition.source,
        reason="Scheduled maintenance",
        created_by="maintenance",
        expires_at=clock.now() + timedelta(hours=1),
    )

    alarm = manager.trigger_alarm(definition.code, definition.source)

    assert alarm.is_suppressed
    assert alarm.suppression_reason == "Scheduled maintenance"
    assert repository.events[-1].event_type is AlarmEventType.SUPPRESSED


def test_unsuppress_updates_active_alarm(manager, definition) -> None:
    manager.register_definition(definition)
    manager.suppress_alarm(definition.code, definition.source, reason="Test", created_by="engineer")
    alarm = manager.trigger_alarm(definition.code, definition.source)

    manager.unsuppress_alarm(definition.code, definition.source, actor="engineer")

    assert not alarm.is_suppressed
    assert alarm.suppression_reason is None


def test_unsuppress_without_rule_is_rejected(manager, definition) -> None:
    manager.register_definition(definition)
    with pytest.raises(SuppressionNotFoundError):
        manager.unsuppress_alarm(definition.code, definition.source, actor="operator")
