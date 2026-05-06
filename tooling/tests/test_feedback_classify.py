import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tooling"))
from lib.feedback_classify import classify_change


CFG = {"thresholds": {"files_changed_cross_cutting": 4, "lines_changed_cross_cutting": 120}}


class TestFeedbackClassify(unittest.TestCase):
    def test_trivial(self):
        res = classify_change(["docs/readme.md"], {"files_changed": 1, "lines_changed": 10}, CFG)
        self.assertEqual(res.change_class, "trivial")

    def test_architecture_binding(self):
        res = classify_change(["apps/api/auth/service.ts"], {"files_changed": 1, "lines_changed": 40}, CFG)
        self.assertEqual(res.change_class, "architecture_binding")

    def test_cross_cutting(self):
        files = ["apps/web/a.ts", "apps/api/b.ts", "packages/shared/c.ts", "mcp/adapter.ts"]
        res = classify_change(files, {"files_changed": 4, "lines_changed": 200}, CFG)
        self.assertEqual(res.change_class, "cross_cutting")


if __name__ == "__main__":
    unittest.main()
