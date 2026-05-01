# calyx-core

## Why Calyx

For most of history, a huge share of careful thinking never became durable—debates, synthesis, and “why we didn’t do X” lived in conversations that left little trace. AI-assisted work increases how much of that thinking happens, which makes the **loss** worse if nothing is captured—and makes **faithful capture** more feasible when teams choose to externalize it.

**Calyx is not about vacuuming chats or harvesting private sessions.** It is **stewardship of reasoning**: lightweight, versioned artifacts (reasoning logs, ADRs, shared vocabulary) so the thinking your organization already pays for **compounds inside the project and org**—where confidentiality and obligation belong. Wider contribution to shared knowledge, when it happens at all, is **opt-in and sanitized**—patterns and arguments, not raw transcripts.

The lasting power is local first: teams keep their “why,” reuse it, and improve it. Any benefit to the broader commons is **spillover**, not extraction.

---

**Calyx-core** is the **generic bundle** for that layer: constitution, specialist prompts, master taxonomy, canonical templates, and minimal tooling. Each **project repo** mounts this bundle as **`.calyx/core/`** (Git submodule) and adds its own reasoning, ADRs, and local tags. Some organizations also use a **second** submodule **`.calyx/org/`** for agency-wide, non-sensitive DNA (see `templates/dot-calyx-README.md`).

## Deliverables (what ships in this repo)

| Deliverable | Location |
|-------------|----------|
| **Brain bundle** (constitution, prompts, master taxonomy, ADR/reasoning templates) | `constitution/`, `prompts/`, `taxonomy/`, `templates/` |
| **New project creation (generic)** | **`tooling/scaffold-cursor-app.sh`** + **`templates/app-scaffold/`** |
| **New project + GitHub push (optional SFS flow)** | **`tooling/create-sfs-workspace.sh`** (wraps the scaffold; needs `gh` for remote create) |
| **Project-creation guide** | **`docs/new-project.md`** — prerequisites, flags, env vars, what gets created |
| **UX flow (Mermaid)** | **`docs/ux-flow.md`** — from “incorporate Calyx” to day-to-day habits |
| **Machine index** | `manifest.yaml` |

**Start here for a new repo:** [docs/new-project.md](docs/new-project.md), then use the commands in **New app repo** below.

## Layout

| Path | Purpose |
|------|---------|
| `constitution/` | Non-negotiable principles and mandatory artifacts |
| `prompts/` | Specialist agent system prompts (10th Man, Librarian, Broker) |
| `taxonomy/` | Master tag vocabulary (`master-tags.yaml`) |
| `templates/` | **Canonical** reasoning log and ADR shapes—sync these into projects |
| `examples/` | Illustrative artifacts (not production data) |
| `tooling/` | Lean scripts: **project creation** (`scaffold-cursor-app.sh`, `create-sfs-workspace.sh`), Ollama, closeout |
| `docs/` | Guides (e.g. **`new-project.md`**) |
| `manifest.yaml` | Machine-readable index for sync automation |
| `templates/app-scaffold/` | Files used by **`tooling/scaffold-cursor-app.sh`** (Calyx + default app layout) |

## Consumption model

1. **Submodule** this repo at **`.calyx/core/`** in each project (pin commits or tags deliberately).
2. **Optional org layer** (e.g. Scalefree): second submodule at **`.calyx/org/`** for non-sensitive agency-wide defaults—see `templates/dot-calyx-README.md` for the layout.
3. **Project-local** content always lives beside those mounts: `.calyx/reasoning/`, `.calyx/decisions/`, `.calyx/taxonomy/local-tags.yaml`.
4. Changes to **generic** behavior start in **calyx-core**; agency-only changes live in **org**; engagement-specific work stays in the **project** repo.

This repository includes **`.cursorrules`** so agents follow Calyx when working only in `calyx-core`.

## New app repo (Cursor + Calyx + layout)

Full detail: **[docs/new-project.md](docs/new-project.md)**.

From a clone of **calyx-core**, or with this repo on your `PATH`:

```bash
bash tooling/scaffold-cursor-app.sh /path/to/new-project --name "My App"
```

This creates **`.cursorrules`**, **`.calyx/`** (reasoning, decisions, taxonomy), **`AGENTS.md`** (norms for AI assistants + Calyx logging), **`VERSION`** (starts at `0.1`), **`docs/GIT.md`**, a starter **`.gitignore`**, **`git init`** on `main`, and **`git submodule add`** for `.calyx/core` (override URL with `CALYX_CORE_URL=...`). By default it also adds **`apps/web`**, **`apps/api`**, **`mcp/`**, **`packages/shared`**, **`infra/`**, and **`local/`** (gitignored) so web + API + MCP + DB/infra work has a home from day one. Use `--minimal` for Calyx-only, or `--no-submodule` / `--no-git` when bootstrapping offline.

### Scale Free Strategy (SFS) — folder + GitHub in one shot

For **Scale Free Strategy** workspaces under **`~/Documents/CURSOR`** (override with `SFS_WORKSPACE_ROOT`), with an **SFS badge** in `README.md` / `AGENTS.md`, **initial commit**, and **private** GitHub repo + push via **`gh`**:

```bash
bash tooling/create-sfs-workspace.sh "Human Project Name" [repo-slug]
```

Requires **`gh auth login`** for automatic `gh repo create`. Use `--no-github` if you only want a local repo; `--public` for a public remote.

## GitHub and consumers

- **`calyx-core`** — generic product bundle; submodule at **`.calyx/core/`** in every project.
- **Org repo** (e.g. **`calyx-scalefree-org`**) — optional second submodule at **`.calyx/org/`** for your studio’s shared, non-sensitive layer.
- **Project repos** — one repo per product or client; each has its own **local** `.calyx/reasoning/` and `.calyx/decisions/`.
- Tag releases on **calyx-core** (e.g. `v0.2.0`) so projects can pin a known-good bundle from `manifest.yaml`.
