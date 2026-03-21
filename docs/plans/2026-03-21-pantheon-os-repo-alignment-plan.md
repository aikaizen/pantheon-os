# PantheonOS repo alignment plan — observational multi-agent surface

> For Hermes: use this as the alignment plan before deeper work on specific agents.

Goal: align the repo with the corrected PantheonOS model: a TMUX-like observation and intervention surface over sovereign persona agents, their channels, runtimes, and controller agents.

Architecture: keep `agents.yaml` as the canonical persona roster, but stop treating it as the whole system. Add explicit objects for runtimes, controllers, channels, and bindings. Keep the state engine observational. Make onboarding support both existing agent estates and greenfield users.

Tech stack: current HTML docs/site, YAML/JSON registry, Python state engine, existing terminal wireframes.

---

## What is already solid

- The four-surface framing is still correct.
- The Operating Terminal concept is directionally right: multi-pane, tmux-like, chats + terminals + interventions.
- Registry + manifests as a canonical identity layer is correct.
- The state engine as a shared state snapshotter is directionally right.
- HTML definitional docs and wireframes are the right communication medium.

## What must change

- Stop describing PantheonOS as if it is primarily a central orchestration router.
- Separate persona agents from runtimes, controllers, channels, and bindings.
- Add a first-class “Connect Existing Setup” onboarding path.
- Teach the state engine to observe more than registry + git + realms.
- Reflect controller/overseer agents in the terminal and registry model.

---

## Target repo end state

### Registry layer

Keep:
- `registry/agents.yaml`
- `registry/agents/*.json`
- `registry/heartbeats.yaml`

Add:
- `registry/runtimes.yaml`
- `registry/controllers.yaml`
- `registry/channels.yaml`
- `registry/bindings.yaml`

### Docs / site layer

Keep:
- `site/operating-terminal.html`
- `site/development-plan.html`
- `site/data-model.html`

Add / revise:
- `site/system-model.html` — definitive explanation of persona agents, runtimes, controllers, channels, bindings, and onboarding modes
- revise `site/operating-terminal.html` to show persona panes and controller panes distinctly
- revise `site/development-plan.html` so “Scale & Orchestration” becomes “Multi-Runtime Observation & Intervention” or equivalent

### Runtime / engine layer

Keep:
- `engine/state_engine.py`

Evolve:
- ingest channels, runtimes, controllers, and bindings
- surface current runtime/controller health separately from persona heartbeat
- keep the engine observational, not authoritative

### UI / terminal layer

Terminal surface should render:
- persona chat panes
- controller terminal panes
- runtime health panes
- artifact panes
- intervention panes
- unified summaries and blockers

---

## Work plan

### Task 1: lock the architecture correction into the repo
Objective: make the corrected system model explicit in-repo.

Files:
- Create: `site/system-model.html`
- Modify: `README.md`
- Modify: `registry/README.md`

Verification:
- README no longer overstates central orchestration
- system-model doc clearly defines persona agents vs runtimes/controllers/channels
- registry README states current scope vs target scope

### Task 2: define the missing registry objects
Objective: add schema docs for runtimes, controllers, channels, and bindings.

Files:
- Create: `registry/runtimes.yaml`
- Create: `registry/controllers.yaml`
- Create: `registry/channels.yaml`
- Create: `registry/bindings.yaml`
- Modify: `docs/data-model-v2.md`
- Modify: `site/data-model.html`

Verification:
- a persona agent can be bound to multiple channels
- a runtime can host multiple persona agents
- a controller can manage one or more runtimes
- existing users can register their current setup without recreating agents

### Task 3: evolve the state engine into a true observer
Objective: expand observation without turning the engine into the router.

Files:
- Modify: `engine/state_engine.py`
- Modify: `data/pantheon-os-state.json` generation contract

Verification:
- state output distinguishes persona status, runtime status, and controller status
- bindings are visible in output
- missing channel/runtime data degrades gracefully

### Task 4: revise the terminal model around panes of relationship
Objective: make the operating terminal render the real topology.

Files:
- Modify: `site/operating-terminal.html`
- Modify: `terminal-manager.html`
- Modify: `docs/plans/terminal-manager-implementation.md`

Verification:
- terminal examples show chat panes, controller panes, and runtime health panes
- interventions target either persona, controller, or runtime explicitly
- multi-pane examples match actual user workflows

### Task 5: add onboarding modes
Objective: support both experienced users and new users.

Files:
- Modify: `site/development-plan.html`
- Create: `site/connect-existing-setup.html` or equivalent

Verification:
- onboarding path A = Connect Existing Setup
- onboarding path B = Start Fresh
- permissions can start at observe-only before message/control access

---

## Immediate next three actions

1. Commit the architecture correction docs now.
2. Define the four missing registry objects and their minimal schemas.
3. Update the state engine contract before touching specific agent manifests again.
