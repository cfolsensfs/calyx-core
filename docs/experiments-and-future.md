# Experiments and future directions

The **maintained baseline** is whatever ships in `manifest.yaml` and the tagged releases: constitution, capture, prompts, and bundled tooling.

This page collects **design directions** that are **not** fully implemented as first-class tooling—optional processes, sketches, and notes you can adopt, adapt, or ignore. Publishing them records the reasoning *“we considered X and chose not to ship it yet”* so the same tradeoffs do not get relitigated in silence. Nothing here implies surveillance or mandatory telemetry ([philosophy.md](philosophy.md)).

## Index

| Topic | Status in bundle | Doc / notes |
|-------|------------------|-------------|
| **Impact telemetry & ROI-style metrics** | **Design / process only** — no dedicated runner in `tooling/` yet | [impact-telemetry.md](impact-telemetry.md) — event sketches, formulas, **release-boundary audits** as the default cadence, optional continuous hooks |
| **Continuous “why latency” (paired open/answer events)** | **Not recommended as a default** — high ceremony; partner-specific (e.g. issue trackers) if ever adopted | Discussed inside [impact-telemetry.md](impact-telemetry.md) § Optional metrics |

[CHANGELOG.md](../CHANGELOG.md) and **`manifest.yaml`** record versioned releases. Items listed here are **not** part of the pin contract until they are added to the manifest.

## Related

- [feedback-loop.md](feedback-loop.md)
- [eow-governance.md](eow-governance.md)
- [workflow.md](workflow.md)
