# Changelog

All notable changes to this bundle are documented here. The **Git tag** (e.g. **`v1.1.0`**) is what consumer repos should pin in `.calyx/core`. The **`manifest.yaml` → `version`** field is a monotonic bundle index for drift tooling and may differ from the tag.

## 1.7.3 (manifest) — ADR for governance scope; experiments legend + recap

- **`docs/decisions/ADR-0001-governance-feedback-and-deferred-telemetry.md`** — ratifies **shipped** EOW + feedback loop vs **deferred** continuous impact/scoring pipeline; points at experiments + impact-telemetry (**2026-05-07**)
- **`docs/experiments-and-future.md`** — **status legend** (not started / parked / won’t do), **scope recap** table, index rows with one-line reasons
- **`docs/eow-governance.md`**, **`docs/feedback-loop.md`**, **`docs/impact-telemetry.md`** — cross-links to ADR and deferred metrics traceability

## 1.7.2 (manifest) — documentation tone (fewer meta / setup prompts)

- **`docs/philosophy.md`** — **In one sentence** replaces GitHub-specific header labeling; topics list removed from philosophy (see hosting doc for `gh` topics example)
- **`docs/github-repository-setup.md`**, **`README.md`**, **`docs/experiments-and-future.md`**, **`docs/impact-telemetry.md`**, **`docs/workflow.md`**, **`docs/why-calyx-now.md`**, **`docs/new-project.md`** — less instructional framing in public descriptors; related-link blurbs shortened

## 1.7.1 (manifest) — experiments index + impact telemetry reference doc

- **`docs/experiments-and-future.md`** — index of design directions **not** shipped as first-class tooling; fork-friendly “thanks for cloning; here is what we thought about”
- **`docs/impact-telemetry.md`** — detailed **process + schema sketch** for ROI-style metrics; **release-boundary audits** as the recommended default; links to feedback-loop outputs
- **`README.md`**, **`docs/philosophy.md`**, **`docs/why-calyx-now.md`**, **`docs/github-repository-setup.md`** — explanatory copy refreshed for **EOW governance**, **feedback loop**, **org lift / taxonomy**, **scaffold quality defaults**, and **experiments** (not only **CHANGELOG**)
- **`docs/philosophy.md`** — **In one sentence** summary block; epistemic sections unchanged in intent
- **`.gitignore`** — ignore **`__pycache__/`** and **`*.py[cod]`**

## 1.7.0 (manifest) — knowledge feedback loop (capture -> distill -> apply -> enforce)

- New runner: **`tooling/calyx-feedback-loop.sh`** + **`tooling/calyx-feedback-loop.py`**
- New engine modules: `tooling/lib/feedback_classify.py`, `feedback_policy.py`, `feedback_override.py`, `feedback_render.py`
- New policy/config/docs: **`templates/feedback-config.json`**, **`docs/feedback-loop.md`**
- New scaffold integrations:
  - `.calyx/feedback-config.json`
  - `.github/workflows/calyx-feedback.yml`
  - PR/issue Calyx compliance templates
- New tests: classifier, policy, override, integration under `tooling/tests/`

## 1.6.1 (manifest) — code quality + formatting baseline in scaffolds

- Scaffold now includes **`.editorconfig`**, **`.prettierrc.json`**, and **`.prettierignore`**
- `templates/app-scaffold/cursorrules` explicitly enforces:
  - working software validation,
  - clear intent-focused code notes,
  - formatter/lint compliance before commit
- `templates/app-scaffold/AGENTS.md` and `docs-GIT.md` now include a concrete quality gate and Prettier usage guidance

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

First **public** release of **calyx-core** as an open bundle: constitution, prompts, taxonomy, templates, capture tooling (Git + Cursor), and documentation—including [docs/philosophy.md](docs/philosophy.md) (stewardship of reasoning). Licensed under the [MIT License](LICENSE).
