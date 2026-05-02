# `.calyx/` — Calyx project layer (**cpl**)

Layer shorthand: **ccl** = core submodule (`.calyx/core/`), **col** = optional org submodule (`.calyx/org/`), **cpl** = project-local folders below + taxonomy. See **calyx-core** `docs/glossary.md` when the submodule is present.

| Path | Purpose |
|------|---------|
| `core/` | **ccl** — **Git submodule** → **calyx-core** (constitution, prompts, master taxonomy, templates, tooling) |
| `org/` | **col** (optional) — org-wide non-sensitive defaults; second submodule when your studio uses it |
| `reasoning/` | **cpl** — thought-stream logs for major work (`_TEMPLATE.md`) |
| `decisions/` | **cpl** — architecture decision records (`ADR-TEMPLATE.md`) |
| `taxonomy/` | **cpl** — `local-tags.yaml` (extends core master tags) |
| `AGENT_ROLES.md` | **cpl** — index of agent prompts (capture → distill, taxonomy sync, **org lift**); refresh via **`calyx-install-agent-roles.sh`** |

## Clone with submodules

```bash
git clone --recurse-submodules <THIS-REPO-URL>.git
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Bump the pinned core

```bash
cd .calyx/core && git fetch origin && git checkout main && git pull && cd ../..
git add .calyx/core
git commit -m "Bump calyx-core pin"
git push
```

Canonical templates (after submodule init): `.calyx/core/templates/reasoning-log.md` and `.calyx/core/templates/adr.md`.
