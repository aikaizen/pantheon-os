# State Engine

The Pantheon OS state engine is an observer and normalizer. It reads registry state, git state, deployment topology, and realm information, then writes a shared state snapshot to `data/pantheon-os-state.json`. The topology model explicitly tracks host overseers, Dockerized Hermes instances, and per-instance agent slots.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 engine/state_engine.py
python3 engine/state_engine.py --output data/pantheon-os-state.json
```

## What it observes

- persona agents
- runtimes
- controllers
- channels
- bindings
- heartbeats
- ventures
- approvals
- skills
- git state
- realms

The state engine is not the workflow router. Its job is legibility.
