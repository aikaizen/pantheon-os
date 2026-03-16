# Terminal Manager MVP — Implementation Plan

## 1. Architecture

### Frontend

- **Framework**: React + TypeScript + Vite
- **State**: Zustand (lightweight, fits pane-based architecture)
- **Styling**: Tailwind CSS with PromptEngines visual language (sharp, dark, minimal — no rounded SaaS bubbles)
- **Layout**: CSS Grid for multi-pane workspaces
- **Real-time**: SSE (Server-Sent Events) for live session streams

### Component Hierarchy

```
<TerminalManager>
  <WorkspaceGrid>
    <Pane type="channel" />
    <Pane type="execution" />
    <Pane type="summary" />
    <Pane type="artifact" />
    <Pane type="portal" />
    <Pane type="oversight" />
    <Pane type="log" />
  </WorkspaceGrid>
  <ControlBar />
  <InterventionPanel />
</TerminalManager>
```

### Backend Dependencies

| Service | Purpose | Status |
|---------|---------|--------|
| Registry API | Agent roster, capabilities, constraints | Exists (YAML files) |
| Portal API | Task state, summaries, checkpoints | Needs build |
| Runtime Bridge | Live session proxy (tmux, shells) | Needs build |
| Intervention API | Pause/resume/kill/reassign actions | Needs build |
| Artifact Store | File outputs, deliverables | Needs build |

## 2. Phased Implementation

### Phase A: Static Wireframe (1-2 days)

Goal: Visual shell that matches the spec, no live data.

- Build React component skeleton for all 7 pane types
- Implement CSS Grid layout with resizable panes
- Add pane chrome (title bar, type indicator, collapse/expand)
- Port visual language from `terminal-manager.html` to React components
- Add workspace switcher UI (tabs or sidebar)
- No backend — all static/mock layout

**Deliverable**: `apps/terminal-manager/` with runnable static wireframe

### Phase B: Mock Data Integration (2-3 days)

Goal: Wire up realistic mock data to prove the pane model works.

- Create TypeScript interfaces for all data contracts (see Section 3)
- Build Zustand stores for each pane type
- Populate with mock data from registry and synthetic sessions
- Add simulated event streams (setInterval with random events)
- Implement pane-level controls (pause indicator, refresh button)
- Test layout persistence (save/restore workspace configs to localStorage)

**Deliverable**: Fully interactive wireframe with mock data

### Phase C: Live Session Bridge (1 week)

Goal: Connect to real agent sessions.

- Build SSE endpoint for runtime event streams
- Implement session attach/detach for tmux panes
- Add portal state integration (poll or stream from portal API)
- Wire registry API for live agent roster
- Handle reconnection, timeouts, error states
- Add real terminal emulation (xterm.js for execution panes)

**Deliverable**: Live terminal manager connected to running agents

### Phase D: Intervention Controls (3-5 days)

Goal: Make the terminal actionable, not just observable.

- Implement all intervention types (pause, resume, restart, kill, reassign, escalate, inspect, inject)
- Add confirmation dialogs for destructive actions
- Wire intervention API to runtime bridge
- Add intervention history pane
- Implement broadcast input (send command to multiple agents)
- Add escalation routing to ai-principal

**Deliverable**: Full operator control surface

## 3. Data Contracts

### Registry API

```typescript
interface Agent {
  id: string;
  name: string;
  type: 'human' | 'agent';
  role: string;
  status: 'active' | 'inactive';
  capabilities: string[];
  constraints: {
    requires_approval_for: string[];
    scope_bound: string;
  };
}
```

### Portal API

```typescript
interface PortalState {
  venture: string;
  task_id: string;
  state: {
    status: string;
    current_agent: string;
    phase: string;
    blockers: string[];
    checkpoints: Checkpoint[];
  };
  summaries: Summary[];
}

interface Checkpoint {
  id: string;
  label: string;
  at: string;
}

interface Summary {
  level: 'brief' | 'detailed';
  text: string;
}
```

### Runtime Bridge Stream

