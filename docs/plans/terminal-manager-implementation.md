# Terminal Manager MVP — Implementation Plan

## 1. Architecture

### Frontend

- **Framework**: React + TypeScript + Vite
- **State**: Zustand
- **Styling**: Tailwind CSS with PromptEngines visual language (sharp, dark, minimal — no rounded SaaS bubbles)
- **Layout**: CSS Grid for multi-pane workspaces
- **Real-time**: SSE first, WebSocket only where truly needed

### Component Hierarchy

```
<TerminalManager>
  <WorkspaceGrid>
    <Pane type="persona_channel" />
    <Pane type="controller_terminal" />
    <Pane type="runtime_health" />
    <Pane type="summary" />
    <Pane type="artifact" />
    <Pane type="intervention" />
  </WorkspaceGrid>
  <ControlBar />
  <InspectorPanel />
</TerminalManager>
```

### Backend Dependencies

| Service | Purpose | Status |
|---------|---------|--------|
| Registry API | Persona roster, runtimes, controllers, channels, bindings | Exists as YAML/JSON, needs serving layer |
| Channel Adapter | Telegram/CLI/other message surfaces | Needs build |
| Runtime Bridge | Runtime health, attach/detach, logs | Needs build |
| Controller Bridge | Host-side controller terminal attach and actions | Needs build |
| Portal API | Task state, summaries, checkpoints | Needs build |
| Artifact Store | File outputs, deliverables | Needs build |

## 2. Phased Implementation

### Phase A: Static Wireframe (1-2 days)

Goal: Visual shell that matches the corrected system model, no live data.

- Build React component skeleton for 6 pane types
- Implement CSS Grid layout with resizable panes
- Add pane chrome (title bar, type indicator, collapse/expand)
- Port visual language from `terminal-manager.html`
- Add workspace switcher UI
- Use example panes for Hermetic_Demiurge, Dzambhala, host controller, and runtime health

**Deliverable**: `apps/terminal-manager/` with runnable static wireframe

### Phase B: Topology-Aware Mock Data (2-3 days)

Goal: Prove the pane model works against real topology contracts.

- Create TypeScript interfaces for persona agents, runtimes, controllers, channels, bindings
- Build Zustand stores for each pane type
- Populate mock data from `registry/agents.yaml`, `registry/runtimes.yaml`, `registry/controllers.yaml`, `registry/channels.yaml`, `registry/bindings.yaml`
- Simulate event streams for persona, controller, and runtime updates
- Add workspace persistence in localStorage

**Deliverable**: Fully interactive wireframe with topology-aware mock data

### Phase C: Live Observation Bridge (1 week)

Goal: Connect to real persona channels, controller consoles, and runtime telemetry.

- Build SSE endpoint for state and event streams
- Attach persona channel panes to real adapters (Telegram/CLI as available)
- Attach controller terminal panes via runtime/controller bridge
- Add runtime health streaming for container/process/model state
- Add portal state integration
- Handle reconnection, timeouts, and degraded adapter states
- Use xterm.js only for panes that truly need interactive terminal behavior

**Deliverable**: Live terminal manager connected to running PromptEngines pilot surfaces

### Phase D: Intervention Controls (3-5 days)

Goal: Make the terminal actionable without breaking the observe-first posture.

- Implement permission-aware actions for `observe`, `message`, and `control`
- Add confirmation dialogs for destructive actions
- Wire controller/runtimes into restart / inspect / send-test-message flows
- Add intervention history pane
- Add audit trail for operator actions
- Gate risky actions behind approval rules where required

**Deliverable**: Useful internal control surface with explicit safety boundaries

## 3. Data Contracts

### Registry API

```typescript
interface Agent {
  id: string;
  ref: string;
  name: string;
  type: 'human' | 'agent';
  role: string;
  status: 'active' | 'inactive';
  runtime_bindings: AgentRuntimeBinding[];
  channel_bindings: AgentChannelBinding[];
}

interface Runtime {
  id: string;
  ref: string;
  runtime_system: 'hermes' | 'openclaw' | string;
  kind: 'docker' | 'process' | 'remote';
  status: 'active' | 'planned' | 'failed';
  access_mode: 'observe' | 'message' | 'control';
}

interface Controller {
  id: string;
  ref: string;
  agent_system: string;
  access_level: 'host' | 'runtime' | 'limited';
  status: 'active' | 'planned' | 'paused';
  manages: string[];
}

interface Channel {
  id: string;
  ref: string;
  platform: 'telegram' | 'cli' | 'whatsapp' | string;
  kind: string;
  status: 'active' | 'planned' | 'offline';
  access_mode: 'observe' | 'message' | 'control';
}
```

### Runtime Event Stream

```typescript
type RuntimeEvent =
  | PersonaEvent
  | ControllerEvent
  | RuntimeHealthEvent
  | ArtifactEvent
  | InterventionEvent;

interface PersonaEvent {
  type: 'persona_event';
  agent_id: string;
  channel_id: string;
  summary: string;
  timestamp: string;
}

interface ControllerEvent {
  type: 'controller_event';
  controller_id: string;
  runtime_id: string;
  summary: string;
  timestamp: string;
}

interface RuntimeHealthEvent {
  type: 'runtime_health';
  runtime_id: string;
  status: string;
  adapters: Record<string, string>;
  timestamp: string;
}
```

## 4. Pane Type Interfaces

### Persona Channel Pane
- **Data**: message thread from Telegram/CLI/other surface
- **Key props**: `channel_id`, `agent_id`, `messages[]`
- **Behaviors**: scroll, reply, pin, request summary

### Controller Terminal Pane
- **Data**: host-side controller session or console transcript
- **Key props**: `controller_id`, `runtime_id`, `session_id`
- **Behaviors**: attach, detach, send input, inspect logs

### Runtime Health Pane
- **Data**: runtime status, adapters, model config, process state
- **Key props**: `runtime_id`, `health`, `telemetry`
- **Behaviors**: refresh, inspect, open linked controller pane

### Summary Pane
- **Data**: state engine output, blockers, handoffs, venture context
- **Key props**: `scope`, `summary`, `blockers[]`
- **Behaviors**: drill-down, filter, escalate

### Artifact Pane
- **Data**: files, outputs, deliverables
- **Key props**: `venture`, `artifacts[]`
- **Behaviors**: preview, download, pin, annotate

### Intervention Pane
- **Data**: allowed actions + history
- **Key props**: `target_ref`, `access_mode`, `history[]`
- **Behaviors**: observe/message/control actions with audit trail

## 5. Open Questions

1. Which adapters land first for the pilot: Telegram read-only, Telegram reply, or CLI bridge?
2. What is the smallest useful controller bridge for the first PromptEngines runtime?
3. How much interactive terminal behavior is truly needed in v1 vs read-only/log-oriented panes?
4. Should workspaces be per-operator, per-deployment, or both?
5. What approval model applies to controller actions that touch runtimes or secrets?

## References

- `terminal-manager.html` — wireframe
- `site/operating-terminal.html` — definitional doc
- `docs/data-model-v2.md` — cross-surface data model
- `registry/agents.yaml` — persona roster
- `registry/runtimes.yaml` — runtime topology
- `registry/controllers.yaml` — controller topology
- `registry/channels.yaml` — channel topology
- `registry/bindings.yaml` — topology bindings
