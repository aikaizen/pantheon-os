"""Structured JSON logging per realm."""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class LogEntry:
    timestamp: str
    realm_id: str
    level: str
    message: str
    context: dict
    source: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)


class RealmLogger:
    """Structured JSON logger for a realm.
    
    Each realm gets isolated log files with structured JSON entries.
    Supports filtering by level, timerange, and context fields.
    """
    
    DEFAULT_LOG_DIR = "/tmp/pantheon/logs"
    
    def __init__(
        self,
        realm_id: str,
        log_dir: Optional[str] = None,
        min_level: LogLevel = LogLevel.DEBUG
    ):
        self.realm_id = realm_id
        self.log_dir = Path(log_dir or self.DEFAULT_LOG_DIR)
        self.min_level = min_level
        self.log_file = self.log_dir / f"{realm_id}.jsonl"
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _should_log(self, level: LogLevel) -> bool:
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3
        }
        return level_order[level] >= level_order[self.min_level]
    
    def _write(self, entry: LogEntry) -> None:
        with open(self.log_file, "a") as f:
            f.write(entry.to_json() + "\n")
    
    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[dict] = None,
        source: Optional[str] = None
    ) -> None:
        """Write a log entry."""
        if not self._should_log(level):
            return
        
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            realm_id=self.realm_id,
            level=level.value,
            message=message,
            context=context or {},
            source=source
        )
        self._write(entry)
    
    def debug(self, message: str, **kwargs) -> None:
        self.log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        self.log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        self.log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        self.log(LogLevel.ERROR, message, **kwargs)
    
    def query(
        self,
        level: Optional[LogLevel] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: int = 100,
        context_filter: Optional[dict] = None
    ) -> list[LogEntry]:
        """Query log entries with filtering."""
        entries = []
        
        if not self.log_file.exists():
            return entries
        
        with open(self.log_file, "r") as f:
            for line in f:
                if len(entries) >= limit:
                    break
                
                try:
                    data = json.loads(line.strip())
                    entry = LogEntry(**data)
                except (json.JSONDecodeError, TypeError):
                    continue
                
                # Filter by level
                if level and entry.level != level.value:
                    continue
                
                # Filter by time range
                entry_time = datetime.fromisoformat(entry.timestamp)
                if since and entry_time < since:
                    continue
                if until and entry_time > until:
                    continue
                
                # Filter by context fields
                if context_filter:
                    match = all(
                        entry.context.get(k) == v
                        for k, v in context_filter.items()
                    )
                    if not match:
                        continue
                
                entries.append(entry)
        
        return entries
    
    def tail(self, n: int = 20) -> list[LogEntry]:
        """Get last N log entries."""
        return self.query(limit=n)
    
    def clear(self) -> None:
        """Clear all logs for this realm."""
        if self.log_file.exists():
            self.log_file.unlink()
    
    @classmethod
    def list_realms(cls, log_dir: Optional[str] = None) -> list[str]:
        """List all realms with log files."""
        log_path = Path(log_dir or cls.DEFAULT_LOG_DIR)
        if not log_path.exists():
            return []
        return [f.stem for f in log_path.glob("*.jsonl")]
