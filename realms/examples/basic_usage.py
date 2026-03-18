#!/usr/bin/env python3
"""
Basic usage example for PantheonOS realm isolation framework.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from realms import IsolatedRealm, list_realms


def main():
    """Demonstrate basic realm operations."""
    print("PantheonOS Realm Isolation - Basic Usage Example")
    print("=" * 50)
    
    # 1. Create a realm
    print("\n1. Creating realm...")
    realm = IsolatedRealm.create("example-realm")
    print(f"   Created realm: {realm.realm_id}")
    print(f"   Port: {realm.port}")
    print(f"   Worktree: {realm.worktree}")
    
    # 2. Check status
    print("\n2. Checking status...")
    status = realm.get_status()
    print(f"   State: {status['state']}")
    
    # 3. Boot instance with a simple command
    print("\n3. Booting instance...")
    pid = realm.boot(
        command=["echo", "Hello from realm!"],
        env={"EXAMPLE": "value"},
    )
    print(f"   Booted with PID: {pid}")
    
    # 4. Wait and check logs
    print("\n4. Waiting for process to complete...")
    time.sleep(0.5)
    
    logs = realm.get_logs()
    print(f"   Logs: {logs.strip()}")
    
    # 5. Check status again
    status = realm.get_status()
    print(f"\n5. Final status: {status['state']}")
    
    # 6. List all realms
    print("\n6. Listing all realms...")
    realms = list_realms()
    for r in realms:
        print(f"   - {r['realm_id']}: {r['state']} (port {r['port']})")
    
    # 7. Cleanup
    print("\n7. Cleaning up...")
    realm.teardown(force=True)
    print("   Realm cleaned up")
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()