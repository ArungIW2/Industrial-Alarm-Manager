# Executable Examples

- `basic_alarm_flow.py`: activation through reset with sequence-of-events output.
- `alarm_reactivation.py`: a cleared fault returning before reset.
- `suppression_and_escalation.py`: audited suppression preventing escalation.
- `sqlite_history.py`: durable history and filtered querying.

Install the package in editable mode before running an example:

```bash
python -m pip install -e .
python examples/basic_alarm_flow.py
```
