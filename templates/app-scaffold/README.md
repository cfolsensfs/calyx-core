# __PROJECT_NAME__

__WORKSPACE_BADGE__

**Version:** see the `VERSION` file in the repo root (starts at **0.1** for new workspaces).

**AI assistants:** start with **`AGENTS.md`** — Calyx reasoning, ADRs, and session wrap-up norms.

Web frontend + API + AI/MCP + data layer. Default layout from **calyx-core** `scaffold-cursor-app.sh`.

## Layout

| Path | Role |
|------|------|
| `apps/web` | Browser UI |
| `apps/api` | HTTP API (auth, business logic, integrations) |
| `mcp/` | MCP servers or tool adapters the app or agents call |
| `packages/shared` | Shared types, constants, validators (optional) |
| `infra/` | Docker Compose, migration home, deployment notes |
| `local/` | **Not in git** — secrets, scratch, large dumps |
| `.calyx/` | Reasoning logs, ADRs, taxonomy; **`core/`** = calyx-core submodule |

Rename folders if you prefer; if layout changes materially, add a short ADR in `.calyx/decisions/`.

## Calyx

- Cursor rules: `.cursorrules`
- Submodule: `.calyx/core` → [calyx-core](https://github.com/cfolsensfs/calyx-core)
- Git workflow: `docs/GIT.md`

## First run after scaffold

```bash
git submodule update --init --recursive
```

Then implement `apps/web`, `apps/api`, and wire `mcp/` and `infra/` to your chosen frameworks.
