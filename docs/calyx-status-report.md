# Calyx status report (v1)

The status report is a **tangible, repo-local** summary so teams can see that Calyx is **installed**, **capturing**, and **accumulating decision memory**—without scoring individuals.

## Run

From the **project Git root** (the folder that contains `.calyx/`):

```bash
bash .calyx/core/tooling/calyx-status-report.sh
```

Options:

```bash
bash .calyx/core/tooling/calyx-status-report.sh --chat-window-days 14
```

## Outputs (committed or not — your choice)

- **Markdown:** `.calyx/reasoning/reports/status/latest-status.md`
- **JSON:** `.calyx/reasoning/reports/status/latest-status.json`

Re-run any time; outputs are overwritten (idempotent).

## What it shows

1. **Presence / wiring** — calyx-core manifest, git post-commit hook referencing Calyx, optional Cursor hooks, `AGENT_ROLES.md`.
2. **Capture pulse** — inbox stub count and age band; recent `local/chat-log/` files (default last 7 days).
3. **Decision memory** — counts of distilled reasoning logs and ADRs; optional Git recency for `.calyx/reasoning/` and `.calyx/decisions/` when this directory is a Git repo.
4. **Automation** — latest EOW report folder (if any); latest feedback-loop JSON summary (if present).
5. **Org lift** — whether `.calyx/org/` (col) exists and has files; pointers to `promote-cpl-to-col.txt` and `org-lift-cadence.txt`.
6. **Suggested next actions** — short, deterministic hints (install hook, distill inbox, run EOW, etc.).

## What it does not do

No contributor rankings, velocity scores, or “who produced more.” See [philosophy.md](philosophy.md#status-surfaces-and-metrics).

## Related

- [automation.md](automation.md) — capture, EOW, feedback loop
- [workflow.md](workflow.md) — rhythm
- [eow-governance.md](eow-governance.md) — weekly governance outputs
