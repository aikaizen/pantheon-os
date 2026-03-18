# PantheonOS Realm Isolation Framework

A framework for creating isolated execution environments (realms) in PantheonOS.

## Overview

Each realm provides:
- **Git Worktree**: Isolated codebase for modifications
- **State Directory**: Persistent storage for realm data
- **Network Port**: Dedicated port for services
- **Process Environment**: Isolated process execution

## Quick Start

### Python API

```python
from realms import IsolatedRealm

# Create realm
realm = IsolatedRealm.create("my-agent")

# Boot instance
pid = realm.boot(
    command=["python", "agent.py"],
    env={"LOG_LEVEL": "DEBUG"},
)

# Check status
status = realm.get_status()

# Stop and cleanup
realm.stop()
realm.teardown()
```

### Command Line

```bash
# Create realm
python -m realms.cli create my-agent

# Boot instance
python -m realms.cli boot my-agent -- python agent.py

# List realms
python -m realms.cli list

# Inspect realm
python -m realms.cli inspect my-agent

# Stop realm
python -m realms.cli stop my-agent

# Teardown
python -m realms.cli teardown my-agent
```

## Module Structure

```
realms/
├── __init__.py          # Module exports
├── isolation.py         # Core IsolatedRealm class
├── bootstrap.py         # High-level management API
├── cli.py               # Command-line interface
├── realm-isolation-spec.md  # Detailed specification
└── README.md            # This file
```

## Directory Layout

```
/tmp/pantheon/
├── realms/              # Realm state directories
│   └── {realm_id}/
│       ├── metadata.json
│       ├── process.json
│       └── process.log
└── worktrees/           # Git worktrees
    └── {realm_id}/     # Isolated codebase
```

## Environment Variables

Each realm process inherits:
- `PANTHEON_REALM_ID`: Realm identifier
- `PANTHEON_REALM_PORT`: Allocated port
- `PANTHEON_REALM_STATE_DIR`: State directory path
- `PANTHEON_REALM_WORKTREE`: Worktree path

## Integration

Realms integrate with PantheonOS components:
- **Agent Runtime**: Deploy agents in isolated realms
- **Registry**: Track and monitor realms
- **Orchestration**: Manage multiple realms

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Cleanup

```python
from realms.isolation import cleanup_all_realms
cleanup_all_realms()  # Remove all realms
```

## See Also

- [Realm Isolation Specification](realm-isolation-spec.md)
- [PantheonOS Documentation](../docs/)