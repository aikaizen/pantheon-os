"""
Output Governor for PantheonOS ACI.

This module provides capping and truncation utilities to prevent context flooding
by limiting output sizes from search results, file reads, and terminal commands.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import os


@dataclass
class CappedSearchResults:
    """
    Caps search results to a maximum number of matches.
    
    If search results exceed the limit, returns a summary count and a suggestion
    to narrow the query.
    """
    max_results: int = 50
    results: List[Any] = field(default_factory=list)
    truncated: bool = False
    total_count: int = 0
    
    def __post_init__(self):
        """Initialize the capped results."""
        if not self.results:
            self.results = []
        self.total_count = len(self.results)
        self._apply_cap()
    
    def _apply_cap(self):
        """Apply the cap to the results."""
        if len(self.results) > self.max_results:
            self.results = self.results[:self.max_results]
            self.truncated = True
    
    def add_results(self, new_results: List[Any]):
        """Add new results and reapply cap."""
        self.results.extend(new_results)
        self.total_count = len(self.results)
        self._apply_cap()
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Return a summary of the search results.
        
        Returns:
            Dictionary with 'total_matches', 'showing', 'truncated', and
            'suggestion' if truncated.
        """
        summary = {
            'total_matches': self.total_count,
            'showing': len(self.results),
            'truncated': self.truncated,
            'results': self.results
        }
        if self.truncated:
            summary['suggestion'] = (
                f"Search returned {self.total_count} matches. "
                f"Only showing first {self.max_results}. "
                "Narrow your query to reduce results."
            )
        return summary


@dataclass
class CappedFileRead:
    """
    Caps file read output to a maximum number of lines.
    
    Provides offset and limit parameters for pagination through large files.
    """
    file_path: str = ""
    max_lines: int = 200
    offset: int = 1  # 1-indexed line number to start from
    limit: Optional[int] = None  # If None, use max_lines
    content: str = ""
    total_lines: int = 0
    truncated: bool = False
    read_lines: int = 0
    
    def __post_init__(self):
        """Initialize and read the file if path provided."""
        if self.file_path:
            self.read_file()
    
    def read_file(self, file_path: Optional[str] = None,
                  offset: Optional[int] = None,
                  limit: Optional[int] = None):
        """
        Read the file with given offset and limit.
        
        Args:
            file_path: Path to the file (optional, uses self.file_path if not provided)
            offset: Starting line number (1-indexed)
            limit: Maximum number of lines to read
            
        Returns:
            True if successful, False otherwise
        """
        if file_path:
            self.file_path = file_path
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        
        effective_limit = self.limit if self.limit is not None else self.max_lines
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                self.total_lines = len(all_lines)
                
                # Adjust offset (convert to 0-indexed)
                start_idx = max(0, self.offset - 1)
                end_idx = min(len(all_lines), start_idx + effective_limit)
                
                self.content = ''.join(all_lines[start_idx:end_idx])
                self.read_lines = end_idx - start_idx
                
                # Determine if truncated
                self.truncated = end_idx < len(all_lines)
                
                return True
        except FileNotFoundError:
            self.content = f"Error: File not found: {self.file_path}"
            self.total_lines = 0
            self.read_lines = 0
            self.truncated = False
            return False
        except Exception as e:
            self.content = f"Error reading file: {str(e)}"
            self.total_lines = 0
            self.read_lines = 0
            self.truncated = False
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Return a summary of the file read.
        
        Returns:
            Dictionary with file information and read status.
        """
        return {
            'file_path': self.file_path,
            'total_lines': self.total_lines,
            'read_lines': self.read_lines,
            'offset': self.offset,
            'limit': self.limit or self.max_lines,
            'truncated': self.truncated,
            'content': self.content,
            'suggestion': (
                f"File has {self.total_lines} lines. "
                f"Read lines {self.offset}-{self.offset + self.read_lines - 1}. "
                "Use offset and limit parameters to paginate."
            ) if self.truncated else None
        }


@dataclass
class TruncatedTerminal:
    """
    Truncates terminal output to a maximum size (default 10KB).
    
    Provides structured metadata about the truncation.
    """
    max_size_bytes: int = 10 * 1024  # 10KB default
    output: str = ""
    original_size: int = 0
    truncated_size: int = 0
    truncated: bool = False
    exit_code: Optional[int] = None
    command: str = ""
    
    def __post_init__(self):
        """Initialize."""
        if self.output:
            self.original_size = len(self.output.encode('utf-8'))
            self._apply_truncation()
    
    def set_output(self, output: str, exit_code: Optional[int] = None,
                   command: str = ""):
        """
        Set the terminal output and apply truncation.
        
        Args:
            output: The raw terminal output
            exit_code: Exit code of the command
            command: The command that was executed
        """
        self.output = output
        self.exit_code = exit_code
        self.command = command
        self.original_size = len(output.encode('utf-8'))
        self._apply_truncation()
    
    def _apply_truncation(self):
        """Apply size truncation to the output."""
        if self.original_size <= self.max_size_bytes:
            self.truncated = False
            self.truncated_size = self.original_size
        else:
            # Truncate at character boundary (approximately)
            # We'll truncate at the byte limit, ensuring we don't split multi-byte chars
            encoded = self.output.encode('utf-8')
            if len(encoded) > self.max_size_bytes:
                # Find a safe cut point (don't split UTF-8 sequences)
                cut_point = self.max_size_bytes
                while cut_point > 0 and (encoded[cut_point] & 0xC0) == 0x80:
                    cut_point -= 1
                self.output = encoded[:cut_point].decode('utf-8', errors='ignore')
                self.truncated = True
                self.truncated_size = cut_point
            else:
                self.truncated = False
                self.truncated_size = self.original_size
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Return a summary of the terminal output.
        
        Returns:
            Dictionary with output information and truncation status.
        """
        return {
            'command': self.command,
            'exit_code': self.exit_code,
            'original_size_bytes': self.original_size,
            'truncated_size_bytes': self.truncated_size,
            'max_size_bytes': self.max_size_bytes,
            'truncated': self.truncated,
            'output': self.output,
            'suggestion': (
                f"Terminal output truncated from {self.original_size} bytes "
                f"to {self.max_size_bytes} bytes. "
                "Consider using grep, head, or tail to limit output."
            ) if self.truncated else None
        }


