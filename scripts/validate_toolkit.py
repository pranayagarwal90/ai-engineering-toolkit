"""Validate toolkit structure: metadata, workflow routing and local paths. No model evaluation.

Checks:
- every skill, profile and prompt has the required frontmatter; skill names match their folder
- profile names are unique
- every skill, profile and prompt is reachable from .github/AI-WORKFLOWS.md
- Markdown links and repository paths written in prose (.agents/..., .github/...) exist
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_MAP = ".github/AI-WORKFLOWS.md"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# Repository paths mentioned in prose or copyable prompts, e.g. ".agents/skills/x/SKILL.md".
PROSE_PATH = re.compile(r"(?<![\w./-])((?:\.agents|\.github)/[\w./-]*\w)")
SKILL_NAME = re.compile(r"[a-z0-9-]{1,64}")


def read(path):
    return path.read_text(encoding="utf-8")


def frontmatter(text):
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def collections(root):
    return {
        "skills": sorted(root.glob(".agents/skills/*/SKILL.md")),
        "profiles": sorted(root.glob(".github/agents/*.agent.md")),
        "prompts": sorted(root.glob(".github/prompts/*.prompt.md")),
    }


def markdown_files(root):
    return sorted(p for p in root.rglob("*.md") if ".git" not in p.relative_to(root).parts)


def check_metadata(root, found):
    errors, names = [], {}
    for label, paths in found.items():
        required = ("description",) if label == "prompts" else ("name", "description")
        for path in paths:
            rel = path.relative_to(root).as_posix()
            fields = frontmatter(read(path))
            if fields is None:
                errors.append(f"Missing frontmatter: {rel}")
                continue
            for key in required:
                if not fields.get(key):
                    errors.append(f"Missing '{key}' metadata: {rel}")
            name = fields.get("name", "")
            if label == "skills" and name and (name != path.parent.name or not SKILL_NAME.fullmatch(name)):
                errors.append(f"Skill name must be lowercase-hyphenated and match its folder: {rel}")
            if label == "profiles" and name:
                if name.lower() in names:
                    errors.append(f"Duplicate profile name '{name}': {rel} and {names[name.lower()]}")
                names[name.lower()] = rel
    return errors


def check_routing(root, found):
    workflow_map = root / WORKFLOW_MAP
    if not workflow_map.exists():
        return [f"Missing {WORKFLOW_MAP}"]
    routed = {(workflow_map.parent / target.split("#")[0]).resolve()
              for target in LINK.findall(read(workflow_map)) if "://" not in target}
    return [f"Not routed from {WORKFLOW_MAP}: {path.relative_to(root).as_posix()}"
            for paths in found.values() for path in paths if path.resolve() not in routed]


def check_paths(root):
    errors = []
    for path in markdown_files(root):
        rel = path.relative_to(root).as_posix()
        text = read(path)
        for target in LINK.findall(text):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"Broken link: {rel} -> {target}")
        for mention in PROSE_PATH.findall(text):
            if not (root / mention).exists():
                errors.append(f"Missing path mentioned in text: {rel} -> {mention}")
    return errors


def validate(root=ROOT):
    root = Path(root)
    found = collections(root)
    errors = check_metadata(root, found) + check_routing(root, found) + check_paths(root)
    return errors, {label: len(paths) for label, paths in found.items()}


def main():
    errors, counts = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validated {skills} skills, {profiles} profiles, {prompts} prompts, routing and local paths.".format(**counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
