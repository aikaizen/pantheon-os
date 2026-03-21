# Registry

The manifest layer of Pantheon OS. Makes the company and operating system legible as structured artifacts.

## Files

| File | Purpose |
|------|---------|
| `agents.yaml` | Canonical agent roster — identity, capabilities, constraints, reporting lines |
| `heartbeats.yaml` | Heartbeat tracking — liveness monitoring and stale detection |
| `agents/*.json` | Per-agent detail manifests — scope, skills, runtime config |

## Agent Manifest Schema

Each `agents/<id>.json` contains:

```
id              — unique identifier (matches agents.yaml)
name            — display name
type            — "human" | "agent"
archetype       — mythic/archetypal role label
role            — functional role description
mandate         — what this agent exists to do
reports_to      — agent id of authority (null for principal)
scope           — list of capability domains
capabilities    — specific skills/permissions
constraints     — approval requirements, scope bounds
runtime         — runtime config (telegram bot, hermes home, etc.)
```

## Runtime Contracts

The registry is consumed by:
- **Company Dashboard** — agent roster, budgets, status
- **Operating Terminal** — agent sessions, intervention targets
- **Runtime/Portal** — agent state transitions, heartbeat monitoring, event routing

## Current Scope vs Target Scope

Today `agents.yaml` is the canonical persona roster. That is correct, but it is not the full system model.

PantheonOS also needs explicit records for:
- `runtimes` — dockerized agent systems or other execution substrates
- `controllers` — overseer agents with host/machine access
- `channels` — Telegram bots/chats, CLI sessions, and other communication surfaces
- `bindings` — relationships between persona agents, channels, runtimes, and controllers

This keeps sovereign agent identity separate from the machines, containers, and channels they happen to use.

## Adding an agent

1. Add entry to `agents.yaml` with id, type, role, budget, capabilities, constraints
2. Create `agents/<id>.json` with full manifest
3. Add heartbeat entry to `heartbeats.yaml`
4. Update `docs/data-model-v2.md` if new capability domains are introduced