# Convenience functions for direct usage
def cap_search_results(results: List[Any], max_results: int = 50) -> Dict[str, Any]:
    """
    Cap search results and return summary.
    
    Args:
        results: List of search results
        max_results: Maximum number of results to keep
        
    Returns:
        Dictionary with capped results and metadata
    """
    capped = CappedSearchResults(max_results=max_results, results=results)
    return capped.get_summary()


def read_file_capped(file_path: str, offset: int = 1,
                     limit: int = 200) -> Dict[str, Any]:
    """
    Read a file with line capping.
    
    Args:
        file_path: Path to the file
        offset: Starting line number (1-indexed)
        limit: Maximum number of lines to read
        
    Returns:
        Dictionary with file content and metadata
    """
    reader = CappedFileRead(file_path=file_path, max_lines=limit, offset=offset)
    return reader.get_summary()


def truncate_terminal_output(output: str, max_size_bytes: int = 10 * 1024,
                             exit_code: Optional[int] = None,
                             command: str = "") -> Dict[str, Any]:
    """
    Truncate terminal output to maximum size.
    
    Args:
        output: Raw terminal output
        max_size_bytes: Maximum size in bytes
        exit_code: Exit code of the command
        command: Command that was executed
        
    Returns:
        Dictionary with truncated output and metadata
    """
    truncator = TruncatedTerminal(max_size_bytes=max_size_bytes)
    truncator.set_output(output, exit_code=exit_code, command=command)
    return truncator.get_summary()


# Test function
def _test_module():
    """Simple test to verify module functionality."""
    print("Testing CappedSearchResults...")
    results = list(range(100))
    capped = CappedSearchResults(max_results=10, results=results)
    summary = capped.get_summary()
    assert summary['total_matches'] == 100
    assert summary['showing'] == 10
    assert summary['truncated'] is True
    assert 'suggestion' in summary
    print("✓ CappedSearchResults works")
    
    print("Testing CappedFileRead...")
    # Create a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for i in range(300):
            f.write(f"Line {i+1}\n")
        temp_path = f.name
    
    try:
        reader = CappedFileRead(file_path=temp_path, max_lines=50, offset=101)
        summary = reader.get_summary()
        assert summary['total_lines'] == 300
        assert summary['read_lines'] == 50
        assert summary['offset'] == 101
        assert summary['truncated'] is True
        assert "Line 101" in summary['content']
        print("✓ CappedFileRead works")
    finally:
        os.unlink(temp_path)
    
    print("Testing TruncatedTerminal...")
    long_output = "x" * 20000  # 20KB of data
    truncator = TruncatedTerminal(max_size_bytes=5000)
    truncator.set_output(long_output, exit_code=0, command="ls -la")
    summary = truncator.get_summary()
    assert summary['original_size_bytes'] == 20000
    assert summary['truncated_size_bytes'] == 5000
    assert summary['truncated'] is True
    assert len(summary['output'].encode('utf-8')) <= 5000
    print("✓ TruncatedTerminal works")
    
    print("Testing convenience functions...")
    summary = cap_search_results([1, 2, 3], max_results=2)
    assert summary['showing'] == 2
    print("✓ Convenience functions work")
    
    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    _test_module()