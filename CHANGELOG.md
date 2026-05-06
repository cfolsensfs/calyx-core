# Changelog

All notable changes to this bundle are documented here. The **Git tag** (e.g. **`v1.1.0`**) is what consumer repos should pin in `.calyx/core`. The **`manifest.yaml` → `version`** field is a monotonic bundle index for drift tooling and may differ from the tag.

## 1.6.0 (manifest) — thin EOW governance workflow

- New runner: **`tooling/calyx-eow-governance.sh`** (entrypoint) + **`tooling/calyx-eow-governance.py`**
- New templates: **`templates/eow-config.json`**, **`templates/eow-weekly-report.md`**
- New docs: **`docs/eow-governance.md`** plus workflow/automation/release integration
- New tests: **`tooling/tests/test_calyx_eow_governance.py`** (trigger/no-trigger, idempotence, overrides)

## 1.5.1 (manifest) — org lift cadence

- **`prompts/org-lift-cadence.txt`** — preferred name **org lift** for cpl → col; suggested cadence; assistant **nudge** rules at checkpoint (non-blocking)
- **`templates/calyx-closeout.md`** — org lift reminder step; **`AGENTS.md`**, **`workflow.md`**, **`automation.md`**, role index aligned

## v1.1.0 — 2026-05-02

**Recommended pin for new projects.** Includes everything from **v1.0.0**, plus **agent-assisted cpl → col** and **taxonomy sync** prompts, **`templates/librarian-taxonomy-review.md`**, **`.calyx/AGENT_ROLES.md`** via **`calyx-install-agent-roles.sh`** (hooked from **`calyx-setup-capture.sh`**), scaffold + verify updates. Bundle index **1.5.0** in `manifest.yaml`.

## 1.5.0 (manifest) — agent-assisted cpl → col + taxonomy

- New prompts: **`promote-cpl-to-col.txt`**, **`librarian-taxonomy-sync.txt`**
- Template: **`librarian-taxonomy-review.md`** (Librarian checklist)
- Project index: **`templates/project-agent-roles.md`** → **`.calyx/AGENT_ROLES.md`** via **`tooling/calyx-install-agent-roles.sh`**
- **`calyx-setup-capture.sh`** runs the installer after hooks; **`calyx-verify-capture.sh`** warns if the index is missing; **`scaffold-cursor-app.sh`** seeds **`AGENT_ROLES.md`** on new projects

## v1.0.0 — 2026-04-30

First **public** release of **calyx-core** as an open bundle: constitution, prompts, taxonomy, templates, capture tooling (Git + Cursor), and documentation—including [docs/philosophy.md](docs/philosophy.md) (stewardship of reasoning, suggested GitHub “About” copy). Licensed under the [MIT License](LICENSE).
