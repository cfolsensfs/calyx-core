#!/usr/bin/env bash
# Install Calyx git hooks in the current repository (run from project root).
#
# Usage:
#   cd /path/to/project
#   bash .calyx/core/tooling/install-calyx-git-hooks.sh
#
# Requires: .calyx/core/tooling/calyx-post-commit.sh (submodule initialized).

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

CORE_SCRIPT="$ROOT/.calyx/core/tooling/calyx-post-commit.sh"
if [[ ! -f "$CORE_SCRIPT" ]]; then
  echo "Missing $CORE_SCRIPT — run: git submodule update --init --recursive" >&2
  exit 1
fi
chmod +x "$CORE_SCRIPT" 2>/dev/null || true

GIT_DIR="$(git rev-parse --git-dir)"
HOOK_DIR="$GIT_DIR/hooks"
POST_COMMIT="$HOOK_DIR/post-commit"
mkdir -p "$HOOK_DIR"

if [[ -f "$POST_COMMIT" ]] && ! grep -q 'calyx-post-commit.sh' "$POST_COMMIT" 2>/dev/null; then
  echo "Existing post-commit hook found without Calyx — backing up to hooks/post-commit.pre-calyx" >&2
  cp "$POST_COMMIT" "$HOOK_DIR/post-commit.pre-calyx"
  echo "Chain your old hook: mv $HOOK_DIR/post-commit.pre-calyx $HOOK_DIR/post-commit.user && chmod +x $HOOK_DIR/post-commit.user" >&2
fi

cat > "$POST_COMMIT" <<'EOF'
#!/bin/sh
# Calyx — post-commit: run Calyx stub, then optional post-commit.user
ROOT="$(git rev-parse --show-toplevel)"
GIT_DIR="$(git rev-parse --git-dir)"
CALYX="$ROOT/.calyx/core/tooling/calyx-post-commit.sh"
if [ -f "$CALYX" ]; then
  /usr/bin/env bash "$CALYX" || true
fi
USER_HOOK="$GIT_DIR/hooks/post-commit.user"
if [ -x "$USER_HOOK" ]; then
  "$USER_HOOK" "$@" || true
fi
EOF
chmod +x "$POST_COMMIT"

echo "Installed $POST_COMMIT"
echo "To skip once: CALYX_SKIP_DIARY=1 git commit ...  or  [calyx skip] in subject"
echo "Tune noise: export CALYX_DIARY_MIN_LINES=0   # stub every commit"
