# Changelog

## Unreleased

- Validator no longer hard-codes file counts. It checks that every skill, profile and prompt is routed from the workflow map, that profile names are unique, and that repository paths quoted in prose exist. It also accepts CRLF frontmatter, and CI now runs its unit tests.
- Corrected the README and roadmap counts; documented Claude Code skill discovery; added issue templates and skill-writing structure to the contribution guide.

## 0.2.0

Added language-independent SonarQube analysis: Code Quality Analyst profile, analysis skill, two prompts, report-input reference and illustrative quality-gate walkthrough. Updated workflow routing and validation counts.

## 0.1.0 — prepared for initial publication

Adapted six homelab skills and three profiles for public reuse. Added a code-review profile, PR-review and custom-module skills, nine prompt entry points, documentation, illustrative examples and structural validation.
