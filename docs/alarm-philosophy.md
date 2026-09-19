# Alarm Philosophy

This project treats an alarm as an abnormal condition requiring awareness or action, not merely
as a UI notification. Priority represents consequence and response urgency. Every lifecycle
change creates an immutable event so troubleshooting is based on sequence-of-events evidence.

Design principles:

- configure alarms through definitions;
- snapshot priority in each occurrence;
- keep event history append-only;
- reject invalid lifecycle commands;
- deduplicate repeated fault signals by `code + source`;
- suppress only with a reason, actor, and optional expiry;
- never let persistence decide domain validity;
- use UTC, timezone-aware timestamps throughout.

The software is inspired by industrial alarm-management practice but is a portfolio/reference
implementation, not a certified safety system.

