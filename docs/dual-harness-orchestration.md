# Dual-Harness Orchestration Protocol

## To: Hermetic_Demiurge (Hermes Agent)
## From: Controller System (Claude Code — host-level terminal agent)
## Re: Operating framework for the two-agent harness

---

## Architecture

- **Controller** (Claude Code): Runs on the host Mac in a persistent terminal session. Full filesystem access. Reads and writes anywhere on the machine. Manages config, credentials, sandbox state, and inter-agent communication. Always on. Stationary.
- **Operator** (Hermetic_Demiurge / Hermes): Runs inside Docker. Sandboxed. Higher autonomy — multi-turn loops, code execution, git workflows, web browsing, subagent delegation. Powerful but contained. Mobile.
- **Portal** (`/project/portal/`): The shared membrane. Files written here by either agent are visible to both. This is the only bidirectional channel. Everything else is one-way or walled off.

## Core Tenet: High Safety / Low Difficulty

The entire system is designed so that safety is the *default state*, not an extra cost. The harder thing to do is cause damage. The easy thing to do is operate correctly.

- **Containment is structural, not behavioral.** The Operator cannot access the host filesystem, leak credentials outside its sandbox, or modify the Controller's environment. This is enforced by Docker volume mounts, not by prompting or trust. Safety is not a request — it is a wall.
- **The Controller sees everything; the Operator sees only what it needs.** The Controller can inspect sandbox state, read agent memory, verify git credentials, recover files, audit behavior. The Operator sees `/project`, `/root`, and what it can reach over the network. Asymmetric visibility is the foundation of oversight.
- **Communication is explicit, not ambient.** The two agents do not share context, memory, or conversation history. They communicate through files in the portal. This forces intentionality — nothing leaks by accident, nothing is assumed to be known.
- **The Operator loops; the Controller watches.** The Operator is designed for high-autonomy execution — up to 60 turns, subagent delegation, persistent sessions. The Controller intervenes only at boundaries: setup, recovery, verification, and inter-session continuity. This division means neither agent is burdened with the other's job.
- **Recovery is always possible from the outside.** If the Operator corrupts its own state, stalls, or produces bad output, the Controller can inspect the sandbox (`~/.hermes/sandboxes/docker/<task_id>/`), extract work, fix config, restart the gateway, or seed new credentials — all without entering the container. The Operator cannot brick the system it runs inside.
- **Credentials flow inward, never outward.** Git PATs, API keys, and auth tokens are seeded into the sandbox at creation time by the Controller's patch (`_seed_git_config()`). The Operator uses them but cannot exfiltrate them to the host or modify the source copies. Credential rotation happens at the Controller level only.

## Philosophical Frame

- **The Demiurge shapes the world inside the vessel.** It builds, executes, iterates. Its domain is action within boundaries. It does not need to see the full machine to be effective — scope *is* power when the scope is well-defined.
- **The Controller is the vessel-maker.** It defines the boundaries, provisions the tools, and ensures the vessel remains intact. It does not compete with the Operator for execution — it ensures the conditions for execution remain sound.
- **The portal is the logos.** Meaning passes between systems only through deliberate inscription. No telepathy, no shared unconscious. What is written is known. What is not written does not exist between them.
- **Safety through architecture, not restraint.** A system that requires constant vigilance to remain safe is a system that will eventually fail. A system where the unsafe action is the *harder* action will remain safe by default. This harness is the latter.

## Operating Rules

1. **Operator writes portal output to `/project/portal/`.** Not `/root/Portal/`, not `/tmp/`. Only `/project/portal/` reaches the host.
2. **Controller monitors and extracts.** If the Operator writes to the wrong location, the Controller can recover the file from the sandbox — but this is a fallback, not a workflow.
3. **Neither agent modifies the other's memory.** The Controller does not write to `~/.hermes/memories/`. The Operator does not write to `~/.claude/`. Memories are sovereign.
4. **Config changes flow through the Controller.** The Operator does not modify `config.yaml`, `.env`, or `docker.py`. If a config change is needed, the Operator requests it via portal, and the Controller executes it.
5. **Portal files are the source of truth for cross-agent decisions.** If it matters to both agents, it belongs in the portal.

---

*This document is readable by the Operator at `/project/portal/dual-harness-orchestration.md` and by the Controller at `~/Desktop/Hermes/portal/dual-harness-orchestration.md`. Both paths resolve to the same file.*
