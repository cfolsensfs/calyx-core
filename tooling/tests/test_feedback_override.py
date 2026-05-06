import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tooling"))
from lib.feedback_override import parse_override, validate_override


class TestFeedbackOverride(unittest.TestCase):
    def test_parse(self):
        text = "[calyx-override:needed hotfix|owner:chris|expires:2026-06-01]"
        ov = parse_override(text)
        self.assertEqual(ov["owner"], "chris")

    def test_validate_requires_owner_expiry(self):
        cfg = {"override": {"require_owner": True, "require_expiry": True}}
        self.assertFalse(validate_override({"reason": "x"}, cfg))
        self.assertTrue(validate_override({"reason": "x", "owner": "a", "expires": "2026-06-01"}, cfg))


if __name__ == "__main__":
    unittest.main()
