#!/usr/bin/env bash
# Calyx checkpoint helper: stage project brain + .cursorrules from repo root.
# Usage: from project root — bash .calyx/core/tooling/calyx-closeout.sh
# You still: git commit -m "..." && git push
set -euo pipefail

if [[ ! -d .calyx ]]; then
  echo "Run this from the project repository root (expected ./.calyx/)." >&2
  exit 1
fi

echo "=== Calyx checkpoint — pre-staging status ==="
git status -sb || true

echo ""
echo "Staging: .calyx/ and .cursorrules (if present)..."
git add .calyx/
if [[ -f .cursorrules ]]; then
  git add .cursorrules
fi

echo ""
echo "=== After staging (review before commit) ==="
git status -sb || true

echo ""
echo "Next: add any app code you want in this commit, then:"
echo "  git commit -m \"calyx: checkpoint — <topic>\""
echo "  git push"
