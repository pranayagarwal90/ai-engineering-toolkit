---
name: drupal-core-update
description: Perform an explicitly requested Drupal core Composer update with a bounded package plan, local database/config review, regression checks, and rollback reporting.
---

# Update Drupal core

Follow [shared rules](../../RULES.md) and the [project map](../../project/README.md). Use the [maintenance command reference](../../project/maintenance.md).

**Scope:** if implementation is not requested, use [upgrade assessment](../drupal-upgrade-assessment/SKILL.md) and stop at the plan. An explicit update request authorizes the scoped local work only: no deploy, push, merge or production change without explicit scope. Production release mechanics stay in the project's deployment runbook.

## Inputs

- The exact requested target and the authorized local environment.
- A current upgrade assessment, or enough evidence to complete one.

## Steps

1. **Confirm the target.**
   - Complete or reuse a current assessment. Verify the exact target and root core requirements rather than carrying a version forward from documentation.
   - Identify the core packages actually in the manifest; check each target's availability and compatibility instead of assuming all core-related packages share every release.
2. **Record the starting point.**
   - Starting diff, manifest/lock state, installed versions, local database/config state. Preserve unrelated work.
   - Before running update hooks locally, establish a recoverable database/files backup and the matching code revision using the project's backup documentation. This skill does not create one.
3. **Plan a targeted solver run.**
   - If the target is outside existing constraints, explain and make only the necessary manifest change.
   - Preview the exact package list and transitive changes. Unlock more dependencies only when the solver requires it, and explain added root-package changes.
   - No unqualified `composer update`; never ignore platform requirements.
4. **Apply locally and review.**
   - Review `composer.json`/`composer.lock`, scaffold changes, removals, plugins and unexpected transitive changes.
   - Never hand-edit core/vendor or force a failed solver result. Stop and report if the target needs an unrequested platform or major migration.
5. **Database and configuration.**
   - On the intended local database: inspect pending updates, apply required hooks, rebuild caches, check `config:status`.
   - If update hooks changed exported configuration, export it (`drush config:export`) and commit those `config/sync` files in the same change. `config:status` must then show no differences; otherwise every later deployment's import will "change" that item (see [config drift](../drupal-config-drift/SKILL.md)).
   - Import/export only reviewed configuration in the correct direction; never overwrite unrelated active configuration as a blanket step. Verify update status afterwards.
6. **Verify.**
   - Shared quality gate, relevant behavior/browser checks, platform requirements check and the CI-equivalent dependency audit.
   - Check the upgraded site and bounded logs. If prerequisites fail, report unverified behavior rather than success.

## Output

Exact before/after packages, changed constraints/scaffolds, database/config implications (including exported config), tests/audit results, unresolved risks and a rollback plan. Code rollback does not reverse update hooks: recovery may require the matching pre-update database/files.
