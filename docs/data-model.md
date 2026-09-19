# Data Model

## AlarmDefinition

Represents relatively stable alarm configuration.

Current Phase 1 fields:

- definition_id
- code
- name
- description
- source
- default_priority
- category
- ack_required
- reset_required
- enabled
- created_at

## AlarmOccurrence

Represents one runtime lifecycle instance.

Current Phase 1 fields:

- occurrence_id
- definition_id
- code
- source
- priority
- state
- first_active_at
- last_active_at
- acknowledged_at
- acknowledged_by
- cleared_at
- reset_at
- activation_count
- duplicate_count
- message
- metadata

An occurrence snapshots `code`, `source`, and `priority` from its definition so historical meaning remains stable.

## Planned AlarmEvent

Introduced in a later phase as an append-only audit record.

Planned event types include:

- ALARM_ACTIVATED
- ALARM_ACKNOWLEDGED
- ALARM_CLEARED
- ALARM_RESET
- ALARM_REACTIVATED
- DUPLICATE_DETECTED
- ALARM_SUPPRESSED
- ALARM_UNSUPPRESSED
- ALARM_ESCALATED

## Relationship

```text
AlarmDefinition 1 ---- N AlarmOccurrence
AlarmOccurrence 1 ---- N AlarmEvent
```
