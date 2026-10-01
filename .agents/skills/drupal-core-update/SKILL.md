---
name: drupal-core-update
description: Perform an explicitly requested Drupal core Composer update with a bounded package plan, local database/config review, regression checks, and rollback reporting.
---

# Update Drupal core

Follow [root guidance](../../../AGENTS.md) and the [architecture map](../../../architecture/README.md). Use the [maintenance command reference](../../../architecture/maintenance.md). If implementation is not requested, use [upgrade assessment](../drupal-upgrade-assessment/SKILL.md) and stop at the plan; an existing explicit update request is sufficient authorization for the scoped local work.

1. Complete or reuse a current upgrade assessment. Verify the exact target and root core requirements instead of carrying forward an old version from documentation. Identify the core packages actually present in the target manifest; verify each target's availability and compatibility rather than assuming all core-related packages share every release.
2. Record the starting diff, manifest/lock state, installed versions and local database/config state. Preserve unrelated work. Before applying update hooks to a local site, establish a recoverable database/files backup and the matching code revision using the existing backup/deployment documentation; no backup is created by this skill file itself.
3. Plan a targeted solver run. If the requested target is outside existing constraints, explain and make only the necessary manifest change within authorized implementation. Preview the exact package list and required transitive changes. Use broader dependency unlocking only when the solver requires it; explain added root-package changes. Do not run an unqualified Composer update or ignore platform requirements.
4. Apply the scoped Composer update locally, review `composer.json`/`composer.lock`, generated scaffold changes, removals, plugins, and unexpected transitive changes. Never hand-edit core/vendor or force a failed solver result. Stop and report a blocker if the target requires an unrequested platform/major migration.
5. On the intended local test database, inspect pending updates, apply required update hooks, rebuild caches, and inspect configuration drift. Import/export only reviewed configuration in the correct direction; never overwrite unrelated active configuration as a blanket upgrade step. Verify update status afterward.
6. Run the shared quality gate, relevant behavior/browser checks, platform requirements check, and CI-equivalent dependency audit from the maintenance/development pages. Check the upgraded site and bounded logs. If prerequisites fail, report unverified behavior rather than claiming success.

Report exact before/after packages, changed constraints/scaffolds, database/config implications, tests/audit results, unresolved risks, and rollback plan. Code rollback does not reverse update hooks: recovery may require the matching pre-update database/files. Do not deploy, push, merge, or mutate production without explicit scope; production release mechanics remain in the existing deployment runbook.
