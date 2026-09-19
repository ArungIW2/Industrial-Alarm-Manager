# Priority Definition

Priority represents the operational significance and expected response urgency of an alarm.

| Priority | Definition | Example |
|---|---|---|
| CRITICAL | Immediate response is expected because consequences can be severe. | Emergency Stop, critical controller fault |
| HIGH | Significant process/equipment impact requiring prompt response. | Motor overload, major communication failure |
| MEDIUM | Abnormal condition requiring action but without immediate severe consequence. | Sensor failure, process timeout |
| LOW | Low-impact condition requiring awareness or routine action. | Low material warning |

## Configuration Rule

Priority belongs to the alarm definition and is not hard-coded only by alarm type.

For example, a high-temperature alarm may be MEDIUM in one process and CRITICAL in another.

When an occurrence is created, its priority is copied from the definition. This snapshot prevents historical occurrences from changing if the alarm definition is later reconfigured.
