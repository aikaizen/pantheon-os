# PromptEngines pilot readiness plan — PantheonOS reference deployment

> For Hermes: use this plan to get the repo ready for internal PromptEngines testing before deeper per-agent expansion.

Goal: make PantheonOS ready to start real internal testing with PromptEngines.com and the PromptEngines suite of ventures/apps, while keeping the system reusable for other operators later.

Architecture: PromptEngines is the first reference deployment, not a one-off special case. PantheonOS should treat PromptEngines as a real company deployment running sovereign persona agents across existing channels and runtimes, with controller agents supervising those runtimes. The repo should become ready for observation-first testing, then selective intervention, then external packaging.

Tech stack: current HTML documentation/site, YAML/JSON registry, Python state engine, terminal wireframes, Telegram + CLI surfaces, dockerized agent runtimes, host-side controller agents.

---

## What “ready to start testing” means

PantheonOS is ready for PromptEngines pilot use when all of the following are true:

1. PromptEngines exists in the repo as a full reference deployment, not just a venture list.
2. The registry can represent persona agents, runtimes, controllers, channels, and bindings.
3. The state engine can observe at least one real runtime, one real controller, and multiple real channels.
4. The Operating Terminal can show real multi-pane relationships: persona chat panes, controller panes, runtime health, artifacts, and interventions.
5. Existing agent setups can be attached without re-creating the agents from scratch.
6. The public docs explain both PromptEngines-first deployment and the later path for outside operators.

---

## Pilot scope

### Tier 1 — first ventures to wire into the pilot

These should be the first PromptEngines surfaces visible in PantheonOS:
- `promptengines-web`
- `lab-notes`
- `kaizen`
- `consulting`

Reason: they give a mix of core brand surface, publishing, product, and service operations without forcing every experimental venture into the first test cycle.

### Tier 2 — add after the pilot works daily

- `norbu`
- `bible`
- `storybook-studio`

### Tier 3 — keep visible in the dashboard, but do not make them first-wave runtime dependencies

- `flow`
- `video-terminal`
- `flow-education`
- `vajra-upaya`

---

## Core design principles for this phase

- PromptEngines first, but not hardcoded forever.
- Observe first, control second.
- Support “Connect Existing Setup” before assuming greenfield provisioning.
- Separate persona agents from runtimes, controllers, channels, and bindings.
- Keep HTML pages as the main communication medium for large plans and system definitions.
- Do not overbuild automation before real operator usage proves the need.

---

## Workstream 1 — PromptEngines reference deployment model

### Objective
Turn PromptEngines from “the first deployment in prose” into an explicit deployment model in the repo.

### Files
- Modify: `registry/deployments/promptengines.json`
- Create: `registry/runtimes.yaml`
- Create: `registry/controllers.yaml`
- Create: `registry/channels.yaml`
- Create: `registry/bindings.yaml`
- Modify: `docs/data-model-v2.md`
- Modify: `site/data-model.html`

### What must be represented
- host machines / computers
- dockerized agent systems
- controller agents with host access
- persona agent → runtime bindings
- persona agent → channel bindings
- runtime → controller bindings
- deployment modes: `observe`, `message`, `control`

### Acceptance criteria
- PromptEngines deployment can be declared without conflating persona identity and machine/runtime identity.
- Existing Telegram channels and CLI sessions can be registered as first-class channels.
- One runtime can host multiple persona agents.
- One controller can supervise one or more runtimes.

---

## Workstream 2 — State engine as real observer

### Objective
Expand the state engine from registry+git+realms into a real observer for the PromptEngines pilot.

### Files
- Modify: `engine/state_engine.py`
- Modify: `data/pantheon-os-state.json` generation contract
- Create: `docs/state-engine-v3-plan.md` or equivalent

### Required outputs
- persona status
- controller status
- runtime status
- channel activity summaries
- heartbeat status by object type
- venture/operator overlays for PromptEngines ventures
- intervention targets with explicit object type

### Acceptance criteria
- state output distinguishes persona liveness from controller/runtime liveness
- missing adapters degrade gracefully without breaking the whole snapshot
- internal pilot can run with partial observability while more adapters are added

---

## Workstream 3 — Operating Terminal internal MVP

### Objective
Make the terminal surface useful for daily PromptEngines work, not just visually interesting.

### Files
- Modify: `terminal-manager.html`
- Modify: `site/operating-terminal.html`
- Modify: `docs/plans/terminal-manager-implementation.md`

### Required pane types
- persona chat pane
- controller terminal pane
- runtime health pane
- artifact pane
- intervention pane
- summary / blocker pane

