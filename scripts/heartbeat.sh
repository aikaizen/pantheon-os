#!/bin/bash
# Pantheon OS Heartbeat Script
# Call this to emit a heartbeat for a persona agent, runtime, or controller.
#
# Usage:
#   ./scripts/heartbeat.sh <target> [status] [summary]
#
# Examples:
#   ./scripts/heartbeat.sh hermetic-demiurge
#   ./scripts/heartbeat.sh agent:hermetic-demiurge healthy "Built state engine v0.3.0"
#   ./scripts/heartbeat.sh runtime:promptengines-hermes-primary healthy "Runtime reachable"
#   ./scripts/heartbeat.sh controller:promptengines-host-overseer stale "Overseer offline"
#
# Statuses: healthy (default), stale, critical
# Updates registry/heartbeats.yaml in place.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
HEARTBEATS_FILE="$REPO_ROOT/registry/heartbeats.yaml"

TARGET="${1:?Usage: heartbeat.sh <target> [status] [summary]}"
STATUS="${2:-healthy}"
SUMMARY="${3:-}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [[ "$TARGET" == *":"* ]]; then
  TARGET_TYPE="${TARGET%%:*}"
  TARGET_ID="${TARGET#*:}"
else
  TARGET_TYPE="agent"
  TARGET_ID="$TARGET"
fi

case "$STATUS" in
  healthy|stale|critical) ;;
  *) echo "Invalid status: $STATUS (use healthy, stale, critical)"; exit 1 ;;
esac

case "$TARGET_TYPE" in
  agent)
    OBJECT_REF="registry:agents.yaml#$TARGET_ID"
    LEGACY_KEY="agent_id"
    ;;
  runtime)
    OBJECT_REF="registry:runtimes.yaml#$TARGET_ID"
    LEGACY_KEY="runtime_id"
    ;;
  controller)
    OBJECT_REF="registry:controllers.yaml#$TARGET_ID"
    LEGACY_KEY="controller_id"
    ;;
  *)
    echo "Invalid target type: $TARGET_TYPE (use agent, runtime, controller)"
    exit 1
    ;;
esac

python3 - "$HEARTBEATS_FILE" "$TARGET_TYPE" "$TARGET_ID" "$LEGACY_KEY" "$OBJECT_REF" "$STATUS" "$TIMESTAMP" "$SUMMARY" << 'PYEOF'
import sys
import yaml

path, target_type, target_id, legacy_key, object_ref, status, timestamp, summary = sys.argv[1:9]

with open(path) as f:
    data = yaml.safe_load(f) or {}

heartbeats = data.get("heartbeats", [])
found = False
for hb in heartbeats:
    if hb.get("object_ref") == object_ref or hb.get(legacy_key) == target_id:
        hb["object_type"] = target_type
        hb["object_ref"] = object_ref
        hb[legacy_key] = target_id
        hb["status"] = status
        hb["last_seen"] = timestamp
        if summary:
            hb["last_summary"] = summary
        found = True
        break

if not found:
    entry = {
        "object_type": target_type,
        "object_ref": object_ref,
        legacy_key: target_id,
        "interval_seconds": 3600,
        "last_seen": timestamp,
        "status": status,
        "last_summary": summary or None,
    }
    heartbeats.append(entry)
    data["heartbeats"] = heartbeats

with open(path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print(f"Heartbeat recorded: {object_ref} [{status}] at {timestamp}")
PYEOF

python3 "$REPO_ROOT/engine/state_engine.py" 2>/dev/null || true
echo "State engine refreshed (if dependencies are installed)."
