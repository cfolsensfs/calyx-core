# ADR-0001: Governance + feedback scope; deferred continuous metrics

- **Status:** Accepted
- **Date:** 2026-05-07

## Context

Calyx gained **thin end-of-week (EOW) governance** (intake, hygiene, consistency, explicit 10th Man trigger / no-trigger) and a **knowledge feedback loop** (change classification, evidence policy, remediation, optional CI). Separately, we explored **impact telemetry** and continuous **“why latency”**-style metrics for ROI narratives and partner conversations.

## Decision (in scope for this repo)

The **calyx-core** bundle ships **runnable** tooling and docs for:

- **EOW governance** — `calyx-eow-governance.sh` / `.py`, config template, weekly report shape, 10th Man trigger rules as **report-first** automation.
- **Knowledge feedback loop** — `calyx-feedback-loop.sh` / `.py`, policy config, modes `learn` / `guided` / `guardrail`, scaffold hooks/CI templates.
- **Capture, org lift, taxonomy** — existing prompts, agent role install, and related docs (see [CHANGELOG.md](../../CHANGELOG.md)).

## Deferred

**Continuous impact / scoring metrics pipeline** (append-only event store, aggregation jobs, automated weekly ROI dashboards, always-on behavioral KPIs) is **not** implemented as first-class `tooling/` in this repo **by design for now**.

- **Index and status legend:** [experiments-and-future.md](../experiments-and-future.md) (updated **2026-05-07**).
- **Reference process + schema sketches:** [impact-telemetry.md](../impact-telemetry.md).

Rationale in brief: prefer **release-boundary audits** and **optional** mirroring of feedback-loop outputs over a bundled telemetry product until requirements and trust boundaries stabilize—avoids relitigating “why isn’t this in the product?” without a paper trail.

## Consequences

- Forks and integrators (e.g. issue trackers) can trace **shipped** vs **parked** work from this ADR and the experiments index.
- Promoting telemetry into `manifest.yaml` / `tooling/` should **supersede** this ADR with a new ADR rather than silent scope creep.
