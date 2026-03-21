#!/usr/bin/env python3
"""
Full readiness check for the PromptEngines PantheonOS pilot.
"""

import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd):
    print(f"$ {' '.join(cmd)}")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())
        raise SystemExit(result.returncode)


def smoke_serve():
    port = 8765
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)
    try:
        for path in [
            "/",
            "/site/",
            "/apps/terminal-manager/",
            "/apps/promptengines-dashboard/",
        ]:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as response:
                body = response.read()
                print(f"SMOKE {path} {response.status} {response.headers.get_content_type()} {len(body)} bytes")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


def main():
    run([sys.executable, "-B", "tools/validate_topology.py"])
    run([
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.realms.test_isolation",
        "tests.tools.test_validate_topology",
        "tests.engine.test_state_engine",
    ])
    run([sys.executable, "-B", "tools/test_output_governor_integration.py"])
    with tempfile.TemporaryDirectory() as tmpdir:
        run([sys.executable, "-B", "engine/state_engine.py", "--output", str(Path(tmpdir) / "state.json")])
    smoke_serve()
    print("PromptEngines pilot readiness checks passed.")


if __name__ == "__main__":
    main()
