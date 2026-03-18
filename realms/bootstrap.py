"""
Bootstrap module for PantheonOS realm isolation.

Provides high-level functions for managing realm lifecycle:
- Worktree creation and management
- Instance boot and teardown
- Realm discovery and inspection
"""

import os
import json
import time
import signal
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from .isolation import (
    IsolatedRealm,
    RealmState,
    RealmMetadata,
    REALMS_BASE,
    WORKTREES_BASE,
    PortAllocator,
)


@dataclass
class WorktreeConfig:
    """Configuration for worktree creation."""
    realm_id: str
    source_repo: Optional[str] = None
    base_branch: str = "main"
    auto_commit: bool = False
    copy_files: Optional[List[str]] = None


@dataclass
class InstanceConfig:
    """Configuration for instance boot."""
    realm_id: str
    command: List[str]
    env: Optional[Dict[str, str]] = None
    working_dir: Optional[str] = None
    timeout: Optional[int] = None
    auto_restart: bool = False


class RealmBootstrap:
    """
    High-level realm management class.
    
    Provides simplified interface for realm lifecycle operations
    with additional features like configuration templates and
    health monitoring.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the bootstrap manager.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self._load_config(config_path)
        self._active_realms: Dict[str, IsolatedRealm] = {}
    
    def create_worktree(self, config: WorktreeConfig) -> IsolatedRealm:
        """
        Create a new realm with isolated worktree.
        
        Args:
            config: Worktree configuration
            
        Returns:
            Created IsolatedRealm instance
            
        Raises:
            ValueError: If realm already exists
            RuntimeError: If worktree creation fails
        """
        # Validate realm doesn't exist
        realm_state_dir = REALMS_BASE / config.realm_id
        if realm_state_dir.exists():
            raise ValueError(f"Realm '{config.realm_id}' already exists")
        
        # Create the realm
        realm = IsolatedRealm.create(
            realm_id=config.realm_id,
            source_repo=config.source_repo,
            base_branch=config.base_branch,
        )
        
        # Copy additional files if specified
        if config.copy_files:
            self._copy_files_to_worktree(realm, config.copy_files)
        
        # Auto-commit if requested
        if config.auto_commit:
            self._auto_commit_worktree(realm, f"Initial realm setup: {config.realm_id}")
        
        # Cache the realm
        self._active_realms[config.realm_id] = realm
        
        return realm
    
    def boot_instance(self, config: InstanceConfig) -> IsolatedRealm:
        """
        Boot a realm instance with the specified configuration.
        
        Args:
            config: Instance configuration
            
        Returns:
            The booted realm instance
            
        Raises:
            ValueError: If realm not found
            RuntimeError: If boot fails
        """
        # Load the realm
        realm = self._get_realm(config.realm_id)
        
        # Prepare environment
        env = config.env or {}
        
        # Add working directory to environment if specified
        if config.working_dir:
            env["PANTHEON_WORKING_DIR"] = config.working_dir
        
        # Boot the instance
        pid = realm.boot(
            command=config.command,
            env=env,
        )
        
        # Wait for startup if timeout specified
        if config.timeout:
            self._wait_for_startup(realm, config.timeout)
        
        return realm
    
    def teardown(self, realm_id: str, force: bool = False) -> None:
        """
        Tear down a realm and clean up all resources.
        
        Args:
            realm_id: Realm identifier
            force: If True, forcefully terminate running processes
        """
        realm = self._get_realm(realm_id)
        realm.teardown(force=force)
        
        # Remove from cache
        if realm_id in self._active_realms:
            del self._active_realms[realm_id]
    
    def inspect(self, realm_id: str) -> Dict[str, Any]:
        """
        Inspect a realm and get detailed status.
        
        Args:
            realm_id: Realm identifier
            
        Returns:
            Detailed realm status information
        """
        realm = self._get_realm(realm_id)
        status = realm.get_status()
        
        # Add additional inspection data
        status["logs"] = realm.get_logs(lines=50)
        status["disk_usage"] = self._get_disk_usage(realm)
        
        return status
    
    def list_realms(self) -> List[Dict[str, Any]]:
        """
        List all realms with their status.
        
        Returns:
            List of realm status dictionaries
        """
        from .isolation import list_realms
        return list_realms()
    
    def restart(self, realm_id: str) -> IsolatedRealm:
        """
        Restart a realm instance.
        
        Args:
            realm_id: Realm identifier
            
        Returns:
            The restarted realm instance
        """
        realm = self._get_realm(realm_id)
        
        # Stop if running
        if realm.metadata.state == RealmState.RUNNING:
            realm.stop()
            time.sleep(1)  # Brief pause for cleanup
        
        # Get previous command from process info
        process_file = realm.state_dir / "process.json"
        if process_file.exists():
            with open(process_file, "r") as f:
                process_info = json.load(f)
                # Note: We'd need to store the command to restart properly
                # For now, this is a limitation
        
        return realm
    
    def execute_in_realm(
        self,
        realm_id: str,
        command: List[str],
        timeout: Optional[int] = None,
    ) -> Tuple[int, str, str]:
        """
        Execute a command within a realm's worktree.
        
        Args:
            realm_id: Realm identifier
            command: Command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        realm = self._get_realm(realm_id)
        
        result = subprocess.run(
            command,
            cwd=str(realm.worktree),
            capture_output=True,
            text=True,
            timeout=timeout,
            env={
                **os.environ,
                "PANTHEON_REALM_ID": realm_id,
                "PANTHEON_REALM_PORT": str(realm.port),
            },
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def _get_realm(self, realm_id: str) -> IsolatedRealm:
        """Get a realm instance, loading if necessary."""
        if realm_id in self._active_realms:
            return self._active_realms[realm_id]
        
        realm = IsolatedRealm.load(realm_id)
        self._active_realms[realm_id] = realm
        return realm
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file."""
        if config_path is None:
            return {}
        
        path = Path(config_path)
        if not path.exists():
            return {}
        
        with open(path, "r") as f:
            if path.suffix == ".json":
                return json.load(f)
            elif path.suffix in (".yaml", ".yml"):
                import yaml
                return yaml.safe_load(f)
        
        return {}
    
    def _copy_files_to_worktree(self, realm: IsolatedRealm, files: List[str]) -> None:
        """Copy specified files to realm worktree."""
        for file_path in files:
            source = Path(file_path)
            if source.exists():
                dest = realm.worktree / source.name
                if source.is_dir():
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
    
    def _auto_commit_worktree(self, realm: IsolatedRealm, message: str) -> None:
        """Auto-commit changes in worktree."""
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=str(realm.worktree),
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=str(realm.worktree),
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            # No changes to commit
            pass
    
    def _wait_for_startup(self, realm: IsolatedRealm, timeout: int) -> None:
        """Wait for realm to start up."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = realm.get_status()
            if status.get("process_alive", False):
                return
            time.sleep(0.5)
        raise TimeoutError(f"Realm failed to start within {timeout} seconds")
    
    def _get_disk_usage(self, realm: IsolatedRealm) -> Dict[str, int]:
        """Get disk usage for realm directories."""
        def get_size(path: Path) -> int:
            total = 0
            if path.exists():
                if path.is_file():
                    total = path.stat().st_size
                else:
                    for item in path.rglob("*"):
                        if item.is_file():
                            total += item.stat().st_size
            return total
        
        return {
            "worktree": get_size(realm.worktree),
            "state_dir": get_size(realm.state_dir),
            "total": get_size(realm.worktree) + get_size(realm.state_dir),
        }


# Convenience functions for direct use
_default_bootstrap = RealmBootstrap()


def create_worktree(
    realm_id: str,
    source_repo: Optional[str] = None,
    base_branch: str = "main",
    auto_commit: bool = False,
    copy_files: Optional[List[str]] = None,
) -> IsolatedRealm:
    """
    Create a new realm with isolated worktree.
    
    This is a convenience function that uses the default bootstrap instance.
    
    Args:
        realm_id: Unique identifier for the realm
        source_repo: Source git repository (defaults to current)
        base_branch: Branch to create worktree from
        auto_commit: Whether to auto-commit initial state
        copy_files: List of files to copy to worktree
        
    Returns:
        Created IsolatedRealm instance
    """
    config = WorktreeConfig(
        realm_id=realm_id,
        source_repo=source_repo,
        base_branch=base_branch,
        auto_commit=auto_commit,
        copy_files=copy_files,
    )
    return _default_bootstrap.create_worktree(config)


def boot_instance(
    realm_id: str,
    command: List[str],
    env: Optional[Dict[str, str]] = None,
    working_dir: Optional[str] = None,
    timeout: Optional[int] = None,
) -> IsolatedRealm:
    """
    Boot a realm instance.
    
    This is a convenience function that uses the default bootstrap instance.
    
    Args:
        realm_id: Realm identifier
        command: Command to execute
        env: Additional environment variables
        working_dir: Working directory within the worktree
        timeout: Startup timeout in seconds
        
    Returns:
        The booted realm instance
    """
    config = InstanceConfig(
        realm_id=realm_id,
        command=command,
        env=env,
        working_dir=working_dir,
        timeout=timeout,
    )
    return _default_bootstrap.boot_instance(config)


def teardown(realm_id: str, force: bool = False) -> None:
    """
    Tear down a realm.
    
    This is a convenience function that uses the default bootstrap instance.
    
    Args:
        realm_id: Realm identifier
        force: If True, forcefully terminate running processes
    """
    _default_bootstrap.teardown(realm_id, force=force)


def list_realms() -> List[Dict[str, Any]]:
    """
    List all realms.
    
    This is a convenience function that uses the default bootstrap instance.
    
    Returns:
        List of realm status dictionaries
    """
    return _default_bootstrap.list_realms()


def get_realm_info(realm_id: str) -> Dict[str, Any]:
    """
    Get information about a specific realm.
    
    This is a convenience function that uses the default bootstrap instance.
    
    Args:
        realm_id: Realm identifier
        
    Returns:
        Realm status dictionary
    """
    return _default_bootstrap.inspect(realm_id)