# Realm Isolation Specification

## Overview

The PantheonOS Realm Isolation Framework provides fully isolated execution environments for agents and processes. Each realm is a sandboxed environment with its own:

- **Git Worktree**: Isolated codebase for modifications without affecting the main repository
- **State Directory**: Persistent storage for realm-specific data
- **Network Port**: Dedicated port for network services
- **Process Environment**: Isolated process space with custom environment variables

## Architecture

### Directory Structure

```
/tmp/pantheon/
├── realms/                    # Realm state directories
│   └── {realm_id}/
│       ├── metadata.json      # Realm metadata
│       ├── process.json       # Process information
│       └── process.log        # Process output logs
└── worktrees/                 # Git worktrees
    └── {realm_id}/           # Isolated codebase
```

### Components

1. **IsolatedRealm**: Core class managing individual realm lifecycle
2. **RealmBootstrap**: High-level management interface
3. **PortAllocator**: Manages port assignment (9000-9999 range)

## Lifecycle

### 1. Creation (`create`)

```python
realm = IsolatedRealm.create(
    realm_id="my-agent-001",
    source_repo="/path/to/repo",
    base_branch="main",
    tags=["agent", "production"]
)
```

**Actions performed:**
- Creates state directory at `/tmp/pantheon/realms/{realm_id}`
- Creates git worktree at `/tmp/pantheon/worktrees/{realm_id}`
- Allocates a port from the available range
- Saves realm metadata

### 2. Boot (`boot`)

```python
pid = realm.boot(
    command=["python", "agent.py", "--port", str(realm.port)],
    env={"LOG_LEVEL": "DEBUG"}
)
```

**Actions performed:**
- Sets up environment variables:
  - `PANTHEON_REALM_ID`: Realm identifier
  - `PANTHEON_REALM_PORT`: Allocated port
  - `PANTHEON_REALM_STATE_DIR`: State directory path
  - `PANTHEON_REALM_WORKTREE`: Worktree path
- Starts process in worktree directory
- Redirects output to `process.log`
- Updates metadata with PID and state

### 3. Inspection (`inspect`)

```python
status = realm.get_status()
logs = realm.get_logs(lines=100)
```

**Provides:**
- Current state (created/running/stopped/error)
- Process status and PID
- Resource usage
- Recent logs

### 4. Teardown (`teardown`)

```python
realm.teardown(force=True)
```

**Actions performed:**
- Stops running process (if any)
- Releases allocated port
- Removes git worktree
- Removes state directory
- Updates state to `teardown`

## Usage Examples

### Basic Usage

```python
from realms import IsolatedRealm, boot_instance, teardown

# Create realm
realm = IsolatedRealm.create("agent-001")

# Boot instance
pid = realm.boot(
    command=["python", "main.py"],
    env={"MODE": "production"}
)

# Check status
status = realm.get_status()
print(f"Realm {status['realm_id']} is {status['state']}")

# Get logs
logs = realm.get_logs()

# Stop instance
realm.stop()

# Clean up
realm.teardown()
```

### Using Bootstrap API

```python
from realms.bootstrap import (
    RealmBootstrap,
    WorktreeConfig,
    InstanceConfig,
)

# Initialize bootstrap
bootstrap = RealmBootstrap()

# Create worktree
realm = bootstrap.create_worktree(WorktreeConfig(
    realm_id="my-agent",
    base_branch="develop",
    auto_commit=True,
    copy_files=["config.yaml", "templates/"]
))

# Boot instance
bootstrap.boot_instance(InstanceConfig(
    realm_id="my-agent",
    command=["python", "agent.py"],
    timeout=30,
))

# Execute command in realm
rc, stdout, stderr = bootstrap.execute_in_realm(
    "my-agent",
    ["ls", "-la"],
)

# Inspect realm
info = bootstrap.inspect("my-agent")

# Tear down
bootstrap.teardown("my-agent", force=True)
```

### CLI Usage

