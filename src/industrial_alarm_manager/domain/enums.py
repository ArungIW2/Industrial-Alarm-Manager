"""Enumerations used by the alarm domain."""

from enum import Enum


class AlarmPriority(str, Enum):
    """Operational priority assigned to an alarm."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AlarmState(str, Enum):
    """Lifecycle state of an alarm occurrence."""

    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    CLEARED = "CLEARED"
    RESET = "RESET"
