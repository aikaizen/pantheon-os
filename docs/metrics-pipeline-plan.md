# Prompt Engines Metrics Pipeline Plan

## Purpose
This document defines the most sensible way to make Pantheon OS stay up to date across Prompt Engines products, experiments, prototypes, and internal systems.

The design goal is simple:
- one dashboard
- one normalized metrics contract
- many source systems
- predictable freshness
- easy incremental wiring

## Core principle
Pantheon OS should not require every venture to share the same backend.
Instead, every venture should expose one adapter contract that maps local data into a shared dashboard shape.

That means:
- local product database stays local
- Pantheon OS receives normalized summary metrics
- missing integrations degrade gracefully
- each venture can be wired independently

## Recommended architecture

### Layer 1 — Source systems
Each venture keeps its own operational stack.
Examples:
- Storybook Studio: app DB, order/checkout data, print/order status, site analytics
- Kaizen: app DB, activation events, usage events, payments
- Bible: app DB and usage tables
- Flow: prototype data, task/workflow events, readiness signals
- PromptEngines.com / Lab Notes: web analytics, activity feed, build stream, publishing events

### Layer 2 — Venture adapter
Each venture gets one adapter that outputs a normalized payload.
This can be:
- an internal API endpoint
- a cron-generated JSON file
- a Supabase edge function
- a small Node/Python adapter service

The adapter should answer:
- current status
- health
- latest activity
- top metrics
- reliability indicators
- budget/cost estimate if available

### Layer 3 — Pantheon OS ingest
Pantheon OS should ingest normalized venture payloads into one central snapshot.
Short-term MVP:
- static JSON snapshot generated on schedule

Next step:
- scheduled pull from venture adapters
- merge into one `pantheon-os.json` payload
- keep a `last_updated_at` and `freshness_state` per venture

### Layer 4 — Dashboard render
The dashboard only reads the normalized snapshot.
It should not know raw product schemas.
This keeps the UI stable while ventures evolve independently.

## Shared metrics contract
Every venture adapter should return the same high-level shape.

Recommended contract:
- meta
  - venture_id
  - generated_at
  - freshness_state
- identity
  - name
  - stage
  - status
  - health
- activity
  - latest_events[]
- metrics
  - growth
  - engagement
  - revenue
  - reliability
- operating
  - owner
  - next_action
  - approvals_needed
- wiring
  - adapter_status
  - missing_inputs[]

## Freshness model
Every venture should carry one of:
- live
- scheduled
- delayed
- stale
- mock

This is critical.
The dashboard should never imply that stale data is live data.

## Per-venture recommendations

### PromptEngines.com
Best source inputs:
- web analytics
- GitHub activity feed output
- build stream output

Most useful MVP metrics:
- visitors
- source mix
- recent repo activity
- published lab notes count
- uptime/basic status

### Lab Notes
Best source inputs:
- article count
- build stream generation logs
- publish timestamps
- top article/page views if available

Most useful MVP metrics:
- publishing cadence
- build stream freshness
- article velocity

### Kaizen
Best source inputs:
- user creation
- active usage
- retention/cohort proxies
- payment events

Most useful MVP metrics:
- weekly active users
- activations
- revenue/credits
- failed sessions or system issues

### Storybook Studio
Use both domains explicitly:
- storybookstudio.promptengines.com
- storybookstudio.co

Best source inputs:
- session and signup events
- story generation count
- export/order funnel events
- payment/order statuses
- print and fulfillment states

Most useful MVP metrics:
- visitors
- story generations
- checkout starts
- paid orders
- shipped/completed orders
- print pipeline failures

Important contract note:
Storybook needs both product metrics and operations metrics. It is not enough to track signups only.

### Bible
Best source inputs:
- session/usage events
- search/read actions
- account creation if applicable
- DB reliability

Most useful MVP metrics:
- active users
- search/read actions
- response/database health

### Norbu
Best source inputs:
- learner sessions
- lesson completions
- content publishing cadence
- usage by curriculum path if available

Most useful MVP metrics:
- active learners
- completions
- content freshness

### Flow
Canonical status is now:
- prototype
- likely experiment soon

Best source inputs now:
- prototype internal usage
- workflow definitions created
- test runs / completions
- internal operator notes

Most useful MVP metrics now:
- prototype sessions
- workflows tested
- successful runs
- blockers

Do not overbuild Flow telemetry before the product has crossed into experiment mode.

### Video Terminal
Best source inputs:
- alpha user sessions
- project creations
- successful media renders/exports
- failure rates

Most useful MVP metrics:
- alpha sessions
- projects created
- render success rate

### Consulting
Best source inputs:
- CRM pipeline
- diagnostics sold
- pilot conversions
- active retainers
- delivery margin proxy

Most useful MVP metrics:
- qualified opportunities
- pilots active
- retained clients
- services-to-product conversion indicators

### Build Stream
Best source inputs:
- generated article timestamps
- repo activity summary
- by-repo commit counts
- publishing status

Most useful MVP metrics:
- freshness
- repos active in last 24h
- output generated yes/no

## Auth and security model
Pantheon OS is now intended to be gated public with Google auth, likely via Supabase Auth.

Recommended pattern:
- Supabase Auth with Google provider
- allowlist admin emails
- authenticated users can view dashboard
- admin users can change visibility states, wiring statuses, and future controls

Important separation:
- public-safe portfolio metadata may be visible to all authenticated users
- secrets, raw credentials, and sensitive budget details should never live in client-side JSON
- adapters should expose summaries, not secret-bearing internals

## Best implementation path

### Phase 1 — current MVP
- static mock snapshot
- explicit wiring notes
- stable dashboard UI

### Phase 2 — adapter contract rollout
Wire adapters in this order:
1. PromptEngines.com / Build Stream
2. Storybook Studio
3. Kaizen
4. Bible
5. Norbu
6. Consulting
7. Flow / Video Terminal / prototypes

This order balances visibility, business importance, and likely data availability.

### Phase 3 — scheduled aggregation
- create one scheduled aggregation job
- pull venture payloads
- write a single normalized snapshot
- mark freshness per venture

### Phase 4 — admin controls
- admin edits for visibility, stage, status, next action, and approvals
- human overrides where source systems lag reality

## Technical recommendation
Most sensible stack from here:
- Supabase Auth for Google login
- one small aggregation job on schedule
- venture adapters as simple edge functions or tiny API routes
- one normalized dashboard payload
- dashboard frontend remains thin and read-only except for admin controls later

## Human-side wiring needed
From the human side, the highest-value next inputs are:
- Supabase project for auth
- Google OAuth config
- domain/deployment hookup for dashboard.promptengines.com
- DB/API credentials for Storybook Studio, Kaizen, Bible, and Flow
- confirmation of which analytics stack each venture actually uses

## Final recommendation
Do not try to centralize all product data first.
Standardize the adapter contract first.

That keeps Pantheon OS current, flexible, and actually maintainable as Prompt Engines keeps changing.
