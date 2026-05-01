# `.calyx/` — Calyx layers (**ccl**, **col**, **cpl**)

Shorthand: **ccl** = core submodule, **col** = org submodule, **cpl** = project-local reasoning/ADRs/tags. See **calyx-core** `docs/glossary.md`.

This project uses **ccl** + **col** (optional) + **cpl**:

| Path | Submodule | Purpose |
|------|-----------|---------|
| `core/` | `https://github.com/cfolsensfs/calyx-core.git` | **ccl** — generic bundle (prompts, templates, master taxonomy) |
| `org/` | `https://github.com/cfolsensfs/calyx-scalefree-org.git` | **col** — org DNA (non-sensitive); **replace URL** if repo name differs |
| `reasoning/` | — | **cpl** — thought streams (major work) |
| `decisions/` | — | **cpl** — ADRs |
| `taxonomy/local-tags.yaml` | — | **cpl** — tags for this project only |

**Precedence:** **cpl** → **col** → **ccl** (unless an ADR says otherwise).

## First-time clone

```bash
git clone --recurse-submodules <THIS-REPO-URL>.git
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Calyx v1 — capture (required)

After **`core/`** is populated, **once per clone** (each machine), from the **project root**:

```bash
bash .calyx/core/tooling/calyx-setup-capture.sh
```

Installs **git** post-commit stubs → **`reasoning/inbox/`** and **Cursor** hooks → **`local/chat-log/`** (gitignored). Requires **`python3`** on your `PATH`. Then run **`bash .calyx/core/tooling/calyx-verify-capture.sh`** until all checks pass. Details: `core/docs/automation.md`, `core/docs/first-run.md`, `core/docs/cursor-local-chat-log.md`, `core/constitution/CONSTITUTION.md`.

## Bump inherited layers

```bash
# calyx-core
cd .calyx/core && git fetch origin && git checkout main && git pull && cd ../..

# Scalefree org
cd .calyx/org && git fetch origin && git checkout main && git pull && cd ../..

git add .calyx/core .calyx/org
git commit -m "Bump calyx-core and/or org Calyx pins"
git push
```

## Templates

- Reasoning: `core/templates/reasoning-log.md` (copy into `reasoning/`).
- ADR: `core/templates/adr.md` (copy into `decisions/`).
- **End-of-day ritual:** `core/templates/calyx-closeout.md` — **Calyx checkpoint** (stage brain, commit, push; optional submodule bump).

## Calyx checkpoint (quick)

From project root, after submodule is present:

```bash
bash .calyx/core/tooling/calyx-closeout.sh
```

Then complete commit + push (see `core/templates/calyx-closeout.md` for full checklist).
