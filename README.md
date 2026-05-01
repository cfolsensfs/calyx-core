# calyx-core

**Company DNA** for the Calyx organizational intelligence layer: constitution, specialist prompts, master taxonomy, canonical templates, and minimal tooling. Each **project repo** mounts this bundle as **`.calyx/core/`** (Git submodule) and adds its own reasoning, ADRs, and local tags. Scalefree also uses a **second** submodule **`.calyx/org/`** for agency-wide, non-sensitive DNA (`calyx-scalefree-org`).

## Layout

| Path | Purpose |
|------|---------|
| `constitution/` | Non-negotiable principles and mandatory artifacts |
| `prompts/` | Specialist agent system prompts (10th Man, Librarian, Broker) |
| `taxonomy/` | Master tag vocabulary (`master-tags.yaml`) |
| `templates/` | **Canonical** reasoning log and ADR shapes—sync these into projects |
| `examples/` | Illustrative artifacts (not production data) |
| `tooling/` | Lean scripts (e.g. local Ollama runner, **new project scaffold**) |
| `manifest.yaml` | Machine-readable index for sync automation |
| `templates/app-scaffold/` | Files used by **`tooling/scaffold-cursor-app.sh`** (Calyx + default app layout) |

## Consumption model

1. **Submodule** this repo at **`.calyx/core/`** in each project (pin commits or tags deliberately).
2. **Optional org layer** (e.g. Scalefree): second submodule at **`.calyx/org/`** for non-sensitive agency-wide defaults—see `templates/dot-calyx-README.md` for the layout.
3. **Project-local** content always lives beside those mounts: `.calyx/reasoning/`, `.calyx/decisions/`, `.calyx/taxonomy/local-tags.yaml`.
4. Changes to **generic** behavior start in **calyx-core**; agency-only changes live in **org**; engagement-specific work stays in the **project** repo.

This repository includes **`.cursorrules`** so agents follow Calyx when working only in `calyx-core`.

## New app repo (Cursor + Calyx + layout)

From a clone of **calyx-core**, or with this repo on your `PATH`:

```bash
bash tooling/scaffold-cursor-app.sh /path/to/new-project --name "My App"
```

This creates **`.cursorrules`**, **`.calyx/`** (reasoning, decisions, taxonomy), **`docs/GIT.md`**, a starter **`.gitignore`**, **`git init`** on `main`, and **`git submodule add`** for `.calyx/core` (override URL with `CALYX_CORE_URL=...`). By default it also adds **`apps/web`**, **`apps/api`**, **`mcp/`**, **`packages/shared`**, **`infra/`**, and **`local/`** (gitignored) so web + API + MCP + DB/infra work has a home from day one. Use `--minimal` for Calyx-only, or `--no-submodule` / `--no-git` when bootstrapping offline.

## GitHub and consumers

- **`calyx-core`** — generic product bundle; submodule at **`.calyx/core/`** in every project.
- **Org repo** (e.g. **`calyx-scalefree-org`**) — optional second submodule at **`.calyx/org/`** for your studio’s shared, non-sensitive layer.
- **Project repos** — one repo per product or client; each has its own **local** `.calyx/reasoning/` and `.calyx/decisions/`.
- Tag releases on **calyx-core** (e.g. `v0.2.0`) so projects can pin a known-good bundle from `manifest.yaml`.
