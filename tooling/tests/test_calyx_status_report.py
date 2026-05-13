import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


_TOOLING = Path(__file__).resolve().parents[1]
SCRIPT = _TOOLING / "calyx-status-report.py"
_TMP_BASE = _TOOLING.parent  # calyx-core/ — sandbox allows .git/ under workspace
SPEC = importlib.util.spec_from_file_location("calyx_status_report", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class StatusReportTests(unittest.TestCase):
    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_build_snapshot_minimal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root / ".calyx" / "core" / "manifest.yaml", 'version: "9.9.9"\n')
            self._write(root / ".calyx" / "reasoning" / "2026-01-01-topic.md", "# Log\n")
            self._write(root / ".calyx" / "decisions" / "ADR-0001.md", "# ADR\n")
            snap = MOD.build_snapshot(root)
            self.assertTrue(snap["calyx_core"]["present"])
            self.assertEqual(snap["calyx_core"]["manifest_version"], "9.9.9")
            self.assertEqual(snap["decision_memory"]["reasoning_log_files"], 1)
            self.assertEqual(snap["decision_memory"]["adr_files"], 1)
            self.assertFalse(snap["signals"]["git_repository"])

    def test_analyze_post_commit_detected(self):
        with tempfile.TemporaryDirectory(dir=_TMP_BASE) as tmp:
            hook = Path(tmp) / "post-commit"
            hook.write_text(
                '#!/bin/sh\nROOT=.\nCALYX="$ROOT/.calyx/core/tooling/calyx-post-commit.sh"\n',
                encoding="utf-8",
            )
            det = MOD.analyze_post_commit_hook(hook)
            self.assertTrue(det["installed"])

    def test_analyze_post_commit_missing_reference(self):
        with tempfile.TemporaryDirectory(dir=_TMP_BASE) as tmp:
            hook = Path(tmp) / "post-commit"
            hook.write_text("#!/bin/sh\necho only\n", encoding="utf-8")
            det = MOD.analyze_post_commit_hook(hook)
            self.assertFalse(det["installed"])

    def test_latest_eow_picks_lexicographic_week(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root / ".calyx" / "core" / "manifest.yaml", "version: 1\n")
            self._write(root / ".calyx" / "reasoning" / "reports" / "eow" / "2026-W01" / "eow-report.md", "# old\n")
            self._write(root / ".calyx" / "reasoning" / "reports" / "eow" / "2026-W02" / "eow-report.md", "# new\n")
            snap = MOD.build_snapshot(root)
            self.assertEqual(snap["automation"]["latest_eow"]["week_slug"], "2026-W02")

    def test_run_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root / ".calyx" / "core" / "manifest.yaml", "version: 1\n")
            rc = MOD.run(["--project-root", str(root)])
            self.assertEqual(rc, 0)
            js = json.loads((root / ".calyx" / "reasoning" / "reports" / "status" / "latest-status.json").read_text(encoding="utf-8"))
            self.assertIn("generated_at", js)
            md = (root / ".calyx" / "reasoning" / "reports" / "status" / "latest-status.md").read_text(encoding="utf-8")
            self.assertIn("Calyx status report", md)
            self.assertIn("does **not** score people", md)


if __name__ == "__main__":
    unittest.main()