```bash
# Create realm
python -m realms.cli create my-agent-001

# Boot instance
python -m realms.cli boot my-agent-001 -- python agent.py

# List realms
python -m realms.cli list

# Inspect realm
python -m realms.cli inspect my-agent-001

# Tear down
python -m realms.cli teardown my-agent-001
```

## Environment Variables

Each realm process inherits the following environment variables:

| Variable | Description |
|----------|-------------|
| `PANTHEON_REALM_ID` | Realm identifier |
| `PANTHEON_REALM_PORT` | Allocated network port |
| `PANTHEON_REALM_STATE_DIR` | Path to state directory |
| `PANTHEON_REALM_WORKTREE` | Path to git worktree |

## Port Allocation

- Default range: 9000-9999
- Ports are allocated sequentially
- Port availability is checked before assignment
- Ports are released on realm teardown

## Error Handling

### Realm States

| State | Description |
|-------|-------------|
| `created` | Realm initialized, not yet running |
| `running` | Process is active |
| `stopped` | Process terminated normally |
| `error` | Error occurred during operation |
| `teardown` | Realm has been destroyed |

### Common Errors

1. **Realm already exists**: Attempting to create a realm with existing ID
2. **No available ports**: Port range exhausted
3. **Worktree creation failed**: Git operation failed
4. **Process startup failed**: Command execution failed
5. **Realm not found**: Attempting to load non-existent realm

## Security Considerations

1. **File System Isolation**: Each realm has its own directories
2. **Port Isolation**: Dedicated port prevents conflicts
3. **Process Isolation**: Processes run in separate sessions
4. **Environment Isolation**: Custom environment variables

## Integration with PantheonOS

Realms integrate with PantheonOS through:

1. **Agent Runtime**: Agents can be deployed in isolated realms
2. **Registry**: Realms can be registered and tracked
3. **Monitoring**: Realm status can be monitored via the registry
4. **Orchestration**: Multiple realms can be managed together

## Configuration

### Default Configuration

```python
REALMS_BASE = Path("/tmp/pantheon/realms")
WORKTREES_BASE = Path("/tmp/pantheon/worktrees")
PORT_RANGE = (9000, 9999)
```

### Custom Configuration

```python
from realms.isolation import REALMS_BASE, WORKTREES_BASE

# Override base directories
REALMS_BASE = Path("/custom/path/realms")
WORKTREES_BASE = Path("/custom/path/worktrees")
```

## Testing

The framework includes utilities for testing:

```python
from realms.isolation import cleanup_all_realms

# Clean up all test realms
cleanup_all_realms()
```

## Future Enhancements

1. **Resource Limits**: CPU/memory constraints per realm
2. **Network Policies**: Firewall rules per realm
3. **Snapshot/Restore**: Save and restore realm state
4. **Clustering**: Multi-node realm distribution
5. **Templates**: Pre-configured realm templates
6. **Metrics**: Detailed resource usage tracking

## API Reference

### IsolatedRealm Class

#### Methods

- `create(realm_id, source_repo, base_branch, tags)` - Create new realm
- `load(realm_id)` - Load existing realm
- `boot(command, env)` - Start process
- `stop()` - Stop process
- `teardown(force)` - Clean up realm
- `get_status()` - Get realm status
- `get_logs(lines)` - Get process logs

### RealmBootstrap Class

#### Methods

- `create_worktree(config)` - Create realm with config
- `boot_instance(config)` - Boot instance with config
- `teardown(realm_id, force)` - Tear down realm
- `inspect(realm_id)` - Get detailed status
- `list_realms()` - List all realms
- `restart(realm_id)` - Restart realm
- `execute_in_realm(command, timeout)` - Run command in realm

### Module Functions

- `create_worktree(realm_id, ...)` - Create realm
- `boot_instance(realm_id, command, ...)` - Boot instance
- `teardown(realm_id, force)` - Tear down realm
- `list_realms()` - List all realms
- `get_realm_info(realm_id)` - Get realm info