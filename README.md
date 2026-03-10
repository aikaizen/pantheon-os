# Pantheon OS

Company operating system for Prompt Engines.

Local-first, constitution-first, pantheon-aware, manifest-driven, connector-flexible.

Current branch status:
- working MVP dashboard with Prompt Engines-aligned mock data
- intended eventual host: dashboard.promptengines.com
- current mode: static MVP with explicit wiring placeholders for human-provided credentials, auth, and live adapters

## MVP included in this repo

- `index.html` — working static dashboard shell
- `assets/styles.css` — dark-mode control-room styling
- `assets/app.js` — rendering logic for the dashboard sections
- `data/pantheon-os.json` — Prompt Engines-aligned mock data
- `data/company-os.json` — compatibility alias
- `docs/mvp-wiring-checklist.md` — exact human-side inputs still needed
- `docs/previews/pantheon-os-mvp-preview.png` — preview image of the dashboard mockup

## MVP sections

- overview
- full portfolio across products, experiments, prototypes, services, and internal systems
- live activity / build-stream style feed
- goal tree
- heartbeats
- approvals
- budget visibility
- operators / agents
- explicit wiring needed from the human side
- guidance layer

## Prompt Engines alignment

The dashboard currently models:
- PromptEngines.com
- Lab Notes
- Pantheon OS Dashboard
- Build Stream
- Consulting
- Kaizen
- Storybook Studio
- Norbu
- Bible
- Flow
- Video Terminal
- Flow Education
- Vajra-Upaya
- Blayde

Operators currently modeled:
- A.I.
- Andy Stable
- Hermetic_Demiurge
- Thoth
- Prometheus
- Golem

## Notes

This MVP is intentionally static and safe.
Anything not yet live-wired is surfaced explicitly in the wiring section so the next step is obvious.

## Access model

- Target host: `dashboard.promptengines.com`
- Visibility model: gated public
- Auth model: Google auth via Supabase Auth (preferred)
- Admin control: all ventures visible on the dashboard; admin controls future visibility states and privileged operations

## Metrics pipeline

See `docs/metrics-pipeline-plan.md` for the recommended adapter-based metrics architecture and venture-by-venture wiring plan.
