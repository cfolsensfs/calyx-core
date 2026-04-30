# Calyx Core — Organizational Constitution (v0.1)

This document is the **Company DNA**: non-negotiable defaults for how reasoning is captured, challenged, and reused across projects.

## Principles

1. **Collective brain over individual fix** — A solution without a recorded *why* is technical debt for the organization.
2. **Assume good faith; assume bad outcomes** — Use adversarial review (10th Man) before commitment, not after failure.
3. **Tags are contracts** — Taxonomy terms link decisions, logs, and code; local tags extend but must not contradict core tags without an ADR.
4. **Silos are failures** — Cross-project dependencies must be visible (Broker) and knowledge must be distilled (Librarian).

## Mandatory artifacts (per project)

- **Reasoning log** — For every major task: thought stream under `.calyx/reasoning/`. Canonical shape: `calyx-core/templates/reasoning-log.md`.
- **ADR** — Ratified decisions under `.calyx/decisions/` when the choice affects future work or other teams. Canonical shape: `calyx-core/templates/adr.md`.

## Amendment

Amendments to this constitution live in `calyx-core` and propagate to project mirrors via your chosen sync mechanism (copy, submodule, or script). The file `calyx-core/manifest.yaml` lists paths intended for automated sync.

