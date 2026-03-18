# Observability Stack Specification

## Overview

Per-realm observability stack for PantheonOS agents. Provides structured logging and basic metrics for self-verification.

## Design Principles

1. **Realm Isolation** - Each realm gets separate log/metrics files
2. **Structured Data** - JSON logs, queryable metrics
3. **Low Overhead** - Minimal impact on agent performance
4. **Agent-Accessible** - Agents can query their own observability data

---

## Structured Logging

### RealmLogger

```python
from observability.logger import RealmLogger, LogLevel

logger = RealmLogger(realm_id="forge-001")
logger.info("Task started", context={"task": "implement-feature"})
logger.error("Build failed", context={"exit_code": 1})
```

### Log Format

Each log entry is a JSON line:

```json
{
  "timestamp": "2026-03-18T05:00:00+00:00",
  "realm_id": "forge-001",
  "level": "info",
  "message": "Task started",
  "context": {"task": "implement-feature"},
  "source": null
}
```

### Query Interface

```python
# Get recent errors
errors = logger.query(level=LogLevel.ERROR, limit=10)

# Get logs from last hour
from datetime import datetime, timezone, timedelta
recent = logger.query(since=datetime.now(timezone.utc) - timedelta(hours=1))

# Filter by context
build_logs = logger.query(context_filter={"phase": "build"})

# Tail last N entries
tail = logger.tail(n=20)
```

### Storage

- Location: `/tmp/pantheon/logs/{realm_id}.jsonl`
- Format: JSON Lines (one entry per line)
- Rotation: Manual via `logger.clear()`

---

## Metrics

### RealmMetrics

```python
from observability.metrics import RealmMetrics

metrics = RealmMetrics(realm_id="forge-001")

# Counters
files_modified = metrics.counter("files_modified")
files_modified.inc()

# Timers
with metrics.time_it("build_duration"):
    run_build()

# Gauges
memory_usage = metrics.gauge("memory_mb")
memory_usage.set(256.5)
```

### Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Monotonically increasing | Files modified, errors encountered |
| Timer | Duration tracking | Build time, search time |
| Gauge | Point-in-time values | Memory usage, queue depth |

### Snapshot & Persistence

```python
# Get current metrics
snapshot = metrics.snapshot()

# Save to disk
metrics.save()

# Load from disk
metrics.load()

# Human-readable summary
print(metrics.summary())
```

### Storage

- Location: `/tmp/pantheon/metrics/{realm_id}.json`
- Format: JSON with counters, timers, gauges sections

---

## Integration with PantheonOS

### State Engine

Metrics can be included in state snapshots:

```python
state["realms"]["forge-001"]["observability"] = {
    "logs": logger.tail(5),
    "metrics": metrics.snapshot()
}
```

### Agent Self-Verification

Agents can query their own observability:

```python
# Check if recent errors occurred
errors = logger.query(level=LogLevel.ERROR, limit=5)
if errors:
    # Investigate and fix
    pass

# Check build performance
build_timer = metrics.timer("build_duration")
if build_timer.average > 30.0:
    # Build is slow, investigate
    pass
```

---

## Future Enhancements (Phase 2)

- LogQL-style query language
- PromQL-style metric queries
- Distributed tracing with trace IDs
- Alerting thresholds
- Log aggregation across realms
