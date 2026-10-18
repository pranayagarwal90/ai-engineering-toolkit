"""Tests for scripts/install.py: installs the real toolkit files into temporary projects."""
import contextlib
import io
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import install  # noqa: E402

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def broken_links(target):
    """Relative Markdown links in installed files that do not resolve inside the target."""
    broken = []
    for path in target.rglob("*.md"):
        for link in LINK.findall(path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith(("#", "mailto:")):
                continue
            resolved = (path.parent / link.split("#")[0]).resolve()
            if not resolved.is_relative_to(target.resolve()) or not resolved.exists():
                broken.append(f"{path.relative_to(target)} -> {link}")
    return broken


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, client, skills, **kwargs):
        return install.install(self.target, client, install.skill_dependencies(skills), out=lambda _: None, **kwargs)

    def test_every_skill_belongs_to_exactly_one_collection(self):
        listed = [s for skills in install.COLLECTIONS.values() for s in skills]
        on_disk = sorted(p.name for p in (install.AGENTS_DIR / "skills").iterdir() if p.is_dir())
        self.assertEqual(sorted(listed), on_disk)
        self.assertEqual(len(listed), len(set(listed)))

    def test_all_links_resolve_after_install_for_every_client(self):
        everything = [s for skills in install.COLLECTIONS.values() for s in skills]
        for client in install.CLIENT_BASE:
            with self.subTest(client=client), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                install.install(target, client, install.skill_dependencies(everything), out=lambda _: None)
                self.assertEqual(broken_links(target), [])

    def test_each_collection_is_self_contained_for_copilot(self):
        for name, skills in install.COLLECTIONS.items():
            with self.subTest(collection=name), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                install.install(target, "copilot", install.skill_dependencies(skills), out=lambda _: None)
                self.assertEqual(broken_links(target), [])

    def test_claude_layout(self):
        self.run_install("claude", ["drupal-config-drift"])
        base = self.target / ".claude"
        self.assertTrue((base / "skills/drupal-config-drift/SKILL.md").exists())
        self.assertTrue((base / "RULES.md").exists())
        self.assertTrue((base / "project/maintenance.md").exists())
        self.assertFalse((self.target / ".github").exists())

    def test_linked_skills_are_included(self):
        self.assertIn("pinned-image-deployment", install.skill_dependencies(["container-image-updates"]))

    def test_copilot_installs_only_profiles_and_prompts_whose_skills_are_present(self):
        self.run_install("copilot", ["sonarqube-analysis"])
        self.assertEqual(sorted(p.name for p in (self.target / ".github/agents").iterdir()),
                         ["code-quality-analyst.agent.md"])
        self.assertEqual(sorted(p.name for p in (self.target / ".github/prompts").iterdir()),
                         ["analyze-sonarqube-report.prompt.md", "fix-sonarqube-findings.prompt.md"])

    def test_dry_run_writes_nothing(self):
        actions = self.run_install("claude", ["homelab-health-triage"], dry_run=True)
        self.assertTrue(actions)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_existing_files_are_kept_and_project_pages_never_overwritten(self):
        page = self.target / ".claude/project/infrastructure.md"
        skill = self.target / ".claude/skills/homelab-health-triage/SKILL.md"
        for path in (page, skill):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("mine", encoding="utf-8")
        self.run_install("claude", ["homelab-health-triage"])
        self.assertEqual(page.read_text(encoding="utf-8"), "mine")
        self.assertEqual(skill.read_text(encoding="utf-8"), "mine")
        self.run_install("claude", ["homelab-health-triage"], force=True)
        self.assertEqual(page.read_text(encoding="utf-8"), "mine")
        self.assertNotEqual(skill.read_text(encoding="utf-8"), "mine")

    def test_unknown_skill_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown skill"):
            install.skill_dependencies(["nope"])

    def test_cli_requires_a_selection_and_refuses_the_toolkit_itself(self):
        for argv in ([str(self.target)], [str(install.ROOT), "--collection", "deployment"]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                install.main(argv)


if __name__ == "__main__":
    unittest.main()
