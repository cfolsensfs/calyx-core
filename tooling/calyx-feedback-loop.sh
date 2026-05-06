#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${SCRIPT_DIR}/calyx-feedback-loop.py"
if ! command -v python3 >/dev/null 2>&1; then
  echo "calyx-feedback: python3 required" >&2
  exit 1
fi
exec python3 "${PY}" "$@"
