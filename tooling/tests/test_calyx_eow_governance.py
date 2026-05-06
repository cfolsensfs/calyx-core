import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "calyx-eow-governance.py"
SPEC = importlib.util.spec_from_file_location("calyx_eow_governance", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class EowGovernanceTests(unittest.TestCase):
    def _write(self, path: Path, text: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _base_project(self, root: Path):
        self._write(root / ".calyx" / "core" / "taxonomy" / "master-tags.yaml", "- id: reliability\n- id: security\n")
        self._write(root / ".calyx" / "taxonomy" / "local-tags.yaml", "- id: shrm-domain\n")
        self._write(root / ".calyx" / "reasoning" / "2026-05-06-topic.md", "# Reasoning\n## Context\n## Outcome\n## Artifacts\n")
        self._write(
            root / ".calyx" / "decisions" / "ADR-0001.md",
            "# ADR-0001: one\n- **Status:** ratified\n## Context\n## Decision\n## Consequences\n",
        )
        self._write(root / ".calyx" / "reasoning" / "inbox" / "auto-1.md", "commit abc1234 change\n")

    def test_no_trigger_basic_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_project(root)
            rc = MOD.run(["--project-root", str(root)])
            self.assertEqual(rc, 0)
            ledger = json.loads((root / ".calyx" / "reasoning" / "eow-status.json").read_text(encoding="utf-8"))
            self.assertTrue(ledger["items"])
            # should write trigger decision
            week = MOD._week_slug(MOD.dt.datetime.now(MOD.dt.timezone.utc))
            trig = json.loads(
                (root / ".calyx" / "reasoning" / "reports" / "eow" / week / "trigger-decision.json").read_text(encoding="utf-8")
            )
            self.assertIn("triggered", trig)
            self.assertFalse(trig["triggered"])

    def test_trigger_on_conflict_and_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_project(root)
            # force conflict marker and architecture divergence
            self._write(
                root / ".calyx" / "reasoning" / "2026-05-06-topic.md",
                "# Reasoning\n## Context\narchitecture divergence without supersede\nconflict: unresolved\n## Outcome\n## Artifacts\n",
            )
            rc = MOD.run(["--project-root", str(root), "--strict"])
            self.assertEqual(rc, 1)

    def test_idempotent_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_project(root)
            rc1 = MOD.run(["--project-root", str(root)])
            rc2 = MOD.run(["--project-root", str(root)])
            self.assertEqual(rc1, 0)
            self.assertEqual(rc2, 0)
            ledger = json.loads((root / ".calyx" / "reasoning" / "eow-status.json").read_text(encoding="utf-8"))
            self.assertEqual(len(ledger["items"]), 1)

    def test_override_logging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_project(root)
            MOD.run(["--project-root", str(root)])
            ledger = json.loads((root / ".calyx" / "reasoning" / "eow-status.json").read_text(encoding="utf-8"))
            item_id = next(iter(ledger["items"]))
            rc = MOD.run(["--project-root", str(root), "--override", f"{item_id}=discarded:manual override"])
            self.assertEqual(rc, 0)
            new_ledger = json.loads((root / ".calyx" / "reasoning" / "eow-status.json").read_text(encoding="utf-8"))
            self.assertEqual(new_ledger["items"][item_id]["status"], "discarded")
            log_path = root / ".calyx" / "reasoning" / "reports" / "eow-overrides.jsonl"
            self.assertTrue(log_path.exists())


if __name__ == "__main__":
    unittest.main()
