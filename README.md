# Industrial Alarm Manager

A software-focused industrial alarm management system designed to demonstrate alarm lifecycle handling, fault management, prioritization, acknowledgement, troubleshooting, and maintainable control-system software architecture.

> This project intentionally uses no physical PLC, HMI, sensor, motor, or hardware simulation. The focus is software architecture and industrial alarm domain logic.

## Project Status

**Phase 0 — Project Foundation: Complete**  
**Phase 1 — Domain Foundation: Complete**  
**Phase 2 — Alarm State Machine: Next**

The current implementation provides the core domain types required before lifecycle behavior is added.

## Goals

The project is designed to demonstrate understanding of:

- industrial alarms and fault handling;
- alarm priorities;
- alarm acknowledgement and lifecycle;
- duplicate alarm concepts;
- alarm history and troubleshooting;
- suppression and escalation concepts;
- domain-oriented control-system software architecture;
- automated testing.

## Alarm Priorities

- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`

## Lifecycle Design

```text
INACTIVE
   |
   | trigger
   v
ACTIVE
   |
   | acknowledge
   v
ACKNOWLEDGED
   |
   | fault condition clears
   v
CLEARED
   |
   | reset
   v
RESET
   |
   | finalize
   v
INACTIVE
```

The detailed design also allows a fault condition to clear before acknowledgement. That behavior will be implemented and validated in Phase 2.

## Architecture

```text
Interface / Examples
        |
        v
Application Services
        |
        v
Domain Model
        |
        v
Repository Abstractions
        |
        v
Persistence
```

The domain layer must not depend on SQLite or any future API/UI layer.

## Current Domain Model

### AlarmDefinition

Represents what an alarm means and how it is configured.

Examples:

- Emergency Stop
- Motor Overload
- Sensor Failure
- Communication Failure
- High Temperature
- Low Material
- Timeout
- Controller Fault

### AlarmOccurrence

Represents one occurrence of an alarm definition. Priority is copied into the occurrence so historical data is not silently changed if alarm configuration changes later.

## Repository Structure

```text
src/
  industrial_alarm_manager/
    application/
    domain/
    policies/
    storage/
tests/
  unit/
docs/
examples/
README.md
pyproject.toml
```

## Development Roadmap

| Phase | Scope | Status |
|---|---|---|
| 0 | Project foundation | Complete |
| 1 | Domain foundation | Complete |
| 2 | Alarm state machine | Next |
| 3 | Alarm manager | Planned |
| 4 | Duplicate handling | Planned |
| 5 | Persistence / SQLite | Planned |
| 6 | History and query | Planned |
| 7 | Suppression | Planned |
| 8 | Escalation | Planned |
| 9 | Examples and broader testing | Planned |
| 10 | Portfolio polish and CI | Planned |

## Development Setup

Requires Python 3.12 or newer.

```bash
python -m venv .venv
```

Activate the virtual environment, then install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Documentation

Design documentation is available under `docs/`:

- `requirements.md`
- `alarm-philosophy.md`
- `alarm-lifecycle.md`
- `priority-definition.md`
- `architecture.md`
- `data-model.md`
- `testing.md`
