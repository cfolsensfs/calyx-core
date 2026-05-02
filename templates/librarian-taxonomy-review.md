# Librarian runbook — taxonomy review (cpl / col / ccl)

Use this checklist when **reconciling tags** across Calyx layers. Pair with **`prompts/librarian-taxonomy-sync.txt`** in Cursor or another LLM front end: attach **`master-tags.yaml`**, **`local-tags.yaml`**, and optional org tag files.

## Before you start

- [ ] Confirm **`.calyx/core/taxonomy/master-tags.yaml`** is the **pinned** version (submodule up to date).
- [ ] Open **`.calyx/taxonomy/local-tags.yaml`** for this repo.
- [ ] If the studio uses **col**, locate org taxonomy paths under **`.calyx/org/`** (or the org repo checkout).
- [ ] Agree **redaction** rules if excerpts from reasoning logs will be pasted (client names, unreleased features).

## Steps

1. **Inventory** — List all tag ids in master + local (+ org if applicable). Note duplicates and near-miss spellings.
2. **Usage spot-check** — Skim recent **`.calyx/reasoning/`** and **`.calyx/decisions/`** for tags in prose or front matter; note ids that appear but are not registered.
3. **Severity** — For each mismatch: **block** (contradicts core meaning), **warn** (orphan or ambiguous), **info** (cosmetic or doc-only).
4. **Patch local first** — Prefer fixing **cpl** (`local-tags.yaml`) before proposing **col** or **ccl** changes.
5. **Escalate** — If a tag should be **studio-wide**, run **org lift** via **`promote-cpl-to-col.txt`** (or human PR) with sanitized wording. If a tag should be **global for all Calyx users**, open/track a **calyx-core** change — do not silently fork core vocabulary in one project without an ADR.

## Done when

- [ ] `local-tags.yaml` validates as YAML and aligns with how the team writes reasoning logs.
- [ ] Open issues are listed (if any) for col or ccl follow-up.
- [ ] No client-sensitive strings in org or core proposals.

## Related

- **`prompts/librarian-taxonomy-sync.txt`** — paste-ready Librarian instruction block
- **`prompts/promote-cpl-to-col.txt`** — org lift (cpl → col) assistant
- **`prompts/org-lift-cadence.txt`** — when to lift + checkpoint nudges
- **`docs/glossary.md`** — **ccl** / **col** / **cpl**
- **`docs/workflow.md`** — ongoing rhythm
