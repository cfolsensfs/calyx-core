# `.calyx/` — project Calyx layer

| Path | Purpose |
|------|---------|
| `core/` | **Git submodule** → **calyx-core** (constitution, prompts, master taxonomy, templates, tooling) |
| `reasoning/` | Thought-stream logs for major work (`_TEMPLATE.md`) |
| `decisions/` | Architecture decision records (`ADR-TEMPLATE.md`) |
| `taxonomy/` | `local-tags.yaml` (extends core master tags) |

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
