#!/usr/bin/env bash
# Install .calyx/AGENT_ROLES.md from calyx-core (idempotent by default).
#
# Run from the project repository root:
#   bash .calyx/core/tooling/calyx-install-agent-roles.sh
#   bash .calyx/core/tooling/calyx-install-agent-roles.sh --force
#
# --force overwrites an existing AGENT_ROLES.md (back up first if customized).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "calyx-install-agent-roles: run from inside a git working tree" >&2
  exit 1
}

SRC="${CORE_DIR}/templates/project-agent-roles.md"
DEST="${ROOT}/.calyx/AGENT_ROLES.md"
FORCE=0

if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

if [[ ! -f "${SRC}" ]]; then
  echo "calyx-install-agent-roles: missing ${SRC} (incomplete calyx-core checkout?)" >&2
  exit 1
fi

mkdir -p "${ROOT}/.calyx"

if [[ -f "${DEST}" && "${FORCE}" -eq 0 ]]; then
  echo "calyx-install-agent-roles: skip (exists): ${DEST}"
  echo "calyx-install-agent-roles: use --force to overwrite from core template"
  exit 0
fi

cp "${SRC}" "${DEST}"
echo "calyx-install-agent-roles: wrote ${DEST}"
