# New Calyx project — creation tooling (deliverable)

This repo ships **scripts and templates** so you can spin up a **new implementation repository** with Calyx already wired: `.calyx/` (local brain), `.cursorrules`, optional **calyx-core** submodule at `.calyx/core`, and a sensible default folder layout for web + API + MCP + infra.

## Deliverables (what you get from this repo)

| Artifact | Purpose |
|----------|---------|
| **`tooling/scaffold-cursor-app.sh`** | **Generic** new-project scaffold: Calyx files, `git init`, `git submodule add` for `.calyx/core`, default `apps/web`, `apps/api`, `mcp/`, etc. |
| **`tooling/create-sfs-workspace.sh`** | **Optional** orchestration for [Scale Free Strategy](https://github.com/cfolsensfs) style workspaces: same scaffold + SFS badge in README/AGENTS, `VERSION` 0.1, initial commit, **`gh repo create --push`**. |
| **`templates/app-scaffold/`** | Files copied by `scaffold-cursor-app.sh` (`.cursorrules`, `AGENTS.md`, `.gitignore`, `.calyx` stubs, README snippets, per-folder READMEs). |
| **`manifest.yaml`** | Machine-readable list of bundle paths (including scaffold templates). |

Everything else in **calyx-core** (constitution, prompts, taxonomy, canonical templates) is the **brain** you mount into projects—usually as **`.calyx/core`** via submodule.

---

## Prerequisites

- **Bash**, **Git**
- **Network** (first run) if you use **`git submodule add`** to clone calyx-core
- **GitHub CLI** (`gh`) + `gh auth login` only if you use **`create-sfs-workspace.sh`** without `--no-github`

---

## 1. Generic scaffold (any org)

From a clone of **calyx-core**:

```bash
bash tooling/scaffold-cursor-app.sh /path/to/new-project --name "My App"
```

### Common flags

| Flag | Meaning |
|------|---------|
| `--minimal` | Calyx + git files only (no `apps/web`, `apps/api`, …). |
| `--no-git` | Do not run `git init`. |
| `--no-submodule` | Do not add `.calyx/core` (offline); add later per project `docs/GIT.md`. |
| `--force` | Overwrite scaffold files if they already exist. |
| `--name "X"` | Human-readable project name (README, `AGENTS.md`). |

### Environment

| Variable | Meaning |
|----------|---------|
| `CALYX_CORE_URL` | Git URL for submodule (default: `https://github.com/cfolsensfs/calyx-core.git`). |
| `SFS_SCAFFOLD=1` | Set automatically by `create-sfs-workspace.sh`; adds SFS badge lines. You can set it manually if you want the badge without the SFS script. |

### After scaffold

```bash
cd /path/to/new-project
git submodule update --init --recursive
```

Open the **project root** in Cursor so `.cursorrules` applies repo-wide.

---

## 2. SFS one-shot (folder + commit + GitHub)

**Scale Free Strategy** convenience wrapper: default parent **`~/Documents/CURSOR`**, private repo under **`cfolsensfs`**, initial commit, push.

```bash
bash tooling/create-sfs-workspace.sh "Human Project Name" [repo-slug]
```

| Flag | Meaning |
|------|---------|
| `--public` | Public GitHub repo. |
| `--no-github` | Local only; prints `gh repo create` for later. |
| `--no-submodule` | Passed through to scaffold. |
| `--root /path` | Parent directory instead of `~/Documents/CURSOR`. |
| `--dry-run` | Print planned actions. |

| Variable | Meaning |
|----------|---------|
| `SFS_WORKSPACE_ROOT` | Default parent for new folders. |
| `GITHUB_OWNER` | Default `cfolsensfs`. |

---

## What the scaffold creates (default, non-minimal)

- **Root:** `.cursorrules`, `.gitignore`, `README.md`, `AGENTS.md`, `VERSION` (`0.1`), `docs/GIT.md`
- **`.calyx/`:** `README.md`, `reasoning/_TEMPLATE.md`, `decisions/ADR-TEMPLATE.md`, `taxonomy/local-tags.yaml`
- **`.calyx/core/`:** submodule checkout of calyx-core (unless `--no-submodule`)
- **Layout:** `apps/web`, `apps/api`, `mcp/`, `packages/shared`, `infra/`, gitignored `local/`

Use **`--minimal`** if you only want the Calyx layer and no opinionated app tree.

---

## Pinning and releases

Pin **calyx-core** in each project to a **commit or tag** you trust:

```bash
cd .calyx/core
git fetch origin
git checkout v0.x.y   # or a commit SHA
cd ../..
git add .calyx/core
git commit -m "Pin calyx-core"
```

Tag releases on this repo so consumers can reference **`manifest.yaml`** and a known-good version.
