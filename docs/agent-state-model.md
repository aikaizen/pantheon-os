# Agent State Model

Pantheon OS should track agent state semantically.

Required states:
- idle
- thinking
- executing
- waiting_on_tool
- waiting_on_human
- blocked
- reviewing
- error
- complete
- paused

Idle must mean operationally idle, not merely silent.
