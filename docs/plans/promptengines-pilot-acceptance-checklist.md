# PromptEngines pilot acceptance checklist

PantheonOS is ready to start real internal testing when every item below is true.

## Topology

- [ ] `registry/runtimes.yaml` exists and reflects the pilot runtime topology
- [ ] `registry/controllers.yaml` exists and reflects host-side overseer agents
- [ ] `registry/channels.yaml` exists and reflects existing PromptEngines channels
- [ ] `registry/bindings.yaml` exists and links persona agents, runtimes, controllers, and channels
- [ ] PromptEngines deployment metadata references the topology registries

## Observation

- [ ] state engine emits deployments, runtimes, controllers, channels, and bindings
- [ ] persona heartbeat is distinct from runtime heartbeat and controller heartbeat
- [ ] partial adapter failure does not break the whole state snapshot
- [ ] data/pantheon-os-state.json can be regenerated locally

## Terminal model

- [ ] terminal docs distinguish persona panes, controller panes, and runtime health panes
- [ ] at least one example workspace shows all three together
- [ ] interventions are scoped by observe / message / control

## Onboarding

- [ ] Connect Existing Setup path is documented
- [ ] Start Fresh path is documented
- [ ] docs do not assume PantheonOS created every agent from scratch

## PromptEngines pilot

- [ ] Tier 1 ventures are explicitly named
- [ ] observe-only pilot has approval
- [ ] message-level and controller-level approvals are explicit
- [ ] known blockers are visible, including promptengines-main write PAT constraints
