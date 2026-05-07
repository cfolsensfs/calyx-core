# Thin EOW Calyx governance (report-first)

This is the weekly (or cadence-adjusted) governance routine for keeping Calyx high-signal with low ceremony.

## Goal

In one command, produce:

- intake manifest,
- distillation status updates,
- hygiene findings,
- consistency/conflict findings,
- 10th Man trigger decision,
- weekly markdown report.

Target: **15-30 minutes** of human review per week in normal operation.

## Entry point

Run from a project repo root (the directory that contains `.calyx/`):

```bash
bash .calyx/core/tooling/calyx-eow-governance.sh
```

Optional flags:

```bash
# fail on trigger/high-severity findings
bash .calyx/core/tooling/calyx-eow-governance.sh --strict

# override one classification with rationale
bash .calyx/core/tooling/calyx-eow-governance.sh \
  --override "inbox_stub:abc123=discarded:duplicate of ratified ADR"
```

## Config

Copy this template into your project if you want custom thresholds:

- `.calyx/core/templates/eow-config.json` -> `.calyx/eow-config.json`

Supported keys:

- `window_days`
- `open_question_days`
- `critical_confidence_threshold`
- `severity_weights`
- `trigger_rules`

## Outputs

Under `.calyx/reasoning/reports/eow/<YYYY-Www>/`:

- `intake-manifest.json`
- `distill-status.json`
- `hygiene-findings.json`
- `conflicts.json`
- `trigger-decision.json`
- `eow-report.md`

Persistent status model:

- `.calyx/reasoning/eow-status.json` (idempotent ledger)
- `.calyx/reasoning/reports/eow-overrides.jsonl` (manual override rationale log)

## Trigger policy

10th Man is triggered only when configured conditions match, such as:

- high-severity decision conflict,
- security/privacy/regulatory contradiction,
- architecture divergence without supersede path,
- repeated rework indicators,
- critical confidence below threshold.

If no condition matches, the runner records explicit **no-trigger** rationale.

## Notes

- Report-first by default; strict mode is optional.
- Classification is heuristic and explainable; human ratification still decides major governance outcomes.
- This workflow does **not** auto-merge or rewrite historical artifacts.

## Deferred (continuous metrics)

Bundled **EOW** and **feedback-loop** outputs can feed **manual** or **org-local** metrics; a **continuous impact/scoring pipeline** in `tooling/` is **out of scope for now**. Traceability: [ADR-0001](decisions/ADR-0001-governance-feedback-and-deferred-telemetry.md) (**2026-05-07**), [experiments-and-future.md](experiments-and-future.md), [impact-telemetry.md](impact-telemetry.md), [adr-adoption-checklist.md](adr-adoption-checklist.md).
