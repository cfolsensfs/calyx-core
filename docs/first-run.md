# Calyx first run — prerequisites, reasoning, and checklist

This is the **canonical setup path** for **Calyx v1**: what to install, **why** (so the org can reuse reasoning, not only code), and how to confirm it worked. Project scaffolds include a short **`SETUP_CALYX.md`** at the repo root that points here—open that in Cursor if you want an agent to walk the checklist with you.

## New teammates (recommended flow)

**Lead devs:** send something like this after someone has access to the repo:

1. `git pull` (and whenever submodules change: **`git submodule update --init --recursive`**).
2. In **Cursor**, **File → Open Folder** on the **repository root** (the folder that contains `.calyx/`), not a subfolder.
3. Open **`SETUP_CALYX.md`** at the root. Either follow it yourself or paste the **agent prompt** below.

**Agent prompt (copy-paste):**

```text
Read SETUP_CALYX.md in the repo root, then walk me through Calyx setup using .calyx/core/docs/first-run.md. Run each step including bash .calyx/core/tooling/calyx-setup-capture.sh and bash .calyx/core/tooling/calyx-verify-capture.sh. Remind me to restart Cursor after hooks are installed. Do not skip verify or smoke test.
```

The agent guides the checklist; it does not replace **you** running **`calyx-setup-capture.sh`**, **restarting Cursor**, or doing a real **commit + chat** smoke test on your machine.

## Why these prerequisites exist (Calyx-y)

Calyx is **stewardship of reasoning**. Most of that reasoning today happens in **human–agent conversations** and in **commits**—but **commit messages alone** rarely hold the constraints, dead ends, and prompts that matter. **v1** therefore expects:

1. **Git** — versioned history, **submodules** for the Calyx bundle, and a **post-commit hook** that drops **inbox stubs** under `.calyx/reasoning/inbox/` so “what just shipped?” is never a blank page.
2. **Cursor** (or another editor with a **hooks** mechanism you wire equivalently) — **session hooks** append turns to **`local/chat-log/`** (gitignored). That is **raw** material for distill; reasoning logs and ADRs stay the **durable** layer.
3. **Python 3** — the bundled hook helper is a small **Python** script (portable, no extra deps). If you remove it, replace it with something that still captures turns and document that in an ADR.

Skipping capture is opting out of the model: **no raw signal → nothing reliable to distill → Calyx does not compound.**

## Prerequisites

| Need | Required for default v1 | Why | Verify |
|------|-------------------------|-----|--------|
| **Git** | Yes | Submodules, hooks, normal engineering | `git --version` |
| **Bash** | Yes | Setup and hook driver scripts | `bash --version` |
| **Python 3** | Yes | `log_chat_turn.py` for Cursor hooks | `python3 --version` |
| **Cursor** | Yes for the default chat-log path | Hook events → `local/chat-log/` | **Settings → Hooks** after install |
| **GitHub CLI (`gh`)** | No | Only for `create-sfs-workspace.sh`-style repo create/push | `gh --version` |

**Multi-root workspaces:** chat logging uses the **first** workspace root Cursor sends in the hook payload. Put the **primary repo first**, or adjust the script (see [cursor-local-chat-log.md](cursor-local-chat-log.md)).

---

## Checklist — new project (scaffold already created)

From the **repository root** (the folder that should contain `.calyx/`):

1. **Submodules**
   ```bash
   git submodule update --init --recursive
   ```
   Confirm `.calyx/core/tooling/calyx-setup-capture.sh` exists.

2. **Capture (one command)**
   ```bash
   bash .calyx/core/tooling/calyx-setup-capture.sh
   ```
   Installs **git post-commit** + **Cursor** hook files and seeds **`.calyx/AGENT_ROLES.md`** (prompt index for distill, **org lift**, taxonomy sync). If `.cursor/hooks.json` already existed, the script does **not** overwrite it—merge hook commands manually if needed.

3. **Restart Cursor** (or reload hooks) so `.cursor/hooks.json` is picked up.

