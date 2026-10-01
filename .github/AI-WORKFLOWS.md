# Workflow map

Select one row. Read root guidance, relevant architecture and the selected skill; inspect source before acting. No automatic handoffs or scheduled actions are configured.

| Task | Profile | Skill |
| --- | --- | --- |
| [Assess Drupal upgrade](prompts/assess-drupal-upgrade.prompt.md) | [drupal-maintenance](agents/drupal-maintenance.agent.md) | [drupal-upgrade-assessment](../.agents/skills/drupal-upgrade-assessment/SKILL.md) |
| [Update Drupal core](prompts/update-drupal-core.prompt.md) | [drupal-maintenance](agents/drupal-maintenance.agent.md) | [drupal-core-update](../.agents/skills/drupal-core-update/SKILL.md) |
| [Update contributed package](prompts/update-drupal-contrib.prompt.md) | [drupal-maintenance](agents/drupal-maintenance.agent.md) | [drupal-contrib-update](../.agents/skills/drupal-contrib-update/SKILL.md) |
| [Assess or apply security update](prompts/apply-drupal-security-update.prompt.md) | [security-reviewer](agents/security-reviewer.agent.md) | [drupal-security-update](../.agents/skills/drupal-security-update/SKILL.md) |
| [Analyze Drupal logs](prompts/analyze-drupal-logs.prompt.md) | [incident-debugger](agents/incident-debugger.agent.md) | [drupal-log-analysis](../.agents/skills/drupal-log-analysis/SKILL.md) |
| [Investigate application error](prompts/investigate-application-error.prompt.md) | [incident-debugger](agents/incident-debugger.agent.md) | [drupal-log-analysis](../.agents/skills/drupal-log-analysis/SKILL.md) |
| [Investigate site outage](prompts/investigate-site-outage.prompt.md) | [incident-debugger](agents/incident-debugger.agent.md) | [site-outage-investigation](../.agents/skills/site-outage-investigation/SKILL.md) |
| [Review Drupal PR](prompts/review-drupal-pr.prompt.md) | [drupal-code-reviewer](agents/drupal-code-reviewer.agent.md) | [drupal-pr-review](../.agents/skills/drupal-pr-review/SKILL.md) |
| [Develop Drupal module](prompts/develop-drupal-module.prompt.md) | Shared development guidance | [drupal-custom-module-development](../.agents/skills/drupal-custom-module-development/SKILL.md) |
| [Analyze SonarQube report](prompts/analyze-sonarqube-report.prompt.md) | [Code Quality Analyst](agents/code-quality-analyst.agent.md) | [SonarQube analysis](../.agents/skills/sonarqube-analysis/SKILL.md) |
| [Fix selected SonarQube findings](prompts/fix-sonarqube-findings.prompt.md) | [Code Quality Analyst](agents/code-quality-analyst.agent.md) | [SonarQube analysis](../.agents/skills/sonarqube-analysis/SKILL.md) |

See [tool compatibility](../docs/tool-compatibility.md) for explicit-path usage. Selecting a prompt does not authorize deployment or production changes.
