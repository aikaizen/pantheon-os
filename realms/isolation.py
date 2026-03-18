"""
Realm isolation implementation for PantheonOS.

Provides the IsolatedRealm class which manages isolated execution
environments with their own git worktrees, state directories, and
network ports.
"""

import os
import json
import shutil
import socket
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime


# Base directories for realm isolation
REALMS_BASE = Path("/tmp/pantheon/realms")
WORKTREES_BASE = Path("/tmp/pantheon/worktrees")


class RealmState(Enum):
    """Possible states of a realm."""
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    TEARDOWN = "teardown"


@dataclass
class RealmMetadata:
    """Metadata associated with a realm."""
    realm_id: str
    created_at: str
    state: RealmState
    port: int
    worktree_path: str
    state_dir: str
    pid: Optional[int] = None
    last_active: Optional[str] = None
    error_message: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        data = asdict(self)
        data["state"] = self.state.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RealmMetadata":
        """Create metadata from dictionary."""
        data["state"] = RealmState(data["state"])
        return cls(**data)


class PortAllocator:
    """Manages port allocation for realms."""
    
    DEFAULT_PORT_RANGE = (9000, 9999)
    
    def __init__(self, port_range: Optional[tuple] = None):
        self.port_range = port_range or self.DEFAULT_PORT_RANGE
        self.allocated_ports: Dict[int, str] = {}  # port -> realm_id
    
    def allocate(self, realm_id: str) -> int:
        """Allocate a port for a realm."""
        for port in range(self.port_range[0], self.port_range[1] + 1):
            if port not in self.allocated_ports and self._is_port_available(port):
                self.allocated_ports[port] = realm_id
                return port
        raise RuntimeError(f"No available ports in range {self.port_range}")
    
    def release(self, port: int) -> None:
        """Release an allocated port."""
        if port in self.allocated_ports:
            del self.allocated_ports[port]
    
    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available for binding."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return True
            except socket.error:
                return False


