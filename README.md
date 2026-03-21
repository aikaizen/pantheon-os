# Pantheon OS

Human-sovereign, agent-native company operating system. Deployable for any company — PromptEngines is the first internal deployment and reference environment.

## Surfaces

Pantheon OS has four integrated surfaces, not four separate products:

**1. Principles** — Constitutional layer. Defines sovereignty, authority, escalation, org structure, agent framing, omnidirectionality across media. Source of truth lives in `constitution/` and `registry/`.

**2. Company Dashboard** — Strategic surface. Makes the company legible: ventures, operators, budgets, approvals, goals, health, priorities. Current MVP is the seed, not the final product.

**3. Operating Terminal** — Tactical surface. TMUX-like multi-pane workspace for working across sovereign agent conversations, controller terminals, runtime health, logs, summaries, artifacts, and interventions in real time.

**4. Runtime / Portal** — Substrate. Observation and integration layer for runtimes, channels, heartbeats, artifacts, memory, and supervision. It is not a workflow engine; it is the shared state and control substrate that powers everything above.

## Repo structure

```
├── index.html                  # Company Dashboard MVP shell
├── terminal-manager.html       # Operating Terminal wireframe
├── assets/                     # Dashboard styles and rendering
├── data/                       # Dashboard mock data
├── constitution/               # Principles source-of-truth
│   ├── CONSTITUTION.md         #   Core constitutional document
│   └── pantheon-os-constitution.md
├── registry/                   # Agent and org manifests
│   ├── agents.yaml             #   Agent roster (canonical)
│   ├── heartbeats.yaml         #   Heartbeat tracking
│   └── agents/                 #   Per-agent manifest files
├── docs/
│   ├── system-architecture.md
│   ├── company-dashboard-spec.md
│   ├── operating-terminal-spec.md
│   ├── pane-system.md
│   ├── portal-model.md
│   ├── agent-state-model.md
│   ├── plans/                  # Specs and work plans
│   ├── workstreams/            # Active workstream definitions
│   ├── concepts/               # Conceptual frameworks
│   └── diagrams/               # Excalidraw diagrams
├── skills/                     # Shared skill definitions
└── apps/                       # Application scaffolds
    ├── promptengines-dashboard/ # Strategic dashboard app scaffold
    └── terminal-manager/        # Topology-aware Operating Terminal scaffold
```

## PromptEngines as first deployment

Pantheon OS is general. PromptEngines is the first real company using it. The repo supports both truths — the system is reusable, the deployment is real.

Quick readiness check:

```bash
python3 scripts/check_promptengines_pilot.py
```

## Related docs

- `site/system-model.html` — corrected system model: persona agents, runtimes, controllers, channels, bindings, and onboarding modes
- `site/promptengines-pilot.html` — PromptEngines-first pilot readiness plan for internal testing and later external packaging
- `site/connect-existing-setup.html` — primary onboarding path for operators with existing agents, runtimes, and channels
- `site/start-fresh.html` — greenfield onboarding path for new operators
- `docs/plans/2026-03-21-promptengines-pilot-readiness-plan.md` — execution plan for getting the repo ready for the PromptEngines reference deployment
- `examples/promptengines/README.md` — first reference deployment package for future operators adapting PantheonOS
- `pantheon-agent-deployment-prd.md` — PRD for dockerized agent deployment, multi-runtime support, and white-labeled Hermes packaging
- `site/agent-deployment.html` — definitional page for deployment paths, supported runtime systems, and white-labeled Hermes
- `site/hermetic-demiurge-handoff.html` — detailed execution handoff for Hermetic_Demiurge
- `site/dzambhala-handoff.html` — detailed execution handoff for Dzambhala

- `docs/plans/pantheon-os-spec-v1.md` — Product spec
- `docs/plans/pantheon-os-repo-work-plan.md` — Work plan
- `docs/system-architecture.md` — Architecture overview
- `docs/status/next-steps.md` — Current priorities
- `docs/workstreams/terminal-manager-mvp.md` — Terminal Manager workstream
- `docs/workstreams/promptengines-dashboard-mvp.md` — Dashboard workstream
