# Cursor-first Calyx showcase

This is a shareable architecture + operations brief for teams evaluating Calyx in a **Cursor-first** workflow.

## Positioning

Calyx fits best where high-value reasoning is created: **inside AI-assisted development sessions**. In practice, that means Cursor is the primary integration surface; ticket systems are downstream distribution surfaces.

**One-line framing:** Calyx keeps the "why" produced in agent-assisted work as durable, reviewable artifacts in Git.

## Why Cursor-first

- **Point of cognition:** constraints, tradeoffs, and rejected options are generated in coding sessions, not only in ticket comments.
- **In-flow capture:** hook and policy nudges are strongest while work is in motion.
- **Lower loss:** post-commit stubs + local chat-log inputs reduce decision loss before distillation.
- **Policy proximity:** ADR and reasoning requirements can be checked near code changes.

## Integration touchpoints (today)

1. **Capture plumbing**  
   - `bash .calyx/core/tooling/calyx-setup-capture.sh`  
   - Git post-commit stubs -> `.calyx/reasoning/inbox/`  
   - Cursor hook sink -> `local/chat-log/`

2. **Verification**  
   - `bash .calyx/core/tooling/calyx-verify-capture.sh`

3. **Decision enforcement loop**  
   - `bash .calyx/core/tooling/calyx-feedback-loop.sh --mode guided`  
   - `architecture_binding` => reasoning + ADR

4. **Weekly governance**  
   - `bash .calyx/core/tooling/calyx-eow-governance.sh`  
   - report-first: conflicts, trigger/no-trigger, next actions

5. **Specialist prompts**  
   - `.calyx/core/prompts/10th-man.txt`  
   - `.calyx/core/prompts/librarian.txt`  
   - `.calyx/core/prompts/broker.txt`

6. **Model routing (scaffold default)**  
   - `agents/MODEL-ROUTING.md` + `.cursor/rules/model-routing.mdc` (`alwaysApply`)  
   - Task-first model choice; optional **Agent context** on reasoning logs / ADRs when distilling

## Model routing (demo beat)

Same task, wrong vs right model:

- **Wrong:** fastest model drafts client-facing compliance copy → tone/claim risk, rework.
- **Right:** classify → prose-tier model → optional Opus if stakes are high → distill with **Agent context** into `.calyx/reasoning/`.

Calyx does not switch models programmatically; routing is discipline + recording, not enforcement.

## Three workflow examples

### 1) Architecture change with guardrails

- Engineer proposes auth boundary change.
- Feedback loop classifies `architecture_binding`.
- PR must link reasoning + ADR (or explicit override with owner/expiry).
- Reviewer confirms supersession chain if prior ADR exists.

**Outcome:** decisions are ratified and traceable, not buried in chat.

### 2) Weekly anti-drift maintenance

- Team runs EOW governance.
- Output flags unresolved decision conflicts and stale questions.
- Trigger status records whether 10th Man review is warranted.

**Outcome:** less silent divergence and lower rework from missing context.

### 3) Org learning without transcript dumping

- Project distills reusable patterns from reasoning/ADRs.
- Org lift proposal is sanitized before moving from project layer to org layer.

**Outcome:** cross-project learning compounds without extracting raw client/session data.

## What this is not

- Not transcript mining.
- Not employee surveillance.
- Not a replacement for issue tracking.

Calyx is stewardship of reasoning: capture -> distill -> apply -> enforce.

## Partner integration boundary (e.g. issue trackers)

- **Cursor/Calyx core owns:** capture, distill, policy, ADR/knowledge hygiene.
- **Tracker integrations own:** distribution of distilled outputs (decision summaries, links, status), not raw cognition streams.

## Suggested demo path (15 minutes)

1. Show a code change classified by feedback loop.
2. Show required reasoning/ADR linkage in PR template.
3. Show EOW report with conflict + trigger decision.
4. Show one ADR supersession chain.

## Related

- [why-calyx-now.md](why-calyx-now.md)
- [workflow.md](workflow.md)
- [feedback-loop.md](feedback-loop.md)
- [eow-governance.md](eow-governance.md)
- [adr-adoption-checklist.md](adr-adoption-checklist.md)
