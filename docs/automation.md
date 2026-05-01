# Calyx automation (opt-in)

Calyx defaults to **manual** judgment for reasoning logs and ADRs. For teams that will not self-enforce a “diary,” use **automation that captures raw signal** and **defers judgment** to a quick distill step.

## What is automated vs manual

| Piece | Automated? | Notes |
|-------|------------|--------|
| **Inbox stub after commit** | **Yes** (with hook) | `tooling/calyx-post-commit.sh` writes `.calyx/reasoning/inbox/auto-*.md` with subject, body, stat, file list. |
| **Noise control** | **Heuristic** | Skips merge commits (unless `CALYX_DIARY_ON_MERGE=1`), skips `[calyx skip]`, skips commits that only touch `inbox/`, skips tiny diffs (default ≥15 lines changed; override with `CALYX_DIARY_MIN_LINES`). |
| **Proper reasoning log / ADR** | **Manual or agent** | Human edits, or run **`prompts/distill-inbox-stub-onepager.txt`** on the stub in Cursor. |
| **Bulk Slack/email import** | **Agent** | `import-distill-onepager.txt` + `templates/distill-external-to-calyx.md`. |
| **Checkpoint staging** | **Semi** | `calyx-closeout.sh` stages `.calyx/`; you still commit/push. |

Nothing here **auto-merges** to `main` or **auto-deletes** stubs—you stay in control.

## Install (per project repo)

From the **project root**, after `git submodule update --init --recursive`:

```bash
bash .calyx/core/tooling/install-calyx-git-hooks.sh
```

This installs **`post-commit`** under `.git/hooks/`. If you already had a hook, it is backed up to **`hooks/post-commit.pre-calyx`**; chain it:

```bash
mv .git/hooks/post-commit.pre-calyx .git/hooks/post-commit.user
chmod +x .git/hooks/post-commit.user
```

## Skip / tune

```bash
# One-off skip
CALYX_SKIP_DIARY=1 git commit -m "wip"

# Or in the subject
git commit -m "typo [calyx skip]"

# Stub on every commit (no line threshold)
export CALYX_DIARY_MIN_LINES=0

# Include merge commits
export CALYX_DIARY_ON_MERGE=1
```

## Suggested team habit

1. **Commit as usual** → stubs appear for non-trivial diffs.  
2. **Weekly or end-of-task:** batch-delete noise stubs; run **distill** prompt on the rest; commit real logs under `.calyx/reasoning/`.  
3. **Delete** processed stubs so `inbox/` stays small (or keep for audit—team choice).

## CI (future)

You can add a **non-blocking** GitHub Action that comments “new inbox stubs” on PRs; not shipped in core yet—avoid blocking merges on Calyx hygiene.

## Related

- [workflow.md](workflow.md) — rhythm
- [new-project.md](new-project.md) — scaffolding
