---
name: drupal-custom-module-development
description: Design and implement a requested Drupal custom module or feature using the target repository's conventions, access rules, configuration and verification workflow.
---

# Develop a custom Drupal module

Follow [shared rules](../../RULES.md) and the [project map](../../project/README.md), especially [development](../../project/development.md).

**Scope:** implement within the user's request. Do not deploy, publish or claim production validation without evidence and scope.

## Inputs

- Requirement and acceptance criteria, target project, Drupal/PHP versions, document root, enabled dependencies, authorized environment.

## Steps

1. **Understand the context.** Read related implementation; ask only for decisions that materially block implementation.
2. **Choose the design.** Reuse an existing module when appropriate. Pick services, routes/forms, plugins, configuration or entities by behavior, not a fixed skeleton; explain significant dependencies and tradeoffs.
3. **Plan the lifecycle.**
   - Access, validation, translation and cacheability.
   - Secrets and environment-specific values (IDs, hosts, keys) stay out of exported configuration; apply them with `settings.php` overrides so a config import cannot remove them.
   - How existing installations receive changes: install defaults alone do not update them. An update hook that changes exported config must ship with the matching `config/sync` export in the same commit, and `config:status` must be clean afterwards.
4. **Implement the smallest complete feature.** Dependency injection and Drupal APIs; permissions, schema and libraries only where required. Preserve unrelated work.
5. **Verify.** Choose meaningful existing checks; add regression tests where the behavior warrants them. Cover denied-access and invalid-input paths alongside the successful one. Run database/config operations only on the intended environment.

## Output

Changed behavior, file responsibilities, checks actually run, setup/update steps (including config export/import) and limitations.
