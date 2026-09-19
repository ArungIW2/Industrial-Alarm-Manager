# Testing Strategy

Unit tests use the in-memory adapter and an injected frozen clock. They cover the transition
matrix, invalid commands, clear-before-acknowledge, deduplication, reactivation, suppression,
escalation, filtering, and error guards.

Integration tests use a temporary SQLite database and reopen it to verify lifecycle state,
metadata, and event history survive a persistence round trip.

Local quality gate:

```bash
python -m pytest --cov=industrial_alarm_manager --cov-report=term-missing
python -m ruff check .
python -m mypy src
```

CI runs the same checks on Python 3.12. Branch coverage must remain at or above 85%.

