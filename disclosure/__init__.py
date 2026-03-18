"""
Disclosure module for progressive documentation discovery.
"""

from .index import DocIndex, DocEntry
from .navigator import Navigator

__all__ = ['DocIndex', 'DocEntry', 'Navigator']