#!/usr/bin/env python3
"""
Test import of output_governor module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from tools import CappedSearchResults, CappedFileRead, TruncatedTerminal
    from tools import cap_search_results, read_file_capped, truncate_terminal_output
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Quick test
results = list(range(100))
capped = CappedSearchResults(max_results=10, results=results)
summary = capped.get_summary()
assert summary['total_matches'] == 100
print("✓ Basic functionality works")

print("All import tests passed!")