#!/usr/bin/env python3
"""
Integration test for output governor module.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.output_governor import CappedSearchResults, CappedFileRead, TruncatedTerminal

def test_integration():
    print("Testing integration...")
    
    # Simulate search results
    results = [{"id": i, "content": f"Result {i}"} for i in range(100)]
    capped = CappedSearchResults(max_results=20, results=results)
    summary = capped.get_summary()
    assert summary['total_matches'] == 100
    assert summary['showing'] == 20
    assert summary['truncated'] == True
    assert 'suggestion' in summary
    print("✓ Search results capping works")
    
    # Simulate file reading
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        for i in range(500):
            f.write(f"LOG LINE {i+1}: Some log entry\n")
        temp_path = f.name
    
    try:
        reader = CappedFileRead(file_path=temp_path, max_lines=50, offset=101)
        summary = reader.get_summary()
        assert summary['total_lines'] == 500
        assert summary['read_lines'] == 50
        assert summary['offset'] == 101
        assert summary['truncated'] == True
        print("✓ File reading with pagination works")
    finally:
        os.unlink(temp_path)
    
    # Simulate terminal output truncation
    large_output = "Output line\n" * 10000  # Large output
    truncator = TruncatedTerminal(max_size_bytes=2*1024)  # 2KB limit
    truncator.set_output(large_output, exit_code=0, command="ls -R /")
    summary = truncator.get_summary()
    assert summary['original_size_bytes'] > 2*1024
    assert summary['truncated'] == True
    assert len(summary['output'].encode('utf-8')) <= 2*1024
    print("✓ Terminal output truncation works")
    
    print("\nAll integration tests passed! ✓")

if __name__ == "__main__":
    test_integration()