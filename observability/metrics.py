"""Simple metrics for per-realm observability.

Counters, timers, and gauges for tracking agent performance.
"""

import time
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from threading import Lock


@dataclass
class Counter:
    """Monotonically increasing counter."""
    name: str
    value: int = 0
    labels: dict = field(default_factory=dict)
    
    def inc(self, amount: int = 1) -> None:
        self.value += amount
    
    def reset(self) -> None:
        self.value = 0


@dataclass
class Timer:
    """Duration timer with start/stop."""
    name: str
    start_time: Optional[float] = None
    elapsed: float = 0.0
    count: int = 0
    total: float = 0.0
    
    def start(self) -> None:
        self.start_time = time.monotonic()
    
    def stop(self) -> float:
        if self.start_time is None:
            return 0.0
        duration = time.monotonic() - self.start_time
        self.elapsed = duration
        self.total += duration
        self.count += 1
        self.start_time = None
        return duration
    
    @property
    def average(self) -> float:
        return self.total / self.count if self.count > 0 else 0.0
    
    def reset(self) -> None:
        self.start_time = None
        self.elapsed = 0.0
        self.count = 0
        self.total = 0.0


@dataclass
class Gauge:
    """Point-in-time value gauge."""
    name: str
    value: float = 0.0
    
    def set(self, value: float) -> None:
        self.value = value
    
    def inc(self, amount: float = 1.0) -> None:
        self.value += amount
    
    def dec(self, amount: float = 1.0) -> None:
        self.value -= amount


class RealmMetrics:
    """Metrics collection for a realm.
    
    Provides counters, timers, and gauges for tracking agent performance.
    Metrics are persisted to disk for post-task analysis.
    """
    
    DEFAULT_METRICS_DIR = "/tmp/pantheon/metrics"
    
    def __init__(
        self,
        realm_id: str,
        metrics_dir: Optional[str] = None
    ):
        self.realm_id = realm_id
        self.metrics_dir = Path(metrics_dir or self.DEFAULT_METRICS_DIR)
        self.metrics_file = self.metrics_dir / f"{realm_id}.json"
        
        self._counters: dict[str, Counter] = {}
        self._timers: dict[str, Timer] = {}
        self._gauges: dict[str, Gauge] = {}
        self._lock = Lock()
        
        # Ensure metrics directory exists
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def counter(self, name: str, labels: Optional[dict] = None) -> Counter:
        """Get or create a counter."""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        with self._lock:
            if key not in self._counters:
                self._counters[key] = Counter(name=name, labels=labels or {})
            return self._counters[key]
    
    def timer(self, name: str) -> Timer:
        """Get or create a timer."""
        with self._lock:
            if name not in self._timers:
                self._timers[name] = Timer(name=name)
            return self._timers[name]
    
    def gauge(self, name: str) -> Gauge:
        """Get or create a gauge."""
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(name=name)
            return self._gauges[name]
    
    def time_it(self, name: str):
        """Context manager for timing operations."""
        return _TimerContext(self.timer(name))
    
    def snapshot(self) -> dict:
        """Get current metrics snapshot."""
        with self._lock:
            return {
                "realm_id": self.realm_id,
                "timestamp": time.time(),
                "counters": {
                    k: {"name": v.name, "value": v.value, "labels": v.labels}
                    for k, v in self._counters.items()
                },
                "timers": {
                    k: {
                        "name": v.name,
                        "count": v.count,
                        "total": v.total,
                        "average": v.average
                    }
                    for k, v in self._timers.items()
                },
                "gauges": {
                    k: {"name": v.name, "value": v.value}
                    for k, v in self._gauges.items()
                }
            }
    
    def save(self) -> None:
        """Persist metrics to disk."""
        snapshot = self.snapshot()
        with open(self.metrics_file, "w") as f:
            json.dump(snapshot, f, indent=2)
    
    def load(self) -> None:
        """Load persisted metrics."""
        if not self.metrics_file.exists():
            return
        
        with open(self.metrics_file, "r") as f:
            data = json.load(f)
        
        with self._lock:
            for key, c in data.get("counters", {}).items():
                self._counters[key] = Counter(**c)
            for key, t in data.get("timers", {}).items():
                self._timers[key] = Timer(**t)
            for key, g in data.get("gauges", {}).items():
                self._gauges[key] = Gauge(**g)
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            for c in self._counters.values():
                c.reset()
            for t in self._timers.values():
                t.reset()
            for g in self._gauges.values():
                g.set(0.0)
    
    def summary(self) -> str:
        """Human-readable metrics summary."""
        snap = self.snapshot()
        lines = [f"Metrics for realm: {self.realm_id}"]
        
        if snap["counters"]:
            lines.append("\nCounters:")
            for k, c in snap["counters"].items():
                labels = f" {c['labels']}" if c['labels'] else ""
                lines.append(f"  {c['name']}{labels}: {c['value']}")
        
        if snap["timers"]:
            lines.append("\nTimers:")
            for k, t in snap["timers"].items():
                lines.append(f"  {t['name']}: count={t['count']}, total={t['total']:.3f}s, avg={t['average']:.3f}s")
        
        if snap["gauges"]:
            lines.append("\nGauges:")
            for k, g in snap["gauges"].items():
                lines.append(f"  {g['name']}: {g['value']}")
        
        return "\n".join(lines)


class _TimerContext:
    """Context manager for timer.start()/stop()."""
    
    def __init__(self, timer: Timer):
        self.timer = timer
    
    def __enter__(self):
        self.timer.start()
        return self.timer
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timer.stop()
        return False
