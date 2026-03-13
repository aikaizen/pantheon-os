# Workstream B — Terminal Manager MVP

## Objective
Define the ideal tactical control surface for Pantheon OS before building the live system.

## Product stance
The operating terminal is not just a terminal emulator.
It is a web-native control room for:
- chats
- terminals
- tmux sessions
- summaries
- interventions
- portal state
- artifacts
- approvals

## Immediate deliverable
Ship a wireframe first.
Do not build the live backend or terminal bridge yet.

## Must-have panes
- Channel pane
- Execution pane
- Summary pane
- Portal pane
- Inspector / control pane
- Log / observer pane

## Must-have controls
- split / resize / save layout
- attach / detach / reconnect session
- pause / resume / restart / kill
- broadcast input
- request summary
- reassign
- escalate
- inspect portal linkage

## Design direction
Use the same sharper PromptEngines / Lab Notes visual language as the dashboard.
This should feel like an operator’s control room, not a consumer app.

## Key promise
The operator should be able to steer the whole pantheon from one command-center interface instead of juggling tmux, chats, and memory manually.

## Success condition
A clear terminal-manager wireframe exists in Pantheon OS showing pane structure, intervention controls, and portal linkage, ready for a later implementation pass.
