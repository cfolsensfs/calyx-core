#!/usr/bin/env bash
# Calyx post-commit capture: write a low-friction stub under .calyx/reasoning/inbox/
# for later human or agent distillation into a proper reasoning log or ADR.
#
# Install (from repo root, after submodule init):
#   bash .calyx/core/tooling/install-calyx-git-hooks.sh
#
# Skip this run:
#   CALYX_SKIP_DIARY=1 git commit ...
#   or put [calyx skip] in the commit message (any case).
#
# Env (optional):
#   CALYX_DIARY_MIN_LINES   Minimum inserted+deleted lines to emit a stub (default: 15). Set 0 for every commit.
#   CALYX_DIARY_ON_MERGE    Set to 1 to also stub on merge commits (default: skip merges).

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$ROOT"

if [[ "${CALYX_SKIP_DIARY:-}" == "1" ]]; then
  exit 0
fi

# Merge commit: more than one parent (MERGE_HEAD is cleared after commit, so inspect parents).
_parent_line="$(git rev-list --parents -n 1 HEAD 2>/dev/null || true)"
_parent_count=0
if [[ -n "$_parent_line" ]]; then
  _parent_count="$(echo "$_parent_line" | wc -w | tr -d ' ')"
fi
if [[ "${_parent_count:-0}" -gt 2 ]]; then
  [[ "${CALYX_DIARY_ON_MERGE:-}" == "1" ]] || exit 0
fi

SUBJECT="$(git log -1 --format=%s)"
if echo "$SUBJECT" | grep -qi '\[calyx skip\]'; then
  exit 0
fi

if [[ ! -d .calyx/reasoning ]]; then
  exit 0
fi

INBOX=".calyx/reasoning/inbox"
mkdir -p "$INBOX"

# Avoid infinite stubs when the only thing committed is inbox files.
# Use `git show` (not `git diff-tree` alone) so root commits and normal commits both list paths.
_any_changed=0
_all_inbox=1
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  _any_changed=1
  case "$f" in
    .calyx/reasoning/inbox/*) ;;
    *) _all_inbox=0 ;;
  esac
done < <(git show --name-only --format="" HEAD)

[[ "$_any_changed" -eq 0 ]] && exit 0
[[ "$_all_inbox" -eq 1 ]] && exit 0

MIN_LINES="${CALYX_DIARY_MIN_LINES:-15}"
if [[ "$MIN_LINES" =~ ^[0-9]+$ ]] && [[ "$MIN_LINES" -gt 0 ]]; then
  total=0
  while read -r add del _; do
    [[ "$add" == "-" ]] && continue
    [[ "$del" == "-" ]] && continue
    [[ -z "$add" ]] && continue
    total=$((total + add + del))
  done < <(git show --numstat --format="" HEAD)
  if [[ "$total" -lt "$MIN_LINES" ]]; then
    exit 0
  fi
fi

SHA="$(git rev-parse --short HEAD)"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="$INBOX/auto-${TS}-${SHA}.md"
AUTHOR="$(git log -1 --format='%an <%ae>')"
BODY="$(git log -1 --format=%b)"

ISO_NOW="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")"

{
  cat <<EOF
<!-- calyx auto-stub: safe to delete after distilling into reasoning/ or an ADR -->
# Inbox stub — commit ${SHA}

- **Auto-captured:** ${ISO_NOW}
- **Author:** ${AUTHOR}
- **Subject:** ${SUBJECT}

## Commit message (body)

EOF
  if [[ -n "${BODY//[$'\t\r\n ']/}" ]]; then
    printf '%s\n' "$BODY"
  else
    echo '_(none)_'
  fi
  cat <<EOF

## Files touched

\`\`\`
$(git show --stat --format="" HEAD)
\`\`\`

## File list

$(git show --name-only --format="" HEAD | sed 's/^/- /')

## Next step (human or agent)

Distill this into **\`.calyx/reasoning/<dated-topic>.md\`** (or an ADR if the commit implies a binding decision).

Use **\`.calyx/core/prompts/distill-inbox-stub-onepager.txt\`** with this file attached, or delete this stub if it was noise.

EOF
} > "$OUT"

echo "calyx: wrote $OUT (distill or delete)" >&2
