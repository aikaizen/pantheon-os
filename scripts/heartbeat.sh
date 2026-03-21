#!/bin/bash
# Pantheon OS Heartbeat Script
# Call this to emit a heartbeat for an agent.
#
# Usage:
#   ./scripts/heartbeat.sh <agent_id> [status] [summary]
#
# Examples:
#   ./scripts/heartbeat.sh hermetic-demiurge
#   ./scripts/heartbeat.sh hermetic-demiurge healthy "Built state engine v0.2.0"
#   ./scripts/heartbeat.sh dzambhala stale "No recent activity"
#
# Statuses: healthy (default), stale, critical
# Updates registry/heartbeats.yaml in place.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
HEARTBEATS_FILE="$REPO_ROOT/registry/heartbeats.yaml"

AGENT_ID="${1:?Usage: heartbeat.sh <agent_id> [status] [summary]}"
STATUS="${2:-healthy}"
SUMMARY="${3:-}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Validate status
case "$STATUS" in
  healthy|stale|critical) ;;
  *) echo "Invalid status: $STATUS (use healthy, stale, critical)"; exit 1 ;;
esac

# Update heartbeats.yaml using Python (handles YAML properly)
python3 - "$HEARTBEATS_FILE" "$AGENT_ID" "$STATUS" "$TIMESTAMP" "$SUMMARY" << 'PYEOF'
import sys
import yaml

path, agent_id, status, timestamp, summary = sys.argv[1:6]

with open(path) as f:
    data = yaml.safe_load(f) or {}

heartbeats = data.get("heartbeats", [])
found = False
for hb in heartbeats:
    if hb.get("agent_id") == agent_id:
        hb["status"] = status
        hb["last_seen"] = timestamp
        if summary:
            hb["last_summary"] = summary
        found = True
        break

if not found:
    heartbeats.append({
        "agent_id": agent_id,
        "interval_seconds": 3600,
        "last_seen": timestamp,
        "status": status,
        "last_summary": summary or None,
    })
    data["heartbeats"] = heartbeats

with open(path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print(f"Heartbeat recorded: {agent_id} [{status}] at {timestamp}")
PYEOF

# Regenerate state after heartbeat
python3 "$REPO_ROOT/engine/state_engine.py" 2>/dev/null
echo "State engine refreshed."
