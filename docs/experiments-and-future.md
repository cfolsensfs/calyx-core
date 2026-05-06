# Experiments and future directions

The **maintained baseline** is whatever ships in `manifest.yaml` and the tagged releases: constitution, capture, prompts, and bundled tooling.

This page collects **design directions** that are **not** fully implemented as first-class tooling—optional processes, sketches, and notes you can adopt, adapt, or ignore. Publishing them records the reasoning *“we considered X and chose not to ship it yet”* so the same tradeoffs do not get relitigated in silence. Nothing here implies surveillance or mandatory telemetry ([philosophy.md](philosophy.md)).

**Ratified scope (governance vs metrics):** [ADR-0001 — Governance + feedback; deferred continuous metrics](decisions/ADR-0001-governance-feedback-and-deferred-telemetry.md).

## Status legend

Use one status per row so reviews do not re-open closed calls every quarter.

| Status | Meaning |
|--------|---------|
| **Not started** | No reference doc or only a mention; may never ship. |
| **Parked** | Written up (often under `docs/`); deliberately **not** in `tooling/` until we revisit demand, ethics, or integration shape. |
| **Won’t do (default)** | Not planned as **core bundle** behavior unless a future ADR reverses this; forks or partners may still build locally. |

One-line reason stays in the **Reason** column below.

## Scope recap

| Area | In this bundle today | Not in this bundle (by design for now) |
|------|----------------------|----------------------------------------|
| **Governance & enforcement** | Thin **EOW** runner (intake, hygiene, conflicts, **10th Man** trigger / no-trigger, reports). **Feedback loop** (classify → policy → remediation; `learn` / `guided` / `guardrail`). | — |
| **Metrics & ROI plumbing** | **Reference only:** [impact-telemetry.md](impact-telemetry.md) (release-boundary audits, optional mirroring of feedback outputs). | **Continuous** impact/scoring pipeline (dedicated event sink, rollup jobs, standing dashboards). Live **“why latency”** KPIs as a default product surface. |

## Index

| Topic | Status | Reason |
|-------|--------|--------|
| **Impact telemetry & ROI-style metrics** (bundled runner, rollups, dashboards) | **Parked** | Process and schema sketched in [impact-telemetry.md](impact-telemetry.md); ship as scripts/BI per org until a future ADR promotes tooling. |
| **Continuous “why latency”** (paired open/answer events as a headline metric) | **Won’t do (default)** | High ceremony and easy to misread as surveillance; partner- or org-specific instrumentation only if explicitly chosen. Details: [impact-telemetry.md](impact-telemetry.md) (optional metrics). |

[CHANGELOG.md](../CHANGELOG.md) and **`manifest.yaml`** record versioned releases. Items listed here are **not** part of the pin contract until they are added to the manifest.

## Related

- [ADR-0001](decisions/ADR-0001-governance-feedback-and-deferred-telemetry.md)
- [feedback-loop.md](feedback-loop.md)
- [eow-governance.md](eow-governance.md)
- [workflow.md](workflow.md)
