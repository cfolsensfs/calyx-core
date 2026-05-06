# Calyx impact telemetry (process + design)

Reference material for **proof-style metrics** (“did reasoning travel with the work?”) and rough **ROI narratives**. There is **no** dedicated telemetry runner in `calyx-core`; teams implement storage and rollups as they prefer (spreadsheet, scripts, BI, or future tooling). See also [experiments-and-future.md](experiments-and-future.md).

---

## Goals

- Make **observable** whether Calyx is doing its job: high-impact changes carry **reasoning** and, where appropriate, **ADRs**.
- Support **honest** reporting to leadership or partners (e.g. integrators) without pretending metrics are laboratory-precise.
- Stay **local-first**, **opt-in**, and aligned with **stewardship of reasoning** — not employee monitoring or transcript harvesting. See [philosophy.md](philosophy.md).

Non-goals for a first adoption pass:

- Perfect attribution of “time saved.”
- Always-on behavioral tracking (“median time to answer why” as a live KPI) unless you deliberately build a humane instrument for it.

---

## Recommended default cadence: release-boundary audits

Many teams get more trust and less gaming from **periodic audits** than from continuous dashboards.

**When:** Each **major or minor release** you care about (semver bump, milestone tag, or internal “ship week”).

**What you do:**

1. **Define the window** — e.g. Git tags `v2.3.0..v2.4.0`, or merge commits into `release/*` in a date range.
2. **List candidate changes** — merged PRs in that window (or commits touching high-signal paths from your [feedback-loop.md](feedback-loop.md) config).
3. **Classify** — reuse the same language as the feedback loop where possible: `trivial`, `feature_local`, `cross_cutting`, `architecture_binding`, `uncertain`.
4. **Score evidence** — for each non-trivial row:
   - **Reasoning:** link present, file exists at merge SHA, and passes a minimal quality bar (title, context, decision).
   - **ADR:** for `architecture_binding`, ADR present or explicit supersession chain.
5. **Publish one report** — percentages, gap list, links. Archive under `.calyx/reasoning/reports/` if you use Calyx paths.

This yields the headline ratios below **without** standing infrastructure.

---

## Optional: lighter continuous signal (if you already run CI checks)

If you run **`calyx-feedback-loop`** in CI, machine-readable outputs already exist:

- `.calyx/reasoning/reports/feedback/latest-feedback.json`
- Override log: `.calyx/reasoning/reports/feedback/overrides.jsonl`

You can **append** or **mirror** those results into your own JSONL or SQLite store **per run**. That is optional telemetry, not a second opinion: keep **one classification source** to avoid drift.

---

## Reference event model (if you implement storage)

Append-only events help audits and automation stay **explainable**. Treat this as a **schema sketch** (`schema_version` in every record).

| `event_type` | When |
|--------------|------|
| `change_evaluated` | A change (PR or commit range) received class + policy result |
| `evidence_linked` | A human or bot recorded links to reasoning / ADR |
| `policy_warned` | Feedback loop (or equivalent) warned in `guided` mode |
| `policy_failed` | Failed in `guardrail` mode |
| `policy_overridden` | Valid override recorded |
| `rework_incident_logged` | Someone filed a rework note with a root-cause tag |

**Optional / partner-specific** (not default Calyx):

| `event_type` | When |
|--------------|------|
| `why_query_opened` | Explicit start of a “why” investigation (e.g. labeled issue) |
| `why_query_answered` | Durable answer linked (paired by `why_id`) |

Suggested common fields (redact as needed):

- `schema_version`, `event_id`, `occurred_at`
- `repo`, `branch` or `ref`, `base_sha`, `head_sha`, optional `pr_number`
- `change_class`, `policy_mode`, `classifier_version`, `policy_config_hash`
- `required_evidence`, `evidence_present` (booleans or enums)
- `paths_touched` (truncated list)
- `issue_id` (external tracker), `actor` (optional hash / service account)
- `override_reason` where relevant

**Privacy:** Prefer **service accounts** and **hashed actors** for shared dashboards; never store raw chat or secrets.

---

## Metric definitions (explicit numerators / denominators)

Define **major** consistently — e.g. `cross_cutting` + `architecture_binding`, or your own release checklist.

| Metric | Formula | Notes |
|--------|---------|--------|
| `major_with_reasoning_pct` | `major_with_valid_reasoning / total_major` | “Valid” = link resolves + minimal structure; document your bar |
| `architecture_with_adr_pct` | `architecture_with_valid_adr / total_architecture` | Count superseded ADRs only if the chain is clear |
| `false_positive_rate` (use carefully) | `warnings_labeled_unnecessary / total_warnings` | Requires **honest labeling**; overrides are often expedience, not “model wrong” |
| `why_answer_median_minutes` | `median(answered_at - opened_at)` | Needs paired events; **skip** unless you implement a clear instrument |
| `rework_missing_context_count` | `count(rework_incidents where tag = missing_decision_context)` | Manual or semi-automated is fine |

Always report **denominators** and **missing data rate** (e.g. PRs with no linked issue).

---

## ROI estimator (optional, ranges not precision)

Configurable assumptions (examples):

- `minutes_saved_per_why_resolved_with_context`
- `minutes_rework_avoided_per_incident_prevented`
- `weekly_maintenance_overhead_minutes` (distillation, audits)
- `blended_hourly_rate_usd` (optional)

Compute:

- `gross_saved_minutes` — from assumptions × counted events
- `net_saved_minutes` — gross minus maintenance
- Optional `net_hours * rate` — present as **low / mid / high** scenarios

Label outputs as **estimates**, not accounting.

---

## Data quality and anti-gaming

- **Link validation ladder:** L0 string present → L1 path exists at SHA → L2 template fields satisfied.
- **Override patterns:** flag high override velocity, expired overrides never cleaned up, or empty “stub” reasoning files.
- **Version policy:** when `classifier_version` or dictionaries change, segment metrics or reset comparisons.
- **Confidence:** per period, report sample size and completeness; suppress charts when N is tiny.

---

## Rollout sketch

- **v0 (manual):** Release spreadsheet + links; no code.
- **v1 (local):** Script over Git range + parse `latest-feedback.json` + markdown report.
- **v2 (team):** Optional SQLite / shared store, tracker webhooks, stricter link checks.

---

## Validation plan

- **Golden cases:** Known PRs with expected class and evidence outcome.
- **Human audit:** Sample 10% of “compliant” rows; measure disagreement.
- **Stability:** Classifier dictionary changes should bump version and be visible in reports.

---

## Related

- [feedback-loop.md](feedback-loop.md)
- [eow-governance.md](eow-governance.md)
- [experiments-and-future.md](experiments-and-future.md)
