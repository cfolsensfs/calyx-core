#!/usr/bin/env bash
# Thin EOW Calyx Governance runner (single entrypoint).
# Run from a project repository root:
#   bash .calyx/core/tooling/calyx-eow-governance.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${SCRIPT_DIR}/calyx-eow-governance.py"

if [[ ! -f "${PY}" ]]; then
  echo "calyx-eow: missing ${PY}" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "calyx-eow: python3 is required" >&2
  exit 1
fi

exec python3 "${PY}" "$@"
