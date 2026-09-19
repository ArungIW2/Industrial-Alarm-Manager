# Testing Strategy

## Unit Tests

Unit tests should validate domain behavior without SQLite or external services.

Phase 1 tests cover:

- stable alarm priority values;
- stable lifecycle state values;
- alarm definition validation;
- timezone-aware timestamps;
- occurrence creation from a definition;
- logical identity keys;
- independent metadata containers;
- invalid occurrence counters.

Phase 2 will add transition-matrix tests, including valid and invalid state transitions.

## Integration Tests

Integration tests will be introduced with persistence. They will use an isolated temporary SQLite database and verify that domain data and history survive repository round trips.

## Commands

```bash
pytest
ruff check .
mypy src
```
