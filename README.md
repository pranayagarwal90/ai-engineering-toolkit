# AI Engineering Toolkit

Skills, prompts and agent profiles that make AI coding assistants (Claude Code, GitHub Copilot, Codex) work like a careful engineer on maintenance and operations tasks. They gather evidence before concluding, stay read-only until asked to change something, never touch secrets, and report what they actually verified.

They cover Drupal maintenance, SonarQube triage, container deployments and self-hosted (homelab) operations. Each procedure comes from real incidents on a production Drupal site and home server, written up as sanitized examples.

It is plain Markdown: nothing runs on its own, and nothing gets permissions it would not already have.

## Try it in 5 minutes

Compare an assistant with and without a skill on a real incident:

```bash
git clone https://github.com/pranayagarwal90/ai-engineering-toolkit.git
cd ai-engineering-toolkit
```

1. Open [evals/cases/deploy-reported-success.md](evals/cases/deploy-reported-success.md) and copy its **Task** and **Evidence** sections, but not the rubric.
2. **Without the skill:** paste them into an assistant session started outside this folder.
3. **With the skill:** start a session inside this folder and ask:
   > Read .agents/RULES.md and .agents/skills/pinned-image-deployment/SKILL.md, then answer the following. Do not open the evals folder.

   Then paste the same text.
4. Score both answers against the case's **Rubric**. [evals/](evals/README.md) explains how to record results.

## Use it in your project

```bash
python3 scripts/install.py --list                                          # collections and skills
python3 scripts/install.py ~/code/my-site --client claude --collection drupal --dry-run
python3 scripts/install.py ~/code/my-site --client claude --collection drupal
```

- `--client` is `claude`, `copilot` or `codex`. See [tool compatibility](docs/tool-compatibility.md) for where each puts files.
- Skills that a selected skill links to are installed too.
- Existing files are kept unless you pass `--force`, and your filled-in project pages are never overwritten.

Then:

1. Add one line to your `CLAUDE.md` or `AGENTS.md`: `Follow .claude/RULES.md` (or `.agents/RULES.md`).
2. Fill in the installed `project/` pages with your project's facts. See [customization](docs/customization.md).
3. Ask for a task as usual. Claude Code picks a skill by its description; with other clients, name the skill's path.

## Collections

| Collection | Skills | Profile (Copilot agent) | Real-use example |
| --- | --- | --- | --- |
| **Drupal** | [upgrade assessment](.agents/skills/drupal-upgrade-assessment/SKILL.md), [core update](.agents/skills/drupal-core-update/SKILL.md), [contrib update](.agents/skills/drupal-contrib-update/SKILL.md), [config drift](.agents/skills/drupal-config-drift/SKILL.md), [security advisory](.agents/skills/drupal-security-update/SKILL.md), [log analysis](.agents/skills/drupal-log-analysis/SKILL.md), [site outage](.agents/skills/site-outage-investigation/SKILL.md), [PR review](.agents/skills/drupal-pr-review/SKILL.md), [module development](.agents/skills/drupal-custom-module-development/SKILL.md) | Drupal Maintenance, Security Reviewer, Incident Debugger, Drupal Code Reviewer | [Config import "changed" a setting nobody touched](examples/unexpected-config-import.md) |
| **Code quality** | [SonarQube analysis](.agents/skills/sonarqube-analysis/SKILL.md) | Code Quality Analyst | [Quality-gate walkthrough](examples/sonarqube-quality-gate.md) (illustrative) |
| **Deployment** | [Pinned image deployment](.agents/skills/pinned-image-deployment/SKILL.md): check for a newer image, deploy by digest, explain a deploy that changed nothing | Release Engineer | [Deploy reported success, site unchanged](examples/deploy-reported-success.md) |
| **Homelab** | [Health triage](.agents/skills/homelab-health-triage/SKILL.md), [container image updates](.agents/skills/container-image-updates/SKILL.md), [service changes](.agents/skills/homelab-service-change/SKILL.md) | Homelab Operator | [Public URL down, private access fine](examples/public-url-one-relay-down.md) |

The [workflow map](.github/AI-WORKFLOWS.md) routes each task to its prompt, profile and skill.

## How it is organized

| Piece | Where | Purpose |
| --- | --- | --- |
| Skills | `.agents/skills/<name>/SKILL.md` | Step-by-step procedures: scope, inputs, steps, output |
| Shared rules | [.agents/RULES.md](.agents/RULES.md) | Scope, secrets and evidence rules every skill follows |
| Project pages | [.agents/project/](.agents/project/README.md) | Templates for your project's facts (paths, checks, hosts) |
| Profiles | `.github/agents/*.agent.md` | Roles that route to skills, in Copilot's custom-agent format. Claude Code uses the skills directly. |
| Prompts | `.github/prompts/*.prompt.md` | Copilot prompt files that start a task with the right inputs |
| Evaluation cases | [evals/](evals/README.md) | Fixed tasks with rubrics, to check whether a skill changes behavior |

## Examples

Real use, sanitized:
- [Config import "changed" a setting nobody touched](examples/unexpected-config-import.md)
- [A deploy reported success, but the site was unchanged](examples/deploy-reported-success.md)
- [Public URL down after a reboot, private access fine](examples/public-url-one-relay-down.md)

Synthetic walkthroughs:
- [Edit form crashes on a missing answer ID](examples/missing-answer-id.md)
- [SonarQube quality gate](examples/sonarqube-quality-gate.md)
- [Assessing a module upgrade before touching Composer](examples/upgrade-assessment.md)
- [Reviewing a personalized greeting: a cache leak in five lines](examples/code-review.md)

## Evaluation

[evals/](evals/README.md) holds five cases, four of them from the real incidents above, each run with and without its skill. First results (Claude Code, claude-opus-5-5, single runs): **without skills 1 of 5 cases passed, with skills 5 of 5**. Two baseline answers proposed reading the secrets file; no skill answer did. See the [write-up and its limits](evals/results/2026-10-18-claude-opus-5-5.md).

## Development

```bash
python3 -m unittest discover -s tests   # validator and installer tests
python3 scripts/validate_toolkit.py     # metadata, routing, links, self-contained skills, eval structure
```

CI runs both on every push and pull request. See [CONTRIBUTING.md](CONTRIBUTING.md), the [roadmap](docs/roadmap.md) and the [changelog](CHANGELOG.md).

## License

MIT. Created by Pranay Agarwal. Review what an assistant proposes and run your project's own tests before applying changes.
