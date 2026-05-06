from __future__ import annotations

from typing import Dict, List


def render_markdown(summary: Dict, remediation_snippet: str) -> str:
    lines: List[str] = [
        "# Calyx feedback loop result",
        "",
        f"- Class: **{summary['class']}**",
        f"- Confidence: **{summary['confidence']:.2f}**",
        f"- Mode: **{summary['mode']}**",
        f"- Should fail: **{str(summary['should_fail']).lower()}**",
        "",
        "## Rationale",
    ]
    lines.extend([f"- {r}" for r in summary["rationale"]] or ["- none"])
    lines.append("")
    lines.append("## Missing required artifacts")
    lines.extend([f"- {m}" for m in summary["missing_required"]] or ["- none"])
    lines.append("")
    lines.append("## Warnings")
    lines.extend([f"- {w}" for w in summary["warnings"]] or ["- none"])
    lines.append("")
    lines.append("## Remediation")
    lines.append(remediation_snippet)
    lines.append("")
    return "\n".join(lines)


def remediation_snippet(change_class: str, missing: List[str]) -> str:
    base_reasoning = ".calyx/reasoning/YYYY-MM-DD-topic.md"
    base_adr = ".calyx/decisions/ADR-XXXX-topic.md"
    hints = [
        f"Detected class: `{change_class}`",
        f"Missing artifacts: {', '.join(missing) if missing else 'none'}",
        f"Add/update: `{base_reasoning}` (if reasoning missing)",
        f"Add/update: `{base_adr}` (if ADR missing)",
        "Commands: `git add .calyx/reasoning .calyx/decisions && git commit -m \"add Calyx evidence\"`",
    ]
    return "\n".join([f"- {h}" for h in hints])