### Acceptance criteria
- at least one workspace can show Hermetic_Demiurge, Dzambhala, a controller pane, and runtime health together
- panes clearly distinguish persona conversations from controller consoles
- operator can understand what is happening without reading raw logs everywhere

---

## Workstream 4 — PromptEngines venture integration

### Objective
Make the dashboard and terminal reflect the actual PromptEngines business surface area.

### Files
- Modify: `registry/ventures.yaml`
- Modify: `site/development-plan.html`
- Modify: `site/index.html`
- Create: `site/promptengines-pilot.html`

### Required outcomes
- Tier 1 ventures have clear owners, operators, domains, repos, and next actions
- the dashboard can show which ventures are actually participating in the pilot
- public/private boundaries are explicit for PromptEngines-first testing

### Acceptance criteria
- PromptEngines.com is visible as the reference deployment
- the pilot scope is clear and does not imply all ventures are equally live on day one
- venture/operator data aligns with the deployment model

---

## Workstream 5 — Onboarding modes

### Objective
Support both experienced operators and new users, starting with the experienced path.

### Files
- Create: `site/connect-existing-setup.html`
- Create or modify: `docs/onboarding/connect-existing-setup.md`
- Create or modify: `docs/onboarding/start-fresh.md`
- Modify: `README.md`

### Required modes
1. Connect Existing Setup
   - register existing agents
   - register existing Telegram bots/channels
   - register existing docker runtimes
   - register existing controller agents
   - start in observe-only mode

2. Start Fresh
   - define persona agents
   - create initial runtime/controller topology
   - create first channels and bindings

### Acceptance criteria
- experienced users can adopt PantheonOS without rebuilding their agent estate
- new users still have a greenfield path
- docs do not assume Pantheon owns the origin of every agent

---

## Workstream 6 — Pilot operations and safety

### Objective
Make the internal PromptEngines pilot safe enough to use and informative enough to improve quickly.

### Files
- Modify: `registry/approvals.yaml`
- Modify: `registry/heartbeats.yaml`
- Create: `docs/plans/promptengines-pilot-rollout.md`
- Create: `docs/plans/promptengines-pilot-acceptance-checklist.md`

### Required controls
- observe/message/control permissions
- controller actions behind explicit approval where needed
- heartbeat expectations for persona agents, controllers, and runtimes
- stale/failing runtime escalation
- manual rollback path when adapters or panes break

### Acceptance criteria
- pilot can fail partially without blinding the operator
- dangerous operations are gated
- there is a written checklist for “ready to start internal testing”

---

## Workstream 7 — Productization for later external users

### Objective
Make the PromptEngines deployment become the first reusable example, not a dead-end internal special case.

### Files
- Create: `examples/promptengines/README.md` or equivalent reference deployment package
- Modify: `README.md`
- Create: `site/reference-deployments.html` or equivalent

### Required outcomes
- PromptEngines is clearly documented as the first reference deployment
- later users can understand what to copy, what to customize, and how to attach existing setups
- repo narrative shows internal dogfooding first, external generalization second

### Acceptance criteria
- the first outside operator can see how to adapt PantheonOS to their own machines, channels, and runtimes
- PromptEngines-specific facts are separated from general system contracts

---

## Key blockers to resolve early

- `promptengines-main` write PAT remains blocked for Hermetic_Demiurge plane work
- state engine runtime dependency on PyYAML is not yet made explicit enough
- no channel/runtime/controller registries yet
- no real observation adapters yet for Telegram/runtime/controller surfaces
- current docs still contain some pre-correction orchestration language

---

## Recommended execution order

1. Lock the PromptEngines pilot scope and reference deployment model.
2. Add the missing registry objects: runtimes, controllers, channels, bindings.
3. Expand the state engine contract.
4. Revise the Operating Terminal around persona/controller/runtime panes.
5. Define onboarding for Connect Existing Setup.
6. Wire Tier 1 PromptEngines ventures into the pilot.
7. Run an internal pilot before pushing harder on external productization.

---

## Repo end state for the first real PromptEngines test

The repo is ready for first internal testing when it has:
- a corrected system model
- a PromptEngines pilot plan
- a declared PromptEngines deployment topology
- registries for runtimes/controllers/channels/bindings
- a state engine that can emit partial real observation
- a terminal model that reflects actual multi-agent work
- onboarding docs for both existing and greenfield users
- a clear pilot checklist and acceptance gate

---

## Immediate next three actions

1. Create the missing registry objects and wire them into the data model.
2. Define the PromptEngines deployment topology: hosts, runtimes, controllers, channels, bindings.
3. Update the state engine contract before changing specific agents again.
