# Organization vs projects (Calyx shape)

**Calyx models a studio or company (the org) and the work it delivers (projects).** How you arrange folders on disk is up to you; **how layers stack in Git** should follow this pattern.

## Layers (reminder)

| Layer | Abbrev. | Who it belongs to | Typical mount |
|--------|---------|-------------------|---------------|
| Core | **ccl** | Everyone (generic, forkable) | `.calyx/core/` → `calyx-core` |
| Org | **col** | **One organization**—shared norms, playbooks, non-sensitive studio DNA | `.calyx/org/` → org repo (optional) |
| Project | **cpl** | **One repo / one engagement**—reasoning, ADRs, tags for that product or client | `.calyx/reasoning/`, `decisions/`, `taxonomy/` |

**Precedence:** **cpl** → **col** → **ccl** (unless an ADR says otherwise).

## Org → projects (conceptual)

```text
                    ┌─────────────────────────────────────┐
                    │  Org (agency, studio, company)      │
                    │  col: shared across all projects    │
                    └─────────────────────────────────────┘
                                        │
          ┌───────────────┬─────────────┼─────────────┬───────────────┐
          ▼               ▼             ▼             ▼               ▼
     ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     ┌─────────┐
     │ Project │   │ Project │   │ Project │   │ Project │     │   …     │
     │ cpl     │   │ cpl     │   │ cpl     │   │ cpl     │     │         │
     └─────────┘   └─────────┘   └─────────┘   └─────────┘     └─────────┘
```

Each **project** repository:

1. Mounts the same **ccl** (usually public `calyx-core`, pinned to a commit/tag).
2. Mounts the same **col** for that org (if the org maintains one)—so studio defaults are consistent.
3. Maintains its own **cpl**—client names, engagement decisions, and local tags stay in **that** repo.

## Disk layout vs Calyx layout

- A **Cursor workspace** or monorepo folder may contain **many** git roots side by side; that is fine.
- **Calyx applies per Git repository root:** each repo that ships work should have its own **`.calyx/`** with **cpl** (and submodules for **ccl** / **col**).
- Do **not** assume one mega-folder on disk equals one Calyx “project”—follow **where `.git` lives**.

## Example (consultancy)

- **Org:** the agency brand (e.g. Scalefree).
- **Org repo (col):** non-sensitive playbooks, taxonomy extensions for the studio—submodule URL identical on every engagement repo.
- **Project repos:** one repo per client product or internal product; each has unique **cpl**.

## Related

- [glossary.md](glossary.md) — **ccl** / **col** / **cpl**
- [new-project.md](new-project.md) — scaffolding a new repo
