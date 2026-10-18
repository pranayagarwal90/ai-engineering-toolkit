---
name: drupal-contrib-update
description: Update an explicitly requested Drupal contributed module or theme through Composer after assessing compatibility, dependent packages, update hooks, and affected behavior.
---

# Update a contributed package

Follow [shared rules](../../RULES.md) and the [project map](../../project/README.md). Commands and environment selection come from [maintenance](../../project/maintenance.md).

**Scope:** without an implementation request, run [upgrade assessment](../drupal-upgrade-assessment/SKILL.md) only, and reuse an assessment already completed for this target. Deploying or changing production is separate from the local package update.

## Inputs

- Package, exact target and the authorized local environment.

## Steps

1. **Identify the package and its users.**
   - Resolve the Composer package name and the Drupal machine name; they may differ.
   - Compare declared, locked, installed and supplied deployed versions. Read the target's release notes, Drupal/PHP requirements, dependencies and conflicts.
   - Find enabled dependents and custom code/config/theme inheritance using the package, without scanning every extension.
2. **Record the starting point and the impact.**
   - Starting diff; protect existing changes.
   - Check whether target update/post-update hooks, schema, config defaults, permissions, removed services/plugins, editor assets or theme templates affect this site.
   - Identify database/files backup and code rollback requirements before local schema changes.
3. **Choose the smallest change.**
   - Smallest requested package/target set; preview the solver result.
   - Adjust only a blocking root constraint, and only when implementation is authorized. Do not broaden into a core upgrade or unrelated modules; report a concrete blocker and the proposed expansion instead.
4. **Apply locally.**
   - Package-scoped Composer update; review lockfile, transitive and scaffold changes. Never hand-edit contributed source or vendor.
   - Existing sites do not automatically adopt new install defaults; inspect actual changes.
5. **Database and configuration.**
   - Apply required hooks on the intended local site, rebuild caches and review `config:status`.
   - If hooks changed exported configuration, export it and commit the `config/sync` files in the same change, then confirm `config:status` is clean (see [config drift](../drupal-config-drift/SKILL.md)).
   - Otherwise export only intended changes or import reviewed repository config. Verify no updates remain pending. Do not uninstall/reinstall the extension to simulate an update.
6. **Verify.**
   - `composer quality` (if defined), the CI-equivalent audit/platform check and behavior tests.
   - Exercise the extension's integration where affected, for example consent gating, editor plugins, cache behavior or theme inheritance. Record failures and missing prerequisites.

## Output

Before/after versions, constraint and transitive changes, update-hook/config impact (including exported config), affected regression coverage, audit results, unknowns and recovery requirements. If update hooks ran, reverting the package alone may not restore compatibility.
