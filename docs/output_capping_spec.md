# Output Capping Specification for PantheonOS ACI

## Overview

The Output Governor module (`tools/output_governor.py`) provides capping and truncation utilities to prevent context flooding in agent contexts. By limiting output sizes from search results, file reads, and terminal commands, the system maintains manageable context windows and prevents performance degradation.

## Design Principles

1. **Prevent Context Flooding**: Agents can become inefficient when given unbounded output. Capping ensures they receive manageable chunks.
2. **Provide Structured Metadata**: When output is capped, include metadata about what was truncated and suggestions for narrowing queries.
3. **Configurable Limits**: All caps are configurable per-call, with sensible defaults.
4. **Pagination Support**: For file reads, support offset/limit parameters to navigate large files.

## Components

### 1. CappedSearchResults

Caps search results to a maximum number of matches.

**Default Cap**: 50 results

**Behavior**:
- If search results exceed the limit, returns only the first N results
- Includes total count of matches
- Provides suggestion message: "Narrow your query to reduce results"

**Usage**:
```python
from tools.output_governor import CappedSearchResults

# Create capped results with default limit (50)
capped = CappedSearchResults(results=search_results)
summary = capped.get_summary()

# Or with custom limit
capped = CappedSearchResults(max_results=100, results=search_results)
```

**Summary Structure**:
```python
{
    'total_matches': int,
    'showing': int,
    'truncated': bool,
    'results': list,
    'suggestion': str  # Only present if truncated
}
```

### 2. CappedFileRead

Caps file read output to a maximum number of lines with pagination support.

**Default Cap**: 200 lines

**Parameters**:
- `offset`: Starting line number (1-indexed, default: 1)
- `limit`: Maximum lines to read (default: max_lines)

**Behavior**:
- Reads specified lines from a file
- Tracks total lines in file
- Indicates if file was truncated
- Provides suggestion for pagination

**Usage**:
```python
from tools.output_governor import CappedFileRead

# Read first 200 lines (default)
reader = CappedFileRead(file_path="/path/to/file.log")
summary = reader.get_summary()

# Read lines 101-150
reader = CappedFileRead(file_path="/path/to/file.log", offset=101, limit=50)
summary = reader.get_summary()
```

**Summary Structure**:
```python
{
    'file_path': str,
    'total_lines': int,
    'read_lines': int,
    'offset': int,
    'limit': int,
    'truncated': bool,
    'content': str,
    'suggestion': str  # Only present if truncated
}
```

### 3. TruncatedTerminal

Truncates terminal output to a maximum size.

**Default Cap**: 10KB (10,240 bytes)

**Behavior**:
- Measures output size in bytes
- Truncates at safe UTF-8 character boundaries
- Preserves original size information
- Provides suggestion for using filtering commands

**Usage**:
```python
from tools.output_governor import TruncatedTerminal

# Create truncator with default limit (10KB)
truncator = TruncatedTerminal()
truncator.set_output(terminal_output, exit_code=0, command="find / -name '*.py'")
summary = truncator.get_summary()

# Or with custom limit (5KB)
truncator = TruncatedTerminal(max_size_bytes=5*1024)
```

**Summary Structure**:
```python
{
    'command': str,
    'exit_code': int,
    'original_size_bytes': int,
    'truncated_size_bytes': int,
    'max_size_bytes': int,
    'truncated': bool,
    'output': str,
    'suggestion': str  # Only present if truncated
}
```

## Convenience Functions

For quick usage without instantiating classes:

```python
from tools.output_governor import cap_search_results, read_file_capped, truncate_terminal_output

# Cap search results
summary = cap_search_results(search_results, max_results=30)

# Read file with caps
summary = read_file_capped("/path/to/file.log", offset=1, limit=100)

# Truncate terminal output
summary = truncate_terminal_output(terminal_output, max_size_bytes=8*1024)
```

## Default Limits

| Component | Default Limit | Configurable Range |
|-----------|---------------|-------------------|
| Search Results | 50 matches | 1-1000 |
| File Reads | 200 lines | 1-10000 |
| Terminal Output | 10KB | 1KB-1MB |

## Error Handling

- **File Not Found**: Returns error message in content field
- **Encoding Errors**: Handles UTF-8 decoding gracefully
- **Empty Input**: Returns empty results with appropriate metadata

## Testing

Run the module's built-in test:
```bash
python tools/output_governor.py
```

Or import and test programmatically:
```python
from tools.output_governor import _test_module
_test_module()
```

## Integration with PantheonOS ACI

This module is designed to be integrated into:
1. **Search Tools**: Wrap search results with CappedSearchResults
2. **File Reading**: Use CappedFileRead for log analysis, config reading
3. **Terminal Commands**: Wrap all terminal output with TruncatedTerminal

## Rationale for Limits

1. **Search Results (50)**: 
   - Agents typically need only top results for context
   - More results increase token usage without proportional value
   - Encourages precise query formulation

2. **File Reads (200 lines)**:
   - Most meaningful file sections are within 200 lines
   - Log files can be navigated with offset/limit
   - Prevents accidental full-file reads of large logs

3. **Terminal Output (10KB)**:
   - 10KB is approximately 2,500 tokens (rough estimate)
   - Sufficient for most command outputs
   - Forces use of filters (grep, head, tail) for large outputs

## Quick Start

```python
from tools.output_governor import CappedSearchResults, CappedFileRead, TruncatedTerminal

# Example 1: Cap search results
search_results = [...]  # Assume 200 results from a search
capped = CappedSearchResults(max_results=50, results=search_results)
summary = capped.get_summary()
if summary['truncated']:
    print(f"Only showing {summary['showing']} of {summary['total_matches']} results.")
    print(summary['suggestion'])

# Example 2: Read a large log file in chunks
reader = CappedFileRead(file_path="/var/log/app.log", offset=1001, limit=200)
if reader.get_summary()['truncated']:
    # There are more lines; read next chunk
    next_reader = CappedFileRead(file_path="/var/log/app.log", offset=1201, limit=200)

# Example 3: Truncate terminal output
import subprocess
result = subprocess.run(["find", "/", "-name", "*.py"], capture_output=True, text=True)
truncator = TruncatedTerminal(max_size_bytes=8*1024)  # 8KB limit
truncator.set_output(result.stdout, exit_code=result.returncode, command="find / -name '*.py'")
summary = truncator.get_summary()
print(summary['output'])
if summary['truncated']:
    print(summary['suggestion'])
```

## Future Enhancements

1. **Adaptive Limits**: Adjust based on available context window
2. **Smart Truncation**: Preserve important sections (errors, headers)
3. **Streaming Support**: For real-time terminal output
4. **Compression**: For storing large outputs with metadata

## Maintenance

- Review limits quarterly based on agent performance metrics
- Adjust defaults based on common usage patterns
- Consider agent feedback on capping effectiveness