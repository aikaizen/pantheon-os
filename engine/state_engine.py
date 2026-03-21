#!/usr/bin/env python3
"""
Pantheon OS State Engine v0.3.1

Reads actual system state from registry, git, deployment topology, and realm files.
Generates data/pantheon-os-state.json for the dashboard and operating terminal.

Usage:
    python3 engine/state_engine.py
    python3 engine/state_engine.py --output data/pantheon-os-state.json

Dependencies:
    pip install -r requirements.txt
"""

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "data" / "pantheon-os-state.json"


def run_git(*args, check=True):
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def load_yaml(path):
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def load_json(path):
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def get_git_state():
    branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    last_commit = run_git("log", "-1", "--format=%H|%s|%ai|%an")
    commit_hash, commit_msg, commit_date, commit_author = last_commit.split("|", 3)

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

    status = run_git("status", "--porcelain")
    clean = len(status) == 0

    run_git("fetch", "origin", check=False)
    remote_ref = f"origin/{branch}" if branch and branch != "HEAD" else "origin/main"
    remote_sha = run_git("rev-parse", remote_ref, check=False)
    local_sha = run_git("rev-parse", "HEAD", check=False)
    synced = bool(remote_sha and local_sha and remote_sha == local_sha)

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
        if elapsed > 5 * interval:
            return "critical"
        if elapsed > 2 * interval:
            return "stale"
        return "healthy"
    except (ValueError, TypeError):
        return "unknown"


def heartbeat_ref(entry):
    if entry.get("object_ref"):
        return entry["object_ref"]
    if entry.get("agent_id"):
        return f"registry:agents.yaml#{entry['agent_id']}"
    if entry.get("runtime_id"):
        return f"registry:runtimes.yaml#{entry['runtime_id']}"
    if entry.get("controller_id"):
        return f"registry:controllers.yaml#{entry['controller_id']}"
    return None


def get_heartbeats_map():
    heartbeats_path = REPO_ROOT / "registry" / "heartbeats.yaml"
    heartbeats_data = load_yaml(heartbeats_path) or {}
    hb_map = {}
    for hb in heartbeats_data.get("heartbeats", []):
        if not hb:
            continue
        ref = heartbeat_ref(hb)
        if ref:
            hb_map[ref] = hb
    return hb_map


def effective_heartbeat(hb):
    computed_status = check_heartbeat_staleness(hb)
    recorded_status = hb.get("status", "unknown")
    status_order = {"healthy": 0, "stale": 1, "critical": 2, "unknown": -1}
    if status_order.get(computed_status, -1) > status_order.get(recorded_status, -1):
        status = computed_status
    else:
        status = recorded_status or computed_status
    return {
        "status": status,
        "last_seen": hb.get("last_seen"),
        "interval_seconds": hb.get("interval_seconds"),
        "computed_status": computed_status,
        "summary": hb.get("last_summary"),
    }


def load_bindings():
    bindings_path = REPO_ROOT / "registry" / "bindings.yaml"
    return load_yaml(bindings_path) or {"bindings": {}}


def build_binding_indexes(bindings_doc):
    bindings = bindings_doc.get("bindings", {})
    indexes = {
        "agent_runtime": {},
        "agent_channel": {},
        "runtime_controller": {},
    }

    for item in bindings.get("agent_runtime", []):
        indexes["agent_runtime"].setdefault(item.get("agent_id"), []).append(item)

    for item in bindings.get("agent_channel", []):
        indexes["agent_channel"].setdefault(item.get("agent_id"), []).append(item)

    for item in bindings.get("runtime_controller", []):
        indexes["runtime_controller"].setdefault(item.get("runtime_id"), []).append(item)

    return indexes


def get_agent_state(binding_indexes, hb_map):
    agents_path = REPO_ROOT / "registry" / "agents.yaml"
    registry = load_yaml(agents_path) or {}
    agents = []

    for agent in registry.get("agents", []):
        agent_id = agent["id"]
        ref = f"registry:agents.yaml#{agent_id}"
        manifest_path = REPO_ROOT / "registry" / "agents" / f"{agent_id}.json"
        manifest = load_json(manifest_path) or {}
        hb = hb_map.get(ref, {})
        runtime_bindings = binding_indexes["agent_runtime"].get(agent_id, [])
        channel_bindings = binding_indexes["agent_channel"].get(agent_id, [])

        agents.append({
            "id": agent_id,
            "ref": ref,
            "name": agent.get("name"),
            "type": agent.get("type"),
            "role": agent.get("role"),
            "status": agent.get("status"),
            "monthly_budget": agent.get("monthly_budget", 0),
            "capabilities": manifest.get("capabilities", []),
            "constraints": manifest.get("constraints", {}),
            "heartbeat": effective_heartbeat(hb),
            "realm": manifest.get("runtime", {}).get("realm"),
            "runtime_bindings": runtime_bindings,
            "channel_bindings": channel_bindings,
        })

    return agents


def get_realm_state():
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
    ws_dir = REPO_ROOT / "docs" / "workstreams"
    workstreams = []
    if ws_dir.exists():
        for f in ws_dir.iterdir():
            if f.suffix == ".md" and f.name != "README.md":
                content = f.read_text()
                title = f.stem
                for line in content.splitlines():
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                workstreams.append({"file": f.name, "title": title})
    return workstreams


def get_venture_state():
    ventures_path = REPO_ROOT / "registry" / "ventures.yaml"
    data = load_yaml(ventures_path) or {}
    return data.get("ventures", [])


def get_budget_state():
    budgets_path = REPO_ROOT / "registry" / "budgets.yaml"
    return load_yaml(budgets_path) or {}


