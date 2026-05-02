# calyx-core

**Calyx v1.0** — constitution, prompts, templates, and **capture tooling** for projects that use **Git + Cursor + bash**. This repo is **not an installable product**; it is a **bundle and convention**. If you fork it and delete the hooks, that is on you—you no longer have the v1 baseline.

**Public release:** **`v1.0.0`** · [CHANGELOG.md](CHANGELOG.md) · [MIT License](LICENSE) · **GitHub “About” copy:** [docs/philosophy.md](docs/philosophy.md#for-github-repository-header) · **Make the repo public + topics:** [docs/github-repository-setup.md](docs/github-repository-setup.md)

**Read next:** [Philosophy — stewardship, not extraction](docs/philosophy.md) · [Why Calyx matters now](docs/why-calyx-now.md)

## Why Calyx

For most of history, a huge share of careful thinking never became durable—debates, synthesis, and “why we didn’t do X” lived in conversations that left little trace. AI-assisted work increases how much of that thinking happens in **human–agent threads**, which makes the **loss** worse if you only keep **commit messages**—and makes **faithful capture** mandatory if anything is to compound.

**Calyx v1 expects automated raw signal:** a **git post-commit** path to **`.calyx/reasoning/inbox/`** and **Cursor hooks** to **`local/chat-log/`** (see **`tooling/calyx-setup-capture.sh`**). Judgment still happens when you **distill** into reasoning logs and ADRs; without capture, there is nothing to distill.

**Calyx is not about vacuuming chats or harvesting private sessions.** It is **stewardship of reasoning**: lightweight, versioned artifacts (reasoning logs, ADRs, shared vocabulary) so the thinking your organization already pays for **compounds inside the project and org**—where confidentiality and obligation belong. Wider contribution to shared knowledge, when it happens at all, is **opt-in and sanitized**—patterns and arguments, not raw transcripts.

The lasting power is local first: teams keep their “why,” reuse it, and improve it. Any benefit to the broader commons is **spillover**, not extraction.

---

**Calyx core layer (ccl):** this repo is the **generic bundle**—constitution, specialist prompts, master taxonomy, canonical templates, and minimal tooling. Each **project repo** mounts it as **`.calyx/core/`** (Git submodule). **Calyx org layer (col):** optional second submodule **`.calyx/org/`** for agency-wide, non-sensitive DNA. **Calyx project layer (cpl):** project-local reasoning, ADRs, and `local-tags.yaml`. Abbreviations: **ccl**, **col**, **cpl** — see [docs/glossary.md](docs/glossary.md).

## Deliverables (what ships in this repo)

| Deliverable | Location |
|-------------|----------|
| **Brain bundle** (constitution, prompts, master taxonomy, ADR/reasoning templates) | `constitution/`, `prompts/`, `taxonomy/`, `templates/` |
| **New project creation (generic)** | **`tooling/scaffold-cursor-app.sh`** + **`templates/app-scaffold/`** |
| **New project + GitHub push (optional SFS flow)** | **`tooling/create-sfs-workspace.sh`** (wraps the scaffold; needs `gh` for remote create) |
| **Project-creation guide** | **`docs/new-project.md`** — prerequisites, flags, env vars, what gets created |
| **First run / onboarding** | **`docs/first-run.md`** — prerequisites + **why**, checklist; **`tooling/calyx-verify-capture.sh`** — guardrail checks; scaffolds add **`SETUP_CALYX.md`** + **`.github/workflows/calyx-verify.yml`** (non-blocking) |
| **UX flow (Mermaid)** | **`docs/ux-flow.md`** — from “incorporate Calyx” to day-to-day habits |
| **Work rhythm (Mermaid)** | **`docs/workflow.md`** — reasoning, ADRs, specialists, checkpoint (**living doc**) |
| **Glossary (ccl / col / cpl)** | **`docs/glossary.md`** |
| **Org vs projects** | **`docs/org-and-projects.md`** — studio/agency → many repos; Calyx shape independent of disk |
| **Capture (v1 baseline)** | **`tooling/calyx-setup-capture.sh`** — git post-commit + Cursor hooks; **`docs/automation.md`**, **`docs/cursor-local-chat-log.md`** |
| **Agent roles / cpl → col / taxonomy prompts** | **`tooling/calyx-install-agent-roles.sh`** → **`.calyx/AGENT_ROLES.md`**; **`prompts/promote-cpl-to-col.txt`**, **`prompts/librarian-taxonomy-sync.txt`**; **`prompts/README.md`** |
| **Machine index** | `manifest.yaml` |
| **Cutting releases** | **`docs/releasing.md`** — maintainers, **`v1.0.0`** tag, pre-flight checklist |
| **GitHub (public + About + topics)** | **`docs/github-repository-setup.md`** |
| **Changelog** | **`CHANGELOG.md`** |
| **License** | **`LICENSE`** (MIT) |
| **Philosophy + GitHub header copy** | **`docs/philosophy.md`** — epistemic framing; stewardship vs extraction; suggested “About” text |
| **Why Calyx now (one page)** | **`docs/why-calyx-now.md`** — org intelligence vs solo speed; capture; boundaries |

**Start here for a new repo:** [docs/new-project.md](docs/new-project.md), then use the commands in **New app repo** below.

## Layout

| Path | Purpose |
|------|---------|
| `constitution/` | Non-negotiable principles and mandatory artifacts |
| `prompts/` | Specialist agent system prompts (10th Man, Librarian, Broker) |
| `taxonomy/` | Master tag vocabulary (`master-tags.yaml`) |
| `templates/` | **Canonical** reasoning log and ADR shapes; **import runbook** (`distill-external-to-calyx.md`) for Slack/email → Calyx |
| `examples/` | Illustrative artifacts (not production data) |
| `tooling/` | Lean scripts: **project creation** (`scaffold-cursor-app.sh`, `create-sfs-workspace.sh`), Ollama, closeout |
| `docs/` | **`philosophy.md`**, **`why-calyx-now.md`**, **`first-run.md`**, **`releasing.md`**, **`new-project.md`**, **`ux-flow.md`**, **`workflow.md`**, **`glossary.md`**, **`org-and-projects.md`**, **`automation.md`** |
| `manifest.yaml` | Machine-readable index for sync automation |
| `templates/app-scaffold/` | Files used by **`tooling/scaffold-cursor-app.sh`** (Calyx + default app layout) |

## Consumption model

1. **Submodule** this repo at **`.calyx/core/`** in each project (pin **`v1.0.0`** or newer **deliberately** once you adopt capture).
2. **After every clone** (each machine): **`bash .calyx/core/tooling/calyx-setup-capture.sh`** from the project root—installs **git** + **Cursor** capture. Requires **`python3`** on `PATH` for chat logging.
3. **Optional org layer** (e.g. Scalefree): second submodule at **`.calyx/org/`** for non-sensitive agency-wide defaults—see `templates/dot-calyx-README.md` for the layout.
4. **Project-local** content always lives beside those mounts: `.calyx/reasoning/`, `.calyx/decisions/`, `.calyx/taxonomy/local-tags.yaml`.
5. Changes to **generic** behavior start in **calyx-core**; agency-only changes live in **org**; engagement-specific work stays in the **project** repo.

This repository includes **`.cursorrules`** so agents follow Calyx when working only in `calyx-core`.

## New app repo (Cursor + Calyx + layout)

Full detail: **[docs/new-project.md](docs/new-project.md)**.

From a clone of **calyx-core**, or with this repo on your `PATH`:

```bash
bash tooling/scaffold-cursor-app.sh /path/to/new-project --name "My App"
```

This creates **`.cursorrules`**, **`.calyx/`** (reasoning, decisions, taxonomy), **`AGENTS.md`** (norms for AI assistants + Calyx logging), **`VERSION`** (starts at `0.1`), **`docs/GIT.md`**, a starter **`.gitignore`**, **`git init`** on `main`, and **`git submodule add`** for `.calyx/core` (override URL with `CALYX_CORE_URL=...`). When the submodule is present, the scaffold runs **`calyx-setup-capture.sh`** so **v1 capture** is live. By default it also adds **`apps/web`**, **`apps/api`**, **`mcp/`**, **`packages/shared`**, **`infra/`**, and **`local/`** (gitignored) so web + API + MCP + DB/infra work has a home from day one. Use `--minimal` for Calyx-only, or `--no-submodule` / `--no-git` when bootstrapping offline—then run **`calyx-setup-capture.sh`** yourself after adding **`.calyx/core`**.

### Scale Free Strategy (SFS) — folder + GitHub in one shot

For **Scale Free Strategy** workspaces under **`~/Documents/CURSOR`** (override with `SFS_WORKSPACE_ROOT`), with an **SFS badge** in `README.md` / `AGENTS.md`, **initial commit**, and **private** GitHub repo + push via **`gh`**:

```bash
bash tooling/create-sfs-workspace.sh "Human Project Name" [repo-slug]
```

Requires **`gh auth login`** for automatic `gh repo create`. Use `--no-github` if you only want a local repo; `--public` for a public remote.

## GitHub and consumers

- **`calyx-core`** — generic Calyx bundle; submodule at **`.calyx/core/`** in every project.
- **Org repo** (e.g. **`calyx-scalefree-org`**) — optional second submodule at **`.calyx/org/`** for your studio’s shared, non-sensitive layer.
- **Project repos** — one repo per product or client; each has its own **local** `.calyx/reasoning/` and `.calyx/decisions/`.
- Tag releases on **calyx-core** (e.g. **`v1.0.0`**) so projects can pin a known-good bundle. Maintainer checklist: **[docs/releasing.md](docs/releasing.md)**.
