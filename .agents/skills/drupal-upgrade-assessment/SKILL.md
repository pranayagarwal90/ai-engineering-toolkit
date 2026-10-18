---
name: drupal-upgrade-assessment
description: Assess a proposed Drupal core or contrib upgrade before implementation, including Composer conflicts, PHP compatibility, custom-code impact, and verification planning.
---

# Assess a Drupal upgrade

Follow [root guidance](../../../AGENTS.md) and select relevant pages through the [architecture map](../../../architecture/README.md). Use [maintenance command evidence](../../../architecture/maintenance.md); do not load unrelated skills.

**Scope:** read-only for application code, dependencies, configuration and database state. Do not interpret "assess", "can we upgrade" or selecting an agent as permission to update. If implementation is explicitly requested, finish this assessment and continue with the matching update skill.

## Inputs

- Exact package(s), requested target, environment and purpose.
- `composer.json`, `composer.lock`, installed metadata if present, and deployed-version evidence if supplied.

## Steps

1. **Pin down the target.**
   - If "latest" is requested, resolve a supported target from current official releases and state the lookup date.
   - If the target is unresolved, give conditional findings and ask for it. Never invent a version.
2. **Compare versions and sources.**
   - Label root constraints, locked, installed and deployed versions separately.
   - Read target metadata, official release notes, changelog, advisories and Drupal change records. Link sources; mark inaccessible ones unknown.
3. **Check platform requirements.**
   - Compare target PHP/extensions, Drupal core, Composer/plugins, Drush and dependent-package requirements with local and Docker/CI declarations.
   - Use scoped `composer show`/`prohibits`/`why`. Do not bypass platform checks or relax constraints as a shortcut.
4. **Find custom-code impact.**
   - Search only relevant custom modules, themes and config for package APIs, services, hooks, plugins, Twig inheritance and deprecated/removed APIs.
   - Inspect target update hooks, schema and config changes when available. Distinguish observed hooks from anticipated effects, and note hooks that change exported configuration (they need an export in the same change; see [config drift](../drupal-config-drift/SKILL.md)).
5. **Choose regression checks** from the development page, covering cache metadata, auth/access, editors, content imports, cron, external integrations or front-end behavior only where affected.
6. **Optionally dry-run the solver.**
   - Package-scoped, with scripts/plugins disabled; record the command, target and proposed transitive changes. Network/cache activity may occur.
   - Never run a real update, require, install, database update or cache rebuild here. Verify manifest and lock are unchanged.
   - If solving fails, preserve the blocker rather than widening scope.

## Output

**Current state**, **Target state**, **Compatibility findings**, **Risks**, **Proposed update procedure**, **Verification plan** and **Unknowns**. The procedure names exact packages/constraints, local database/config steps, backup/rollback needs and any separately scoped production work. Reuse this result during implementation instead of repeating discovery.
