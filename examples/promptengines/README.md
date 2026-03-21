# PromptEngines Reference Deployment

PromptEngines is the first real deployment of PantheonOS.

This example package exists so later operators can see:
- what is specific to PromptEngines
- what is generic to the PantheonOS model
- how to attach an existing agent estate without rebuilding it from scratch

## What this example demonstrates

- sovereign persona agents are defined separately from runtimes and controllers
- existing channels are treated as first-class surfaces
- dockerized agent systems are modeled as runtimes
- host-side overseer agents are modeled as controllers
- bindings explicitly connect persona agents, channels, runtimes, and controllers

## Current reference objects

- deployment: `registry/deployments/promptengines.json`
- persona agents: `registry/agents.yaml`
- runtimes: `registry/runtimes.yaml`
- controllers: `registry/controllers.yaml`
- channels: `registry/channels.yaml`
- bindings: `registry/bindings.yaml`

## PromptEngines-first pilot shape

Tier 1 ventures:
- PromptEngines.com
- Lab Notes
- Kaizen
- Consulting

Primary runtime:
- `promptengines-hermes-primary`

Optional comparison runtime:
- `promptengines-openclaw-lab`

Primary controller:
- `promptengines-host-controller`

Primary onboarding path:
- Connect Existing Setup

## How to adapt this example later

1. copy the topology model, not the PromptEngines names
2. replace ventures and repos with your own
3. keep persona agents, runtimes, controllers, channels, and bindings separate
4. start in observe mode before enabling message or control
5. validate the topology and regenerate the state snapshot
