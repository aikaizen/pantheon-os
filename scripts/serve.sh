#!/bin/bash
# Serve PantheonOS site locally for development
# Usage: ./scripts/serve.sh [port]

PORT="${1:-8080}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Serving PantheonOS site on http://localhost:$PORT"
echo "  Site: http://localhost:$PORT/site/"
echo "  Dashboard: http://localhost:$PORT/"
echo "  Forge: http://localhost:$PORT/forge/"
echo ""
echo "Press Ctrl+C to stop"

cd "$REPO_ROOT"
python3 -m http.server "$PORT"
