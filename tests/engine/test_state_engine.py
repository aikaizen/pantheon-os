#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


class TestStateEngine(TestCase):
    def test_state_engine_generates_topology(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "state.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "engine" / "state_engine.py"), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            self.assertTrue(output.exists())
            data = json.loads(output.read_text())
            self.assertEqual(data["meta"]["engine_version"], "0.3.1")
            self.assertIn("deployments", data)
            self.assertIn("runtimes", data)
            self.assertIn("controllers", data)
            self.assertIn("channels", data)
            self.assertIn("bindings", data)
            self.assertGreaterEqual(data["summary"]["runtime_count"], 1)
            self.assertGreaterEqual(data["summary"]["controller_count"], 1)
            self.assertGreaterEqual(data["summary"]["channel_count"], 1)
            self.assertGreaterEqual(data["summary"]["runtime_system_count"], 1)
            self.assertGreaterEqual(data["summary"]["white_labeled_runtime_count"], 1)
            self.assertIn(data["deployments"][0]["default_runtime_system"], data["deployments"][0]["supported_runtime_systems"])
            self.assertIn("branding_mode", data["runtimes"][0])
            self.assertIn("deployment_mode", data["runtimes"][0])


if __name__ == "__main__":
    main()
