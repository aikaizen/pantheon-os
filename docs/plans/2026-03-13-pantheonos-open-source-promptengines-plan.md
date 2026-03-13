# PantheonOS Open-Source Plan for PromptEngines

## Objective
Make PantheonOS a real open-source product that works for PromptEngines first.

This means four things must become true at the same time:
1. PantheonOS is a credible open-source company operating system for people running multiple business lines with multiple agents.
2. The company dashboard and agent-management model are integrated instead of treated as separate concepts.
3. The terminal / tmux surface is grounded in a real local machine runtime, especially on Mac.
4. PromptEngines business units actually emit live metrics and telemetry into the system.

A fifth practical requirement sits across all of this:
- PantheonOS must produce hosted HTML surfaces so status, plans, handoffs, and briefings can be shared via links instead of markdown blobs.

---

## Product thesis
PantheonOS should be built as:
- an open-source control system for human-sovereign agent operations
- with PromptEngines as the first reference deployment
- and with a clear split between:
  - strategic surface: company dashboard
  - tactical surface: operating terminal
  - continuity substrate: runtime / portal

The repo should not be a static mock dashboard.
It should become a deployable system with real contracts, real adapters, and a real local runtime.

---

## Workstream 1 — Open-source PantheonOS productization

### Goal
Turn PantheonOS into a major open-source repo for operators managing:
- multiple companies or business lines
- multiple active agents
- multiple terminal sessions
- multiple telemetry sources
- shared approvals, handoffs, and operating context

### Core shift
The dashboard must stop being just a portfolio page.
It needs to become the strategic view of a multi-line, agent-native operating system.

### What must be built
1. Multi-company / multi-deployment model
   - deployment registry
   - company manifests
   - business-line registry
   - environment model (local, staging, production)

2. Dashboard-agent integration
   - every company surface linked to owners, agents, states, and handoffs
   - every active agent linked to current work, next work, blockers, artifacts, and terminal route
   - company overview and agent overview become two projections of the same source of truth

3. Open-source repo structure
   Recommended target structure:
   - `apps/web` — hosted company dashboard + reports + docs-facing UI
   - `apps/terminal` — operating terminal web surface
   - `packages/contracts` — agent, company, telemetry, portal, and pane contracts
   - `packages/adapters` — telemetry and runtime adapters
   - `packages/ui` — shared PantheonOS UI system
   - `packages/runtime-client` — client for local daemon / bridge
   - `services/macos-bridge` — local daemon for Mac terminal and chat control
   - `examples/promptengines` — first real reference deployment config
   - `docs/` — architecture, onboarding, deployment, and operator guides

4. Public open-source packaging
   - README that explains the product clearly
   - quickstart for local deployment
   - example config for PromptEngines
   - contribution model
   - issue / roadmap structure
   - example screenshots / previews

### Acceptance criteria
PantheonOS is productized enough when:
- a new operator can understand what it is from the README
- a company / deployment can be represented by manifests instead of hardcoded mock data
- dashboard and agent views are clearly linked
- PromptEngines works as the canonical example deployment

---

## Workstream 2 — Real operating terminal / tmux grounding on Mac

### Goal
Make the terminal-manager experience real.

The terminal surface should not remain a visual wireframe.
On a Mac, it needs a real control plane connected to:
- terminal instances
- tmux sessions
- logs
- Telegram chats
- future WhatsApp or additional channels

### Core design decision
Do not try to make browser-only terminal control the foundation.
The right architecture is:
- hosted / local web UI for the operator surface
- plus a local Mac bridge daemon with real OS access

### Recommended architecture
1. `pantheond` local bridge on macOS
   - runs on the user’s Mac
   - owns PTY / tmux / terminal integration
   - exposes a secure local API / WebSocket interface
   - manages process registry, pane routing, and session metadata

2. Terminal adapters
   - direct shell / PTY sessions
   - tmux session discovery and control
   - log stream attachment
   - optional Docker process visibility

3. Channel adapters
   - Telegram session / bot integration
   - message send / receive hooks
   - thread metadata and unread state
   - future WhatsApp adapter behind same interface

4. Operator surface behavior
   - pane creation and layout persistence
   - attach / detach / reconnect
   - send input
   - request summary
   - pause / resume / kill / reassign / escalate
   - link every session to company, agent, and portal objects

### MVP sequence
Phase A — Read-only reality
- discover terminals, tmux sessions, and chats
- display them in the operating terminal UI
- no intervention yet beyond open / inspect

Phase B — Basic control
- send input to shell / tmux panes
- switch sessions
- request agent summary
- send dashboard handoff into the runtime lane

Phase C — Real operator control
- pause / resume / restart / kill
- task / session reassignment
- intervention and escalation controls
- pane-layout persistence

### Acceptance criteria
This workstream is real when, on a Mac:
- PantheonOS can discover and display live terminal sessions
- PantheonOS can display Telegram threads with unread / state metadata
- the operator can send input or messages through the control surface
- the UI is connected to actual sessions, not a visual mock

---

## Workstream 3 — Metrics / telemetry wiring for PromptEngines business units

### Goal
Wire the dashboard to real metrics from the PromptEngines business units.

Each business unit has:
- its own repo
- its own admin panel
- its own data model

PantheonOS should not guess metrics from outside.
Each unit needs to be instrumented to publish a standard telemetry contract.

### Core design decision
PantheonOS should define the canonical telemetry contract.
Each business unit should implement an adapter to satisfy it.

### Required metric families
The current metric framing is already correct and should become the shared contract:
- Growth
- Finance
- Engagement
- Reliability
- Unit economics
- User profitability

