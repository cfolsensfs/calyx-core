#!/usr/bin/env python3
"""
Calyx Status report (v1) — artifact- and repo-level signals only.

Run from a project repository root (folder containing .calyx/), typically via:
  bash .calyx/core/tooling/calyx-status-report.sh

Does not score, rank, or compare individuals. See docs/philosophy.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_FEEDBACK_PATHS = {
    "json_path": ".calyx/reasoning/reports/feedback/latest-feedback.json",
}


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def _parse_manifest_version(manifest_path: Path) -> Optional[str]:
    if not manifest_path.exists():
        return None
    for line in manifest_path.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]:
        m = re.match(r"^version:\s*[\"']?([^\"'#]+?)[\"']?\s*(?:#.*)?$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def _git_dir(project_root: Path) -> Path:
    return project_root / ".git"


def _git_available(project_root: Path) -> bool:
    return _git_dir(project_root).exists()


def _git_output(project_root: Path, *args: str) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "-C", str(project_root), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _git_rev_count_since(project_root: Path, since: str, paths: Tuple[str, ...]) -> Optional[int]:
    out = _git_output(project_root, "rev-list", "--count", f"--since={since}", "HEAD", "--", *paths)
    if out is None or out == "":
        return None
    try:
        return int(out)
    except ValueError:
        return None


def _git_last_commit_iso(project_root: Path, path: str) -> Optional[str]:
    out = _git_output(project_root, "log", "-1", "--format=%cI", "--", path)
    return out or None


def analyze_post_commit_hook(hook_path: Path) -> Dict[str, Any]:
    """Inspect a post-commit hook file (path may be outside .git for tests)."""
    if not hook_path.is_file():
        return {"installed": False, "detail": "no .git/hooks/post-commit"}
    try:
        text = hook_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        text = ""
    ok = "calyx-post-commit.sh" in text
    return {
        "installed": bool(ok),
        "detail": "invokes calyx-post-commit.sh" if ok else "post-commit exists but does not reference calyx-post-commit.sh",
    }


def _post_commit_hook_status(project_root: Path) -> Dict[str, Any]:
    hook = _git_dir(project_root) / "hooks" / "post-commit"
    return analyze_post_commit_hook(hook)


def _cursor_hooks_present(project_root: Path) -> bool:
    p = project_root / ".cursor" / "hooks.json"
    return p.is_file()


def _agent_roles_present(project_root: Path) -> bool:
    return (project_root / ".calyx" / "AGENT_ROLES.md").is_file()


def _count_org_files(org_root: Path) -> int:
    if not org_root.is_dir():
        return 0
    n = 0
    for p in org_root.rglob("*"):
        if p.is_file():
            n += 1
    return n


def _list_reasoning_logs(reasoning: Path) -> List[Path]:
    out: List[Path] = []
    if not reasoning.is_dir():
        return out
    for p in sorted(reasoning.glob("*.md")):
        if p.name.startswith("_") or p.name.startswith("."):
            continue
        out.append(p)
    return out


def _list_adrs(decisions: Path) -> List[Path]:
    out: List[Path] = []
    if not decisions.is_dir():
        return out
    for p in sorted(decisions.glob("*.md")):
        if "TEMPLATE" in p.name.upper():
            continue
        out.append(p)
    return out


def _inbox_stubs(inbox: Path) -> List[Path]:
    if not inbox.is_dir():
        return []
    return sorted(inbox.glob("*.md"))


def _chat_logs(chat_log: Path, since: dt.datetime) -> List[Path]:
    if not chat_log.is_dir():
        return []
    recent: List[Path] = []
    for p in chat_log.glob("*.md"):
        if not p.is_file():
            continue
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, tz=dt.timezone.utc)
        if mtime >= since:
            recent.append(p)
    return sorted(recent)


def _oldest_mtime_days(paths: List[Path], now: dt.datetime) -> Optional[float]:
    if not paths:
        return None
    oldest = min(p.stat().st_mtime for p in paths)
    oldest_dt = dt.datetime.fromtimestamp(oldest, tz=dt.timezone.utc)
    return max(0.0, (now - oldest_dt).total_seconds() / 86400.0)


def _latest_eow_week(project_root: Path) -> Optional[Dict[str, Any]]:
    eow_root = project_root / ".calyx" / "reasoning" / "reports" / "eow"
    if not eow_root.is_dir():
        return None
    weeks = sorted([p for p in eow_root.iterdir() if p.is_dir() and (p / "eow-report.md").is_file()])
    if not weeks:
        return None
    latest = weeks[-1]
    report = latest / "eow-report.md"
    mtime = dt.datetime.fromtimestamp(report.stat().st_mtime, tz=dt.timezone.utc).isoformat()
    return {"week_slug": latest.name, "report_path": str(report.relative_to(project_root)), "generated_at_mtime": mtime}


def _load_feedback_summary(project_root: Path, feedback_json_rel: str) -> Optional[Dict[str, Any]]:
    path = project_root / feedback_json_rel
    if not path.is_file():
        return None
    try:
        data = _load_json(path)
    except (json.JSONDecodeError, OSError):
        return None
    return {
        "path": feedback_json_rel,
        "mode": data.get("mode"),
        "class": data.get("class"),
        "should_fail": data.get("should_fail"),
        "missing_required": data.get("missing_required"),
        "warnings": data.get("warnings"),
    }


def _feedback_json_path(project_root: Path) -> str:
    cfg_path = project_root / ".calyx" / "feedback-config.json"
    rel = DEFAULT_FEEDBACK_PATHS["json_path"]
    if cfg_path.is_file():
        try:
            cfg = _load_json(cfg_path)
            out = cfg.get("output") or {}
            if isinstance(out, dict) and out.get("json_path"):
                rel = str(out["json_path"])
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    return rel


def build_snapshot(project_root: Path, chat_window_days: int = 7) -> Dict[str, Any]:
    project_root = project_root.resolve()
    now = dt.datetime.now(dt.timezone.utc)
    since_chat = now - dt.timedelta(days=chat_window_days)
    calyx = project_root / ".calyx"
    reasoning = calyx / "reasoning"
    inbox = reasoning / "inbox"
    decisions = calyx / "decisions"
    core_manifest = calyx / "core" / "manifest.yaml"
    org_root = calyx / "org"

    reasoning_logs = _list_reasoning_logs(reasoning)
    adrs = _list_adrs(decisions)
    stubs = _inbox_stubs(inbox)
    chat_recent = _chat_logs(project_root / "local" / "chat-log", since_chat)

    git_repo = _git_available(project_root)
    hook_info: Dict[str, Any] = {"git_repository": git_repo}
    if git_repo:
        hook_info["post_commit"] = _post_commit_hook_status(project_root)
        hook_info["commits_last_30d_touching_decision_memory"] = _git_rev_count_since(
            project_root,
            "30 days ago",
            (".calyx/reasoning", ".calyx/decisions"),
        )
        hook_info["last_commit_iso_reasoning_tree"] = _git_last_commit_iso(project_root, ".calyx/reasoning")
        hook_info["last_commit_iso_decisions_tree"] = _git_last_commit_iso(project_root, ".calyx/decisions")
    else:
        hook_info["post_commit"] = {"installed": False, "detail": "not a git repository (no .git/)"}
        hook_info["commits_last_30d_touching_decision_memory"] = None
        hook_info["last_commit_iso_reasoning_tree"] = None
        hook_info["last_commit_iso_decisions_tree"] = None

    feedback_rel = _feedback_json_path(project_root)
    snapshot: Dict[str, Any] = {
        "generated_at": _now_iso(),
        "project_root": str(project_root),
        "calyx_core": {
            "manifest_path": str(core_manifest.relative_to(project_root)) if core_manifest.is_file() else None,
            "manifest_version": _parse_manifest_version(core_manifest),
            "present": core_manifest.is_file(),
        },
        "signals": {
            "cursor_hooks_json": _cursor_hooks_present(project_root),
            "agent_roles_md": _agent_roles_present(project_root),
            **hook_info,
        },
        "capture": {
            "inbox_stub_count": len(stubs),
            "oldest_inbox_stub_age_days": (
                round(age, 2) if (age := _oldest_mtime_days(stubs, now)) is not None else None
            ),
            "chat_log_files_last_n_days": len(chat_recent),
            "chat_window_days": chat_window_days,
        },
        "decision_memory": {
            "reasoning_log_files": len(reasoning_logs),
            "adr_files": len(adrs),
        },
        "automation": {
            "latest_eow": _latest_eow_week(project_root),
            "latest_feedback": _load_feedback_summary(project_root, feedback_rel),
        },
        "org_lift": {
            "col_mount_path": str(org_root.relative_to(project_root)),
            "col_mount_present": org_root.is_dir(),
            "col_mount_file_count": _count_org_files(org_root) if org_root.is_dir() else 0,
            "prompts": {
                "promote": ".calyx/core/prompts/promote-cpl-to-col.txt",
                "cadence": ".calyx/core/prompts/org-lift-cadence.txt",
            },
        },
    }
    snapshot["next_actions"] = _suggest_next_actions(snapshot)
    return snapshot


def _suggest_next_actions(snapshot: Dict[str, Any]) -> List[str]:
    actions: List[str] = []
    sig = snapshot["signals"]
    cap = snapshot["capture"]
    mem = snapshot["decision_memory"]
    core = snapshot["calyx_core"]
    auto = snapshot["automation"]
    org = snapshot["org_lift"]

    if not core.get("present"):
        actions.append("Initialize or update `.calyx/core/` (calyx-core submodule) so tooling and prompts stay pinned.")
    pc = sig.get("post_commit") or {}
    if sig.get("git_repository") and not pc.get("installed"):
        actions.append("Install Calyx git capture: `bash .calyx/core/tooling/calyx-setup-capture.sh` (or `install-calyx-git-hooks.sh`).")
    if not sig.get("cursor_hooks_json"):
        actions.append("Optional: add `.cursor/hooks.json` via `calyx-setup-capture.sh` for local chat-log capture.")
    if cap.get("inbox_stub_count", 0) > 0:
        actions.append(
            f"Distill or discard **{cap['inbox_stub_count']}** inbox stub(s); pair with `distill-inbox-stub-onepager.txt` when useful."
        )
    if mem.get("reasoning_log_files", 0) == 0 and mem.get("adr_files", 0) == 0:
        actions.append("Start decision memory: add one reasoning log under `.calyx/reasoning/` or an ADR under `.calyx/decisions/`.")
    if not auto.get("latest_eow"):
        actions.append("Run weekly governance when ready: `bash .calyx/core/tooling/calyx-eow-governance.sh`.")
    if org.get("col_mount_present") and org.get("col_mount_file_count", 0) > 0:
        actions.append(
            "Org layer mounted — when you have sanitized reusable patterns, run org lift via `promote-cpl-to-col.txt` (human merges to col)."
        )
    # Cap list
    return actions[:7]


def render_markdown(snapshot: Dict[str, Any]) -> str:
    sig = snapshot["signals"]
    pc = sig.get("post_commit") or {}
    core = snapshot["calyx_core"]
    cap = snapshot["capture"]
    mem = snapshot["decision_memory"]
    auto = snapshot["automation"]
    org = snapshot["org_lift"]

    lines = [
        "# Calyx status report (v1)",
        "",
        f"_Generated (UTC): `{snapshot['generated_at']}`_",
        "",
        "## How to read this",
        "",
        "This report summarizes **artifacts and automation** in the repo. It does **not** score people, compare contributors, or infer individual productivity.",
        "",
        "---",
        "",
        "## 1. Calyx is present and wired",
        "",
        f"- **calyx-core manifest:** `{'yes — v' + core['manifest_version'] if core.get('manifest_version') else ('yes' if core.get('present') else 'no')}`",
        f"- **Git repository:** `{'yes' if sig.get('git_repository') else 'no'}`",
        f"- **post-commit capture hook:** `{str(pc.get('installed')).lower()}` — {pc.get('detail', '')}",
        f"- **`.cursor/hooks.json`:** `{'yes' if sig.get('cursor_hooks_json') else 'no'}`",
        f"- **`.calyx/AGENT_ROLES.md`:** `{'yes' if sig.get('agent_roles_md') else 'no'}`",
        "",
        "---",
        "",
        "## 2. Capture pulse (raw signal → distill)",
        "",
        f"- **Inbox stubs** (`.calyx/reasoning/inbox/`): **{cap['inbox_stub_count']}**",
        f"- **Oldest inbox stub age (days):** {cap['oldest_inbox_stub_age_days'] if cap['oldest_inbox_stub_age_days'] is not None else '—'}",
        f"- **Chat log files** (`local/chat-log/`, last {cap['chat_window_days']}d): **{cap['chat_log_files_last_n_days']}**",
        "",
        "---",
        "",
        "## 3. Decision memory (distilled nous)",
        "",
        f"- **Reasoning logs** (top-level `.calyx/reasoning/*.md`, excluding templates): **{mem['reasoning_log_files']}**",
        f"- **ADRs** (`.calyx/decisions/*.md`, excluding templates): **{mem['adr_files']}**",
    ]
    if sig.get("git_repository"):
        lines.extend(
            [
                f"- **Commits (last 30d) touching** `.calyx/reasoning` **or** `.calyx/decisions`: **{sig.get('commits_last_30d_touching_decision_memory') if sig.get('commits_last_30d_touching_decision_memory') is not None else '—'}**",
                f"- **Last commit touching** `.calyx/reasoning/`: `{sig.get('last_commit_iso_reasoning_tree') or '—'}`",
                f"- **Last commit touching** `.calyx/decisions/`: `{sig.get('last_commit_iso_decisions_tree') or '—'}`",
            ]
        )
    lines.extend(["", "---", "", "## 4. Automation artifacts", ""])
    eow = auto.get("latest_eow")
    if eow:
        lines.append(f"- **Latest EOW report:** `{eow['week_slug']}` → `{eow['report_path']}` (mtime `{eow['generated_at_mtime']}`)")
    else:
        lines.append("- **Latest EOW report:** none found under `.calyx/reasoning/reports/eow/*/eow-report.md`")
    fb = auto.get("latest_feedback")
    if fb:
        lines.append(
            f"- **Latest feedback loop output:** `{fb['path']}` — mode `{fb.get('mode')}`, class `{fb.get('class')}`, "
            f"should_fail `{fb.get('should_fail')}`"
        )
    else:
        lines.append("- **Latest feedback loop output:** not found (run `calyx-feedback-loop.sh` on a change set).")
    lines.extend(["", "---", "", "## 5. Org lift (cpl → col)", ""])
    if org.get("col_mount_present"):
        lines.append(
            f"- **Org layer (col) mount:** yes — `{org['col_mount_path']}` ({org['col_mount_file_count']} files)"
        )
    else:
        lines.append(f"- **Org layer (col) mount:** no — optional submodule not present at `{org['col_mount_path']}`")
    lines.extend(
        [
            f"- **Prompts:** `{org['prompts']['promote']}`, `{org['prompts']['cadence']}`",
            "",
            "---",
            "",
            "## Suggested next actions",
            "",
        ]
    )
    for a in snapshot.get("next_actions") or []:
        lines.append(f"- {a}")
    lines.extend(["", "---", "", "## Machine-readable output", "", "JSON twin: `.calyx/reasoning/reports/status/latest-status.json`", ""])
    return "\n".join(lines)


def run(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Calyx Status report (v1).")
    parser.add_argument("--project-root", default=".", help="Project root (contains .calyx/).")
    parser.add_argument("--chat-window-days", type=int, default=7, help="Window for recent chat-log files.")
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    if not (project_root / ".calyx").is_dir():
        print("calyx-status: expected .calyx/ under project root", file=sys.stderr)
        return 2

    snapshot = build_snapshot(project_root, chat_window_days=args.chat_window_days)
    out_dir = project_root / ".calyx" / "reasoning" / "reports" / "status"
    json_path = out_dir / "latest-status.json"
    md_path = out_dir / "latest-status.md"
    _write_json(json_path, snapshot)
    md_path.write_text(render_markdown(snapshot), encoding="utf-8")

    print(f"calyx-status: wrote {json_path}")
    print(f"calyx-status: wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
