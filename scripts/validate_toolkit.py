"""Validate toolkit metadata and local Markdown links; no model evaluation."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
errors = []
skills = list(root.glob(".agents/skills/*/SKILL.md"))
agents = list(root.glob(".github/agents/*.agent.md"))
prompts = list(root.glob(".github/prompts/*.prompt.md"))
for collection, count, label in ((skills, 8, "skills"), (agents, 4, "profiles"), (prompts, 9, "prompts")):
    if len(collection) != count:
        errors.append(f"{label}: expected {count}, found {len(collection)}")
for path in skills + agents + prompts:
    content = path.read_text()
    front = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    required = ("description",) if path in prompts else ("name", "description")
    if not front or any(not re.search(rf"^{key}: .+", front.group(1), re.M) for key in required):
        errors.append(f"Missing metadata: {path.relative_to(root)}")
    if path in skills and front:
        name = re.search(r"^name: (.+)$", front.group(1), re.M)
        if name and (name.group(1) != path.parent.name or not re.fullmatch(r"[a-z0-9-]{1,64}", name.group(1))):
            errors.append(f"Invalid skill name: {path.relative_to(root)}")
for path in root.rglob("*.md"):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (path.parent / target.split("#")[0]).resolve()
        if not resolved.is_relative_to(root) or not resolved.exists():
            errors.append(f"Broken/local external link: {path.relative_to(root)} -> {target}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(skills)} skills, {len(agents)} profiles, {len(prompts)} prompts and local Markdown links.")
