# AI Engineering Toolkit

Reusable agents, skills and prompts for AI-assisted development, maintenance and troubleshooting.

The toolkit includes Drupal workflows, language-independent SonarQube analysis, container image deployment and homelab operations. Future collections can cover DevOps, Python and other engineering use cases.

Created by Pranay Agarwal from workflows developed for a personal Drupal homelab/portfolio project. This public edition removes application-specific details and adds review and module-development procedures.

## What this demonstrates

- Separating shared instructions, specialist responsibilities, reusable procedures and task inputs.
- Loading only relevant context and grounding conclusions in code, configuration and logs.
- Distinguishing assessment from implementation and local checks from deployment evidence.
- Planning Drupal access, cacheability, configuration lifecycle and regression verification.

## Collection: Drupal

The [workflow map](.github/AI-WORKFLOWS.md) is the complete, validated list of skills, profiles and prompts.

| Profile | Skills |
| --- | --- |
| Drupal Maintenance | Upgrade assessment, core update, contrib update, configuration drift |
| Security Reviewer | Security advisory assessment/remediation |
| Incident Debugger | Log analysis, outage investigation |
| Drupal Code Reviewer | PR review |
| (none; root guidance) | Custom module development |

## Collection: Code quality (SonarQube)

Use the Code Quality Analyst profile with the [SonarQube analysis skill](.agents/skills/sonarqube-analysis/SKILL.md), [report analysis prompt](.github/prompts/analyze-sonarqube-report.prompt.md) or [selected-fixes prompt](.github/prompts/fix-sonarqube-findings.prompt.md). Start with supplied reports and relevant source; this toolkit does not install a scanner or connect to a server.

See the [worked quality-gate example](examples/sonarqube-quality-gate.md) for separating a code defect, coverage evidence and hotspot review.

## Collection: Deployment

The Release Engineer profile with the [pinned image deployment skill](.agents/skills/pinned-image-deployment/SKILL.md) covers two tasks: a read-only check for a newer image, and deploying by digest with backups, migrations, configuration import and verification. It also explains deployments that "succeeded" without changing what runs. Example: [a deployment that reported success](examples/deploy-reported-success.md) (real use, sanitized).

## Collection: Homelab operations

| Profile | Skills |
| --- | --- |
| Homelab Operator | [Health triage](.agents/skills/homelab-health-triage/SKILL.md), [container image updates](.agents/skills/container-image-updates/SKILL.md), [service changes](.agents/skills/homelab-service-change/SKILL.md) |

These assume a self-hosted Compose stack and record host specifics in [architecture/infrastructure.md](architecture/infrastructure.md). Example: [public URL down while private access worked](examples/public-url-one-relay-down.md) (real use, sanitized).

## Quick start

1. Review these instructions before copying them into a project. Merge existing AGENTS.md and CLAUDE.md guidance rather than overwriting it.
2. Copy the relevant .agents/skills/, .github/agents/ and .github/prompts/ files. Adapt the architecture references using [customization](docs/customization.md). For automatic skill discovery in Claude Code, also place the skills under .claude/skills/ ([tool compatibility](docs/tool-compatibility.md#claude-code-skill-discovery)).
3. In your coding assistant, ask: “Read AGENTS.md and .agents/skills/drupal-upgrade-assessment/SKILL.md. Assess the supplied package and target; do not apply updates.”
4. Supply the actual package/target and project evidence. Review the result and recorded checks.

[Tool compatibility](docs/tool-compatibility.md) explains manual entry points. These Markdown files do not run an autonomous service, provide tools or grant permissions.

## Examples and validation

[Upgrade assessment](examples/upgrade-assessment.md) and [code review](examples/code-review.md) are illustrative walkthroughs, not transcripts of measured production outcomes.

For a concrete problem and reusable investigation prompt, see [Fixing an edit form that crashes on a missing answer ID](examples/missing-answer-id.md). This worked example includes synthetic evidence, a conditional fix and a verification plan.

[A deployment's config import "changed" a setting nobody touched](examples/unexpected-config-import.md) is a sanitized real case: an update hook's key-order side effect, found by comparing stored, effective and exported configuration.

Run python3 scripts/validate_toolkit.py to check metadata, that every skill, profile and prompt is routed from the workflow map, internal links and repository paths quoted in prose. python3 -m unittest discover -s tests tests the validator itself. CI runs both. This does not evaluate model accuracy or prove workflows succeed in a live application.

## Behavior evaluation

[evals/](evals/README.md) holds fixed tasks with supplied evidence and Must/Must-not rubrics. Most come from the real incidents above. Run each case with and without its skill, then record the scores to see whether the skill changes what an assistant does. No results are recorded yet; the validator checks only that each case is well-formed.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), [roadmap](docs/roadmap.md) and [changelog](CHANGELOG.md). Share sanitized evidence and distinguish illustrative results from real executions.

MIT licensed. Review generated changes and use the target project's own tests before applying them.
