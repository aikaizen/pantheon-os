"""
DocIndex: Machine-readable catalog of PantheonOS documentation.

Scans the docs root, extracts titles from markdown headers,
tracks last_modified timestamps, supports find(query) for ranked results.
Includes staleness detection and dependency tracking.
"""

import os
import re
import yaml
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict


@dataclass
class DocEntry:
    """Single document entry."""
    path: str  # relative to docs root
    title: str
    last_modified: str  # ISO format
    size: int
    dependencies: List[str]  # paths of linked docs
    staleness: Optional[str] = None  # e.g., "old" if >30 days
    tags: Optional[List[str]] = None


class DocIndex:
    """Documentation index with search and staleness detection."""
    
    def __init__(self, docs_root: str):
        self.docs_root = Path(docs_root).resolve()
        self.entries: Dict[str, DocEntry] = {}
        self._staleness_threshold_days = 30
    
    def scan(self):
        """Walk the docs root and index all .md files."""
        self.entries.clear()
        for md_file in self.docs_root.rglob("*.md"):
            if md_file.is_file():
                rel_path = str(md_file.relative_to(self.docs_root))
                self._index_file(rel_path)
        self._compute_staleness()
    
    def set_staleness_threshold(self, days: int):
        """Set staleness threshold in days and recompute staleness."""
        self._staleness_threshold_days = days
        self._compute_staleness()
    
    def get_staleness_threshold(self) -> int:
        """Return current staleness threshold in days."""
        return self._staleness_threshold_days
    
    def _index_file(self, rel_path: str):
        """Index a single markdown file."""
        full_path = self.docs_root / rel_path
        stat = full_path.stat()
        last_modified = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        title = self._extract_title(full_path)
        dependencies = self._extract_dependencies(full_path)
        
        self.entries[rel_path] = DocEntry(
            path=rel_path,
            title=title,
            last_modified=last_modified,
            size=stat.st_size,
            dependencies=dependencies
        )
    
    def _extract_title(self, file_path: Path) -> str:
        """Extract title from first H1 markdown header."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    # Remove the '# ' and any extra spaces
                    return line[2:].strip()
        # Fallback: filename without extension
        return file_path.stem.replace('-', ' ').title()
    
    def _extract_dependencies(self, file_path: Path) -> List[str]:
        """Extract relative links to other .md files."""
        dependencies = set()
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                for match in link_pattern.finditer(line):
                    href = match.group(2)
                    # skip external links, anchors, etc.
                    if href.startswith('http') or href.startswith('#'):
                        continue
                    # normalize path relative to file's directory
                    parent = file_path.parent
                    linked = (parent / href).resolve()
                    try:
                        # ensure it's inside docs_root
                        linked.relative_to(self.docs_root)
                        if linked.suffix == '.md':
                            rel = str(linked.relative_to(self.docs_root))
                            dependencies.add(rel)
                    except ValueError:
                        # outside docs root, ignore
                        pass
        return list(dependencies)
    
    def _compute_staleness(self):
        """Mark entries older than threshold as stale."""
        now = datetime.datetime.now()
        for entry in self.entries.values():
            mod = datetime.datetime.fromisoformat(entry.last_modified)
            age_days = (now - mod).days
            if age_days > self._staleness_threshold_days:
                entry.staleness = "old"
            else:
                entry.staleness = None
    
    def find(self, query: str, max_results: int = 10, include_content: bool = False) -> List[DocEntry]:
        """
        Search documents by title, path, and optionally content.
        Returns ranked results based on relevance.
        """
        query_lower = query.lower()
        scored: List[Tuple[int, DocEntry]] = []
        for entry in self.entries.values():
            score = 0
            # title match
            if query_lower in entry.title.lower():
                score += 10
            # path match
            if query_lower in entry.path.lower():
                score += 5
            # substring in title words
            title_words = entry.title.lower().split()
            for word in title_words:
                if query_lower in word:
                    score += 3
            if include_content:
                # read file and search content
                full_path = self.docs_root / entry.path
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if query_lower in content:
                            score += 7
                except Exception:
                    pass
            if score > 0:
                scored.append((score, entry))
        # sort by score descending, then by path
        scored.sort(key=lambda x: (-x[0], x[1].path))
        return [entry for _, entry in scored[:max_results]]
    
    def search_content(self, query: str, max_results: int = 10) -> List[DocEntry]:
        """Search within document content only."""
        query_lower = query.lower()
        matches = []
        for entry in self.entries.values():
            full_path = self.docs_root / entry.path
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    if query_lower in content:
                        matches.append(entry)
            except Exception:
                pass
            if len(matches) >= max_results:
                break
        return matches
    
    def get_entry(self, path: str) -> Optional[DocEntry]:
        return self.entries.get(path)
    
    def list_entries(self) -> List[DocEntry]:
        return list(self.entries.values())
    
    def staleness_report(self) -> Dict[str, List[str]]:
        """Return dict of stale and fresh entries."""
        stale = []
        fresh = []
        for entry in self.entries.values():
            if entry.staleness == "old":
                stale.append(entry.path)
            else:
                fresh.append(entry.path)
        return {"stale": stale, "fresh": fresh}
    
    def dependency_graph(self) -> Dict[str, List[str]]:
        """Return adjacency list of dependencies."""
        graph = {}
        for entry in self.entries.values():
            graph[entry.path] = entry.dependencies
        return graph
    
    def save_catalog(self, output_path: str):
        """Save index to YAML file."""
        catalog = {
            "generated": datetime.datetime.now().isoformat(),
            "docs_root": str(self.docs_root),
            "staleness_threshold_days": self._staleness_threshold_days,
            "entries": {}
        }
        for path, entry in self.entries.items():
            catalog["entries"][path] = asdict(entry)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(catalog, f, default_flow_style=False, sort_keys=False)
    
    def load_catalog(self, input_path: str):
        """Load index from YAML file (does not rescan)."""
        with open(input_path, 'r', encoding='utf-8') as f:
            catalog = yaml.safe_load(f)
        self.docs_root = Path(catalog["docs_root"])
        self._staleness_threshold_days = catalog.get("staleness_threshold_days", 30)
        self.entries.clear()
        for path, entry_data in catalog["entries"].items():
            entry = DocEntry(**entry_data)
            self.entries[path] = entry
        self._compute_staleness()
    
    def refresh(self):
        """Rescan and update catalog."""
        self.scan()
    
    def __len__(self):
        return len(self.entries)
    
    def __contains__(self, path: str):
        return path in self.entries


# Example usage
if __name__ == "__main__":
    import sys
    docs_root = sys.argv[1] if len(sys.argv) > 1 else "docs"
    index = DocIndex(docs_root)
    index.scan()
    print(f"Indexed {len(index)} documents")
    for entry in index.list_entries()[:5]:
        print(f"- {entry.path}: {entry.title} ({entry.staleness or 'fresh'})")
    
    # Save catalog
    catalog_path = os.path.join(docs_root, "doc-index.yaml")
    index.save_catalog(catalog_path)
    print(f"Saved catalog to {catalog_path}")