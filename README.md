# AI Engineering Toolkit

Reusable agents, skills and prompts for AI-assisted development, maintenance and troubleshooting.

The initial collection focuses on Drupal. Future collections can cover homelab operations, DevOps, Python and other engineering use cases.

Created by Pranay Agarwal from workflows developed for a personal Drupal homelab/portfolio project. This public edition removes application-specific details and adds review and module-development procedures.

## What this demonstrates

- Separating shared instructions, specialist responsibilities, reusable procedures and task inputs.
- Loading only relevant context and grounding conclusions in code, configuration and logs.
- Distinguishing assessment from implementation and local checks from deployment evidence.
- Planning Drupal access, cacheability, configuration lifecycle and regression verification.

## Initial collection: Drupal

Four specialist profiles, eight skills and nine prompts. Browse the [workflow map](.github/AI-WORKFLOWS.md).

| Profiles | Skills |
| --- | --- |
| Drupal Maintenance | Upgrade assessment, core update, contrib update |
| Security Reviewer | Security advisory assessment/remediation |
| Incident Debugger | Log analysis, outage investigation |
| Drupal Code Reviewer | PR review |
| Shared development guidance | Custom module development |

## Quick start

1. Review these instructions before copying them into a project. Merge existing AGENTS.md and CLAUDE.md guidance rather than overwriting it.
2. Copy the relevant .agents/skills/, .github/agents/ and .github/prompts/ files. Adapt the architecture references using [customization](docs/customization.md).
3. In your coding assistant, ask: “Read AGENTS.md and .agents/skills/drupal-upgrade-assessment/SKILL.md. Assess the supplied package and target; do not apply updates.”
4. Supply the actual package/target and project evidence. Review the result and recorded checks.

[Tool compatibility](docs/tool-compatibility.md) explains manual entry points. These Markdown files do not run an autonomous service, provide tools or grant permissions.

## Examples and validation

[Upgrade assessment](examples/upgrade-assessment.md) and [code review](examples/code-review.md) are illustrative walkthroughs, not transcripts of measured production outcomes.

Run python3 scripts/validate_toolkit.py to check metadata, internal links and expected file counts. CI runs the same structural check. This does not evaluate model accuracy or prove workflows succeed in a live Drupal application.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), [roadmap](docs/roadmap.md) and [changelog](CHANGELOG.md). Share sanitized evidence and distinguish illustrative results from real executions.

MIT licensed. Review generated changes and use the target project's own tests before applying them.
