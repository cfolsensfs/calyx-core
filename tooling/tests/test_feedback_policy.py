import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tooling"))
from lib.feedback_policy import evaluate_policy


CFG = {
    "thresholds": {"confidence_uncertain_below": 0.6},
    "requirements": {
        "trivial": {},
        "feature_local": {"reasoning_recommended": True},
        "cross_cutting": {"reasoning_required": True},
        "architecture_binding": {"reasoning_required": True, "adr_required": True},
        "uncertain": {},
    },
}


class TestFeedbackPolicy(unittest.TestCase):
    def test_learn_never_fails(self):
        out = evaluate_policy("cross_cutting", "learn", {"reasoning": False, "adr": False}, 0.8, CFG)
        self.assertFalse(out.should_fail)
        self.assertIn("reasoning", out.missing_required)

    def test_guardrail_fails_high_impact_missing(self):
        out = evaluate_policy("architecture_binding", "guardrail", {"reasoning": True, "adr": False}, 0.9, CFG)
        self.assertTrue(out.should_fail)
        self.assertEqual(out.missing_required, ["adr"])


if __name__ == "__main__":
    unittest.main()