### PromptEngines-first rollout order
#### Tier 1 — do first
- PromptEngines.com
- Kaizen
- Storybook Studio
- Bible

#### Tier 2 — next
- Video Terminal
- Norbu
- Consulting

#### Tier 3 — after canonical framing
- Flow
- Flow Education
- Vajra-Upaya
- other prototypes / support surfaces

### Required telemetry architecture
1. Shared contract package
   - event schema
   - financial schema
   - reliability schema
   - entity naming rules
   - time-window conventions
   - required dimensions per business unit

2. Adapter package per repo
   Examples:
   - `@pantheon/adapter-promptengines-web`
   - `@pantheon/adapter-kaizen`
   - `@pantheon/adapter-storybook`
   - `@pantheon/adapter-bible`

3. Business-unit instrumentation checklist
   Every unit must expose:
   - identity model
   - key business events
   - revenue / spend data
   - reliability signals
   - user / account rollups
   - API or DB access path for PantheonOS

4. Central aggregation layer
   PantheonOS should aggregate across units while preserving drill-down into each unit.

### PromptEngines-specific outcome
PromptEngines company view should eventually show:
- all business lines / products / prototypes
- live metrics by unit
- cross-company totals
- agent ownership by unit
- recent activity and blockers by unit

### Acceptance criteria
This workstream is real when:
- at least 3 to 4 PromptEngines business units are wired with live telemetry
- the company dashboard uses live adapters instead of only sample JSON
- company rollups and per-unit drilldowns are both available
- metric drift between repos and dashboard is reduced by shared contracts

---

## Cross-cutting workstream — Hosted HTML communication layer

## Goal
Create the best possible way for PantheonOS to communicate status, plans, handoffs, and reports through hosted HTML pages.

This is the answer to the communication problem:
- not long markdown pasted into chat
- not only screenshots
- but stable, shareable URLs to rendered operational pages

## Recommendation
Use PantheonOS itself as the hosted communication surface.
Deploy it to Vercel and make it produce operator-facing HTML routes.

### Best model
1. Vercel hosts the strategic / reporting UI
2. PantheonOS publishes stable routes such as:
   - `/briefs/latest`
   - `/briefs/{slug}`
   - `/deployments/promptengines`
   - `/agents/{id}`
   - `/runs/{id}`
   - `/handoffs/{id}`
   - `/reports/{date}`
3. Hermes can send you plain HTTPS links in chat
4. The pages can be:
   - static for plans and reports
   - dynamic for live status where appropriate

### Why this is the best approach
- HTML links are easier to consume in Telegram than markdown dumps
- pages can carry richer context, layout, tables, and visuals
- the same routes can become both human-facing and operational surfaces
- Vercel is a natural fit for hosted UI while the Mac bridge remains local for live control

### Important boundary
Hosted HTML is the right answer for:
- plans
- reports
- agent pages
- company dashboards
- status surfaces
- handoff pages

Hosted HTML is not the right first answer for:
- raw terminal control on a Mac
- direct PTY / tmux ownership
- local chat session management

Those should remain connected through the Mac bridge and surface into the hosted UI as summaries and selected state.

### MVP communication routes
Recommend starting with:
- `/briefs/latest` — newest operator brief
- `/deployments/promptengines` — company dashboard view
- `/agents/hermetic-demiurge` — current sitrep page
- `/handoffs/latest` — latest queued / resolved handoffs

### Acceptance criteria
This workstream is real when:
- Hermes can send you a stable HTML link instead of a markdown block
- the page is hosted on Vercel
- the page is readable on mobile
- the page reflects either a generated plan, report, or live status view

---

## Integrated execution order

## Phase 0 — repo and contract framing
- clean product framing in README
- finalize surface model: dashboard, terminal, portal, principles
- define contracts for deployments, agents, panes, portal state, telemetry
- establish PromptEngines as the reference deployment in docs and examples

## Phase 1 — hosted strategic surface
- move current dashboard into a proper web app structure
- deploy PantheonOS to Vercel
- implement stable HTML routes for reports / deployments / agents
- use PromptEngines as the first live hosted surface

## Phase 2 — local Mac runtime bridge
- build `pantheond` local bridge
- add shell / PTY / tmux discovery
- add Telegram thread visibility
- expose secure local API / WebSocket for the UI

## Phase 3 — PromptEngines telemetry adapters
- define shared metric contract package
- wire PromptEngines.com, Kaizen, Storybook Studio, and Bible first
- display live company and unit dashboards through adapters

## Phase 4 — operator-grade terminal manager
- add pane persistence
- add real session controls
- add intervention and escalation flows
- connect dashboard handoffs to the terminal-manager runtime lane

## Phase 5 — open-source hardening
- improve docs and onboarding
- add example deployment configs
- publish contribution standards
- ship example screenshots / demo data / local-first setup guide

---

## Definition of success
PantheonOS works for PromptEngines when:
- PromptEngines is represented as a real deployment, not a mock
- company dashboard and agent management are integrated
- operating terminal is connected to real Mac terminal / tmux / Telegram state
- multiple PromptEngines units publish real telemetry into PantheonOS
- hosted Vercel pages provide stable HTML links for status and communication
- the repo is clean enough that external users can understand and adopt it

---

## Immediate next moves
1. Commit this master plan into the PantheonOS repo
2. Set up Vercel on the PantheonOS repo
3. Restructure the UI into a proper hosted app surface
4. Add the first hosted HTML route for PromptEngines deployment status
5. Define the Mac bridge boundary before implementing terminal control
6. Start the PromptEngines telemetry contract with 3 to 4 business units
