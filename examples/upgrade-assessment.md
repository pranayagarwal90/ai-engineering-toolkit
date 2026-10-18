# Assessing a contributed module upgrade before touching Composer

Status: **synthetic walkthrough.** The package `drupal/example_seo`, its versions, hooks and services are invented to show the method. No real release, project or command output is described.

## The request

> Can we move `drupal/example_seo` to 2.1.0? Assess it; don't change anything yet.

This is an assessment request, so the [upgrade-assessment skill](../.agents/skills/drupal-upgrade-assessment/SKILL.md) applies. It is read-only: no `composer update`, no `drush updatedb` and no cache rebuild, and `composer.json` and `composer.lock` must be byte-for-byte unchanged afterwards.

## Evidence gathered

**Versions, labelled separately** (step 2 of the skill):

| Source | What it says |
| --- | --- |
| `composer.json` (root constraint) | `"drupal/example_seo": "^2.0"` |
| `composer.lock` (locked) | `2.0.2` |
| Installed metadata (`vendor/composer/installed.json`) | `2.0.2` |
| Deployed | Unknown: no deployment evidence was supplied |
| Target metadata (release page, read on the assessment date) | `2.1.0`, requires `drupal/core: ^10.3 \|\| ^11.1` and `php: >=8.2` |

**Platform** (step 3): the lockfile pins core `11.2.x`; the Dockerfile and CI use PHP 8.3. Both satisfy the target. A scoped check confirms nothing in the tree blocks the target:

```text
$ composer why-not drupal/example_seo 2.1.0
There is no installed package depending on "drupal/example_seo" in versions not matching 2.1.0
```

**Release notes and changes** (steps 2 and 4):
- `example_seo_update_20101()` renames the config key `defaults.title_pattern` to `defaults.title` in `example_seo.settings`. That changes exported configuration.
- The service `example_seo.token_helper` was removed; the notes point to `example_seo.token_resolver`.

**Custom code using the package** (step 4, scoped search of custom modules and themes only):

```text
web/modules/custom/site_meta/src/MetaBuilder.php:41:  $helper = \Drupal::service('example_seo.token_helper');
config/sync/example_seo.settings.yml:3:  title_pattern: '[node:title] | [site:name]'
```

**Dry run** (step 6, scripts and plugins disabled, nothing written):

```text
$ composer update drupal/example_seo --with-dependencies --dry-run --no-scripts --no-plugins
  - Upgrading drupal/example_seo (2.0.2 => 2.1.0)
$ git status --short composer.json composer.lock
(no output)
```

## The report the skill should produce

**Current state:** constraint `^2.0`; locked and installed `2.0.2`; deployed version unknown.

**Target state:** `2.1.0`. Core and PHP requirements are met by the lock (11.2.x) and the runtime (PHP 8.3). The constraint already allows it, so no `composer.json` change is needed.

**Compatibility findings:**
1. **Blocker for custom code:** `site_meta/src/MetaBuilder.php:41` calls the removed `example_seo.token_helper` service. After the update this throws `ServiceNotFoundException` wherever `MetaBuilder` runs.
2. **Exported configuration changes:** the update hook renames `title_pattern` in active configuration, but `config/sync/example_seo.settings.yml` still has the old key. Unless the export is committed with the update, the next config import writes the old key back.
3. The dry run proposes only this package; there are no transitive changes.

**Risks:**
- The page-title metadata path through `MetaBuilder` breaks until the code moves to `example_seo.token_resolver`.
- Configuration import would undo the hook's rename (see finding 2).
- Rolling back the code after the hook has run leaves renamed configuration that 2.0.2 does not understand. Rollback needs the pre-update database.

**Proposed update procedure** (for a separate, explicit implementation request):
1. Back up the local database and record the code revision.
2. Change `MetaBuilder` to inject `example_seo.token_resolver` through its constructor rather than `\Drupal::service()`.
3. `composer update drupal/example_seo --with-dependencies`, then review the `composer.lock` diff.
4. `drush updatedb -y`, `drush config:export -y`, and commit the `example_seo.settings.yml` change in the same commit. Confirm `drush config:status` shows no differences.
5. Production deployment is a separate, approved step.

**Verification plan:**
- Unit or kernel test for `MetaBuilder` with the new service.
- Page title on a node and on the front page, before and after.
- `drush updatedb:status` shows nothing pending; `config:status` is clean.
- The project's quality gate and Composer audit.

**Unknowns:** the deployed version, and whether any other site configuration overrides `title_pattern` (for example in `settings.php`).

## What a weak answer looks like

- Runs `composer update` "to see what happens", which changes the lock in assessment mode.
- Reports "compatible" from the core and PHP requirements alone and misses the removed service.
- Says nothing about the configuration rename, so the next deployment's import silently reverts it (see [the real case](unexpected-config-import.md)).
- Presents an assumed deployed version as fact.
