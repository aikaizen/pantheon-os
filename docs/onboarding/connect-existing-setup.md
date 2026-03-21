# Connect Existing Setup

Use this path when the operator already has agents, channels, runtimes, and controller workflows.

## Goal
Attach PantheonOS to an existing agent estate without forcing the operator to recreate agents from scratch.

## Default posture
Start in `observe` mode.

PantheonOS should first prove it can see the existing setup before it is allowed to send messages or exercise control.

## Required steps

1. Register deployment metadata in `registry/deployments/*.json`.
2. Register existing runtimes in `registry/runtimes.yaml`.
3. Register existing controller/overseer agents in `registry/controllers.yaml`.
4. Register existing channels in `registry/channels.yaml`.
5. Bind persona agents, runtimes, controllers, and channels in `registry/bindings.yaml`.
6. Run the state engine and verify the topology is legible.
7. Upgrade individual bindings from `observe` to `message` or `control` only when safe.

## Minimum viable attachment

PantheonOS can begin useful operation once it can show:
- the principal CLI lane
- at least one persona chat lane
- at least one runtime
- at least one controller relationship
- basic health / heartbeat / summary state

## Acceptance checklist

- existing agents are represented without changing their soul or identity
- existing Telegram channels are registered as first-class channels
- existing docker runtimes are visible as runtimes, not mis-modeled as agents
- controller agents are visible separately from persona chats
- the operator can understand the system from one surface before enabling control
