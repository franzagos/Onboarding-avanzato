from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts" / "init_kb.py"
VALIDATE = ROOT / "scripts" / "validate_kb.py"


class SkillScriptTests(unittest.TestCase):
    def init_kb(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INIT), "--brand", "Test Brand", "--output", str(target)],
            check=False,
            text=True,
            capture_output=True,
        )

    def validate(self, target: Path, stage: str = "draft") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE), str(target), "--mode", "full", "--stage", stage],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_init_creates_canonical_v2(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = self.init_kb(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((target / "13-funnel-awareness-matrix.yaml").exists())
            self.assertTrue((target / "sources.yaml").exists())
            self.assertTrue((target / "evidence-ledger.yaml").exists())
            self.assertFalse((target / "13-funnel-awareness-matrix.md").exists())
            self.assertIn('schema_version: "2.0"', (target / "sources.yaml").read_text())

    def test_second_init_skips_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.init_kb(target)
            second = self.init_kb(target)
            self.assertEqual(second.returncode, 0)
            self.assertIn("Skipped existing (28)", second.stdout)

    def test_draft_warns_and_review_fails_on_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.init_kb(target)
            draft = self.validate(target, "draft")
            review = self.validate(target, "review")
            self.assertEqual(draft.returncode, 0, draft.stdout)
            self.assertIn("WARN:", draft.stdout)
            self.assertEqual(review.returncode, 1)
            self.assertIn("placeholder remains", review.stdout)

    def test_orphan_evidence_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.init_kb(target)
            registry = target / "11-product-offer-registry.yaml"
            registry.write_text(registry.read_text() + 'test:\n  evidence_ids: ["EV-missing"]\n')
            result = self.validate(target, "draft")
            self.assertEqual(result.returncode, 1)
            self.assertIn("orphan evidence_ids reference EV-missing", result.stdout)

    def test_blocking_prompt_is_concrete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.init_kb(target)
            gaps = target / "assumptions-and-gaps.yaml"
            gaps.write_text(gaps.read_text().replace("Mi serve il feed prodotto autorevole.", "Invia più dati."))
            result = self.validate(target, "draft")
            self.assertEqual(result.returncode, 1)
            self.assertIn("request_text must start with 'Mi serve '", result.stdout)


if __name__ == "__main__":
    unittest.main()
