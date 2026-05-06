#!/usr/bin/env python3
"""
Calyx Thin EOW Governance runner (report-first).

Runs from a project repo root (the folder containing .calyx/), typically via:
  bash .calyx/core/tooling/calyx-eow-governance.sh
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_CONFIG = {
    "window_days": 7,
    "open_question_days": 21,
    "critical_confidence_threshold": 0.6,
    "severity_weights": {"low": 1, "medium": 2, "high": 4},
    "trigger_rules": {
        "high_severity_conflict": True,
        "security_privacy_regulatory_conflict": True,
        "major_architecture_divergence_without_supersede": True,
        "repeated_rework_unresolved_assumptions": True,
        "critical_confidence_below_threshold": True,
    },
}


@dataclass
class IntakeItem:
    item_id: str
    source_path: str
    source_type: str
    discovered_at: str
    inferred_topic: str
    candidate_tags: List[str]
    source_hash: str
    commit_sha: Optional[str]


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def _sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()  # noqa: S324


def _rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def _week_slug(now: dt.datetime) -> str:
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _parse_tag_ids(path: Path) -> List[str]:
    if not path.exists():
        return []
    ids: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^\s*-\s+id:\s*([a-z0-9-]+)\s*$", line)
        if m:
            ids.append(m.group(1))
    return ids


def _extract_candidate_tags(text: str) -> List[str]:
    found = re.findall(r"\b([a-z][a-z0-9-]{2,})\b", text.lower())
    # lightweight heuristic: keep unique-ish short list
    out: List[str] = []
    for token in found:
        if token in {"the", "and", "with", "that", "from", "this", "were", "have"}:
            continue
        if token not in out:
            out.append(token)
        if len(out) >= 8:
            break
    return out


def _extract_commit_sha(text: str) -> Optional[str]:
    m = re.search(r"\b([0-9a-f]{7,40})\b", text)
    return m.group(1) if m else None


def _discover_intake_items(project_root: Path, config: Dict, now: dt.datetime) -> List[IntakeItem]:
    calyx = project_root / ".calyx"
    inbox = calyx / "reasoning" / "inbox"
    chat_log = project_root / "local" / "chat-log"
    window_days = int(config["window_days"])
    threshold = now - dt.timedelta(days=window_days)
    items: List[IntakeItem] = []

    def maybe_add(path: Path, source_type: str) -> None:
        if not path.exists() or not path.is_file():
            return
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc)
        if mtime < threshold:
            return
        text = path.read_text(encoding="utf-8", errors="ignore")
        source_hash = _sha1_text(text)
        item_id = f"{source_type}:{source_hash[:12]}"
        topic = path.stem
        items.append(
            IntakeItem(
                item_id=item_id,
                source_path=_rel(path, project_root),
                source_type=source_type,
                discovered_at=_now_iso(),
                inferred_topic=topic,
                candidate_tags=_extract_candidate_tags(text),
                source_hash=source_hash,
                commit_sha=_extract_commit_sha(text),
            )
        )

    if inbox.exists():
        for p in sorted(inbox.glob("*.md")):
            maybe_add(p, "inbox_stub")
    if chat_log.exists():
        for p in sorted(chat_log.glob("*.md")):
            maybe_add(p, "chat_log")
    return items


def _load_reasoning_text(project_root: Path) -> str:
    reasoning_dir = project_root / ".calyx" / "reasoning"
    chunks: List[str] = []
    if reasoning_dir.exists():
        for p in sorted(reasoning_dir.glob("*.md")):
            if p.name.startswith("_"):
                continue
            if p.parent.name == "inbox":
                continue
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def _apply_overrides(statuses: Dict, overrides: List[str], log_path: Path) -> List[str]:
    applied: List[str] = []
    if not overrides:
        return applied
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as logf:
        for ov in overrides:
            # item_id=status:reason
            m = re.match(r"^([^=]+)=([a-z-]+):(.+)$", ov)
            if not m:
                continue
            item_id, status, reason = m.group(1), m.group(2), m.group(3).strip()
            if item_id not in statuses:
                continue
            statuses[item_id]["status"] = status
            statuses[item_id]["rationale"] = reason
            statuses[item_id]["overridden"] = True
            line = {
                "timestamp": _now_iso(),
                "item_id": item_id,
                "status": status,
                "reason": reason,
            }
            logf.write(json.dumps(line) + "\n")
            applied.append(item_id)
    return applied


def _distill_status_pass(
    project_root: Path, intake_items: List[IntakeItem], status_ledger: Dict, overrides: List[str], override_log_path: Path
) -> Dict:
    reasoning_text = _load_reasoning_text(project_root)
    statuses = status_ledger.get("items", {})
    results = {"distilled": [], "deferred": [], "discarded": []}

    for item in intake_items:
        if item.item_id in statuses:
            st = statuses[item.item_id]["status"]
            results.setdefault(st, []).append(item.item_id)
            continue

        status = "deferred"
        rationale = "Pending human distillation in weekly pass."
        if item.commit_sha and item.commit_sha in reasoning_text:
            status = "distilled"
            rationale = f"Commit SHA {item.commit_sha[:12]} already referenced in reasoning logs."
        elif item.source_type == "chat_log" and len(item.candidate_tags) < 2:
            status = "discarded"
            rationale = "Low-signal chat fragment; no clear topic tags inferred."

        statuses[item.item_id] = {
            "item_id": item.item_id,
            "source_path": item.source_path,
            "source_hash": item.source_hash,
            "status": status,
            "rationale": rationale,
            "updated_at": _now_iso(),
            "overridden": False,
        }
        results.setdefault(status, []).append(item.item_id)

    applied = _apply_overrides(statuses, overrides, override_log_path)
    status_ledger["items"] = statuses
    status_ledger["applied_overrides"] = applied
    return {"ledger": status_ledger, "results": results}


def _find_md_links(text: str) -> List[str]:
    # markdown links only
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def _severity(score: int) -> str:
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def _hygiene_checks(project_root: Path, known_tags: List[str]) -> List[Dict]:
    findings: List[Dict] = []
    calyx = project_root / ".calyx"
    reasoning = calyx / "reasoning"
    decisions = calyx / "decisions"

    for p in sorted(reasoning.glob("*.md")):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        required = ["## Context", "## Outcome", "## Artifacts"]
        for heading in required:
            if heading not in text:
                findings.append(
                    {
                        "kind": "missing_required_heading",
                        "path": _rel(p, project_root),
                        "detail": f"Missing heading: {heading}",
                        "severity": "medium",
                        "rationale": "Reasoning entries should preserve canonical structure for search/reuse.",
                    }
                )
        if not re.match(r"^\d{4}-\d{2}-\d{2}-", p.name):
            findings.append(
                {
                    "kind": "naming_convention",
                    "path": _rel(p, project_root),
                    "detail": "Reasoning file does not start with YYYY-MM-DD-",
                    "severity": "low",
                    "rationale": "Date-prefixed naming keeps weekly scans deterministic.",
                }
            )
        tags_line = re.search(r"^\s*-\s+\*\*Tags:\*\*\s*(.+)$", text, re.MULTILINE)
        if tags_line:
            raw = tags_line.group(1)
            tags = [t.strip().strip(",") for t in raw.split() if re.match(r"^[a-z0-9-]+$", t.strip(", "))]
            for tag in tags:
                if tag and tag not in known_tags:
                    findings.append(
                        {
                            "kind": "unknown_tag",
                            "path": _rel(p, project_root),
                            "detail": f"Unknown tag '{tag}'",
                            "severity": "medium",
                            "rationale": "Tags should align with master/local taxonomy registries.",
                        }
                    )
        for link in _find_md_links(text):
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            link_path = (p.parent / link).resolve()
            if not link_path.exists():
                findings.append(
                    {
                        "kind": "broken_link",
                        "path": _rel(p, project_root),
                        "detail": f"Broken relative link: {link}",
                        "severity": "medium",
                        "rationale": "Broken links reduce traceability between reasoning/ADRs/artifacts.",
                    }
                )

    for p in sorted(decisions.glob("*.md")):
        if "ADR-TEMPLATE" in p.name:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for heading in ["## Context", "## Decision", "## Consequences"]:
            if heading not in text:
                findings.append(
                    {
                        "kind": "missing_required_heading",
                        "path": _rel(p, project_root),
                        "detail": f"Missing ADR heading: {heading}",
                        "severity": "high",
                        "rationale": "ADR structure is required for consistent interpretation over time.",
                    }
                )
    return findings


def _consistency_checks(project_root: Path, config: Dict) -> List[Dict]:
    findings: List[Dict] = []
    calyx = project_root / ".calyx"
    decisions = calyx / "decisions"
    reasoning = calyx / "reasoning"
    open_question_days = int(config["open_question_days"])
    threshold = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=open_question_days)

    # Duplicate ratified ADR titles -> potential conflict
    ratified_titles: Dict[str, List[str]] = {}
    for p in sorted(decisions.glob("*.md")):
        if "ADR-TEMPLATE" in p.name:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^\s*-\s+\*\*Status:\*\*\s*ratified\b", text, re.IGNORECASE | re.MULTILINE):
            title = text.splitlines()[0].strip().lower()
            title = re.sub(r"[^a-z0-9]+", "-", title).strip("-")
            ratified_titles.setdefault(title, []).append(_rel(p, project_root))
    for title, paths in ratified_titles.items():
        if len(paths) > 1:
            findings.append(
                {
                    "kind": "ratified_adr_overlap",
                    "severity": "high",
                    "score": 4,
                    "detail": f"Multiple ratified ADRs with similar title '{title}': {paths}",
                    "rationale": "Parallel ratified ADRs on same topic can encode conflicting constraints.",
                }
            )

    # Architecture divergence without superseding ADR (keyword heuristic)
    for p in sorted(reasoning.glob("*.md")):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        if "architecture divergence" in text and "supersede" not in text and "supersedes" not in text:
            findings.append(
                {
                    "kind": "architecture_divergence_without_supersede",
                    "severity": "high",
                    "score": 4,
                    "detail": f"{_rel(p, project_root)} mentions architecture divergence without supersede marker.",
                    "rationale": "Major divergence should reference an ADR supersession path.",
                }
            )
        if any(x in text for x in ["conflict:", "contradict", "inconsistent decision"]):
            findings.append(
                {
                    "kind": "explicit_conflict_marker",
                    "severity": "medium",
                    "score": 2,
                    "detail": f"Conflict marker found in {_rel(p, project_root)}",
                    "rationale": "Reasoning logs explicitly indicate unresolved or competing decisions.",
                }
            )
        if any(x in text for x in ["security", "privacy", "regulatory", "compliance"]) and "contradict" in text:
            findings.append(
                {
                    "kind": "security_privacy_regulatory_conflict",
                    "severity": "high",
                    "score": 4,
                    "detail": f"Potential compliance contradiction in {_rel(p, project_root)}",
                    "rationale": "Security/privacy/regulatory contradictions require elevated scrutiny.",
                }
            )

        has_open_q = any(x in text for x in ["open question", "open questions", "todo", "tbd"])
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc)
        if has_open_q and mtime < threshold:
            findings.append(
                {
                    "kind": "stale_open_question",
                    "severity": "low",
                    "score": 1,
                    "detail": f"Open question older than {open_question_days} days in {_rel(p, project_root)}",
                    "rationale": "Stale open questions can hide recurring rework and uncertainty.",
                }
            )

    return findings


def _trigger_10th_man(conflicts: List[Dict], status_results: Dict, config: Dict) -> Dict:
    rules = config["trigger_rules"]
    threshold = float(config["critical_confidence_threshold"])
    deferred = len(status_results.get("deferred", []))
    distilled = len(status_results.get("distilled", []))
    total = deferred + distilled + len(status_results.get("discarded", []))
    deferred_ratio = (deferred / total) if total else 0.0
    weighted_conflict = sum(int(c.get("score", {"low": 1, "medium": 2, "high": 4}.get(c["severity"], 1))) for c in conflicts)
    confidence_score = max(0.0, 1.0 - min(1.0, weighted_conflict / 12.0 + deferred_ratio * 0.5))

    matched: List[str] = []
    critical_area_present = any(
        c["kind"]
        in {
            "ratified_adr_overlap",
            "security_privacy_regulatory_conflict",
            "architecture_divergence_without_supersede",
            "explicit_conflict_marker",
        }
        for c in conflicts
    )
    if rules.get("high_severity_conflict") and any(c["severity"] == "high" for c in conflicts):
        matched.append("high_severity_conflict")
    if rules.get("security_privacy_regulatory_conflict") and any(
        c["kind"] == "security_privacy_regulatory_conflict" for c in conflicts
    ):
        matched.append("security_privacy_regulatory_conflict")
    if rules.get("major_architecture_divergence_without_supersede") and any(
        c["kind"] == "architecture_divergence_without_supersede" for c in conflicts
    ):
        matched.append("major_architecture_divergence_without_supersede")
    if rules.get("repeated_rework_unresolved_assumptions") and sum(
        1 for c in conflicts if c["kind"] in {"stale_open_question", "explicit_conflict_marker"}
    ) >= 2:
        matched.append("repeated_rework_unresolved_assumptions")
    if rules.get("critical_confidence_below_threshold") and critical_area_present and confidence_score < threshold:
        matched.append("critical_confidence_below_threshold")

    triggered = bool(matched)
    rationale = (
        "Trigger conditions matched: " + ", ".join(matched)
        if triggered
        else "No trigger this week; no configured trigger conditions were met."
    )
    return {
        "triggered": triggered,
        "matched_conditions": matched,
        "rationale": rationale,
        "confidence_score": round(confidence_score, 4),
        "reviewer_required": triggered,
    }


def _render_report(
    week_slug: str,
    intake: List[IntakeItem],
    status_results: Dict,
    hygiene: List[Dict],
    conflicts: List[Dict],
    trigger: Dict,
) -> str:
    def bullet(items: List[str]) -> str:
        return "\n".join(f"- {x}" for x in items) if items else "- none"

    distilled = status_results.get("distilled", [])
    deferred = status_results.get("deferred", [])
    discarded = status_results.get("discarded", [])
    high_conflicts = [c for c in conflicts if c["severity"] == "high"]
    next_actions: List[str] = []
    if deferred:
        next_actions.append("Distill highest-signal deferred items from this week's intake.")
    if hygiene:
        next_actions.append("Fix medium/high hygiene findings to keep reasoning/ADR search quality high.")
    if high_conflicts:
        next_actions.append("Resolve high-severity decision conflicts or open/supersede ADRs.")
    if trigger["triggered"]:
        next_actions.append("Run 10th Man review this week on triggered conflict set.")
    if not next_actions:
        next_actions.append("No urgent governance actions this week; keep regular checkpoint rhythm.")
    next_actions = next_actions[:5]

    lines = [
        f"# Calyx EOW governance report — {week_slug}",
        "",
        "## Intake summary",
        f"- Total intake items: **{len(intake)}**",
        f"- Distilled: **{len(distilled)}**",
        f"- Deferred: **{len(deferred)}**",
        f"- Discarded: **{len(discarded)}**",
        "",
        "## Distilled items",
        bullet(distilled),
        "",
        "## Deferred items",
        bullet(deferred),
        "",
        "## Discarded items (with reason in status ledger)",
        bullet(discarded),
        "",
        "## Hygiene findings",
        f"- Total findings: **{len(hygiene)}**",
        bullet([f"{f['severity']} — {f['kind']} — {f['detail']}" for f in hygiene[:20]]),
        "",
        "## Consistency findings",
        f"- Total conflicts: **{len(conflicts)}**",
        bullet([f"{c['severity']} — {c['kind']} — {c['detail']}" for c in conflicts[:20]]),
        "",
        "## 10th Man trigger status",
        f"- Triggered: **{str(trigger['triggered']).lower()}**",
        f"- Reason: {trigger['rationale']}",
        f"- Confidence score: **{trigger['confidence_score']}**",
        "",
        "## Recommended next actions (max 5)",
        "\n".join(f"- {a}" for a in next_actions),
        "",
        "## Notes",
        "- This is report-first governance; strict mode is optional.",
        "- Every classification and trigger result is stored in JSON for auditability.",
    ]
    return "\n".join(lines) + "\n"


def run(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run Thin EOW Calyx Governance workflow.")
    parser.add_argument("--project-root", default=".", help="Project repository root (contains .calyx).")
    parser.add_argument("--config", default=".calyx/eow-config.json", help="Path to EOW config JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on high-severity findings or trigger.")
    parser.add_argument(
        "--override",
        action="append",
        default=[],
        help="Override status: item_id=status:reason (may repeat). Logged to overrides JSONL.",
    )
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    if not (project_root / ".calyx").exists():
        print("calyx-eow: expected .calyx/ under project root", file=sys.stderr)
        return 2

    config_path = (project_root / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    config = DEFAULT_CONFIG.copy()
    config.update(_load_json(config_path, {}))

    now = dt.datetime.now(dt.timezone.utc)
    week_slug = _week_slug(now)
    reports_dir = project_root / ".calyx" / "reasoning" / "reports" / "eow" / week_slug
    reports_dir.mkdir(parents=True, exist_ok=True)

    intake_items = _discover_intake_items(project_root, config, now)
    intake_manifest = {
        "generated_at": _now_iso(),
        "window_days": config["window_days"],
        "items": [item.__dict__ for item in intake_items],
    }
    _write_json(reports_dir / "intake-manifest.json", intake_manifest)

    ledger_path = project_root / ".calyx" / "reasoning" / "eow-status.json"
    ledger = _load_json(ledger_path, {"generated_at": _now_iso(), "items": {}})
    override_log = project_root / ".calyx" / "reasoning" / "reports" / "eow-overrides.jsonl"
    distill = _distill_status_pass(project_root, intake_items, ledger, args.override, override_log)
    distill["ledger"]["generated_at"] = _now_iso()
    _write_json(ledger_path, distill["ledger"])
    _write_json(
        reports_dir / "distill-status.json",
        {"generated_at": _now_iso(), "results": distill["results"], "applied_overrides": distill["ledger"].get("applied_overrides", [])},
    )

    master_tags = _parse_tag_ids(project_root / ".calyx" / "core" / "taxonomy" / "master-tags.yaml")
    local_tags = _parse_tag_ids(project_root / ".calyx" / "taxonomy" / "local-tags.yaml")
    known_tags = sorted(set(master_tags + local_tags))
    hygiene_findings = _hygiene_checks(project_root, known_tags)
    _write_json(reports_dir / "hygiene-findings.json", {"generated_at": _now_iso(), "findings": hygiene_findings})

    conflicts = _consistency_checks(project_root, config)
    _write_json(reports_dir / "conflicts.json", {"generated_at": _now_iso(), "conflicts": conflicts})

    trigger = _trigger_10th_man(conflicts, distill["results"], config)
    _write_json(reports_dir / "trigger-decision.json", {"generated_at": _now_iso(), **trigger})

    report_md = _render_report(week_slug, intake_items, distill["results"], hygiene_findings, conflicts, trigger)
    (reports_dir / "eow-report.md").write_text(report_md, encoding="utf-8")

    print(f"calyx-eow: report generated at {reports_dir / 'eow-report.md'}")
    print(f"calyx-eow: intake={len(intake_items)} distilled={len(distill['results'].get('distilled', []))} deferred={len(distill['results'].get('deferred', []))}")
    print(f"calyx-eow: conflicts={len(conflicts)} trigger={str(trigger['triggered']).lower()} confidence={trigger['confidence_score']}")

    if args.strict and (trigger["triggered"] or any(c["severity"] == "high" for c in conflicts)):
        print("calyx-eow: strict mode failure due to trigger/high-severity findings", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
