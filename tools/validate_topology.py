#!/usr/bin/env python3
"""
Validate PantheonOS registry topology for pilot readiness.
"""

import json
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def collect_ids(items, key="id"):
    return {item[key] for item in items}


def validate():
    errors = []
    notes = []

    agents_doc = load_yaml(REGISTRY / "agents.yaml")
    runtimes_doc = load_yaml(REGISTRY / "runtimes.yaml")
    controllers_doc = load_yaml(REGISTRY / "controllers.yaml")
    channels_doc = load_yaml(REGISTRY / "channels.yaml")
    bindings_doc = load_yaml(REGISTRY / "bindings.yaml")
    ventures_doc = load_yaml(REGISTRY / "ventures.yaml")
    heartbeats_doc = load_yaml(REGISTRY / "heartbeats.yaml")
    deployment = load_json(REGISTRY / "deployments" / "promptengines.json")

    agents = agents_doc.get("agents", [])
    runtimes = runtimes_doc.get("runtimes", [])
    controllers = controllers_doc.get("controllers", [])
    channels = channels_doc.get("channels", [])
    bindings = bindings_doc.get("bindings", {})
    ventures = ventures_doc.get("ventures", [])
    heartbeats = heartbeats_doc.get("heartbeats", [])

    agent_ids = collect_ids(agents)
    runtime_ids = collect_ids(runtimes)
    controller_ids = collect_ids(controllers)
    channel_ids = collect_ids(channels)
    venture_ids = collect_ids(ventures)

    for label, ids, items in [
        ("agents", agent_ids, agents),
        ("runtimes", runtime_ids, runtimes),
        ("controllers", controller_ids, controllers),
        ("channels", channel_ids, channels),
    ]:
        if len(ids) != len(items):
            errors.append(f"Duplicate IDs detected in {label}")

    for runtime in runtimes:
        if runtime.get("deployment") != deployment["id"]:
            errors.append(f"Runtime {runtime['id']} points to unexpected deployment")
        for agent_id in runtime.get("agent_bindings", []):
            if agent_id not in agent_ids:
                errors.append(f"Runtime {runtime['id']} references unknown agent {agent_id}")
        for controller_id in runtime.get("controller_bindings", []):
            if controller_id not in controller_ids:
                errors.append(f"Runtime {runtime['id']} references unknown controller {controller_id}")

    for controller in controllers:
        for runtime_id in controller.get("manages", []):
            if runtime_id not in runtime_ids:
                errors.append(f"Controller {controller['id']} manages unknown runtime {runtime_id}")

    known_participants = agent_ids | controller_ids
    for channel in channels:
        for participant in channel.get("participants", []):
            if participant not in known_participants:
                errors.append(f"Channel {channel['id']} references unknown participant {participant}")

    for item in bindings.get("agent_runtime", []):
        if item.get("agent_id") not in agent_ids:
            errors.append(f"agent_runtime binding references unknown agent {item.get('agent_id')}")
        if item.get("runtime_id") not in runtime_ids:
            errors.append(f"agent_runtime binding references unknown runtime {item.get('runtime_id')}")

    for item in bindings.get("agent_channel", []):
        if item.get("agent_id") not in known_participants:
            errors.append(f"agent_channel binding references unknown actor {item.get('agent_id')}")
        if item.get("channel_id") not in channel_ids:
            errors.append(f"agent_channel binding references unknown channel {item.get('channel_id')}")

    for item in bindings.get("runtime_controller", []):
        if item.get("runtime_id") not in runtime_ids:
            errors.append(f"runtime_controller binding references unknown runtime {item.get('runtime_id')}")
        if item.get("controller_id") not in controller_ids:
            errors.append(f"runtime_controller binding references unknown controller {item.get('controller_id')}")

    for item in bindings.get("deployment_scope", []):
        if item.get("deployment_id") != deployment["id"]:
            errors.append(f"deployment_scope references unexpected deployment {item.get('deployment_id')}")
        for venture_id in item.get("venture_ids", []):
            if venture_id not in venture_ids:
                errors.append(f"deployment_scope references unknown venture {venture_id}")

    for tier_name, tier_values in deployment.get("pilot_scope", {}).items():
        for venture_id in tier_values:
            if venture_id not in venture_ids:
                errors.append(f"deployment pilot_scope {tier_name} references unknown venture {venture_id}")

    valid_refs = {
        **{f"registry:agents.yaml#{v}": "agent" for v in agent_ids},
        **{f"registry:runtimes.yaml#{v}": "runtime" for v in runtime_ids},
        **{f"registry:controllers.yaml#{v}": "controller" for v in controller_ids},
    }
    for hb in heartbeats:
        ref = hb.get("object_ref")
        if ref and ref not in valid_refs:
            errors.append(f"Heartbeat references unknown object_ref {ref}")

    notes.append(
        f"agents={len(agent_ids)} runtimes={len(runtime_ids)} controllers={len(controller_ids)} channels={len(channel_ids)} ventures={len(venture_ids)}"
    )
    return errors, notes


def main():
    errors, notes = validate()
    for note in notes:
        print(f"INFO: {note}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)
    print("Topology validation passed.")


if __name__ == "__main__":
    main()
