"""
PantheonOS Realm Isolation Framework

This module provides isolated execution environments (realms) for PantheonOS
agents and processes. Each realm is fully isolated with its own git worktree,
state directory, and network port.

Lifecycle:
    create -> run -> inspect -> teardown
"""

from .bootstrap import (
    create_worktree,
    boot_instance,
    teardown,
    list_realms,
    get_realm_info,
)

from .isolation import IsolatedRealm, RealmState

__version__ = "0.1.0"
__all__ = [
    "create_worktree",
    "boot_instance",
    "teardown",
    "list_realms",
    "get_realm_info",
    "IsolatedRealm",
    "RealmState",
]