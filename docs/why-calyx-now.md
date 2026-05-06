# Why Calyx matters now

Calyx is an **organizational intelligence** layer for teams that already work **with AI**. It is not a replacement for your editor, your Git host, or a “second brain” app—it is a **small, strict convention** on top of **Git + Cursor (or similar) + capture hooks**, so the reasoning you already pay for **compounds** instead of disappearing when the chat tab closes.

For the **cultural / epistemic** framing (stewardship vs extraction, the “great library” in the Calyx sense), see **[philosophy.md](philosophy.md)**.

---

## The shift

Solo AI use optimizes **speed**. Studio and agency work optimizes **clarity, reuse, and alignment** across people, clients, and time. Those two goals diverge the moment **more than one human**—or **more than one engagement**—depends on the same decisions.

Most careful thinking today happens in **human–agent threads**: constraints, rejected options, prompts that worked, and failure modes that never made it into a PR title. **Commit messages and tickets rarely carry that load.** As AI multiplies how much of that thinking happens in-session, **the loss gets worse** unless something **captures** it on purpose.

Calyx’s bet is simple: **treat capture as load-bearing**, then **distill** into durable artifacts—reasoning logs, ADRs, shared vocabulary—**inside the repo** where obligation and confidentiality already live.

---

## What Calyx is (and is not)

**Calyx is:** a **bundle and constitution** (prompts, templates, taxonomy), **automation** (git post-commit inbox stubs, Cursor hooks to a **local, gitignored** chat trail), **verify** scripts so “did we actually install this?” is not a personality test, plus **optional rhythm tools**—a **weekly governance** runner, a **feedback loop** that maps change impact to reasoning/ADR expectations, and **scaffold** defaults (formatting, CI templates) so new repos start consistent.

**Calyx is not:** installable “Calyx software,” a vacuum for private chats, or a mandate to paste every transcript into Git. Wider sharing, when it happens, stays **opt-in and sanitized**—patterns and arguments, not raw exports.

If you delete the hooks and hope discipline alone will save you, you still have Git—but you **do not have Calyx**. The model assumes **raw signal** (stubs + short-lived local logs) before judgment (distill, ADR, delete noise).

---

## Why **now**

1. **Volume** — Agent-assisted work produces more **decision-shaped** text than traditional commits capture.
2. **Fragility** — Without a default path, **nobody** consistently promotes “why” into the record; **lazy defaults win**, and the org relearns the same lessons weekly.
3. **Falsifiable hygiene** — Lightweight **verify** and optional CI make “capture drift” visible before it silently rots every project.
4. **Client and studio boundaries** — One **repo per engagement** keeps **client reasoning (cpl)** separate while **studio DNA (col)** and **generic Calyx (ccl)** stay pinned and comparable across work.

---

## What you do differently day to day

- **After clone:** run `**calyx-setup-capture.sh`**; `**calyx-verify-capture.sh**` until green; **restart** the editor so hooks apply.
- **While working:** let machines capture **inbox stubs** and **local chat logs**; humans (or agents under supervision) **distill** what should survive into `**.calyx/reasoning/`** or **ADRs**.
- **Hands off the layout:** `**.calyx/core`**, `**.calyx/org**`, and the standard **cpl** folders are **load-bearing paths**—not a refactor target for a tidy model session. Structural change requires a **ratified ADR** and human agreement.

---

## Closing

Calyx does not promise magic. It promises **honesty**: if you won’t capture, you won’t compound. If you will—**Git, hooks, verify, distill**—you give your future self and your team something **better than memory and commit blurbs**: a **versioned trail of thinking** that survives the session that produced it.

---

## Related

- [philosophy.md](philosophy.md) — stewardship, not extraction; epistemic framing; GitHub header copy
- [README.md](../README.md) — bundle overview and consumption
- [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) — v1 principles (capture + structure)
- [first-run.md](first-run.md) — install and onboarding
- [glossary.md](glossary.md) — **ccl** / **col** / **cpl**

