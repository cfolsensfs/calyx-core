from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PolicyResult:
    should_fail: bool
    missing_required: List[str]
    warnings: List[str]


def evaluate_policy(change_class: str, mode: str, evidence: Dict[str, bool], confidence: float, cfg: Dict) -> PolicyResult:
    requirements = cfg["requirements"].get(change_class, {})
    missing_required: List[str] = []
    warnings: List[str] = []

    if requirements.get("reasoning_required") and not evidence.get("reasoning", False):
        missing_required.append("reasoning")
    if requirements.get("adr_required") and not evidence.get("adr", False):
        missing_required.append("adr")
    if requirements.get("reasoning_recommended") and not evidence.get("reasoning", False):
        warnings.append("Reasoning log recommended for feature_local change.")

    if change_class == "uncertain" and confidence < cfg["thresholds"]["confidence_uncertain_below"]:
        warnings.append("Uncertain classification; request human class label.")

    if mode == "learn":
        return PolicyResult(False, missing_required, warnings)
    if mode == "guided":
        return PolicyResult(False, missing_required, warnings + ([f"Missing required evidence: {', '.join(missing_required)}"] if missing_required else []))

    should_fail = bool(missing_required and change_class in {"cross_cutting", "architecture_binding"})
    return PolicyResult(should_fail, missing_required, warnings)
