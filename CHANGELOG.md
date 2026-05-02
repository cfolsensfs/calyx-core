# Changelog

All notable changes to this bundle are documented here. The **Git tag** (e.g. `v1.0.0`) is what consumer repos should pin in `.calyx/core`. The **`manifest.yaml` → `version`** field is a monotonic bundle index for drift tooling and may differ from the tag.

## 1.5.0 (manifest) — agent-assisted cpl → col + taxonomy

- New prompts: **`promote-cpl-to-col.txt`**, **`librarian-taxonomy-sync.txt`**
- Template: **`librarian-taxonomy-review.md`** (Librarian checklist)
- Project index: **`templates/project-agent-roles.md`** → **`.calyx/AGENT_ROLES.md`** via **`tooling/calyx-install-agent-roles.sh`**
- **`calyx-setup-capture.sh`** runs the installer after hooks; **`calyx-verify-capture.sh`** warns if the index is missing; **`scaffold-cursor-app.sh`** seeds **`AGENT_ROLES.md`** on new projects

## v1.0.0 — 2026-04-30

First **public** release of **calyx-core** as an open bundle: constitution, prompts, taxonomy, templates, capture tooling (Git + Cursor), and documentation—including [docs/philosophy.md](docs/philosophy.md) (stewardship of reasoning, suggested GitHub “About” copy). Licensed under the [MIT License](LICENSE).
