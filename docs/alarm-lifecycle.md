# Alarm Lifecycle

## States

| State | Meaning |
|---|---|
| INACTIVE | No active alarm condition is being handled. |
| ACTIVE | The fault condition is active and has not been acknowledged. |
| ACKNOWLEDGED | The fault remains active but acknowledgement has been recorded. |
| CLEARED | The underlying fault condition is no longer active. |
| RESET | The completed occurrence has been reset before returning to idle. |

## Primary Flow

```text
INACTIVE -> ACTIVE -> ACKNOWLEDGED -> CLEARED -> RESET -> INACTIVE
```

## Clear Before Acknowledgement

Industrial conditions may recover before an operator acknowledges the alarm.

```text
ACTIVE -> CLEARED
```

The occurrence can still retain the fact that it was never acknowledged. Phase 2 will define the exact commands permitted against a cleared-but-unacknowledged occurrence.

## Reactivation

If the same condition returns before the existing occurrence is reset:

```text
CLEARED -> ACTIVE
```

The design treats that behavior as a reactivation of the same occurrence rather than automatically creating a second active occurrence.

## Transition Ownership

Lifecycle rules belong to the domain/state-machine layer. SQLite or any future API must not decide whether a transition is valid.

Implementation of transition validation is intentionally deferred to Phase 2.
