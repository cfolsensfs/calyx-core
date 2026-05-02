# Calyx automation — capture and distill

**Calyx v1** treats **capture as load-bearing**, not a nice-to-have. Commit messages are **too thin** to preserve human–agent reasoning. This page describes the **git post-commit** path that drops **inbox stubs** under **`.calyx/reasoning/inbox/`**; pair it with **[cursor-local-chat-log.md](cursor-local-chat-log.md)** (Cursor hooks → **`local/chat-log/`**).

**One command after clone** (project root, submodule present):

```bash
bash .calyx/core/tooling/calyx-setup-capture.sh
```

That installs the hook below **and** syncs Cursor hook scripts. Forks may strip automation; **what ships in calyx-core assumes you keep it** or document an equivalent in an ADR.

**Verify:** `bash .calyx/core/tooling/calyx-verify-capture.sh` — local checks including git post-commit. In CI, `bash .calyx/core/tooling/calyx-verify-capture.sh --ci` (skips “hook installed on this runner”). See [first-run.md](first-run.md).

## What is automated vs manual

| Piece | Automated? | Notes |
|-------|------------|-------|
| **Inbox stub after commit** | **Yes** (with hook) | `tooling/calyx-post-commit.sh` writes `.calyx/reasoning/inbox/auto-*.md` with subject, body, stat, file list. |
| **Noise control** | **Heuristic** | Skips merge commits (unless `CALYX_DIARY_ON_MERGE=1`), skips `[calyx skip]`, skips commits that only touch `inbox/`, skips tiny diffs (default ≥15 lines changed; override with `CALYX_DIARY_MIN_LINES`). |
| **Proper reasoning log / ADR** | **Manual or agent** | Human edits, or run **`prompts/distill-inbox-stub-onepager.txt`** on the stub in Cursor. |
| **Bulk Slack/email import** | **Agent** | `import-distill-onepager.txt` + `templates/distill-external-to-calyx.md`. |
| **Checkpoint staging** | **Semi** | `calyx-closeout.sh` stages `.calyx/`; you still commit/push. |
| **Layout / hook sanity** | **Script** | `calyx-verify-capture.sh` — onboarding and optional CI (`--ci`). |
| **Agent role index (cpl)** | **Script** | `calyx-install-agent-roles.sh` — writes **`.calyx/AGENT_ROLES.md`** from core; invoked by **`calyx-setup-capture.sh`**; **`--force`** overwrites. |
| **cpl → col / taxonomy** | **Agent + prompts** | `promote-cpl-to-col.txt`, `librarian-taxonomy-sync.txt` — human merges; see [workflow.md](workflow.md). |

Nothing here **auto-merges** to `main` or **auto-deletes** stubs—you stay in control of what gets promoted. **Org-layer** promotion is **not** automated beyond agent instructions.

## Install (per project repo)

Prefer **`calyx-setup-capture.sh`** (installs git hook **and** Cursor hooks). To install **only** the git hook:

```bash
bash .calyx/core/tooling/install-calyx-git-hooks.sh
```

Run from the **project root**, after `git submodule update --init --recursive`.

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

## v1 rhythm

1. **Commit as usual** → stubs appear for non-trivial diffs; Cursor appends turns to **`local/chat-log/`** if hooks are enabled.
2. **On a steady beat** (end of day or end of task): run **distill** on stubs that matter; skim **recent chat-log**; promote into **`.calyx/reasoning/`** or **delete** noise.
3. **Delete** processed stubs so `inbox/` stays small (or keep for audit—team choice).

## CI (future)

You can add a **non-blocking** GitHub Action that comments “new inbox stubs” on PRs; not shipped in core yet—avoid blocking merges on Calyx hygiene.

## Related

- [cursor-local-chat-log.md](cursor-local-chat-log.md) — Cursor hooks → `local/chat-log/`
- [workflow.md](workflow.md) — rhythm
- [new-project.md](new-project.md) — scaffolding
- [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) — v1 capture principle
