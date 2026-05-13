
Calyx is a **cultural and epistemic** frame: why organizational reasoning belongs in the repo, and what stewardship means as distinct from extraction or transcript hoarding. [why-calyx-now.md](why-calyx-now.md) is the companion on urgency and boundaries; [README.md](../README.md) and [first-run.md](first-run.md) cover installation and day-one mechanics.

---

## In one sentence

> Calyx core — Git-native bundle for **organizational reasoning**: constitution, prompts, taxonomy, **capture hooks** (Git + Cursor), **weekly governance**, **change-to-evidence feedback loop**, and **agent workflows** (org lift, taxonomy). **Stewardship of thinking**, not transcript mining or data extraction. A **convention + bundle** for teams who work **with AI** and want reasoning to **compound** inside the repo.

---

## What this repository is *not*

It is **not** a warehouse of other people’s **private** sessions. It is **not** an attempt to “own the noûs” or to treat every model reply as fuel for a centralized corpus. The ethical shape is **stewardship of reasoning**, **not extraction** of chat data.

---

## Status surfaces and metrics

Calyx may emit **repo- and artifact-level** signals (for example the [status report](calyx-status-report.md): hooks wired, inbox depth, distilled logs/ADRs, latest EOW/feedback outputs, org lift readiness). Those surfaces answer “is the discipline working?” and “is there memory we can lean on?”—tied to **paths and commits**, not résumés.

**Calyx does not score, rank, or compare individuals.** Short-term log counts cannot fairly represent foundational work or long-horizon impact; comparative “productivity” or “Calyx value” dashboards for people are **out of scope** by design. Anything that looks like a metric should be **explainable from Git artifacts** and safe to show on a projector without embarrassing anyone.

---

## The shift (why this exists)

For most of history, a large share of **careful thinking** lived in **conversations that left no durable trace**—office debates, hallway synthesis, the “why we didn’t do X” that never became a memo. That thinking **dissipated as heat**.

**AI-assisted work amplifies** that kind of thinking: more iterations, faster exploration, richer threads. That makes the **loss function worse** if **nothing** is captured—but it also makes **faithful capture more feasible** when a team **chooses** to externalize what matters.

So the “great library” in the Calyx sense is **aggregate human capability**: not a vault of raw transcripts, but the **slow accretion** of better arguments, clearer tradeoffs, and reusable patterns—**first** inside the **project and org**, where **obligation and confidentiality** already live, and **only where appropriate** as **opt-in, sanitized** contribution to wider discourse.

---

## What Calyx does in practice

Calyx is the **discipline and the file formats** that let teams **deposit what deserves to survive**—**for themselves first**, and for the commons **only when** that is coherent with **trust**.

Concretely, this repo ships **templates, prompts, taxonomy, and small scripts** so teams can:

- Keep **reasoning logs** and **ADRs** next to code, under **`.calyx/`**, with clear **ccl / col / cpl** layers.
- Use **automated raw signal** (inbox stubs, short-lived local chat logs) as **input** to human or Librarian-style **distill**—not as the system of record by themselves.
- Run a **thin weekly governance** pass (intake, hygiene, consistency hints, optional 10th Man trigger) when you want the “brain” to stay legible without a heavy process.
- Apply a **knowledge feedback loop** so higher-impact code changes **meet** (or **warn toward**) Calyx evidence in **`learn` / `guided` / `guardrail`** modes—still your policy, not a cloud service.
- Use **agent prompts and indexes** for **org lift** (reusable patterns from **cpl** to **col**) and **taxonomy** hygiene, when you choose to invest in cross-project alignment.

The goal is to **reduce how much good thinking dissipates**, not to maximize how much text you store.

---

**We help organizations keep the thinking they’re already paying for**—instead of treating every model reply as disposable UI noise. Calyx makes that **explicit, versioned, and reviewable** in Git, without pretending that a chat tab is a knowledge base.

---

## Related

- [why-calyx-now.md](why-calyx-now.md)
- [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md)
- [README.md](../README.md)
- [calyx-status-report.md](calyx-status-report.md) — concrete artifact-level status surface (v1)
