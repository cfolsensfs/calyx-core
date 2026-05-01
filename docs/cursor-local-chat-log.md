# Local Cursor chat log (workspace, retained)

**Calyx v1** expects this path: human–agent turns are **not** preserved in Git history or in typical commit messages. Cursor does **not** (today) dump full chat into your repo by default, so we use hooks.

**Baseline (install via `tooling/calyx-setup-capture.sh` or scaffold):**

1. **Cursor Hooks** — `beforeSubmitPrompt` + `afterAgentResponse` (+ optional `stop`) fire once per turn with JSON on stdin.
2. **A small script** — append to **`local/chat-log/YYYY-MM-DD.md`** under the **first** `workspace_roots` entry.
3. **Retention** — delete `local/chat-log/*.md` older than **3 days** (override with `CALYX_CHAT_LOG_RETENTION_DAYS`).

This is **not** a substitute for Calyx reasoning logs; it is **raw session material** for distill or debugging. Keep **`local/`** gitignored (default in Calyx scaffolds).

## Limitations (honest)

- **Multi-root workspaces:** the template logs only to **`workspace_roots[0]`**. Put your primary repo first, or copy the hook and adjust the script.
- **Payload fields** can vary by Cursor version; the script reads common keys defensively. If a release changes shape, check the **Hooks** output channel and adjust `log_chat_turn.py`.
- **Windows:** some users report UTF-8 issues in hook stdin; if you hit corruption, log base64 or open a Cursor forum thread—this is upstream.
- **Full history:** hooks see **turns while enabled**, not retroactive history before install.

## Install (scaffold)

**`tooling/scaffold-cursor-app.sh`** copies **`templates/cursor-hooks/`** into **`.cursor/hooks/`** and adds **`.cursor/hooks.json`** when that file is not already present (or when **`--force`** overwrites). New projects get logging without a manual step.

## Install (per project, existing repo)

From the **calyx-core** submodule in your repo:

```bash
mkdir -p .cursor/hooks
cp .calyx/core/templates/cursor-hooks/log_chat_turn.py .cursor/hooks/
cp .calyx/core/templates/cursor-hooks/log-chat-turn.sh .cursor/hooks/
chmod +x .cursor/hooks/log-chat-turn.sh
```

Merge **`hooks.example.json`** into **`.cursor/hooks.json`** (preserve any existing hooks). Minimal merge:

```json
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [{ "command": ".cursor/hooks/log-chat-turn.sh" }],
    "afterAgentResponse": [{ "command": ".cursor/hooks/log-chat-turn.sh" }],
    "stop": [{ "command": ".cursor/hooks/log-chat-turn.sh" }]
  }
}
```

Requires **`python3`** on `PATH`. Restart Cursor or save `hooks.json`; confirm in **Settings → Hooks**.

## User-level install (all workspaces)

Place the same scripts under **`~/.cursor/hooks/`** and use **`~/.cursor/hooks.json`** with commands like **`hooks/log-chat-turn.sh`** (paths relative to `~/.cursor/` per Cursor docs). Logging still uses **`workspace_roots[0]`** from each event.

## EOD distill

Point your **EOD / Librarian** prompt at **`local/chat-log/*.md`** (last day or two) plus **git diff** and **inbox stubs**—then approve what gets promoted to **`.calyx/reasoning/`**.

## Related

- [automation.md](automation.md) — post-commit inbox stubs + **`calyx-setup-capture.sh`**
- [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) — v1 capture
- Cursor hooks: project `.cursor/hooks.json`
