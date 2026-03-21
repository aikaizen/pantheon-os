#!/usr/bin/env python3
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from tools.validate_topology import validate


class TestTopologyValidation(TestCase):
    def test_registry_topology_is_valid(self):
        errors, notes = validate()
        self.assertEqual(errors, [], msg="\n".join(errors + notes))


if __name__ == "__main__":
    main()
