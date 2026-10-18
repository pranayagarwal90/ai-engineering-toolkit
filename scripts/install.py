"""Install toolkit skills into another project (or your home directory) for a given client.

    python3 scripts/install.py --list
    python3 scripts/install.py ~/code/my-site --client claude --collection drupal --dry-run
    python3 scripts/install.py ~/code/my-site --client copilot --collection homelab deployment

Layouts:
  claude   .claude/skills/<name>/, .claude/RULES.md, .claude/project/
  copilot  .agents/skills/<name>/, .agents/RULES.md, .agents/project/, plus matching
           .github/agents/*.agent.md profiles and .github/prompts/*.prompt.md prompts
  codex    .agents/skills/<name>/, .agents/RULES.md, .agents/project/  (also the generic layout)

Skills that a selected skill links to are installed too. Existing files are kept unless --force;
project pages (your filled-in facts) are never overwritten. Nothing is written with --dry-run.
"""
import argparse
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".agents"
COLLECTIONS = {
    "drupal": [
        "drupal-upgrade-assessment", "drupal-core-update", "drupal-contrib-update", "drupal-config-drift",
        "drupal-security-update", "drupal-log-analysis", "site-outage-investigation", "drupal-pr-review",
        "drupal-custom-module-development",
    ],
    "code-quality": ["sonarqube-analysis"],
    "deployment": ["pinned-image-deployment"],
    "homelab": ["homelab-health-triage", "container-image-updates", "homelab-service-change"],
}
CLIENT_BASE = {"claude": ".claude", "copilot": ".agents", "codex": ".agents"}
SKILL_LINK = re.compile(r"\]\(\.\./([a-z0-9-]+)/SKILL\.md")
GITHUB_SKILL_LINK = re.compile(r"\.agents/skills/([a-z0-9-]+)/SKILL\.md")
GITHUB_PROFILE_LINK = re.compile(r"\]\(\.\./agents/([\w.-]+\.agent\.md)\)")


def skill_dependencies(names):
    """The selected skills plus every skill they link to, transitively."""
    selected, pending = set(), list(names)
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        skill = AGENTS_DIR / "skills" / name / "SKILL.md"
        if not skill.exists():
            raise ValueError(f"Unknown skill: {name}")
        selected.add(name)
        pending.extend(SKILL_LINK.findall(skill.read_text(encoding="utf-8")))
    return selected


def github_files(skills):
    """Profiles and prompts whose every linked skill (and profile) is being installed."""
    profiles = [p for p in sorted((ROOT / ".github/agents").glob("*.agent.md"))
                if set(GITHUB_SKILL_LINK.findall(p.read_text(encoding="utf-8"))) <= skills
                and GITHUB_SKILL_LINK.search(p.read_text(encoding="utf-8"))]
    names = {p.name for p in profiles}
    prompts = []
    for p in sorted((ROOT / ".github/prompts").glob("*.prompt.md")):
        text = p.read_text(encoding="utf-8")
        if set(GITHUB_SKILL_LINK.findall(text)) <= skills and set(GITHUB_PROFILE_LINK.findall(text)) <= names \
                and GITHUB_SKILL_LINK.search(text):
            prompts.append(p)
    return profiles, prompts


def plan(target, client, skills):
    """List of (source, destination, kind) where kind is 'skill', 'rules', 'project' or 'github'."""
    base = target / CLIENT_BASE[client]
    items = [(AGENTS_DIR / "RULES.md", base / "RULES.md", "rules")]
    for page in sorted((AGENTS_DIR / "project").glob("*.md")):
        items.append((page, base / "project" / page.name, "project"))
    for name in sorted(skills):
        for src in sorted((AGENTS_DIR / "skills" / name).rglob("*")):
            if src.is_file():
                items.append((src, base / "skills" / name / src.relative_to(AGENTS_DIR / "skills" / name), "skill"))
    if client == "copilot":
        profiles, prompts = github_files(skills)
        items += [(p, target / ".github/agents" / p.name, "github") for p in profiles]
        items += [(p, target / ".github/prompts" / p.name, "github") for p in prompts]
    return items


def install(target, client, skills, force=False, dry_run=False, out=print):
    actions = []
    for src, dest, kind in plan(target, client, skills):
        if dest.exists() and (kind == "project" or not force):
            action = "keep"
        else:
            action = "overwrite" if dest.exists() else "create"
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
        actions.append((action, dest))
        out(f"{action:9} {dest.relative_to(target).as_posix()}")
    return actions


def next_steps(client):
    base = CLIENT_BASE[client]
    entry = "CLAUDE.md" if client == "claude" else "AGENTS.md"
    return (f"\nNext steps:\n"
            f"  1. Add to your {entry}: \"Follow {base}/RULES.md. Project facts for the skills are in {base}/project/.\"\n"
            f"  2. Fill in {base}/project/*.md with your project's facts (they are templates).\n"
            f"  3. Ask your assistant for a task; it can also read a skill by path, e.g. {base}/skills/<name>/SKILL.md.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", nargs="?", type=Path, help="Project directory (or ~ for personal Claude skills).")
    parser.add_argument("--client", choices=sorted(CLIENT_BASE), default="claude")
    parser.add_argument("--collection", nargs="+", default=[], choices=sorted(COLLECTIONS) + ["all"])
    parser.add_argument("--skill", nargs="+", default=[], help="Individual skills, in addition to collections.")
    parser.add_argument("--force", action="store_true", help="Overwrite installed skills and rules (never project pages).")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written; write nothing.")
    parser.add_argument("--list", action="store_true", help="List collections and their skills.")
    args = parser.parse_args(argv)

    if args.list:
        for name, skills in COLLECTIONS.items():
            print(f"{name}: {', '.join(skills)}")
        return 0
    if args.target is None or not (args.collection or args.skill):
        parser.error("give a target directory and at least one --collection or --skill (see --list)")
    target = args.target.expanduser().resolve()
    if not target.is_dir():
        parser.error(f"{target} is not a directory")
    if target == ROOT:
        parser.error("refusing to install the toolkit into itself")

    names = list(args.skill)
    for collection in args.collection:
        names += [s for c in COLLECTIONS.values() for s in c] if collection == "all" else COLLECTIONS[collection]
    skills = skill_dependencies(names)
    extra = sorted(skills - set(names))
    print(f"{'Dry run: ' if args.dry_run else ''}installing {len(skills)} skill(s) for {args.client} into {target}")
    if extra:
        print(f"Also installing linked skills: {', '.join(extra)}")
    install(target, args.client, skills, force=args.force, dry_run=args.dry_run)
    print(next_steps(args.client))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
