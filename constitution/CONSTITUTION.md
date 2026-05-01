# Calyx Core — Organizational Constitution (v1.0)

This document is the **Company DNA**: non-negotiable defaults for how reasoning is captured, challenged, and reused across projects.

**Calyx v1** is **not a product or service** you install from an app store. It is a **convention + bundle**—Git for history, **Cursor** (or an equivalent editor with hook support) for human–agent sessions, and **small shell scripts** in this repo. If you remove the **capture** path and keep only commit messages, you do not have Calyx; you have a wiki-shaped hole. **Forks and experiments may strip automation**; what ships here assumes capture is **load-bearing**.

## Principles

1. **Collective brain over individual fix** — A solution without a recorded *why* is technical debt for the organization.
2. **Capture is load-bearing (v1)** — Commit blurbs are **not** reasoning. **Human–agent interaction** is where constraints, dead ends, and good prompts show up. Calyx v1 expects **automated raw signal**: a **git post-commit** path to **`.calyx/reasoning/inbox/`** and **Cursor hooks** to **`local/chat-log/`** (or replacements you document in an ADR). **No raw signal → nothing useful to distill → no compounding.**
3. **Assume good faith; assume bad outcomes** — Use adversarial review (10th Man) before commitment, not after failure.
4. **Tags are contracts** — Taxonomy terms link decisions, logs, and code; local tags extend but must not contradict core tags without an ADR.
5. **Silos are failures** — Cross-project dependencies must be visible (Broker) and knowledge must be distilled (Librarian).
6. **Preserve `.calyx/` structure (v1)** — **Humans and agents must not rename, remove, or “reorganize”** the standard Calyx layout unless a **ratified ADR** says otherwise. That includes: **`.calyx/core`** and **`.calyx/org`** as **submodule mount points** (not vendored copies), and **`.calyx/reasoning/`**, **`.calyx/reasoning/inbox/`**, **`.calyx/decisions/`**, **`.calyx/taxonomy/`** (and **`local-tags.yaml`** in that folder). **Adding or editing files inside `reasoning/` and `decisions/`** is normal **cpl** work; **moving mounts, collapsing layers, or replacing submodules with ad-hoc folders** breaks capture scripts, **`calyx-verify-capture`**, onboarding docs, and cross-repo alignment. If something truly must change, **draft an ADR first** and get **human** agreement—agents do not improvise structural edits here.

## Mandatory artifacts (per project)

- **Capture** — After clone: **`bash .calyx/core/tooling/calyx-setup-capture.sh`** (git hook + Cursor hooks). See **`docs/automation.md`** and **`docs/cursor-local-chat-log.md`**.
- **Reasoning log** — For every major task: thought stream under `.calyx/reasoning/`. Canonical shape: `calyx-core/templates/reasoning-log.md`. Inbox stubs from commits are **inputs**; logs are **durable**.
- **ADR** — Ratified decisions under `.calyx/decisions/` when the choice affects future work or other teams. Canonical shape: `calyx-core/templates/adr.md`.

## Amendment

Amendments to this constitution live in `calyx-core` and propagate to project mirrors via your chosen sync mechanism (copy, submodule, or script). The file `calyx-core/manifest.yaml` lists paths intended for automated sync.
