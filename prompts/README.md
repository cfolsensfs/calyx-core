# Specialist prompts

Plain-text system prompts for use with any LLM runtime (cloud or local, e.g. `tooling/ollama-run.sh`).

| File | Role | When to use |
|------|------|-------------|
| `10th-man.txt` | Adversarial review, pre-mortem, kill criteria | Before committing to a risky architecture, rollout, or irreversible choice |
| `librarian.txt` | Distill messy notes/transcripts into tagged, durable summaries | After a session or task; before archiving or sharing widely |
| `broker.txt` | Cross-task overlap, dependency hypotheses, silo warnings | When starting work that might touch shared systems, teams, or prior decisions |
| `import-distill-onepager.txt` | **Paste-ready** distill of Slack/email exports → reasoning log + optional ADR; maps **participants** and **decision authority** tiers | Bootstrapping `.calyx/` from a file dump; pair with `templates/distill-external-to-calyx.md` for the long form |

Feed each prompt as the system or leading instruction block, then attach the **task-specific context** (and for Librarian, the taxonomy YAMLs). For **import distillation**, attach the export and any redaction rules.
