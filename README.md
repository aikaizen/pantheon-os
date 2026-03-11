# Pantheon OS

Pantheon OS is a human-sovereign, agent-native company operating system.

It is being developed as a reusable best-practice system that can be deployed for any company, with PromptEngines as the first internal deployment and reference environment.

## Product framing

Pantheon OS has four major surfaces:

1. Principles
2. Company Dashboard
3. Operating Terminal
4. Runtime / Portal

### Principles
The constitutional and organizational layer.

This defines:
- sovereignty
- authority
- escalation
- org structure
- agent framing
- omnipotence within scope
- omnidirectionality across media

### Company Dashboard
The strategic surface.

This is the most visible part of the current project.

It exists to make the company legible:
- products
- prototypes
- experiments
- services
- internal systems
- budgets
- approvals
- health
- priorities

### Operating Terminal
The tactical surface.

This is the second major visible surface after the dashboard.

It is the command-center IDE for operating teams of agents across:
- chats
- terminals
- tmux panes
- tools
- logs
- summaries
- artifacts
- interventions

### Runtime / Portal
The substrate beneath the visible surfaces.

This includes:
- dual-harness orchestration
- portal state
- event flow
- memory
- runtime supervision
- agent state transitions

## Current repo state

This repository currently contains:
- a working static company dashboard MVP
- PromptEngines-aligned mock data
- dual-harness notes
- metrics wiring notes
- early structure for constitution and registry artifacts

The current dashboard MVP is the seed, not the full product.

## Current emphasis

Right now, the project emphasis is:
1. dashboard as the primary visible surface
2. operating terminal as the next major surface
3. principles as the already-strong conceptual foundation
4. runtime / portal as the substrate that ties the system together

## PromptEngines as first deployment

PromptEngines is the first internal deployment of Pantheon OS.

That means this repo should support two truths at once:
- Pantheon OS is a general operating system for companies
- PromptEngines is the first real company using it

The repo should therefore avoid collapsing the whole product into a PromptEngines-only dashboard.

## Repository structure

### Current important files
- `index.html` — current static dashboard shell
- `assets/styles.css` — current dashboard styling
- `assets/app.js` — rendering logic for the static dashboard
- `data/pantheon-os.json` — dashboard mock data
- `data/pantheon-os.js` — browser-loaded mock data wrapper
- `docs/dual-harness-orchestration.md` — current dual-harness note
- `docs/mvp-wiring-checklist.md` — current MVP wiring needs

### Principles layer
- `constitution/`
- `registry/`

### Docs layer
- `docs/`

## What needs to happen next

### 1. Reframe the repo
The repo needs to clearly present Pantheon OS as:
- Principles
- Company Dashboard
- Operating Terminal
- Runtime / Portal

### 2. Populate the principles layer
The empty structure in `constitution/` and `registry/` needs to become real source-of-truth artifacts.

### 3. Add the operating terminal spec
The repo needs explicit docs for:
- pane system
- portal model
- agent state model
- operating terminal behavior

### 4. Evolve the data model
The current data model is dashboard-first.
It should evolve to also represent:
- org structure
- agent manifests
- runtime state
- portal summaries
- pane/workspace models

### 5. Reposition the current UI
The current UI should be treated as the Company Dashboard surface, not the whole of Pantheon OS.

## Access / deployment notes

The PromptEngines website dashboard itself may be built in the PromptEngines repo.

Within Pantheon OS, the dashboard remains a first-class surface of the product, but Pantheon OS should not be reduced to that single surface.

## Related docs

- `docs/system-architecture.md`
- `docs/company-dashboard-spec.md`
- `docs/operating-terminal-spec.md`
- `docs/pane-system.md`
- `docs/portal-model.md`
- `docs/agent-state-model.md`
- `constitution/pantheon-os-constitution.md`
- `registry/README.md`
- `docs/workstreams/promptengines-dashboard-mvp.md`
- `docs/workstreams/terminal-manager-mvp.md`
- `docs/concepts/inverted-pyramid-org.md`
- `docs/concepts/agent-capability-skill-model.md`
- `docs/concepts/model-scaling-thesis.md`
