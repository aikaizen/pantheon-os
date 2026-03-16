#!/usr/bin/env python3
"""
Pantheon OS State Engine

Reads actual system state from registry, git, and realm files.
Generates data/pantheon-os-state.json for the dashboard to consume.

Usage:
    python3 engine/state_engine.py [--output path/to/state.json]

The engine observes:
- Registry: agent roster, capabilities, heartbeats
- Git: recent commits, branch state, file changes
- Realms: agent forge/realm pages and status
- Docs: workstream status, open plans
"""

import json
import os
import subprocess
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "data" / "pantheon-os-state.json"


def run_git(*args):
    """Run a git command in the repo root."""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def load_yaml(path):
    """Load a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def get_git_state():
    """Read git repository state."""
    branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    last_commit = run_git("log", "-1", "--format=%H|%s|%ai|%an")
    commit_hash, commit_msg, commit_date, commit_author = last_commit.split("|", 3)

    # Recent commits (last 10)
    log_raw = run_git("log", "-10", "--format=%H|%s|%ai")
    recent_commits = []
    for line in log_raw.splitlines():
        if "|" in line:
            h, msg, date = line.split("|", 2)
            recent_commits.append({
                "hash": h[:7],
                "message": msg,
                "date": date,
            })

    # Check for uncommitted changes
    status = run_git("status", "--porcelain")
    clean = len(status) == 0

    # Remote sync check
    run_git("fetch", "origin")
    remote_sha = run_git("rev-parse", f"origin/{branch}" if branch != "HEAD" else "origin/main")
    local_sha = run_git("rev-parse", "HEAD")
    synced = remote_sha == local_sha

    return {
        "branch": branch,
        "last_commit": {
            "hash": commit_hash[:7],
            "message": commit_msg,
            "date": commit_date,
            "author": commit_author,
        },
        "recent_commits": recent_commits,
        "working_tree_clean": clean,
        "remote_synced": synced,
    }


def get_agent_state():
    """Read agent roster and heartbeats from registry."""
    agents_path = REPO_ROOT / "registry" / "agents.yaml"
    heartbeats_path = REPO_ROOT / "registry" / "heartbeats.yaml"

    registry = load_yaml(agents_path)
    heartbeats_data = load_yaml(heartbeats_path) or {}
    heartbeats_list = heartbeats_data.get("heartbeats", [])

    # Index heartbeats by agent_id
    hb_map = {}
    for hb in heartbeats_list:
        if hb and "agent_id" in hb:
            hb_map[hb["agent_id"]] = hb

    agents = []
    for agent in registry.get("agents", []):
        agent_id = agent["id"]
        hb = hb_map.get(agent_id, {})

        # Read per-agent manifest for more detail
        manifest_path = REPO_ROOT / "registry" / "agents" / f"{agent_id}.json"
        manifest = {}
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)

        agents.append({
            "id": agent_id,
            "name": agent.get("name"),
            "type": agent.get("type"),
            "role": agent.get("role"),
            "status": agent.get("status"),
            "monthly_budget": agent.get("monthly_budget", 0),
            "capabilities": manifest.get("capabilities", []),
            "constraints": manifest.get("constraints", {}),
            "heartbeat": {
                "status": hb.get("status", "unknown"),
                "last_seen": hb.get("last_seen"),
                "interval_seconds": hb.get("interval_seconds"),
            },
            "realm": manifest.get("runtime", {}).get("realm"),
        })

    return agents


def get_realm_state():
    """Scan realm directories for agent spaces."""
    forge_dir = REPO_ROOT / "forge"
    realms = []

    if forge_dir.exists():
        pages = [f.name for f in forge_dir.iterdir() if f.suffix == ".html"]
        realms.append({
            "agent_id": "hermetic-demiurge",
            "realm_name": "Forge",
            "path": "forge/",
            "pages": pages,
            "page_count": len(pages),
        })

    return realms


def get_workstream_state():
    """Read active workstreams from docs."""
    ws_dir = REPO_ROOT / "docs" / "workstreams"
    workstreams = []

    if ws_dir.exists():
        for f in ws_dir.iterdir():
            if f.suffix == ".md" and f.name != "README.md":
                content = f.read_text()
                # Extract title from first heading
                title = f.stem
                for line in content.splitlines():
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                workstreams.append({
                    "file": f.name,
                    "title": title,
                })

    return workstreams


def get_system_summary(agents, git_state, realms):
    """Generate high-level system summary."""
    active_agents = [a for a in agents if a["status"] == "active"]
    stale_heartbeats = [a for a in agents if a["heartbeat"]["status"] in ("stale", "critical")]

    return {
        "agent_count": len(agents),
        "active_agent_count": len(active_agents),
        "realm_count": len(realms),
        "stale_heartbeat_count": len(stale_heartbeats),
        "current_branch": git_state["branch"],
        "working_tree_clean": git_state["working_tree_clean"],
        "remote_synced": git_state["remote_synced"],
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT

    print(f"Pantheon OS State Engine")
    print(f"Repo: {REPO_ROOT}")
    print(f"Output: {output_path}")
    print()

    # Gather state from all sources
    print("Reading git state...")
    git_state = get_git_state()

    print("Reading agent registry...")
    agents = get_agent_state()

    print("Scanning realms...")
    realms = get_realm_state()

    print("Reading workstreams...")
    workstreams = get_workstream_state()

    print("Generating summary...")
    summary = get_system_summary(agents, git_state, realms)

    # Assemble state document
    state = {
        "meta": {
            "system_name": "Pantheon OS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": "0.1.0",
            "source": "engine/state_engine.py",
        },
        "summary": summary,
        "git": git_state,
        "agents": agents,
        "realms": realms,
        "workstreams": workstreams,
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(state, f, indent=2)

    print()
    print(f"State written to {output_path}")
    print(f"  Agents: {len(agents)}")
    print(f"  Realms: {len(realms)}")
    print(f"  Workstreams: {len(workstreams)}")
    print(f"  Branch: {git_state['branch']}")
    print(f"  Clean: {git_state['working_tree_clean']}")
    print(f"  Synced: {git_state['remote_synced']}")


if __name__ == "__main__":
    main()
