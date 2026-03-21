# Terminal Manager MVP

Topology-aware static app scaffold for the PantheonOS Operating Terminal.

Purpose:
- prove the corrected persona/runtime/controller model in a real app surface
- render a usable multi-pane workspace from `data/pantheon-os-state.json`
- stay migration-ready and static-host friendly before a richer React runtime lands

Files:
- `index.html`
- `assets/styles.css`
- `assets/app.js`
- `data/mock-state.json`

Behavior:
- tries to load `../../data/pantheon-os-state.json`
- falls back to `./data/mock-state.json`
- renders persona lanes, controller lanes, runtime health, and a workspace summary
