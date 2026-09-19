from datetime import UTC, datetime

import pytest

from industrial_alarm_manager import AlarmDefinition, AlarmPriority, InMemoryAlarmRepository
from industrial_alarm_manager.application import AlarmManager


class FrozenClock:
    def __init__(self, value: datetime) -> None:
        self.value = value

    def now(self) -> datetime:
        return self.value


@pytest.fixture
def clock() -> FrozenClock:
    return FrozenClock(datetime(2026, 9, 19, 8, 0, tzinfo=UTC))


@pytest.fixture
def definition() -> AlarmDefinition:
    return AlarmDefinition(
        code="MOTOR_OVERLOAD",
        name="Motor 01 Overload",
        description="Motor protection detected overload",
        source="MOTOR_01",
        default_priority=AlarmPriority.HIGH,
        category="MOTOR",
    )


@pytest.fixture
def repository() -> InMemoryAlarmRepository:
    return InMemoryAlarmRepository()


@pytest.fixture
def manager(repository: InMemoryAlarmRepository, clock: FrozenClock) -> AlarmManager:
    return AlarmManager(repository, clock)
