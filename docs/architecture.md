# Architecture

## Architectural Direction

```text
+-----------------------------+
| Interface / Examples        |
+-------------+---------------+
              |
              v
+-----------------------------+
| Application Layer           |
| AlarmManager, Query Service |
+-------------+---------------+
              |
              v
+-----------------------------+
| Domain Layer                |
| Models, State Machine       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Repository Abstractions     |
+-------------+---------------+
              |
              v
+-----------------------------+
| Persistence Adapters        |
| In-memory / SQLite          |
+-----------------------------+
```

## Dependency Rule

Dependencies point inward toward the domain.

The domain package must not import SQLite, CLI, REST API, or presentation code.

## Package Responsibilities

### domain

Contains alarm concepts and lifecycle rules.

### application

Coordinates use cases such as trigger, acknowledge, clear, reset, and history queries.

### policies

Contains replaceable rules for duplicate handling, suppression, and escalation.

### storage

Contains repository interfaces and persistence adapters.

### examples

Demonstrates realistic industrial scenarios without simulating physical hardware.

## Planned Application Flow

```text
caller
  |
  v
AlarmManager
  |
  +--> duplicate/suppression policy
  |
  +--> state machine
  |
  +--> occurrence repository
  |
  +--> event repository
```

Phase 1 implements only the domain foundation. Application services and persistence intentionally remain empty package boundaries.
