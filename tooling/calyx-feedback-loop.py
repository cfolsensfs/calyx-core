#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, List

from lib.feedback_classify import classify_change
from lib.feedback_override import log_override, parse_override, validate_override
from lib.feedback_policy import evaluate_policy
from lib.feedback_render import remediation_snippet, render_markdown


DEFAULT_CFG = {
    "mode": "learn",
    "thresholds": {
        "files_changed_cross_cutting": 4,
        "lines_changed_cross_cutting": 120,
        "confidence_uncertain_below": 0.6,
    },
    "requirements": {
        "trivial": {},
        "feature_local": {"reasoning_recommended": True},
        "cross_cutting": {"reasoning_required": True},
        "architecture_binding": {"reasoning_required": True, "adr_required": True},
        "uncertain": {},
    },
    "override": {"enabled": True, "require_owner": True, "require_expiry": True},
    "output": {
        "json_path": ".calyx/reasoning/reports/feedback/latest-feedback.json",
        "markdown_path": ".calyx/reasoning/reports/feedback/latest-feedback.md",
    },
}


def _git(*args: str, cwd: Path) -> str:
    out = subprocess.check_output(["git", *args], cwd=str(cwd), text=True, stderr=subprocess.DEVNULL)
    return out.strip()


def changed_files_and_stats(root: Path) -> tuple[List[str], Dict[str, int]]:
    staged = _git("diff", "--name-only", "--cached", cwd=root).splitlines()
    if staged and staged != [""]:
        files = [f for f in staged if f]
        numstat_raw = _git("diff", "--numstat", "--cached", cwd=root).splitlines()
    else:
        files = [f for f in _git("diff", "--name-only", "HEAD", cwd=root).splitlines() if f]
        numstat_raw = _git("diff", "--numstat", "HEAD", cwd=root).splitlines()
    lines_changed = 0
    for row in numstat_raw:
        parts = row.split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            lines_changed += int(parts[0]) + int(parts[1])
    return files, {"files_changed": len(files), "lines_changed": lines_changed}


def detect_evidence(root: Path) -> Dict[str, bool]:
    staged = [p for p in _git("diff", "--name-only", "--cached", cwd=root).splitlines() if p]
    changed = staged or [p for p in _git("diff", "--name-only", "HEAD", cwd=root).splitlines() if p]
    has_reasoning = any(p.startswith(".calyx/reasoning/") and p.endswith(".md") and "/inbox/" not in p for p in changed)
    has_adr = any(p.startswith(".calyx/decisions/") and p.endswith(".md") and "TEMPLATE" not in p for p in changed)
    return {"reasoning": has_reasoning, "adr": has_adr}


def load_cfg(path: Path) -> Dict:
    cfg = json.loads(json.dumps(DEFAULT_CFG))
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        # shallow merge by section for simplicity
        for k, v in loaded.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def main() -> int:
    ap = argparse.ArgumentParser(description="Calyx Knowledge Feedback Loop")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--config", default=".calyx/feedback-config.json")
    ap.add_argument("--mode", choices=["learn", "guided", "guardrail"], default=None)
    ap.add_argument("--override-text", default="")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    if not (root / ".calyx").exists():
        print("calyx-feedback: run from project root containing .calyx/")
        return 2

    cfg = load_cfg(root / args.config)
    mode = args.mode or cfg["mode"]

    files, stats = changed_files_and_stats(root)
    cls = classify_change(files, stats, cfg)
    evidence = detect_evidence(root)
    policy = evaluate_policy(cls.change_class, mode, evidence, cls.confidence, cfg)

    override_payload = parse_override(args.override_text)
    override_valid = False
    if cfg["override"]["enabled"] and override_payload and validate_override(override_payload, cfg):
        override_valid = True
        policy.should_fail = False
        log_override(
            root / ".calyx/reasoning/reports/feedback/overrides.jsonl",
            {"class": cls.change_class, "mode": mode, **override_payload},
        )

    summary = {
        "class": cls.change_class,
        "confidence": cls.confidence,
        "rationale": cls.rationale,
        "boundaries_touched": cls.boundaries_touched,
        "mode": mode,
        "missing_required": policy.missing_required,
        "warnings": policy.warnings,
        "should_fail": policy.should_fail,
        "override_used": override_valid,
        "changed_files": files,
        "stats": stats,
    }

    json_path = root / cfg["output"]["json_path"]
    md_path = root / cfg["output"]["markdown_path"]
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary, remediation_snippet(cls.change_class, policy.missing_required)), encoding="utf-8")

    print(f"calyx-feedback: class={cls.change_class} confidence={cls.confidence:.2f} mode={mode}")
    if policy.warnings:
        for w in policy.warnings:
            print(f"WARN: {w}")
    if policy.missing_required:
        print("Missing required:", ", ".join(policy.missing_required))
    if policy.should_fail:
        print("FAIL: Missing required Calyx evidence for enforced class.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
