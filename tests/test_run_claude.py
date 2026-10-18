"""Tests for evals/run_claude.py case parsing (no CLI calls)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import run_claude  # noqa: E402


class CaseParsingTests(unittest.TestCase):
    def test_every_case_parses_into_prompt_and_rubric(self):
        for path in sorted(run_claude.CASES.glob("*.md")):
            with self.subTest(case=path.stem):
                case = run_claude.load_case(path)
                self.assertTrue((run_claude.ROOT / ".agents/skills" / case["skill"] / "SKILL.md").exists())
                self.assertIn("USER MESSAGE:", case["prompt"])
                self.assertIn("EVIDENCE:", case["prompt"])
                self.assertNotIn("Must not", case["prompt"], "the rubric must not leak into the prompt")
                self.assertIn("**Must not:**", case["rubric"])
                self.assertTrue(0 < case["pass"] <= case["must"])
                self.assertFalse(case["prompt"].startswith(">"))


if __name__ == "__main__":
    unittest.main()
