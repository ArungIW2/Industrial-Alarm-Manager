# Priority Definition

| Priority | Operational meaning | Typical example |
|---|---|---|
| `CRITICAL` | Immediate response; severe safety, equipment, or process consequence | Emergency stop, controller fault |
| `HIGH` | Prompt response; major production or equipment impact | Motor overload, communication failure |
| `MEDIUM` | Timely operator action; limited immediate consequence | Sensor failure, process timeout |
| `LOW` | Awareness or routine intervention | Low material warning |

Priority belongs to `AlarmDefinition`, not to an alarm type hard-coded in application logic. The
value is copied to `AlarmOccurrence`, preserving historical meaning if configuration changes.

