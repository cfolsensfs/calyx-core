#!/usr/bin/env python3
"""
Cursor hook helper: append chat turns to <workspace>/local/chat-log/YYYY-MM-DD.md
and delete log files older than RETENTION_DAYS (default 3).

Hook events (stdin JSON, Cursor): beforeSubmitPrompt, afterAgentResponse, optionally stop.
Field names vary by Cursor version; we read defensively.

Usage: hooked from log-chat-turn.sh; stdin = hook JSON payload.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RETENTION_DAYS = int(os.environ.get("CALYX_CHAT_LOG_RETENTION_DAYS", "3"))


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _workspace_roots(payload: dict) -> list[str]:
    roots = payload.get("workspace_roots") or []
    out = []
    for r in roots:
        if isinstance(r, str) and r.strip():
            out.append(os.path.expanduser(r.strip()))
    return out


def _first_root(payload: dict) -> Path | None:
    roots = _workspace_roots(payload)
    if not roots:
        return None
    return Path(roots[0])


def _get_prompt(payload: dict) -> str:
    for key in ("prompt", "text", "user_prompt", "message", "content"):
        v = payload.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _get_assistant(payload: dict) -> str:
    v = payload.get("text")
    if isinstance(v, str) and v.strip():
        return v.strip()
    for key in ("response", "assistant_message", "content"):
        v = payload.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _prune(log_dir: Path) -> None:
    if not log_dir.is_dir():
        return
    cutoff = time.time() - RETENTION_DAYS * 86400
    for p in log_dir.glob("*.md"):
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
        except OSError:
            pass


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    root = _first_root(payload)
    if root is None:
        return 0

    log_dir = root / "local" / "chat-log"
    log_dir.mkdir(parents=True, exist_ok=True)

    event = str(payload.get("hook_event_name") or "")
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = log_dir / f"{day}.md"

    lines: list[str] = []
    if event == "beforeSubmitPrompt":
        prompt = _get_prompt(payload)
        if prompt:
            lines.append(f"\n### User — {_iso()}\n\n{prompt}\n")
    elif event == "afterAgentResponse":
        text = _get_assistant(payload)
        if text:
            cid = payload.get("conversation_id") or ""
            gid = payload.get("generation_id") or ""
            meta = ""
            if cid or gid:
                meta = f"\n<!-- conversation_id={cid} generation_id={gid} -->\n"
            lines.append(f"{meta}\n### Assistant — {_iso()}\n\n{text}\n")
    elif event == "stop":
        lines.append(f"\n--- stop — {_iso()} ---\n")

    if lines:
        with open(path, "a", encoding="utf-8") as f:
            if f.tell() == 0:
                f.write(f"# Cursor chat log — {day}\n\n")
            f.writelines(lines)

    _prune(log_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