4. **Verify (guardrails)** — from repo root:
   ```bash
   bash .calyx/core/tooling/calyx-verify-capture.sh
   ```
   Expect **`=== All checks passed ===`**. This checks `.calyx/core`, `python3`, `.cursor/hooks`, `hooks.json` shape, and (on your machine) the **git post-commit** hook. In **CI**, use **`--ci`** so the git-hook install step is skipped. New scaffolds include **`.github/workflows/calyx-verify.yml`** (`continue-on-error: true`) so PRs get a **non-blocking** signal when capture layout drifts.

5. **Smoke test**
   - Make a small real commit (or tune **`CALYX_DIARY_MIN_LINES`** if your test diff is tiny—see [automation.md](automation.md)).
   - Confirm a new file under **`.calyx/reasoning/inbox/`** (unless skipped by heuristics).
   - Send a short message in Cursor chat; confirm **`local/chat-log/<today>.md`** grows (folder is gitignored).

6. **Habit** — skim [workflow.md](workflow.md) and run **distill** on stubs / chat-log on a steady beat; promote to **`.calyx/reasoning/`** or delete noise.

---

## Checklist — brownfield repo (Calyx added later)

1. Add **`.calyx/core`** as a submodule and create **`.calyx/reasoning`**, **`.calyx/decisions`**, **`.calyx/taxonomy`** as in [new-project.md](new-project.md) / [ux-flow.md](ux-flow.md).
2. Run **`calyx-setup-capture.sh`** as above (also creates **`.calyx/AGENT_ROLES.md`** when missing). If you already ran capture before upgrading **calyx-core**, run **`bash .calyx/core/tooling/calyx-install-agent-roles.sh`** once to backfill the agent index.
3. If the team already uses **`.cursor/hooks.json`**, **merge** the `beforeSubmitPrompt` / `afterAgentResponse` / `stop` entries from **`templates/cursor-hooks/hooks.example.json`** instead of blind overwrite.
4. Run **`calyx-verify-capture.sh`** until green; add **`.github/workflows/calyx-verify.yml`** by copying **`templates/app-scaffold/github-workflows-calyx-verify.yml`** from this bundle if you want the same CI guardrail as new scaffolds.

---

## For Cursor agents (onboarding playbook)

When the user says they are **setting up Calyx**, **onboarding**, or **first run**:

1. **Read** this file: **`.calyx/core/docs/first-run.md`** (if `.calyx/core` is missing, stop and help them add the submodule per [new-project.md](new-project.md)).
2. **Execute the checklist in order** for their situation (scaffold vs brownfield). **Do not skip verify steps**—run the commands or have the user paste output.
3. **Explain briefly** why each prerequisite exists when the user asks; point to the table above.
4. After **`calyx-setup-capture.sh`**, **remind** them to **restart Cursor** before expecting chat-log files.
5. Run **`calyx-verify-capture.sh`** and fix any **FAIL** lines before declaring onboarding done.
6. **Optional:** propose one **test commit** and one **chat message** to validate inbox + `local/chat-log/`.

Do **not** invent alternate install paths unless the user’s environment cannot satisfy the defaults; if so, suggest documenting an ADR for their replacement capture mechanism.

Do **not** rename or reorganize **`.calyx/`** (submodule mounts, **`reasoning/`**, **`decisions/`**, **`taxonomy/`**). Content edits inside **`reasoning/`** / **`decisions/`** are fine; structural changes require a **human-approved ADR** (see **constitution** principle 6).

---

## Community / brownfield

Windows paths, exotic hook chains, and merged **`hooks.json`** are **documentation + judgment**—and fair game for **community recipes** (issues, PRs to this repo) that harden Calyx without turning it into a product installer.

## Related

- [automation.md](automation.md) — post-commit stub behavior and env tunables
- [cursor-local-chat-log.md](cursor-local-chat-log.md) — Cursor hooks, retention, limitations
- [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) — v1 capture principle
- [new-project.md](new-project.md) — scaffolding and flags
- [eow-governance.md](eow-governance.md) — thin weekly governance runner
- [calyx-status-report.md](calyx-status-report.md) — v1 status report (tangible adoption pulse)
- [feedback-loop.md](feedback-loop.md) — classify/apply/enforce loop (learn -> guided -> guardrail)
- [releasing.md](releasing.md) — maintainers: cutting **v1.x.y** tags and bundle version
