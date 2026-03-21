# Pantheon OS Data Model v2

Cross-surface data model covering all four Pantheon OS surfaces. Extends the dashboard-only v1 model (`data/pantheon-os.json`).

PantheonOS is an observational and intervention surface over sovereign persona agents, their channels, their runtimes, and the controller agents that maintain those runtimes. The model below keeps those object types explicit instead of flattening everything into a single agent list.

## Principles Layer

### Organization

```json
{
  "org_id": "promptengines",
  "name": "PromptEngines",
  "type": "company",
  "founded": "2024",
  "sovereignty": {
    "principal": "registry:agents.yaml#ai-principal",
    "authority_model": "human-sovereign",
    "agent_mandate_source": "constitution/CONSTITUTION.md"
  }
}
```

### Authority Chain

Defines who can approve what, per domain.

```json
{
  "domain": "production_deploy",
  "chain": [
    {"agent": "registry:agents.yaml#hermetic-demiurge", "action": "propose"},
    {"agent": "registry:agents.yaml#ai-principal", "action": "approve", "threshold": "required"}
  ],
  "escalation_timeout_seconds": 86400
}
```

### Escalation Rules

```json
{
  "rule_id": "heartbeat-stale",
  "condition": "heartbeat.status == 'critical'",
  "action": "notify",
  "target": "registry:agents.yaml#ai-principal",
  "severity": "high"
}
```

### Deployment Descriptor

```json
{
  "deployment_id": "promptengines",
  "deployment_ref": "registry:deployments/promptengines.json",
  "modes": ["observe", "message", "control"],
  "pilot_scope": {
    "tier_1": ["promptengines-web", "lab-notes", "kaizen", "consulting"]
  }
}
```

## Dashboard Layer

Preserves existing v1 schema and adds deployment-aware overlays.

### Venture

```json
{
  "id": "promptengines-web",
  "name": "PromptEngines.com",
  "stage": "product",
  "status": "active",
  "owner": "registry:agents.yaml#ai-principal",
  "operators": ["registry:agents.yaml#hermetic-demiurge"],
  "repo": "aikaizen/promptengines-main",
  "deployment": "promptengines"
}
```

### Goal

```json
{
  "id": "goal-001",
  "venture": "promptengines-web",
  "title": "Run internal PantheonOS pilot over PromptEngines deployment",
  "status": "in_progress",
  "owner": "registry:agents.yaml#hermetic-demiurge",
  "due": "2026-04-01"
}
```

### Approval

```json
{
  "id": "approval-042",
  "type": "budget_escalation|deploy|external_comm",
  "requester": "registry:agents.yaml#hermetic-demiurge",
  "approver": "registry:agents.yaml#ai-principal",
  "status": "pending|approved|rejected"
}
```

## Operating Terminal Layer

### Workspace

```json
{
  "id": "ws-main",
  "name": "Primary Control Room",
  "layout": {"type": "grid", "columns": 3, "rows": 2},
  "panes": [
    {"id": "p1", "type": "persona_channel", "source": "registry:channels.yaml#hermetic-demiurge-telegram", "position": {"col": 0, "row": 0}},
    {"id": "p2", "type": "persona_channel", "source": "registry:channels.yaml#dzambhala-telegram", "position": {"col": 1, "row": 0}},
    {"id": "p3", "type": "controller_terminal", "source": "registry:channels.yaml#promptengines-host-overseer-cli", "position": {"col": 2, "row": 0}},
    {"id": "p4", "type": "runtime_health", "source": "registry:runtimes.yaml#promptengines-hermes-primary", "position": {"col": 0, "row": 1}},
    {"id": "p5", "type": "artifact", "scope": "promptengines", "position": {"col": 1, "row": 1}},
    {"id": "p6", "type": "summary", "scope": "all", "position": {"col": 2, "row": 1}}
  ]
}
```

### Pane Types

| Type | Data Source | Purpose |
|------|-----------|---------|
| `persona_channel` | `channels.yaml` | Conversation with a sovereign persona agent |
| `controller_terminal` | `channels.yaml` / runtime bridge | Host-side controller console |
| `runtime_health` | `runtimes.yaml` + telemetry | Runtime health, model config, container/process state |
| `summary` | State engine | Cross-pane state and blockers |
| `artifact` | Artifact store | Files, outputs, deliverables |
| `portal` | Portal state | Task state, checkpoints, handoffs |
| `intervention` | Registry + runtime | Human/operator control actions |

