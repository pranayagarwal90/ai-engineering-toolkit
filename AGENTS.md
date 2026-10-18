# Working on this repository

This repository is the toolkit itself: reusable Markdown skills, profiles and prompts, plus a validator and an installer. It contains no application.

- **Rules for using the toolkit** are in [.agents/RULES.md](.agents/RULES.md), and they apply here too. When you test a skill against an evaluation case or example, follow the skill as a user's assistant would.
- **Layout:**
  - `.agents/` is everything an installed skill needs: `skills/`, `RULES.md` and the `project/` templates.
  - `.github/agents/` holds profiles and `.github/prompts/` holds prompts (Copilot formats).
  - `.github/AI-WORKFLOWS.md` routes tasks to them.
- **Keep skills self-contained.** A skill may link only inside `.agents/` or to full URLs, so it still works after `scripts/install.py` copies it into another project.
- **Before finishing a change,** run `python3 -m unittest discover -s tests` and `python3 scripts/validate_toolkit.py`. Add the change under **Unreleased** in the changelog.
- **Sanitize.** Examples and evaluation cases must not contain real hostnames, IP addresses, registry paths, IDs, domains or personal data. Label each one as illustrative, synthetic or real use.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for the skill format and the pull-request flow.
