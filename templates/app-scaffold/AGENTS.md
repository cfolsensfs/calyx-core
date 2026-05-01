# Guidance for AI assistants — __PROJECT_NAME__

__WORKSPACE_BADGE__

## Read first

1. **`SETUP_CALYX.md`** — if the user is **new to this repo** or **onboarding Calyx**, walk **`.calyx/core/docs/first-run.md`** with them (verify steps, restart Cursor after hooks). After setup, run **`bash .calyx/core/tooling/calyx-verify-capture.sh`** and fix failures.
2. **`.cursorrules`** — Calyx norms for this implementation repo.
3. **`docs/GIT.md`** — clone, submodules, pushing.
4. **`.calyx/README.md`** — where reasoning, ADRs, and taxonomy live.

## `.calyx/` layout is fixed

**Never** rename, delete, or reorganize **`.calyx/core`**, **`.calyx/org`**, **`.calyx/reasoning/`** (including **`inbox/`**), **`.calyx/decisions/`**, or **`.calyx/taxonomy/`**. Never replace submodules with copied trees. **Do** add or edit **files** in **`reasoning/`** and **`decisions/`**. If the user wants a different layout, stop and require a **human-gated ADR**—otherwise capture and verify will fail.

## Calyx: add knowledge, not only code

This project uses **Calyx v1** so reasoning survives the chat session. **Capture is mandatory for the model to work:** run **`bash .calyx/core/tooling/calyx-setup-capture.sh`** after clone (git inbox stubs + Cursor → **`local/chat-log/`**). Commit messages are not enough; distill stubs and chat-log into **`.calyx/reasoning/`** on a steady beat.

| Situation | Where to write |
|-----------|----------------|
| Multi-step, architectural, security, data model, infra, or anything that affects others | **`.calyx/reasoning/`** — new dated file from `_TEMPLATE.md` (or copy from `.calyx/core/templates/reasoning-log.md`). |
| A decision that should bind future work | **`.calyx/decisions/`** — new ADR from `ADR-TEMPLATE.md` (canonical shape in `.calyx/core/templates/adr.md`). |
| Project-specific tags | **`.calyx/taxonomy/local-tags.yaml`** — align with `.calyx/core/taxonomy/master-tags.yaml`. |

After a substantive session, **summarize**: context, options, what you chose, risks, and open questions. Link any new ADR. Prefer **superseding** old ADRs over silent rewrites.

Specialist framing (prompts under `.calyx/core/prompts/`): **10th Man** (challenge assumptions), **Librarian** (distill and tag), **Broker** (dependencies and silos).

## Version

Release / scaffold version for this repo is in **`VERSION`** (semantic-ish `0.1` at creation). Bump when you ship meaningful milestones; record notable bumps in a reasoning log or ADR if the change is architectural.

## Secrets and client material

Do not commit secrets, credentials, or material that belongs in **`local/`** (gitignored). If something sensitive was ever committed, say so and stop — remediation is a separate step.
