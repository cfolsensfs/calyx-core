# calyx-core

**Company DNA** for the Calyx organizational intelligence layer: constitution, specialist prompts, master taxonomy, canonical templates, and minimal tooling. Implementation repos (e.g. `scalefree`) mirror or copy subsets into their `.calyx/` directory and add project-local reasoning, ADRs, and tags.

## Layout

| Path | Purpose |
|------|---------|
| `constitution/` | Non-negotiable principles and mandatory artifacts |
| `prompts/` | Specialist agent system prompts (10th Man, Librarian, Broker) |
| `taxonomy/` | Master tag vocabulary (`master-tags.yaml`) |
| `templates/` | **Canonical** reasoning log and ADR shapes—sync these into projects |
| `examples/` | Illustrative artifacts (not production data) |
| `tooling/` | Lean scripts (e.g. local Ollama runner) |
| `manifest.yaml` | Machine-readable index for sync automation |

## Consumption model

1. **Human or script** copies or symlinks `templates/`, `prompts/`, `taxonomy/`, and `constitution/` into each repo’s `.calyx/core/` (or equivalent), per your org’s sync policy.
2. **Project-local** content always lives beside that mirror: `.calyx/reasoning/`, `.calyx/decisions/`, `.calyx/taxonomy/local-tags.yaml`.
3. Changes to global behavior start here; project overrides are documented in local ADRs when they diverge from core.

This repository includes **`.cursorrules`** so agents follow Calyx when working only in `calyx-core`.

## GitHub and consumers

- Publish **`calyx-core`** as its own repository (company DNA only).
- Implementation repos (e.g. **scalefree**) stay **separate**; they pull this content via a **Git submodule** at `.calyx/core/` (see the scalefree repo’s `.calyx/README.md`).
- Tag releases here (e.g. `v0.2.0`) so projects can pin a known-good bundle from `manifest.yaml`.
