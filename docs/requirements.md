# Requirements

## Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Define alarm types and configuration. |
| FR-02 | Trigger an alarm occurrence. |
| FR-03 | Support CRITICAL, HIGH, MEDIUM, and LOW priorities. |
| FR-04 | Record alarm timestamps. |
| FR-05 | Acknowledge alarms. |
| FR-06 | Clear alarms when the underlying fault condition disappears. |
| FR-07 | Reset completed alarms according to lifecycle rules. |
| FR-08 | Record lifecycle changes in alarm history. |
| FR-09 | Prevent repeated signals from creating duplicate active occurrences. |
| FR-10 | Filter alarms by priority. |
| FR-11 | Filter alarms by state/status. |
| FR-12 | Query active alarms. |
| FR-13 | Query alarm history. |
| FR-14 | Support explicit alarm suppression. |
| FR-15 | Keep a reason and audit trail for suppression. |
| FR-16 | Support escalation when configured response thresholds are exceeded. |
| FR-17 | Handle fault reactivation before reset. |
| FR-18 | Cover domain behavior with automated tests. |

## Non-Functional Requirements

- Python 3.12 or newer.
- No physical hardware dependency.
- No PLC or HMI dependency.
- No hardware simulation.
- Domain logic must remain independent from persistence.
- Timestamps must be timezone-aware and stored as UTC when persisted.
- Lifecycle transitions must be deterministic and validated.
- Alarm history should be append-only once event history is introduced.
- Storage implementations must be replaceable behind repository abstractions.
- Unit tests must run without a production database.
