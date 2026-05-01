#!/usr/bin/env bash
# Calyx - verify capture plumbing (local dev sanity check).
#
# Usage (project root):
#   bash .calyx/core/tooling/calyx-verify-capture.sh
#   bash .calyx/core/tooling/calyx-verify-capture.sh --ci
#
# --ci / CALYX_VERIFY_CI=1: skip checks that require `install-calyx-git-hooks.sh`
# to have been run on this machine (for GitHub Actions after checkout).

set -euo pipefail

CI_MODE=0
if [[ "${1:-}" == "--ci" ]] || [[ "${CALYX_VERIFY_CI:-}" == "1" ]]; then
  CI_MODE=1
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "FAIL: not inside a git repository" >&2
  exit 1
}
cd "$ROOT"

FAILS=0
ok() { echo "OK   $*"; }
fail() { echo "FAIL $*" >&2; FAILS=$((FAILS + 1)); }
warn() { echo "WARN $*" >&2; }

echo "=== Calyx verify capture ==="
echo "Root: $ROOT"
[[ "${CI_MODE}" -eq 1 ]] && echo "(CI mode: skipping local git hook install check)"
echo

# --- Core bundle ---
if [[ -f "$ROOT/.calyx/core/tooling/calyx-post-commit.sh" ]]; then
  ok ".calyx/core post-commit script present"
else
  fail ".calyx/core/tooling/calyx-post-commit.sh missing - run: git submodule update --init --recursive"
fi

if [[ -f "$ROOT/.calyx/core/tooling/calyx-setup-capture.sh" ]]; then
  ok "calyx-setup-capture.sh present"
else
  fail ".calyx/core/tooling/calyx-setup-capture.sh missing"
fi

if [[ -f "$ROOT/.calyx/core/templates/cursor-hooks/hooks.example.json" ]]; then
  ok "cursor-hooks templates in core bundle"
else
  fail ".calyx/core/templates/cursor-hooks/ incomplete"
fi

# --- Toolchain ---
if command -v python3 >/dev/null 2>&1; then
  ok "python3: $(python3 --version 2>&1)"
else
  fail "python3 not on PATH (required for Cursor chat-log hook)"
fi

# --- Cursor hook files ---
HOOK_PY="$ROOT/.cursor/hooks/log_chat_turn.py"
HOOK_SH="$ROOT/.cursor/hooks/log-chat-turn.sh"
if [[ -f "$HOOK_PY" && -f "$HOOK_SH" ]]; then
  ok "Cursor hook scripts present under .cursor/hooks/"
  if [[ -x "$HOOK_SH" ]]; then
    ok "log-chat-turn.sh is executable"
  else
    fail "log-chat-turn.sh is not executable - chmod +x .cursor/hooks/log-chat-turn.sh"
  fi
else
  fail "Missing .cursor/hooks/log_chat_turn.py or log-chat-turn.sh - run calyx-setup-capture.sh"
fi

HOOKS_JSON="$ROOT/.cursor/hooks.json"
if [[ -f "$HOOKS_JSON" ]]; then
  export CALYX_VERIFY_HOOKS_JSON="$HOOKS_JSON"
  if python3 <<'PY' 2>/dev/null; then
import json, os, sys
path = os.environ.get("CALYX_VERIFY_HOOKS_JSON", "")
with open(path, encoding="utf-8") as f:
    data = json.load(f)
hooks = data.get("hooks") or {}
for name in ("beforeSubmitPrompt", "afterAgentResponse"):
    block = hooks.get(name)
    if not block:
        sys.exit(f"hooks.json: missing {name}")
    text = json.dumps(block)
    if "log-chat-turn" not in text:
        sys.exit(f"hooks.json: {name} should reference log-chat-turn.sh")
sys.exit(0)
PY
    ok "hooks.json parses and references log-chat-turn"
  else
    fail "hooks.json invalid or missing beforeSubmitPrompt/afterAgentResponse -> log-chat-turn - merge templates/cursor-hooks/hooks.example.json"
  fi
  unset CALYX_VERIFY_HOOKS_JSON
else
  fail "Missing .cursor/hooks.json - run calyx-setup-capture.sh"
fi

# --- Local git hook (developer machine) ---
if [[ "${CI_MODE}" -eq 0 ]]; then
  GIT_DIR="$(git rev-parse --git-dir)"
  PC="$GIT_DIR/hooks/post-commit"
  if [[ -f "$PC" ]] && grep -q 'calyx-post-commit.sh' "$PC" 2>/dev/null; then
    ok "post-commit invokes calyx-post-commit.sh"
  else
    fail "Git post-commit hook missing or does not call calyx-post-commit.sh - run: bash .calyx/core/tooling/install-calyx-git-hooks.sh (or calyx-setup-capture.sh)"
  fi
else
  ok "(skipped) post-commit hook install - not required in CI"
fi

# --- Optional: inbox dir (created on first stub) ---
if [[ -d "$ROOT/.calyx/reasoning/inbox" ]]; then
  ok ".calyx/reasoning/inbox/ exists"
else
  warn ".calyx/reasoning/inbox/ not yet created - normal until first qualifying commit"
fi

echo
if [[ "${FAILS}" -eq 0 ]]; then
  echo "=== All checks passed ==="
  echo "Smoke test: make a small commit (see docs/automation.md for CALYX_DIARY_MIN_LINES) and confirm inbox + local/chat-log/ after using Cursor."
  exit 0
else
  echo "=== ${FAILS} check(s) failed ===" >&2
  exit 1
fi
