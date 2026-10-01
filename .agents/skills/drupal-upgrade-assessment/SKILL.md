---
name: drupal-upgrade-assessment
description: Assess a proposed Drupal core or contrib upgrade before implementation, including Composer conflicts, PHP compatibility, custom-code impact, and verification planning.
---

# Assess a Drupal upgrade

Follow [root guidance](../../../AGENTS.md) and select relevant pages through the [architecture map](../../../architecture/README.md). Use [maintenance command evidence](../../../architecture/maintenance.md); do not load unrelated skills.

This procedure is read-only for application code, dependencies, configuration, and database state. It must not change dependencies unless the user explicitly requests implementation; then complete the assessment and use the corresponding update skill. Do not interpret “assess,” “can we upgrade,” or selecting an agent as permission to update.

1. Establish the exact package(s), requested target, environment, and purpose. If “latest” is requested, resolve a supported target from current official releases and state the lookup date. If unresolved, give conditional findings and ask for the missing target; never invent a version.
2. Compare root constraints in `composer.json`, locked versions in `composer.lock`, installed metadata if present, and deployed evidence if supplied. Label each separately. Inspect target metadata and official release notes, changelog, advisories, and Drupal change records; link sources and mark inaccessible sources unknown.
3. Check target PHP/extensions, Drupal core, Composer/plugin, Drush, and dependent-package requirements against local and Docker/CI declarations. Use the scoped show/prohibits/why commands. Do not bypass platform checks or relax constraints as an assessment shortcut.
4. Search only relevant custom modules/themes/config for package APIs, services, hooks, plugins, Twig inheritance, and deprecated/removed APIs. Inspect target update hooks/schema/config changes when available; distinguish observed hooks from anticipated effects.
5. Identify regression surfaces and select existing checks from the development page. Include cache metadata, auth/access, editors, content imports, cron, external integrations, or front-end behavior only where affected.
6. If useful and feasible, perform a package-scoped dry run with scripts/plugins disabled, recording the command, target and proposed transitive changes. Network/cache activity may occur; never run a real update, require, install, database update, or cache rebuild in assessment mode. Verify manifest/lock remain unchanged. If solving fails, preserve the blocker rather than widening scope automatically.

Return: **Current state**, **Target state**, **Compatibility findings**, **Risks**, **Proposed update procedure**, **Verification plan**, and **Unknowns**. The proposed procedure must identify exact packages/constraints, local database/config steps, backup/rollback needs, and any separately scoped production work. Reuse this result during implementation rather than repeating discovery.
