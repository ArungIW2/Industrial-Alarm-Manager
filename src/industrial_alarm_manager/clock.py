"""Injectable time source for deterministic domain tests."""

from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)
