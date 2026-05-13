#!/usr/bin/env bash
# Calyx Status report (v1) — single entrypoint.
# Run from a project repository root:
#   bash .calyx/core/tooling/calyx-status-report.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${SCRIPT_DIR}/calyx-status-report.py"

if [[ ! -f "${PY}" ]]; then
  echo "calyx-status: missing ${PY}" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "calyx-status: python3 is required" >&2
  exit 1
fi

exec python3 "${PY}" "$@"
