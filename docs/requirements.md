# Requirements Traceability

| Requirement | Implementation |
|---|---|
| Lifecycle validation | `AlarmStateMachine` transition matrix |
| Create/trigger alarms | `AlarmManager.trigger_alarm` |
| Priority and timestamps | Definition/occurrence/event models |
| Acknowledge, clear, reset | Alarm manager lifecycle commands |
| Immutable history | Append-only `AlarmEvent` records |
| Duplicate handling | Active identity lookup plus duplicate counter/event |
| Reactivation | `CLEARED → ACTIVE` on the same occurrence |
| Filtering | `HistoryQueryService` and repository filters |
| Suppression | Auditable rule with reason, actor, and expiry |
| Escalation | Priority policy plus unacknowledged timeout evaluation |
| Simple storage | In-memory and SQLite repository adapters |
| Testability | Repository/clock dependency injection and automated tests |

Out of scope: physical PLC/HMI integration, hardware or process simulation, safety certification,
notification delivery, authentication, and distributed-system guarantees.

