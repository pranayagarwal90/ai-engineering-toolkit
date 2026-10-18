---
name: drupal-config-drift
description: Investigate unexpected Drupal configuration differences, such as config:import listing changes nobody made, settings that revert after a deployment, or active configuration that disagrees with config/sync.
---

# Investigate configuration drift

Follow [shared rules](../../RULES.md) and the [project map](../../project/README.md). Use [maintenance](../../project/maintenance.md) for the project's Drush command prefix.

**Scope:** read-only until a direction is agreed. Do not run `config:import`, `config:export`, `config:set` or a UI save on any environment without explicit scope, and never on production as a diagnostic step. Configuration can hold secrets: redact values such as keys and tokens in anything you report.

## Inputs

- The configuration names involved (from `config:status`, an import preview or a deployment log) and the environment.
- Recent deployments, update hooks, module installs, UI changes and database restores, with timing.
- The repository revision whose `config/sync` was, or will be, imported.

## Steps

1. **Capture before acting.** Record `drush config:status` and, for each item, the stored value (`drush config:get <name>`). Do not import yet: an import rewrites the evidence.
2. **Compare three views of each item.**
   - **Stored (active)** value: `config:get <name>`. This is what `config:status` and imports compare.
   - **Effective** value: `config:get <name> --include-overridden`, which adds `settings.php` `$config[...]` overrides. Overrides are never stored, so an import cannot remove them.
   - **Sync** value: the YAML in `config/sync` at the revision being deployed (not the local working tree).
3. **Classify the difference.**
   - Real value change, or only key order or formatting. Drupal reports a reordered mapping as a change.
   - Dependencies, `uuid` or `langcode` only.
   - An environment-specific value (IDs, hosts, credentials) that should never be in `config/sync`.
4. **Find what wrote the stored value.** Check, with evidence:
   - Update or post-update hooks that edited configuration with the config API. They do not normalize key order the way an export does. Check update logs from deployments.
   - A deployment that ran database updates but skipped config import, leaving the hook's version in place.
   - Saves through the admin UI, `drush config:set`, module installs or cron jobs that write configuration.
   - A database restore from before or after the export.
5. **Decide the direction, and say why.**
   - **The repository is right:** importing is safe. List exactly what it changes.
   - **The active value is intended:** export it in the development repository, commit `config/sync`, and deploy normally. Do not export from production into Git without review.
   - **The value is environment-specific:** keep a placeholder (or disabled state) in `config/sync` and apply the real value with a `settings.php` override from an environment variable.
6. **Prevent recurrence.** Recommend the relevant rules:
   - An update hook that changes exported config ships with the matching export in the same commit, and `config:status` is clean afterwards.
   - Every deployment imports configuration, and logs `config:status` just before importing.
   - Environment-specific values stay out of `config/sync`.

## Output

A table per item: name, stored vs effective vs sync summary (redacted), classification, writer (evidence or "unknown"), recommended direction and risk. Then the prevention steps, and the exact commands that were run (read-only) versus proposed.

See the [unexpected config import example](https://github.com/pranayagarwal90/ai-engineering-toolkit/blob/main/examples/unexpected-config-import.md) for a real case.
