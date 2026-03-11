# Operating Terminal Spec

## Purpose
The Operating Terminal is the tactical command-center surface of Pantheon OS.

It exists to help a human operator supervise and steer teams of agents in real time.

## Core idea
This is not just a terminal emulator. It is a multi-pane operating surface that can show:
- chats
- terminals
- tmux sessions
- tools
- logs
- summaries
- artifacts
- oversight state

## Required capabilities
- Multi-pane layout
- Workspaces per monitor
- Channel panes for Telegram, WhatsApp, and internal threads
- Execution panes for shells, tmux, docker consoles, logs
- Summary panes for agent state and blockers
- Oversight panes for outer harness and portal state

## Core controls
- pause
- resume
- restart
- kill
- reassign
- escalate
- inspect terminal
- inspect logs
- inspect portal
- request summary

## State model
- idle
- thinking
- executing
- waiting_on_tool
- waiting_on_human
- blocked
- reviewing
- error
- complete
- paused
