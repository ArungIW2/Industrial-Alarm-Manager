# Alarm Philosophy

## Purpose

An alarm exists to identify an abnormal condition that requires awareness or action. The project treats alarms as engineering domain objects rather than generic application notifications.

## Core Principles

1. **Alarm definition, occurrence, and event are different concepts.**
   - A definition describes configuration.
   - An occurrence represents one lifecycle instance.
   - An event records a lifecycle change for audit and troubleshooting.

2. **Priority communicates operational significance.**
   Priority should reflect consequence and response urgency, not cosmetic UI color.

3. **Acknowledgement does not clear a fault.**
   Acknowledgement records that the alarm has been seen or accepted. The underlying condition may remain active.

4. **Clearing reflects process condition recovery.**
   Clearing is caused by removal of the fault condition, not by an operator pressing an acknowledgement button.

5. **Reset completes lifecycle handling.**
   Reset is only permitted when lifecycle rules allow it.

6. **History must support troubleshooting.**
   Lifecycle changes should later be recorded as immutable events so sequence-of-events analysis is possible.

7. **Software architecture remains independent from hardware.**
   This repository models industrial alarm behavior without PLC, HMI, sensors, motors, or hardware simulation.
