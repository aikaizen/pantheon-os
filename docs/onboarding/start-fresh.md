# Start Fresh

Use this path when the operator is new to agents and does not already have an existing runtime/controller/channel topology.

## Goal
Provision the smallest useful PantheonOS deployment with explicit persona agents, a runtime, a controller, and channels.

## Required steps

1. Define persona agents in `registry/agents.yaml` and `registry/agents/*.json`.
2. Define at least one runtime in `registry/runtimes.yaml`.
3. Define at least one controller in `registry/controllers.yaml`.
4. Define at least one principal-facing channel and one persona-facing channel in `registry/channels.yaml`.
5. Bind the topology in `registry/bindings.yaml`.
6. Start in `observe` mode where possible, then enable `message`, then `control`.
7. Run the state engine and verify the deployment renders correctly in the dashboard and Operating Terminal.

## Minimum useful topology

- 1 principal
- 1 persona agent
- 1 runtime
- 1 controller
- 2 channels
  - principal CLI
  - persona channel

## Acceptance checklist

- the deployment is legible in a single PantheonOS surface
- persona chat and controller console are distinct panes
- runtime health is visible
- bindings are explicit instead of implied
- the system can scale to more agents without changing the model
