# `.calyx/` — project Calyx layer

This project uses **two** inherited layers plus **local** brain:

| Path | Submodule | Purpose |
|------|-----------|---------|
| `core/` | `https://github.com/cfolsensfs/calyx-core.git` | Generic Calyx product bundle (prompts, templates, master taxonomy) |
| `org/` | `https://github.com/cfolsensfs/calyx-scalefree-org.git` | Scalefree org DNA (non-sensitive); **replace URL** if repo name differs |
| `reasoning/` | — | This project’s thought streams (major work) |
| `decisions/` | — | This project’s ADRs |
| `taxonomy/local-tags.yaml` | — | Tags **only** for this project |

**Precedence:** project local → org → core (unless an ADR says otherwise).

## First-time clone

```bash
git clone --recurse-submodules <THIS-REPO-URL>.git
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

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
