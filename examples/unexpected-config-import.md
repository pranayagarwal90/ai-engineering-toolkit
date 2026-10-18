# A deployment's config import "changed" a setting nobody touched

Status: **real use, sanitized.** This happened on a personal Drupal 11 site in October 2026. Identifiers are replaced with placeholders; the commands and their results are the ones observed.

## The problem

A routine deployment printed this before importing configuration:

```text
| Collection | Config                   | Operation |
|            | google_tag.container.ga4 | Update    |
```

Nobody had edited analytics settings, and the release did not touch them. The owner's question was simple: *why did Google Tag change, and did tracking break?*

## Investigation with the toolkit

Prompt: [investigate-config-drift](../.github/prompts/investigate-config-drift.prompt.md), skill: [drupal-config-drift](../.agents/skills/drupal-config-drift/SKILL.md).

**Three views of the item** (step 2 of the skill):

| View | `status` | `tag_container_ids` |
| --- | --- | --- |
| Sync (`config/sync` in the image) | `false` | `G-XXXXXXXXXX` placeholder |
| Stored, after the import | `false` | `G-XXXXXXXXXX` placeholder |
| Effective (`--include-overridden`) | `true` | the real measurement ID |

`settings.php` enables the container and sets the real ID from an environment variable. That override is never stored, so the import could not remove it. The live page still loaded the real ID: **tracking was never affected.**

**What actually differed** (steps 3 and 4): the stored value taken from a database backup made just before the deployment had exactly the same values as `config/sync`. The only difference was the order of two keys under `conditions`. The deployment log from three weeks earlier showed why:

- That deployment ran a custom module's update hook, which added a `conditions.<visitor_condition>` entry with the config API. The hook appended it **after** the existing `request_path` condition.
- The exported YAML lists the visitor condition **first**.
- That deployment used a script that skipped config import, so the reordered value stayed in active configuration until the next deployment that imported config.

Drupal compares the serialized data, so a reordered mapping counts as an "Update".

## Outcome

- **Direction** (step 5): the repository was right; the import only restored the exported key order. No action was needed on the site.
- **Prevention** (step 6), adopted in both the application and infrastructure repositories:
  - A rule in the development guide: an update hook that changes exported configuration ships with `drush config:export` output in the same commit, and `config:status` must be clean afterwards.
  - A single deployment script that always imports configuration and logs `config:status` immediately before the import, so any future "Update" is visible and explained.
- The next deployment's import reported **"No differences between DB and sync directory."**

## Takeaways

- An import "Update" is a prompt to compare stored, effective and sync values, not proof that a setting changed.
- Runtime overrides survive imports; check them with `--include-overridden` before worrying.
- Deployments that sometimes skip config import let update-hook side effects sit in active config and surface weeks later as unexplained changes.
