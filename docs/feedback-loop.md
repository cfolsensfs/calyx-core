# Calyx Knowledge Feedback Loop

Turn Calyx into active delivery support:

`capture -> distill -> apply -> enforce`

## Entry point

From project root:

```bash
bash .calyx/core/tooling/calyx-feedback-loop.sh
```

Modes:

- `learn` (suggestions only)
- `guided` (warnings + remediation)
- `guardrail` (fail only for missing required evidence on high-impact classes)

Example:

```bash
bash .calyx/core/tooling/calyx-feedback-loop.sh --mode guided
```

## Classification classes

- `trivial`
- `feature_local`
- `cross_cutting`
- `architecture_binding`
- `uncertain`

The runner emits class, confidence, rationale, and boundaries touched.

## Evidence policy

- `trivial`: none
- `feature_local`: reasoning recommended
- `cross_cutting`: reasoning required
- `architecture_binding`: reasoning + ADR required
- `uncertain`: warn, ask human to classify

## Overrides

Use explicit override tag text:

`[calyx-override:<reason>|owner:<name>|expires:<YYYY-MM-DD>]`

Pass via `--override-text` in CI or hook integrations. Valid overrides are logged to:

`.calyx/reasoning/reports/feedback/overrides.jsonl`

## Outputs

- JSON: `.calyx/reasoning/reports/feedback/latest-feedback.json`
- Markdown: `.calyx/reasoning/reports/feedback/latest-feedback.md`

Both include remediation guidance (class, missing artifacts, paths, snippet, commands).

## Config

Copy and tune:

`templates/feedback-config.json` -> `.calyx/feedback-config.json`

Tune thresholds, requirements, mode, and override rules per repo.

## Rollout

1. `learn` for 1-2 weeks
2. `guided` for 2-4 weeks
3. `guardrail` once false positives are acceptable

## Related

- [ADR-0001 — Governance + feedback; deferred continuous metrics](decisions/ADR-0001-governance-feedback-and-deferred-telemetry.md)
- [adr-adoption-checklist.md](adr-adoption-checklist.md)
- [experiments-and-future.md](experiments-and-future.md) (status legend, scope recap)
- [impact-telemetry.md](impact-telemetry.md) (reference: release-boundary audits, optional mirroring of feedback outputs)
