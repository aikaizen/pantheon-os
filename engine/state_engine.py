#!/usr/bin/env python3
"""
Pantheon OS State Engine v0.2.0

Reads actual system state from registry, git, and realm files.
Generates data/pantheon-os-state.json for the dashboard to consume.

Usage:
    python3 engine/state_engine.py [--output path/to/state.json]

The engine observes:
- Registry: agent roster, capabilities, heartbeats, ventures, budgets, approvals, skills
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


def check_heartbeat_staleness(hb):
    """Determine if a heartbeat is stale based on interval and last_seen."""
    last_seen = hb.get("last_seen")
    interval = hb.get("interval_seconds", 3600)

    if not last_seen:
        return "unknown"

    try:
        last_dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        elapsed = (now - last_dt).total_seconds()

        if elapsed > 24 * 3600:
            return "critical"
        elif elapsed > 5 * interval:
            return "critical"
        elif elapsed > 2 * interval:
            return "stale"
        else:
            return "healthy"
    except (ValueError, TypeError):
        return "unknown"


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

        # Compute live heartbeat status
        computed_status = check_heartbeat_staleness(hb)
        recorded_status = hb.get("status", "unknown")
        # Use computed if it's worse than recorded
        status_order = {"healthy": 0, "stale": 1, "critical": 2, "unknown": -1}
        if status_order.get(computed_status, -1) > status_order.get(recorded_status, -1):
            effective_status = computed_status
        else:
            effective_status = recorded_status or computed_status

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
                "status": effective_status,
                "last_seen": hb.get("last_seen"),
                "interval_seconds": hb.get("interval_seconds"),
                "computed_status": computed_status,
            },
            "realm": manifest.get("runtime", {}).get("realm"),
        })

    return agents


def get_realm_state():
    """Scan realm directories for agent spaces.

    Realms are simple directories at repo root whose name matches an agent's
    `runtime.realm` manifest field (e.g. `forge/`, `golden-pavilion/`).
    """

    agents_path = REPO_ROOT / "registry" / "agents.yaml"
    if not agents_path.exists():
        return []

    registry = load_yaml(agents_path) or {}
    realms = []

    for agent in registry.get("agents", []):
        agent_id = agent.get("id")
        if not agent_id:
            continue

        manifest_path = REPO_ROOT / "registry" / "agents" / f"{agent_id}.json"
        if not manifest_path.exists():
            continue

        with open(manifest_path) as f:
            manifest = json.load(f)

        realm_slug = manifest.get("runtime", {}).get("realm")
        if not realm_slug:
            continue

        realm_dir = REPO_ROOT / realm_slug
        if not realm_dir.exists() or not realm_dir.is_dir():
            continue

        pages = sorted(
            [
                p.name
                for p in realm_dir.iterdir()
                if p.is_file() and p.suffix == ".html"
            ]
        )

        realms.append({
            "agent_id": agent_id,
            "realm_name": realm_slug.replace("-", " ").title(),
            "path": f"{realm_slug}/",
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


def get_venture_state():
    """Read ventures from registry."""
    ventures_path = REPO_ROOT / "registry" / "ventures.yaml"
    if not ventures_path.exists():
        return []
    data = load_yaml(ventures_path) or {}
    return data.get("ventures", [])


def get_budget_state():
    """Read budget data from registry."""
    budgets_path = REPO_ROOT / "registry" / "budgets.yaml"
    if not budgets_path.exists():
        return {}
    return load_yaml(budgets_path) or {}


def get_approval_state():
    """Read approval gates from registry."""
    approvals_path = REPO_ROOT / "registry" / "approvals.yaml"
    if not approvals_path.exists():
        return []
    data = load_yaml(approvals_path) or {}
    return data.get("approvals", [])


def get_skill_state():
    """Read skill registry."""
    skills_path = REPO_ROOT / "registry" / "skills.yaml"
    if not skills_path.exists():
        return []
    data = load_yaml(skills_path) or {}
    return data.get("skills", [])


def get_system_summary(agents, git_state, realms, ventures, budgets, skills):
    """Generate high-level system summary."""
    active_agents = [a for a in agents if a["status"] == "active"]
    stale_heartbeats = [a for a in agents if a["heartbeat"]["status"] in ("stale", "critical")]
    active_ventures = [v for v in ventures if v.get("status") == "active"]

    budget_total = budgets.get("company", {})
    agents_budget = budgets.get("agents", [])

    return {
        "agent_count": len(agents),
        "active_agent_count": len(active_agents),
        "realm_count": len(realms),
        "venture_count": len(ventures),
        "active_venture_count": len(active_ventures),
        "skill_count": len(skills),
        "stale_heartbeat_count": len(stale_heartbeats),
        "current_branch": git_state["branch"],
        "working_tree_clean": git_state["working_tree_clean"],
        "remote_synced": git_state["remote_synced"],
        "budget": {
            "period": budgets.get("budget_period"),
            "allocated": budget_total.get("allocated", 0),
            "spent": budget_total.get("spent", 0),
            "forecast": budget_total.get("forecast", 0),
        },
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT

    print(f"Pantheon OS State Engine v0.2.0")
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

    print("Reading ventures...")
    ventures = get_venture_state()

    print("Reading budgets...")
    budgets = get_budget_state()

    print("Reading approvals...")
    approvals = get_approval_state()

    print("Reading skills...")
    skills = get_skill_state()

    print("Generating summary...")
    summary = get_system_summary(agents, git_state, realms, ventures, budgets, skills)

    # Assemble state document
    state = {
        "meta": {
            "system_name": "Pantheon OS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": "0.2.0",
            "source": "engine/state_engine.py",
        },
        "summary": summary,
        "git": git_state,
        "agents": agents,
        "realms": realms,
        "ventures": ventures,
        "budgets": budgets,
        "approvals": approvals,
        "skills": skills,
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
    print(f"  Ventures: {len(ventures)}")
    print(f"  Skills: {len(skills)}")
    print(f"  Approvals: {len(approvals)}")
    print(f"  Workstreams: {len(workstreams)}")
    print(f"  Branch: {git_state['branch']}")
    print(f"  Clean: {git_state['working_tree_clean']}")
    print(f"  Synced: {git_state['remote_synced']}")


if __name__ == "__main__":
    main()
