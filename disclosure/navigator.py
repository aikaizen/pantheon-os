"""
Navigator: Guided discovery through PantheonOS documentation.

Provides progressive disclosure: start() -> entry point, next(current) -> suggestions.
Uses DocIndex for knowledge of documents and their relationships.
"""

import random
from typing import List, Optional
from .index import DocIndex, DocEntry


class Navigator:
    """Guided tour through documentation."""
    
    def __init__(self, doc_index: DocIndex):
        self.index = doc_index
        self._entry_point_candidates = self._identify_entry_points()
    
    def _identify_entry_points(self) -> List[DocEntry]:
        """Identify likely entry point documents."""
        entry_points = []
        for entry in self.index.entries.values():
            # Prefer files in root, with "readme", "guide", "overview", "intro" in title/path
            title_lower = entry.title.lower()
            path_lower = entry.path.lower()
            if (any(kw in title_lower for kw in ["readme", "guide", "overview", "introduction", "getting started"]) or
                any(kw in path_lower for kw in ["readme", "guide", "overview", "intro"])):
                entry_points.append(entry)
            # also include root-level files (no subdirectory)
            if '/' not in entry.path and '\\' not in entry.path:
                if entry not in entry_points:
                    entry_points.append(entry)
        return entry_points
    
    def start(self) -> Optional[DocEntry]:
        """Return a starting document for guided discovery."""
        if not self._entry_point_candidates:
            # fallback to any document
            entries = self.index.list_entries()
            if entries:
                return random.choice(entries)
            return None
        # pick the first entry point (could be randomized)
        return self._entry_point_candidates[0]
    
    def next(self, current: DocEntry, max_suggestions: int = 5) -> List[DocEntry]:
        """
        Suggest next documents to read after current.
        Prioritizes:
        1. Direct dependencies (outgoing links)
        2. Reverse dependencies (documents that link to current)
        3. Documents in same directory
        4. Documents with similar tags (if available)
        """
        suggestions = []
        visited = {current.path}
        
        # 1. Outgoing dependencies
        for dep_path in current.dependencies:
            if dep_path not in visited:
                dep_entry = self.index.get_entry(dep_path)
                if dep_entry:
                    suggestions.append(dep_entry)
                    visited.add(dep_path)
        
        # 2. Reverse dependencies (backlinks)
        for entry in self.index.entries.values():
            if current.path in entry.dependencies and entry.path not in visited:
                suggestions.append(entry)
                visited.add(entry.path)
        
        # 3. Same directory
        current_dir = '/'.join(current.path.split('/')[:-1])
        for entry in self.index.entries.values():
            if entry.path not in visited:
                entry_dir = '/'.join(entry.path.split('/')[:-1])
                if entry_dir == current_dir:
                    suggestions.append(entry)
                    visited.add(entry.path)
        
        # 4. If still not enough, add random fresh documents
        if len(suggestions) < max_suggestions:
            fresh_entries = [e for e in self.index.entries.values()
                             if e.path not in visited and e.staleness != "old"]
            random.shuffle(fresh_entries)
            suggestions.extend(fresh_entries[:max_suggestions - len(suggestions)])
        
        return suggestions[:max_suggestions]
    
    def tour(self, start_path: Optional[str] = None, steps: int = 5) -> List[DocEntry]:
        """Generate a guided tour of N steps."""
        if start_path:
            current = self.index.get_entry(start_path)
            if not current:
                current = self.start()
        else:
            current = self.start()
        
        if not current:
            return []
        
        tour = [current]
        for _ in range(steps - 1):
            next_docs = self.next(current)
            if not next_docs:
                break
            # pick the first suggestion (could be smarter)
            current = next_docs[0]
            tour.append(current)
        return tour
    
    def related(self, entry: DocEntry, depth: int = 2) -> List[DocEntry]:
        """Find related documents up to depth links away."""
        related = set()
        queue = [(entry, 0)]
        visited = {entry.path}
        
        while queue:
            current_entry, level = queue.pop(0)
            if level >= depth:
                continue
            # add dependencies
            for dep_path in current_entry.dependencies:
                if dep_path not in visited:
                    dep_entry = self.index.get_entry(dep_path)
                    if dep_entry:
                        related.add(dep_entry)
                        visited.add(dep_path)
                        queue.append((dep_entry, level + 1))
            # add backlinks
            for other_entry in self.index.entries.values():
                if current_entry.path in other_entry.dependencies and other_entry.path not in visited:
                    related.add(other_entry)
                    visited.add(other_entry.path)
                    queue.append((other_entry, level + 1))
        return list(related)


# Example usage
if __name__ == "__main__":
    from .index import DocIndex
    import sys
    
    docs_root = sys.argv[1] if len(sys.argv) > 1 else "docs"
    catalog_path = sys.argv[2] if len(sys.argv) > 2 else "docs/doc-index.yaml"
    
    index = DocIndex(docs_root)
    try:
        index.load_catalog(catalog_path)
        print(f"Loaded catalog with {len(index)} entries")
    except FileNotFoundError:
        index.scan()
        index.save_catalog(catalog_path)
        print(f"Scanned and saved catalog with {len(index)} entries")
    
    nav = Navigator(index)
    start = nav.start()
    if start:
        print(f"Start at: {start.path} - {start.title}")
        next_docs = nav.next(start)
        print("Next suggestions:")
        for doc in next_docs:
            print(f"  - {doc.path}: {doc.title}")