### Intervention

```json
{
  "id": "int-001",
  "type": "pause|resume|restart|kill|reassign|escalate|inspect|inject",
  "target": {
    "object_type": "persona|controller|runtime",
    "ref": "registry:runtimes.yaml#promptengines-hermes-primary"
  },
  "operator": "registry:agents.yaml#ai-principal",
  "reason": "Runtime unhealthy",
  "result": "success|failed|pending"
}
```

## Runtime / Portal Layer

### Runtime

```json
{
  "id": "promptengines-hermes-primary",
  "ref": "registry:runtimes.yaml#promptengines-hermes-primary",
  "runtime_system": "hermes",
  "kind": "docker",
  "status": "active|planned|failed",
  "host": {"id": "promptengines-local-macbook", "os": "macos"},
  "access_mode": "observe|message|control"
}
```

### Controller

```json
{
  "id": "promptengines-host-overseer",
  "ref": "registry:controllers.yaml#promptengines-host-overseer",
  "agent_system": "hermes-operator",
  "access_level": "host",
  "status": "active|paused|failed"
}
```

### Channel

```json
{
  "id": "dzambhala-telegram",
  "ref": "registry:channels.yaml#dzambhala-telegram",
  "platform": "telegram",
  "kind": "telegram_chat",
  "status": "active",
  "access_mode": "message"
}
```

### Binding

```json
{
  "binding_type": "agent_runtime|agent_channel|runtime_controller",
  "source_ref": "registry:agents.yaml#hermetic-demiurge",
  "target_ref": "registry:runtimes.yaml#promptengines-hermes-primary",
  "relationship": "primary",
  "status": "active|planned"
}
```

### Portal State

```json
{
  "venture": "promptengines-web",
  "task_id": "task-172",
  "state": {
    "status": "in_progress",
    "current_agent": "registry:agents.yaml#hermetic-demiurge",
    "blockers": [],
    "handoff_notes": "Define runtime/channel bindings next"
  }
}
```

### Runtime Instance

```json
{
  "instance_id": "inst-runtime-001",
  "runtime_ref": "registry:runtimes.yaml#promptengines-hermes-primary",
  "controllers": ["registry:controllers.yaml#promptengines-host-overseer"],
  "channels": [
    "registry:channels.yaml#ai-principal-cli",
    "registry:channels.yaml#dzambhala-telegram"
  ],
  "resource_usage": {"api_calls": 47, "cost_usd": 2.31}
}
```

### Event

```json
{
  "event_id": "evt-8891",
  "type": "state_change|log|artifact|approval|heartbeat",
  "source_ref": "registry:runtimes.yaml#promptengines-hermes-primary",
  "timestamp": "2026-03-16T14:45:00Z",
  "payload": {"summary": "Controller attached to runtime"}
}
```

### Heartbeat

```json
{
  "object_type": "persona|controller|runtime",
  "object_ref": "registry:agents.yaml#hermetic-demiurge",
  "timestamp": "2026-03-16T15:00:00Z",
  "interval_seconds": 3600,
  "status": "healthy|stale|critical|unknown",
  "summary": "Completed registry expansion"
}
```

## Cross-Surface References

Use explicit registry references for each object type:
- Persona agent → `registry:agents.yaml#<id>`
- Runtime → `registry:runtimes.yaml#<id>`
- Controller → `registry:controllers.yaml#<id>`
- Channel → `registry:channels.yaml#<id>`
- Binding → `registry:bindings.yaml#<binding-type>/<index-or-id>` or embedded references in state output

This keeps identity centralized while allowing each surface to refer to the same underlying topology.

## v1 → v2 Migration

The existing `data/pantheon-os.json` is v1 (dashboard-only). v2 is additive:

- `meta`, `summary`, `agents[]`, `ventures[]` — preserved
- `goals[]`, `kpis[]`, `deployments[]` — expanded dashboard layer
- `workspaces[]`, `interventions[]` — expanded terminal layer
- `runtimes[]`, `controllers[]`, `channels[]`, `bindings[]` — deployment topology layer
- `portal_states[]`, `runtime_instances[]`, `events[]`, `heartbeats[]` — runtime/portal layer

No breaking changes to v1 consumers. New surfaces and topology objects are opt-in.
