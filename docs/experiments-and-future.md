# Experiments and future directions

If you **fork** or **submodule** this repo: thank you. The tagged bundle is the **maintained baseline**—constitution, capture, prompts, and the scripts that ship in `manifest.yaml`.

This page is different. It collects **directions we have thought through** (and sometimes sketched in design docs) that are **not** fully implemented as first-class tooling in the bundle. Treat everything here as **optional**: adopt the **process** in your own repo, adapt it, or ignore it.

**Why publish half-built ideas?** Calyx is about **organizational reasoning**. A fair share of that reasoning is *“we considered X and chose not to ship it yet.”* Writing it down helps forks avoid rediscovering the same dead ends—and gives maintainers a place to point when someone asks *“did you think about…?”*

## How to use this page

- **Maintainers:** When a design discussion stabilizes into something worth sharing but not worth automating yet, add a row below and link a doc under `docs/`.
- **Forks:** Prefer **copying patterns** into your org’s process over expecting upstream to ship code immediately.
- **Ethics:** Nothing here implies surveillance or mandatory telemetry. See [philosophy.md](philosophy.md).

## Index (ideas and design docs)

| Topic | Status in bundle | Doc / notes |
|-------|------------------|-------------|
| **Impact telemetry & ROI-style metrics** | **Design / process only** — no dedicated runner in `tooling/` yet | [impact-telemetry.md](impact-telemetry.md) — event sketches, formulas, **release-boundary audits** as the default cadence, optional continuous hooks |
| **Continuous “why latency” (paired open/answer events)** | **Not recommended as a default** — high ceremony; partner-specific (e.g. issue trackers) if ever adopted | Discussed inside [impact-telemetry.md](impact-telemetry.md) § Optional metrics |
| *Add rows as new design docs appear* | | |

## Relationship to the changelog

Shipped, versioned work lives in [CHANGELOG.md](../CHANGELOG.md) and **`manifest.yaml`**. This page is intentionally **outside** the “what you get when you pin a tag” contract unless we later promote an item into the manifest.

## Related

- [feedback-loop.md](feedback-loop.md) — enforced / guided evidence today (closest upstream to telemetry)
- [eow-governance.md](eow-governance.md) — weekly hygiene without productizing every metric
- [workflow.md](workflow.md) — day-to-day rhythm
