#!/usr/bin/env python3
"""
Command-line interface for PantheonOS realm isolation framework.

Usage:
    python -m realms.cli create <realm_id> [--branch <branch>] [--repo <repo>]
    python -m realms.cli boot <realm_id> -- <command>...
    python -m realms.cli stop <realm_id>
    python -m realms.cli teardown <realm_id> [--force]
    python -m realms.cli list
    python -m realms.cli inspect <realm_id>
    python -m realms.cli logs <realm_id> [--lines <n>]
    python -m realms.cli cleanup
"""

import sys
import argparse
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from realms import (
    IsolatedRealm,
    RealmState,
    list_realms,
    get_realm_info,
    teardown,
)
from realms.bootstrap import RealmBootstrap, WorktreeConfig, InstanceConfig


def create_realm(args):
    """Create a new realm."""
    try:
        realm = IsolatedRealm.create(
            realm_id=args.realm_id,
            source_repo=args.repo,
            base_branch=args.branch,
            tags=args.tags.split(",") if args.tags else [],
        )
        print(f"Created realm '{realm.realm_id}'")
        print(f"  Port: {realm.port}")
        print(f"  Worktree: {realm.worktree}")
        print(f"  State dir: {realm.state_dir}")
    except Exception as e:
        print(f"Error creating realm: {e}", file=sys.stderr)
        sys.exit(1)


def boot_realm(args):
    """Boot a realm instance."""
    try:
        realm = IsolatedRealm.load(args.realm_id)
        env_dict = {}
        if args.env:
            for env_str in args.env:
                k, v = env_str.split("=", 1)
                env_dict[k] = v
        pid = realm.boot(
            command=args.boot_command,
            env=env_dict,
        )
        print(f"Booted realm '{realm.realm_id}' with PID {pid}")
    except Exception as e:
        print(f"Error booting realm: {e}", file=sys.stderr)
        sys.exit(1)


def stop_realm(args):
    """Stop a running realm."""
    try:
        realm = IsolatedRealm.load(args.realm_id)
        realm.stop()
        print(f"Stopped realm '{realm.realm_id}'")
    except Exception as e:
        print(f"Error stopping realm: {e}", file=sys.stderr)
        sys.exit(1)


def teardown_realm(args):
    """Teardown a realm."""
    try:
        teardown(args.realm_id, force=args.force)
        print(f"Teared down realm '{args.realm_id}'")
    except Exception as e:
        print(f"Error tearing down realm: {e}", file=sys.stderr)
        sys.exit(1)


def list_all_realms(args):
    """List all realms."""
    realms = list_realms()
    if not realms:
        print("No realms found")
        return
    
    for realm in realms:
        print(f"{realm['realm_id']:<20} {realm['state']:<10} port={realm['port']}")
        if realm.get('pid'):
            print(f"  PID: {realm['pid']}")


def inspect_realm(args):
    """Inspect a realm."""
    try:
        info = get_realm_info(args.realm_id)
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"Error inspecting realm: {e}", file=sys.stderr)
        sys.exit(1)


def show_logs(args):
    """Show realm logs."""
    try:
        realm = IsolatedRealm.load(args.realm_id)
        logs = realm.get_logs(lines=args.lines)
        print(logs)
    except Exception as e:
        print(f"Error getting logs: {e}", file=sys.stderr)
        sys.exit(1)


def cleanup_all(args):
    """Clean up all realms."""
    from realms.isolation import cleanup_all_realms
    count = cleanup_all_realms()
    print(f"Cleaned up {count} realms")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PantheonOS Realm Isolation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new realm")
    create_parser.add_argument("realm_id", help="Realm identifier")
    create_parser.add_argument("--branch", default="main", help="Base branch")
    create_parser.add_argument("--repo", help="Source repository")
    create_parser.add_argument("--tags", help="Comma-separated tags")
    
    # Boot command
    boot_parser = subparsers.add_parser("boot", help="Boot a realm instance")
    boot_parser.add_argument("realm_id", help="Realm identifier")
    boot_parser.add_argument("boot_command", nargs="+", help="Command to execute")
    boot_parser.add_argument("--env", action="append", help="Environment variables (KEY=VALUE)")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a running realm")
    stop_parser.add_argument("realm_id", help="Realm identifier")
    
    # Teardown command
    teardown_parser = subparsers.add_parser("teardown", help="Teardown a realm")
    teardown_parser.add_argument("realm_id", help="Realm identifier")
    teardown_parser.add_argument("--force", action="store_true", help="Force teardown")
    
    # List command
    subparsers.add_parser("list", help="List all realms")
    
    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a realm")
    inspect_parser.add_argument("realm_id", help="Realm identifier")
    
    # Logs command
    logs_parser = subparsers.add_parser("logs", help="Show realm logs")
    logs_parser.add_argument("realm_id", help="Realm identifier")
    logs_parser.add_argument("--lines", type=int, default=100, help="Number of lines")
    
    # Cleanup command
    subparsers.add_parser("cleanup", help="Clean up all realms")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Dispatch to appropriate handler
    handlers = {
        "create": create_realm,
        "boot": boot_realm,
        "stop": stop_realm,
        "teardown": teardown_realm,
        "list": list_all_realms,
        "inspect": inspect_realm,
        "logs": show_logs,
        "cleanup": cleanup_all,
    }
    
    handlers[args.command](args)


if __name__ == "__main__":
    main()