```typescript
type RuntimeEvent =
  | StateChangeEvent
  | LogEvent
  | ExecutionEvent
  | TelemetryEvent
  | ArtifactEvent
  | InterventionEvent;

interface StateChangeEvent {
  type: 'state_change';
  agent_id: string;
  from: AgentState;
  to: AgentState;
  reason: string;
  timestamp: string;
}

interface LogEvent {
  type: 'log';
  agent_id: string;
  level: 'info' | 'warn' | 'error';
  message: string;
  timestamp: string;
}

interface ExecutionEvent {
  type: 'execution';
  agent_id: string;
  stream: 'stdout' | 'stderr';
  data: string;
  timestamp: string;
}

type AgentState = 'idle' | 'thinking' | 'executing' | 'waiting_on_tool'
  | 'waiting_on_human' | 'blocked' | 'reviewing' | 'error'
  | 'complete' | 'paused';
```

## 4. Pane Type Interfaces

### Channel Pane
- **Data**: Message threads from Telegram/WhatsApp/internal
- **Key props**: `channel_type`, `agent_id`, `messages[]`
- **Behaviors**: Scroll, reply, pin, search

### Execution Pane
- **Data**: Live shell/tmux/docker output
- **Key props**: `agent_id`, `session_id`, `stream_data`
- **Behaviors**: Scroll, copy, attach/detach, send input

### Summary Pane
- **Data**: Agent state, blockers, current task
- **Key props**: `agent_id`, `portal_state`, `heartbeat`
- **Behaviors**: Refresh, drill-down to execution, escalate

### Artifact Pane
- **Data**: Files, outputs, deliverables
- **Key props**: `venture`, `artifacts[]`
- **Behaviors**: Preview, download, pin, annotate

### Portal Pane
- **Data**: Task state, checkpoints, handoffs
- **Key props**: `venture`, `portal_state`
- **Behaviors**: View checkpoints, add notes, trigger handoff

### Telemetry Pane
- **Data**: Metrics, heartbeat, resource usage
- **Key props**: `agent_id`, `metrics`, `heartbeat`
- **Behaviors**: Time range select, metric toggle, alert config

### Oversight Pane
- **Data**: Harness state, control actions, approval queue
- **Key props**: `harness_state`, `pending_approvals[]`
- **Behaviors**: Approve/reject, trigger intervention, view audit log

## 5. Open Questions

### Architecture
1. **SSE vs WebSocket**: SSE is simpler and sufficient for one-way streams. WebSocket needed only if we need bidirectional real-time (e.g., interactive terminal). Start with SSE + REST.
2. **Charting library**: For telemetry pane. Recharts (React-native) vs lightweight custom SVG.
3. **Terminal emulation**: xterm.js is the standard. Needed for Phase C.

### Product
4. **Default workspace layout**: What panes are visible on first load?
5. **Multi-session**: Can operator view multiple agent sessions simultaneously?
6. **Permissions**: Can all operators see all agents, or role-based visibility?
7. **Mobile**: Is there a mobile view, or desktop-only?

### Technical
8. **Portal API contract**: Does the portal API exist, or does it need to be built alongside?
9. **Runtime bridge scope**: Just tmux, or also Docker containers, remote SSH?
10. **State model evolution**: The 10-state model in `agent-state-model.md` — is this final?
11. **Stream volume**: How much log data flows per agent per hour? Affects buffering strategy.
12. **Persistence**: Are workspace layouts user-specific? Stored where?
13. **Integration timeline**: Does the terminal manager ship before or after the portal API?

## References

- `terminal-manager.html` — existing wireframe
- `docs/workstreams/terminal-manager-mvp.md` — workstream definition
- `docs/operating-terminal-spec.md` — terminal spec
- `docs/pane-system.md` — pane type definitions
- `docs/portal-model.md` — portal data model
- `docs/agent-state-model.md` — agent state definitions
- `docs/data-model-v2.md` — cross-surface data model
- `registry/agents.yaml` — agent roster
