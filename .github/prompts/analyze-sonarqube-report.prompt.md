---
description: Analyze SonarQube findings and quality-gate conditions without modifying code.
---

Read [root guidance](../../AGENTS.md), [Code Quality Analyst](../agents/code-quality-analyst.agent.md) and [SonarQube analysis](../../.agents/skills/sonarqube-analysis/SKILL.md).

Inputs: Report excerpt/export, relevant source, analysis revision, branch/PR and gate conditions. Analysis only.
Follow the selected skill; distinguish findings from confirmed defects and hotspots from vulnerabilities. Never suppress rules or weaken the quality gate to pass. Report actual checks and whether reanalysis confirmed resolution. Do not run a network scan, post comments or change server issue status without explicit scope.
