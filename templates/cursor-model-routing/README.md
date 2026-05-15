# Cursor model routing templates (calyx-core)

Portable kit for **task-first model choice** in Cursor. Ships with **`scaffold-cursor-app.sh`** by default; opt out with **`--no-model-routing`**.

## Files

| Template | Install target |
|----------|----------------|
| `MODEL-ROUTING.md` | `agents/MODEL-ROUTING.md` |
| `model-routing.mdc` | `.cursor/rules/model-routing.mdc` |

## Capability tiers vs product names

- **`.mdc` (always applied):** literal Cursor model names — what people pick in Settings.
- **`MODEL-ROUTING.md`:** full table + **capability tiers** so teams can remap when Cursor renames models.

Edit the model table when your org drops or adds models; keep tiers stable for Calyx **Agent context** fields in reasoning logs.

## Without Calyx

Copy the two files manually; no submodule required. Routing is useful in any multi-model Cursor workspace.

## Related

- `docs/first-run.md` — enable models in Cursor Settings
- `docs/cursor-first-showcase.md` — demo subsection
- `templates/reasoning-log.md` — optional **Agent context** (model metadata)
