import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tooling" / "calyx-feedback-loop.py"


class TestFeedbackIntegration(unittest.TestCase):
    def _init_repo(self, d: Path):
        subprocess.check_call(["git", "init", "-b", "main"], cwd=d)
        (d / ".calyx/reasoning").mkdir(parents=True, exist_ok=True)
        (d / ".calyx/decisions").mkdir(parents=True, exist_ok=True)
        (d / ".calyx").mkdir(exist_ok=True)
        (d / "apps/api").mkdir(parents=True, exist_ok=True)
        (d / "apps/api/auth.ts").write_text("x=1\n")
        subprocess.check_call(["git", "add", "."], cwd=d)
        subprocess.check_call(
            ["git", "-c", "user.name=CalyxTest", "-c", "user.email=calyx@example.com", "commit", "-m", "init"],
            cwd=d,
        )

    def test_guided_outputs_json_md(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            self._init_repo(d)
            (d / "apps/api/auth.ts").write_text("auth change\n")
            subprocess.check_call(
                ["python3", str(RUNNER), "--project-root", str(d), "--mode", "guided"],
                cwd=ROOT,
            )
            data = json.loads((d / ".calyx/reasoning/reports/feedback/latest-feedback.json").read_text())
            self.assertIn("class", data)
            self.assertTrue((d / ".calyx/reasoning/reports/feedback/latest-feedback.md").exists())


if __name__ == "__main__":
    unittest.main()
