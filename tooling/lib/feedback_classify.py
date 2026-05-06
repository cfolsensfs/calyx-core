from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class ClassificationResult:
    change_class: str
    confidence: float
    rationale: List[str]
    boundaries_touched: List[str]


def _boundary(path: str) -> str:
    p = Path(path)
    parts = p.parts
    if len(parts) >= 2 and parts[0] in {"apps", "packages"}:
        return "/".join(parts[:2])
    if parts:
        return parts[0]
    return "root"


def classify_change(changed_files: List[str], stats: Dict[str, int], cfg: Dict) -> ClassificationResult:
    rationale: List[str] = []
    if not changed_files:
        return ClassificationResult("trivial", 1.0, ["No changed files detected."], [])

    boundaries = sorted({_boundary(p) for p in changed_files})
    boundaries_count = len(boundaries)
    total_files = stats.get("files_changed", len(changed_files))
    total_lines = stats.get("lines_changed", 0)

    arch_keywords = ("auth", "security", "privacy", "migration", "schema", "infra", "runtime", "contract")
    trivial_suffixes = (".md", ".txt")
    code_suffixes = (".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".java", ".kt", ".rb")

    if all(p.endswith(trivial_suffixes) for p in changed_files) and total_lines <= cfg["thresholds"]["lines_changed_cross_cutting"]:
        rationale.append("Only docs/text files changed with low line delta.")
        return ClassificationResult("trivial", 0.95, rationale, boundaries)

    if any(k in p.lower() for p in changed_files for k in arch_keywords):
        rationale.append("Architecture/security/data/infra keyword hit in changed path.")
        return ClassificationResult("architecture_binding", 0.9, rationale, boundaries)

    if boundaries_count >= 2 and (
        total_files >= cfg["thresholds"]["files_changed_cross_cutting"]
        or total_lines >= cfg["thresholds"]["lines_changed_cross_cutting"]
    ):
        rationale.append("Multiple boundaries touched and threshold exceeded.")
        return ClassificationResult("cross_cutting", 0.82, rationale, boundaries)

    if any(p.endswith(code_suffixes) for p in changed_files):
        rationale.append("Code files changed within limited boundary scope.")
        return ClassificationResult("feature_local", 0.78, rationale, boundaries)

    rationale.append("Low-signal pattern; defaulting to uncertain.")
    return ClassificationResult("uncertain", 0.45, rationale, boundaries)
