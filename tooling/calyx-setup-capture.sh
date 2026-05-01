#!/usr/bin/env bash
# Calyx v1 — install capture plumbing for a project repo:
#   • Git post-commit → .calyx/reasoning/inbox/ stubs (see calyx-post-commit.sh)
#   • Cursor hooks → local/chat-log/ (requires python3 on PATH)
#
# Run from the project repository root (the folder that contains .calyx/core):
#   bash .calyx/core/tooling/calyx-setup-capture.sh
#
# Safe to re-run: refreshes hook scripts from core; does not overwrite .cursor/hooks.json if present.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "calyx-setup-capture: run from inside a git working tree" >&2
  exit 1
}
cd "$ROOT"

INSTALL_GIT="${SCRIPT_DIR}/install-calyx-git-hooks.sh"
[[ -f "${INSTALL_GIT}" ]] || {
  echo "calyx-setup-capture: missing ${INSTALL_GIT}" >&2
  exit 1
}

bash "${INSTALL_GIT}"

TEMPL="${CORE_DIR}/templates/cursor-hooks"
if [[ ! -d "${TEMPL}" ]]; then
  echo "calyx-setup-capture: warning — no ${TEMPL} (incomplete calyx-core checkout?)" >&2
  echo "calyx-setup-capture: git post-commit installed; Cursor chat hooks skipped."
  exit 0
fi

mkdir -p "${ROOT}/.cursor/hooks"
cp "${TEMPL}/log_chat_turn.py" "${ROOT}/.cursor/hooks/"
cp "${TEMPL}/log-chat-turn.sh" "${ROOT}/.cursor/hooks/"
chmod +x "${ROOT}/.cursor/hooks/log-chat-turn.sh" "${ROOT}/.cursor/hooks/log_chat_turn.py"

if [[ ! -f "${ROOT}/.cursor/hooks.json" ]]; then
  cp "${TEMPL}/hooks.example.json" "${ROOT}/.cursor/hooks.json"
  echo "calyx-setup-capture: wrote .cursor/hooks.json — restart Cursor (or reload hooks)."
else
  echo "calyx-setup-capture: .cursor/hooks.json already exists — ensure it runs .cursor/hooks/log-chat-turn.sh"
fi

echo "calyx-setup-capture: done."
echo "calyx-setup-capture: run: bash .calyx/core/tooling/calyx-verify-capture.sh"
