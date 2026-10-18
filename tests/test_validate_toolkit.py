"""Tests for scripts/validate_toolkit.py using small fixture repositories."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_toolkit as vt  # noqa: E402

SKILL = "---\nname: {name}\ndescription: Does a thing.\n---\n\n# Skill\n"
PROFILE = "---\nname: {name}\ndescription: Owns a thing.\n---\n\nUse the skill.\n"
PROMPT = "---\ndescription: Start a thing.\n---\n\nRead .agents/skills/demo/SKILL.md.\n"
WORKFLOW_MAP = ("| Task | Profile | Skill |\n| --- | --- | --- |\n"
                "| [Demo](prompts/demo.prompt.md) | [Demo](agents/demo.agent.md) "
                "| [demo](../.agents/skills/demo/SKILL.md) |\n")


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write(".agents/skills/demo/SKILL.md", SKILL.format(name="demo"))
        self.write(".github/agents/demo.agent.md", PROFILE.format(name="Demo"))
        self.write(".github/prompts/demo.prompt.md", PROMPT)
        self.write(".github/AI-WORKFLOWS.md", WORKFLOW_MAP)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def errors(self):
        return vt.validate(self.root)[0]

    def test_valid_fixture_passes_and_counts_files(self):
        errors, counts = vt.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(counts, {"skills": 1, "profiles": 1, "prompts": 1})

    def test_new_routed_files_need_no_validator_change(self):
        self.write(".agents/skills/second/SKILL.md", SKILL.format(name="second"))
        self.write(".github/AI-WORKFLOWS.md", WORKFLOW_MAP + "| x | x | [second](../.agents/skills/second/SKILL.md) |\n")
        self.assertEqual(self.errors(), [])

    def test_unrouted_skill_is_reported(self):
        self.write(".agents/skills/orphan/SKILL.md", SKILL.format(name="orphan"))
        self.assertIn("Not routed from .github/AI-WORKFLOWS.md: .agents/skills/orphan/SKILL.md", self.errors())

    def test_missing_metadata_and_bad_skill_name(self):
        self.write(".agents/skills/demo/SKILL.md", "---\nname: Demo Skill\n---\n")
        errors = self.errors()
        self.assertIn("Missing 'description' metadata: .agents/skills/demo/SKILL.md", errors)
        self.assertIn("Skill name must be lowercase-hyphenated and match its folder: .agents/skills/demo/SKILL.md",
                      errors)

    def test_crlf_frontmatter_is_accepted(self):
        self.write(".agents/skills/demo/SKILL.md", SKILL.format(name="demo").replace("\n", "\r\n"))
        self.assertEqual(self.errors(), [])

    def test_duplicate_profile_names(self):
        self.write(".github/agents/copy.agent.md", PROFILE.format(name="demo"))
        self.write(".github/AI-WORKFLOWS.md", WORKFLOW_MAP + "| x | [copy](agents/copy.agent.md) | x |\n")
        self.assertTrue(any(e.startswith("Duplicate profile name") for e in self.errors()))

    def test_broken_link_and_missing_prose_path(self):
        self.write("README.md", "See [docs](docs/missing.md). Read .agents/skills/gone/SKILL.md first.\n")
        errors = self.errors()
        self.assertIn("Broken link: README.md -> docs/missing.md", errors)
        self.assertIn("Missing path mentioned in text: README.md -> .agents/skills/gone/SKILL.md", errors)

    def test_external_links_and_anchors_are_ignored(self):
        self.write("README.md", "[a](https://example.com/x) [b](#top) [c](mailto:x@example.com)\n")
        self.assertEqual(self.errors(), [])

    def test_links_may_not_escape_the_repository(self):
        self.write("README.md", "[up](../../outside.md)\n")
        self.assertIn("Broken link: README.md -> ../../outside.md", self.errors())


if __name__ == "__main__":
    unittest.main()
