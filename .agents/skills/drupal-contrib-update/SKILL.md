---
name: drupal-contrib-update
description: Update an explicitly requested Drupal contributed module or theme through Composer after assessing compatibility, dependent packages, update hooks, and affected behavior.
---

# Update a contributed package

Follow [root guidance](../../../AGENTS.md) and the [architecture map](../../../architecture/README.md). Commands and environment selection come from [maintenance](../../../architecture/maintenance.md). Without an implementation request, run [upgrade assessment](../drupal-upgrade-assessment/SKILL.md) only; reuse an assessment already completed for this target.

1. Resolve the extension's Composer package name and Drupal machine name; they may differ. Compare declared, locked, installed and supplied deployed versions. Inspect the target release notes, Drupal/PHP requirements, dependencies and conflicts. Identify enabled dependents and custom code/config/theme inheritance using the package, rather than scanning all extensions.
2. Record the starting diff and protect existing changes. Determine whether target update/post-update hooks, schema, config defaults, permissions, removed services/plugins, editor assets, or theme templates affect this site. Identify database/files backup and code rollback requirements before local schema changes.
3. Select the smallest requested package/target set. Preview the solver result using the maintenance reference. Adjust only a blocking root constraint when implementation authorizes it; do not broaden into a core upgrade or update unrelated modules. If wider changes are required, report the concrete dependency blocker and proposed expansion.
4. Apply the package-scoped Composer update locally, review lockfile/transitive/scaffold changes, and never hand-edit contributed source or vendor. Existing-site configuration does not automatically adopt every new install default; inspect actual changes.
5. Inspect pending database updates on the intended local site, apply required hooks, rebuild cache and review active/exported configuration differences. Export only intended config changes or import reviewed repository config as appropriate; verify pending updates are resolved. Do not uninstall/reinstall the extension to simulate an update.
6. Run `composer quality`, the CI-equivalent audit/platform check and behavior tests from the maintenance/development map. Exercise the extension's integration: for example consent gating, editor plugins, cache behavior, or theme inheritance where affected. Record failures and missing prerequisites.

Report before/after versions, constraint and transitive changes, update-hook/config impact, affected regression coverage, audit results, unknowns and recovery requirements. If update hooks ran, reverting the package alone may not restore compatibility. Deploying or changing production is separate from the local package update.