def get_approval_state():
    approvals_path = REPO_ROOT / "registry" / "approvals.yaml"
    data = load_yaml(approvals_path) or {}
    return data.get("approvals", [])


def get_skill_state():
    skills_path = REPO_ROOT / "registry" / "skills.yaml"
    data = load_yaml(skills_path) or {}
    return data.get("skills", [])


def get_runtime_state(binding_indexes, hb_map):
    runtimes_path = REPO_ROOT / "registry" / "runtimes.yaml"
    data = load_yaml(runtimes_path) or {}
    runtimes = []
    for runtime in data.get("runtimes", []):
        runtime_id = runtime["id"]
        ref = f"registry:runtimes.yaml#{runtime_id}"
        controller_bindings = binding_indexes["runtime_controller"].get(runtime_id, [])
        hb = hb_map.get(ref, {})
        runtimes.append({
            **runtime,
            "ref": ref,
            "controller_bindings": controller_bindings,
            "heartbeat": effective_heartbeat(hb),
        })
    return runtimes


def get_controller_state(hb_map):
    controllers_path = REPO_ROOT / "registry" / "controllers.yaml"
    data = load_yaml(controllers_path) or {}
    controllers = []
    for controller in data.get("controllers", []):
        controller_id = controller["id"]
        ref = f"registry:controllers.yaml#{controller_id}"
        hb = hb_map.get(ref, {})
        controllers.append({
            **controller,
            "ref": ref,
            "heartbeat": effective_heartbeat(hb),
        })
    return controllers


def get_channel_state():
    channels_path = REPO_ROOT / "registry" / "channels.yaml"
    data = load_yaml(channels_path) or {}
    channels = []
    for channel in data.get("channels", []):
        channels.append({
            **channel,
            "ref": f"registry:channels.yaml#{channel['id']}",
        })
    return channels


def get_deployment_state():
    deployments_dir = REPO_ROOT / "registry" / "deployments"
    deployments = []
    if not deployments_dir.exists():
        return deployments
    for path in sorted(deployments_dir.glob("*.json")):
        deployment = load_json(path)
        if deployment:
            deployments.append(deployment)
    return deployments


def get_system_summary(agents, runtimes, controllers, channels, git_state, realms, ventures, budgets, skills, deployments):
    active_agents = [a for a in agents if a.get("status") == "active"]
    active_runtimes = [r for r in runtimes if r.get("status") == "active"]
    active_controllers = [c for c in controllers if c.get("status") == "active"]
    runtime_systems = {r.get("runtime_system") for r in runtimes if r.get("runtime_system")}
    white_labeled_runtimes = [r for r in runtimes if r.get("branding_mode") == "white_labeled"]
    active_channels = [c for c in channels if c.get("status") == "active"]
    active_ventures = [v for v in ventures if v.get("status") == "active"]

    stale_heartbeats = []
    for collection in (agents, runtimes, controllers):
        stale_heartbeats.extend([item for item in collection if item.get("heartbeat", {}).get("status") in ("stale", "critical")])

    budget_total = budgets.get("company", {})

    return {
        "agent_count": len(agents),
        "active_agent_count": len(active_agents),
        "runtime_count": len(runtimes),
        "active_runtime_count": len(active_runtimes),
        "controller_count": len(controllers),
        "active_controller_count": len(active_controllers),
        "runtime_system_count": len(runtime_systems),
        "white_labeled_runtime_count": len(white_labeled_runtimes),
        "channel_count": len(channels),
        "active_channel_count": len(active_channels),
        "deployment_count": len(deployments),
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


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Pantheon OS state snapshot")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to write the state snapshot JSON")
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = Path(args.output)

    print("Pantheon OS State Engine v0.3.1")
    print(f"Repo: {REPO_ROOT}")
    print(f"Output: {output_path}")
    print()

    print("Reading git state...")
    git_state = get_git_state()

    print("Reading bindings...")
    bindings_doc = load_bindings()
    binding_indexes = build_binding_indexes(bindings_doc)

    print("Reading heartbeats...")
    hb_map = get_heartbeats_map()

    print("Reading agent registry...")
    agents = get_agent_state(binding_indexes, hb_map)

    print("Reading runtimes...")
    runtimes = get_runtime_state(binding_indexes, hb_map)

    print("Reading controllers...")
    controllers = get_controller_state(hb_map)

    print("Reading channels...")
    channels = get_channel_state()

    print("Reading deployments...")
    deployments = get_deployment_state()

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
    summary = get_system_summary(agents, runtimes, controllers, channels, git_state, realms, ventures, budgets, skills, deployments)

    state = {
        "meta": {
            "system_name": "Pantheon OS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": "0.3.1",
            "source": "engine/state_engine.py",
        },
        "summary": summary,
        "git": git_state,
        "deployments": deployments,
        "agents": agents,
        "runtimes": runtimes,
        "controllers": controllers,
        "channels": channels,
        "bindings": bindings_doc.get("bindings", {}),
        "realms": realms,
        "ventures": ventures,
        "budgets": budgets,
        "approvals": approvals,
        "skills": skills,
        "workstreams": workstreams,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(state, f, indent=2)

    print()
    print(f"State written to {output_path}")
    print(f"  Agents: {len(agents)}")
    print(f"  Runtimes: {len(runtimes)}")
    print(f"  Controllers: {len(controllers)}")
    print(f"  Channels: {len(channels)}")
    print(f"  Deployments: {len(deployments)}")
    print(f"  Realms: {len(realms)}")
    print(f"  Ventures: {len(ventures)}")
    print(f"  Skills: {len(skills)}")
    print(f"  Branch: {git_state['branch']}")
    print(f"  Clean: {git_state['working_tree_clean']}")
    print(f"  Synced: {git_state['remote_synced']}")


if __name__ == "__main__":
    main()
