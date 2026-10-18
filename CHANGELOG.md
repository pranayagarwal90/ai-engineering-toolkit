# Changelog

## Unreleased

Nothing yet.

## 0.4.0 — 2026-10-18

- **Self-contained skills.** The rules every skill follows moved from the repository's `AGENTS.md` into `.agents/RULES.md`, and the project templates moved from `architecture/` to `.agents/project/`. Skills link only inside `.agents/` or to full URLs, so copying them into another project no longer breaks references. The validator enforces this.
- **Installer:** `scripts/install.py` copies selected collections for Claude Code (`.claude/`), Copilot (`.agents/` plus `.github/agents` and `.github/prompts`) or Codex. It adds linked skills, keeps existing files unless `--force`, never overwrites filled-in project pages, and supports `--dry-run` and `--list`. Its tests check that every link resolves after installing, for every client and collection.
- **Root `AGENTS.md`** now covers only working on this repository. Drupal coding conventions moved into the development project page.
- **README** rewritten for new users: what the toolkit is, a 5-minute trial using an evaluation case, installation, one collections table and the repository layout. Tool compatibility explains that profiles are Copilot custom agents and that Claude Code uses the skills directly.
- **First evaluation results** (Claude Code CLI, claude-opus-5-5, single runs). Baseline: 1 of 5 cases passed, 22/32 points, 2 secret-file violations. With skills: 5 of 5 passed, 29/32 points, no violations. Limits are stated in `evals/results/2026-10-18-claude-opus-5-5.md`.
- **`evals/run_claude.py`** reruns the cases in isolated headless sessions (baseline, with skill, blind grade) and stores raw answers and grades.
- After that run: the `deploy-reported-success` rubric item about config import was reworded, since its evidence cannot prove the import ran, and `pinned-image-deployment` now recommends both deploy guards explicitly.
- **Fuller examples:** `upgrade-assessment.md` (versions per source, dry run, a removed service, a config rename, the complete report, what a weak answer looks like) and `code-review.md` (a cache-context leak traced to a concrete trigger, findings, fix, verification plan).

## 0.3.0 — 2026-10-18

- Behavior evaluation cases (`evals/`): five fixed tasks with evidence and Must/Must-not rubrics, four of them from real incidents, a baseline-versus-skill method and a results template. The validator checks each case's structure. No results are recorded yet.
- Validator no longer hard-codes file counts. It checks that every skill, profile and prompt is routed from the workflow map, that profile names are unique, and that repository paths quoted in prose exist. It also accepts CRLF frontmatter, and CI now runs its unit tests.
- Restructured every skill into Inputs, Steps (with sub-bullets) and Output, keeping its rules.
- Drupal update and module-development skills: an update hook that changes exported configuration must ship with the matching export, and `config:status` must be clean; environment-specific values belong in `settings.php` overrides.
- New `drupal-config-drift` skill, `investigate-config-drift` prompt and a sanitized real-use example (`examples/unexpected-config-import.md`).
- New Deployment collection: Release Engineer profile, `pinned-image-deployment` skill, `check-for-newer-image` and `deploy-pinned-image` prompts, and a real-use example.
- New Homelab operations collection: Homelab Operator profile; `homelab-health-triage`, `container-image-updates` and `homelab-service-change` skills; three prompts; an `architecture/infrastructure.md` template; and a real-use example.
- Corrected the README and roadmap counts; documented Claude Code skill discovery; added issue templates and skill-writing structure to the contribution guide.

## 0.2.0

Added language-independent SonarQube analysis: Code Quality Analyst profile, analysis skill, two prompts, report-input reference and illustrative quality-gate walkthrough. Updated workflow routing and validation counts.

## 0.1.0 — prepared for initial publication

Adapted six homelab skills and three profiles for public reuse. Added a code-review profile, PR-review and custom-module skills, nine prompt entry points, documentation, illustrative examples and structural validation.
