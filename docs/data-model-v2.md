# Pantheon OS Data Model v2

Cross-surface data model covering all four Pantheon OS surfaces. Extends the dashboard-only v1 model (`data/pantheon-os.json`).

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
    {"agent": "hermetic-demiurge", "action": "propose"},
    {"agent": "ai-principal", "action": "approve", "threshold": "required"}
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

## Dashboard Layer

Preserves existing v1 schema. Key entities:

### Venture

```json
{
  "id": "pantheon-os",
  "name": "Pantheon OS",
  "type": "product|prototype|experiment|internal",
  "status": "active|paused|archived",
  "owner": "registry:agents.yaml#hermetic-demiurge",
  "budget": {"monthly": 900, "currency": "USD"},
  "health": "green|yellow|red",
  "goals": ["goal-001"],
  "repos": ["aikaizen/pantheon-os"]
}
```

### Goal

```json
{
  "id": "goal-001",
  "venture": "pantheon-os",
  "title": "Ship Terminal Manager MVP",
  "status": "in_progress",
  "milestones": [
    {"id": "m1", "title": "Wireframe", "done": true},
    {"id": "m2", "title": "Mock data integration", "done": false}
  ],
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
  "status": "pending|approved|rejected",
  "payload": {"amount": 500, "reason": "Lambda GPU hours"},
  "created_at": "2026-03-16T12:00:00Z",
  "decided_at": null
}
```

## Operating Terminal Layer

### Workspace

```json
{
  "id": "ws-main",
  "name": "Primary Control Room",
  "layout": {
    "type": "grid",
    "columns": 3,
    "rows": 2
  },
  "panes": [
    {"id": "p1", "type": "channel", "source": "telegram", "position": {"col": 0, "row": 0}},
    {"id": "p2", "type": "execution", "agent": "hermetic-demiurge", "position": {"col": 1, "row": 0}},
    {"id": "p3", "type": "summary", "scope": "all", "position": {"col": 2, "row": 0}},
    {"id": "p4", "type": "portal", "venture": "pantheon-os", "position": {"col": 0, "row": 1}},
    {"id": "p5", "type": "oversight", "position": {"col": 1, "row": 1}},
    {"id": "p6", "type": "log", "position": {"col": 2, "row": 1}}
  ]
}
```

### Pane Types

| Type | Data Source | Purpose |
|------|-----------|---------|
| channel | Telegram/WhatsApp/internal | Message threads per agent |
| execution | Runtime bridge | Shell, tmux, docker console |
| summary | Portal | Agent state and blockers |
| artifact | Artifact store | Files, outputs, deliverables |
| portal | Portal | Task state, checkpoints, handoffs |
| telemetry | Runtime | Metrics, heartbeat, resource usage |
| oversight | Outer harness | Harness state, control actions |

### Intervention

```json
{
  "id": "int-001",
  "type": "pause|resume|restart|kill|reassign|escalate|inspect|inject",
  "target_agent": "hermetic-demiurge",
  "operator": "registry:agents.yaml#ai-principal",
  "reason": "Budget threshold exceeded",
  "executed_at": "2026-03-16T14:30:00Z",
  "result": "success|failed|pending"
}
```

## Runtime / Portal Layer

### Portal State

```json
{
  "venture": "pantheon-os",
  "task_id": "task-172",
  "state": {
    "status": "in_progress",
    "current_agent": "registry:agents.yaml#hermetic-demiurge",
    "phase": "implementation",
    "blockers": [],
    "checkpoints": [
      {"id": "cp1", "label": "README rewritten", "at": "2026-03-16T13:00:00Z"}
    ],
    "handoff_notes": "Registry expansion next"
  },
  "summaries": [
    {"level": "brief", "text": "Rewriting PantheonOS README and registry"},
    {"level": "detailed", "text": "..."}
  ]
}
```

### Agent Runtime Instance

```json
{
  "instance_id": "inst-hd-042",
  "agent_id": "registry:agents.yaml#hermetic-demiurge",
  "state": "running|idle|paused|waiting|error|terminated",
  "started_at": "2026-03-16T12:24:00Z",
  "session": {
    "harness": "hermes",
    "channel": "telegram",
    "chat_id": "5692327956"
  },
  "resource_usage": {
    "api_calls": 47,
    "cost_usd": 2.31,
    "tokens_in": 125000,
    "tokens_out": 48000
  }
}
```

### Event

```json
{
  "event_id": "evt-8891",
  "type": "state_change|log|artifact|approval|heartbeat",
  "source": "runtime:hermetic-demiurge",
  "timestamp": "2026-03-16T14:45:00Z",
  "payload": {
    "agent": "hermetic-demiurge",
    "from_state": "executing",
    "to_state": "waiting_on_human",
    "reason": "Needs approval for production deploy"
  }
}
```

### Heartbeat

```json
{
  "agent_id": "registry:agents.yaml#hermetic-demiurge",
  "timestamp": "2026-03-16T15:00:00Z",
  "interval_seconds": 3600,
  "status": "healthy|stale|critical",
  "summary": "Completed README rewrite, working on registry",
  "metrics": {
    "tasks_active": 1,
    "tasks_queued": 3,
    "uptime_seconds": 9600
  }
}
```

## Cross-Surface References

All agent references use `registry:agents.yaml#<id>` format. This keeps identity centralized in the registry while allowing all surfaces to reference agents by stable ID.

- Venture → agent ownership via `owner` field
- Approval → agent requesters/approvers via `requester`/`approver`
- Portal state → current agent via `current_agent`
- Runtime instance → agent identity via `agent_id`
- Heartbeat → agent liveness via `agent_id`

## v1 → v2 Migration

The existing `data/pantheon-os.json` is v1 (dashboard-only). v2 is additive:

- `meta`, `summary`, `guidance`, `agents[]`, `ventures[]` — preserved as-is
- `goals[]`, `kpis[]` — new additions to dashboard
- `workspaces[]`, `interventions[]` — new terminal layer
- `portal_states[]`, `runtime_instances[]`, `events[]`, `heartbeats[]` — new runtime layer

No breaking changes to v1 consumers. New surfaces are opt-in.