class IsolatedRealm:
    """
    Represents an isolated execution environment (realm) in PantheonOS.
    
    Each realm has:
    - A git worktree for code isolation
    - A state directory for persistent data
    - A dedicated network port
    - Isolated process environment
    
    Example:
        realm = IsolatedRealm.create("my-agent-001")
        realm.boot(command=["python", "agent.py"])
        status = realm.get_status()
        realm.teardown()
    """
    
    _port_allocator = PortAllocator()
    
    def __init__(self, realm_id: str, metadata: RealmMetadata):
        self.realm_id = realm_id
        self.metadata = metadata
        self.state_dir = Path(metadata.state_dir)
        self.worktree = Path(metadata.worktree_path)
        self.port = metadata.port
    
    @classmethod
    def create(
        cls,
        realm_id: str,
        source_repo: Optional[str] = None,
        base_branch: str = "main",
        tags: Optional[List[str]] = None,
    ) -> "IsolatedRealm":
        """
        Create a new isolated realm.
        
        Args:
            realm_id: Unique identifier for the realm
            source_repo: Source git repository (defaults to current)
            base_branch: Branch to create worktree from
            tags: Optional tags for categorization
            
        Returns:
            IsolatedRealm instance
        """
        # Ensure base directories exist
        REALMS_BASE.mkdir(parents=True, exist_ok=True)
        WORKTREES_BASE.mkdir(parents=True, exist_ok=True)
        
        # Create realm paths
        realm_state_dir = REALMS_BASE / realm_id
        realm_worktree = WORKTREES_BASE / realm_id
        
        if realm_state_dir.exists():
            raise ValueError(f"Realm '{realm_id}' already exists")
        
        # Create directories
        realm_state_dir.mkdir(parents=True, exist_ok=True)
        
        # Allocate port
        port = cls._port_allocator.allocate(realm_id)
        
        # Create metadata
        metadata = RealmMetadata(
            realm_id=realm_id,
            created_at=datetime.now().isoformat(),
            state=RealmState.CREATED,
            port=port,
            worktree_path=str(realm_worktree),
            state_dir=str(realm_state_dir),
            tags=tags or [],
        )
        
        # Create git worktree
        cls._create_git_worktree(
            worktree_path=realm_worktree,
            source_repo=source_repo,
            branch_name=f"realm/{realm_id}",
            base_branch=base_branch,
        )
        
        # Save metadata
        realm = cls(realm_id, metadata)
        realm._save_metadata()
        
        return realm
    
    @classmethod
    def load(cls, realm_id: str) -> "IsolatedRealm":
        """
        Load an existing realm from disk.
        
        Args:
            realm_id: Realm identifier
            
        Returns:
            IsolatedRealm instance
        """
        realm_state_dir = REALMS_BASE / realm_id
        metadata_file = realm_state_dir / "metadata.json"
        
        if not metadata_file.exists():
            raise ValueError(f"Realm '{realm_id}' not found")
        
        with open(metadata_file, "r") as f:
            data = json.load(f)
        
        metadata = RealmMetadata.from_dict(data)
        return cls(realm_id, metadata)
    
    def boot(self, command: List[str], env: Optional[Dict[str, str]] = None) -> int:
        """
        Boot the realm instance with the specified command.
        
        Args:
            command: Command to execute in the realm
            env: Additional environment variables
            
        Returns:
            Process ID of the booted instance
        """
        import subprocess
        
        if self.metadata.state == RealmState.RUNNING:
            raise RuntimeError(f"Realm '{self.realm_id}' is already running")
        
        # Prepare environment
        realm_env = os.environ.copy()
        realm_env.update({
            "PANTHEON_REALM_ID": self.realm_id,
            "PANTHEON_REALM_PORT": str(self.port),
            "PANTHEON_REALM_STATE_DIR": str(self.state_dir),
            "PANTHEON_REALM_WORKTREE": str(self.worktree),
        })
        if env:
            realm_env.update(env)
        
        # Ensure worktree exists
        if not self.worktree.exists():
            raise RuntimeError(f"Worktree not found: {self.worktree}")
        
        # Start process
        log_file = self.state_dir / "process.log"
        with open(log_file, "w") as f:
            process = subprocess.Popen(
                command,
                cwd=str(self.worktree),
                env=realm_env,
                stdout=f,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        
        # Update metadata
        self.metadata.pid = process.pid
        self.metadata.state = RealmState.RUNNING
        self.metadata.last_active = datetime.now().isoformat()
        self._save_metadata()
        
        # Save process info
        self._save_process_info(process.pid)
        
        return process.pid
    
    def stop(self) -> None:
        """Stop the running realm instance."""
        import signal
        
        if self.metadata.state != RealmState.RUNNING:
            return
        
        if self.metadata.pid:
            try:
                os.kill(self.metadata.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        
        self.metadata.state = RealmState.STOPPED
        self.metadata.pid = None
        self.metadata.last_active = datetime.now().isoformat()
        self._save_metadata()
    
    def teardown(self, force: bool = False) -> None:
        """
        Tear down the realm, removing all resources.
        
        Args:
            force: If True, forcefully terminate running processes
        """
        # Stop if running
        if self.metadata.state == RealmState.RUNNING:
            if not force:
                raise RuntimeError(
                    f"Realm '{self.realm_id}' is running. Stop it first or use force=True"
                )
            self.stop()
        
        # Release port
        self._port_allocator.release(self.port)
        
        # Remove worktree
        if self.worktree.exists():
            self._remove_git_worktree(self.worktree)
        
        # Remove state directory
        if self.state_dir.exists():
            shutil.rmtree(self.state_dir)
        
        self.metadata.state = RealmState.TEARDOWN
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the realm.
        
        Returns:
            Dictionary with realm status information
        """
        status = {
            "realm_id": self.realm_id,
            "state": self.metadata.state.value,
            "port": self.port,
            "created_at": self.metadata.created_at,
            "last_active": self.metadata.last_active,
            "worktree": str(self.worktree),
            "state_dir": str(self.state_dir),
            "tags": self.metadata.tags,
        }
        
        # Check if process is actually running
        if self.metadata.pid and self.metadata.state == RealmState.RUNNING:
            if not self._is_process_running(self.metadata.pid):
                status["state"] = RealmState.STOPPED.value
                status["process_alive"] = False
            else:
                status["process_alive"] = True
                status["pid"] = self.metadata.pid
        
        return status
    
    def get_logs(self, lines: int = 100) -> str:
        """
        Get recent logs from the realm.
        
        Args:
            lines: Number of lines to return
            
        Returns:
            Log content
        """
        log_file = self.state_dir / "process.log"
        if not log_file.exists():
            return ""
        
        with open(log_file, "r") as f:
            all_lines = f.readlines()
            return "".join(all_lines[-lines:])
    
    def _save_metadata(self) -> None:
        """Save realm metadata to disk."""
        metadata_file = self.state_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(self.metadata.to_dict(), f, indent=2)
    
    def _save_process_info(self, pid: int) -> None:
        """Save process information."""
        process_file = self.state_dir / "process.json"
        with open(process_file, "w") as f:
            json.dump({
                "pid": pid,
                "started_at": datetime.now().isoformat(),
                "command_env": {
                    "PANTHEON_REALM_ID": self.realm_id,
                    "PANTHEON_REALM_PORT": self.port,
                }
            }, f, indent=2)
    
    @staticmethod
    def _create_git_worktree(
        worktree_path: Path,
        source_repo: Optional[str],
        branch_name: str,
        base_branch: str,
    ) -> None:
        """Create a git worktree for the realm."""
        import subprocess
        
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
        
        if source_repo is None:
            # Use current directory as source
            source_repo = os.getcwd()
        
        try:
            # Create worktree
            subprocess.run(
                ["git", "worktree", "add", "-b", branch_name, str(worktree_path), base_branch],
                cwd=source_repo,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            # If branch already exists, try to add worktree to existing branch
            if "already exists" in e.stderr.decode():
                subprocess.run(
                    ["git", "worktree", "add", str(worktree_path), branch_name],
                    cwd=source_repo,
                    check=True,
                    capture_output=True,
                )
            else:
                raise
    
    @staticmethod
    def _remove_git_worktree(worktree_path: Path) -> None:
        """Remove a git worktree."""
        import subprocess
        
        try:
            # Get the source repo (parent git dir)
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=worktree_path,
                capture_output=True,
                text=True,
            )
            
            if result.returncode == 0:
                # Remove worktree
                subprocess.run(
                    ["git", "worktree", "remove", "--force", str(worktree_path)],
                    check=False,
                    capture_output=True,
                )
        except Exception:
            pass
        
        # Ensure directory is removed
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
    
    @staticmethod
    def _is_process_running(pid: int) -> bool:
        """Check if a process is running."""
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False


def list_realms() -> List[Dict[str, Any]]:
    """
    List all realms.
    
    Returns:
        List of realm status dictionaries
    """
    realms = []
    
    if not REALMS_BASE.exists():
        return realms
    
    for realm_dir in REALMS_BASE.iterdir():
        if realm_dir.is_dir():
            metadata_file = realm_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    realm = IsolatedRealm.load(realm_dir.name)
                    realms.append(realm.get_status())
                except Exception as e:
                    realms.append({
                        "realm_id": realm_dir.name,
                        "state": "error",
                        "error": str(e),
                    })
    
    return realms


def get_realm_info(realm_id: str) -> Dict[str, Any]:
    """
    Get information about a specific realm.
    
    Args:
        realm_id: Realm identifier
        
    Returns:
        Realm status dictionary
    """
    realm = IsolatedRealm.load(realm_id)
    return realm.get_status()


def cleanup_all_realms() -> int:
    """
    Clean up all realms (for testing/maintenance).
    
    Returns:
        Number of realms cleaned up
    """
    count = 0
    
    if REALMS_BASE.exists():
        for realm_dir in REALMS_BASE.iterdir():
            if realm_dir.is_dir():
                try:
                    realm = IsolatedRealm.load(realm_dir.name)
                    realm.teardown(force=True)
                    count += 1
                except Exception:
                    pass
    
    if WORKTREES_BASE.exists():
        shutil.rmtree(WORKTREES_BASE)
        WORKTREES_BASE.mkdir(parents=True, exist_ok=True)
    
    return count