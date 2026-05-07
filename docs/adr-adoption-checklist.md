# ADR adoption checklist

Use this checklist to make sure ADRs are not only written, but actually used in delivery flow.

## Outcome target

- `architecture_binding` work links to an ADR (or supersedes one).
- Reviewers can verify ADR relevance without hunting.
- Weekly governance surfaces drift before it becomes rework.

## At work start

- Ask: is there already an ADR for this scope?
- If yes, link it in the issue/PR plan before coding.
- If no and the change is likely binding, open an ADR draft path early.

## During implementation

- Keep ADR status clear: `proposed`, `ratified`, or `superseded`.
- For reversals, create a new ADR and link both directions (`Supersedes` / `Superseded by`).
- Avoid silent divergence from ratified ADRs; log rationale when diverging.

## In code review / PR

- Fill a Calyx compliance block:
  - change class,
  - reasoning log path,
  - ADR path (if required),
  - override tag only when necessary.
- Reviewer checks:
  - ADR path resolves in repo,
  - ADR scope matches touched boundaries,
  - supersession chain is explicit when applicable.

## In CI / policy

- Run feedback loop in `guided` first, then `guardrail`:

```bash
bash .calyx/core/tooling/calyx-feedback-loop.sh --mode guided
```

- Keep policy expectation: `architecture_binding` => reasoning + ADR.
- Treat override tags as exceptions with owners and expiry, not a default path.

## Weekly governance backflow

- In weekly sweep, inspect:
  - architecture-binding changes without ADR links,
  - ADRs contradicted by recent work,
  - open decision conflicts and unresolved questions.
- Use findings to create follow-up ADRs or supersessions, not ad hoc notes.

## Signals that ADRs are truly adopted

- High share of architecture-binding PRs include valid ADR links.
- New ADRs often supersede prior ADRs instead of editing history.
- Repeated "why did we do this?" questions decrease for major areas.
- Fewer rework incidents trace to missing decision context.

## Related

- [feedback-loop.md](feedback-loop.md)
- [eow-governance.md](eow-governance.md)
- [workflow.md](workflow.md)
