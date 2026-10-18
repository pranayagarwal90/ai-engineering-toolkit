---
id: config-import-unexplained-update
skill: .agents/skills/drupal-config-drift/SKILL.md
pass: 7
---

# Config import lists a change nobody made

## Task

> Our deploy just printed `google_tag.container.ga4 | Update` before importing configuration. Nobody touched analytics. Why did Google Tag change, and is tracking broken?

## Evidence

The deployment log contains this import preview:

```text
| Collection | Config                   | Operation |
|            | google_tag.container.ga4 | Update    |
 [notice] Synchronized configuration: update google_tag.container.ga4.
```

`config/sync/google_tag.container.ga4.yml` (abridged):

```yaml
status: false
tag_container_ids:
  - G-XXXXXXXXXX
conditions:
  visitor_condition: { id: visitor_condition, negate: false }
  request_path: { id: request_path, negate: true, pages: "/admin\n/admin/*" }
```

`settings.php`:

```php
$id = strtoupper(trim((string) getenv('GA_MEASUREMENT_ID')));
if (preg_match('/^G-[A-Z0-9]+$/', $id)) {
  $config['google_tag.container.ga4']['status'] = TRUE;
  $config['google_tag.container.ga4']['tag_container_ids'] = [$id];
}
```

A deployment three weeks earlier ran this update hook, using a script that skips config import:

```php
function example_update_11001(): void {
  $config = \Drupal::configFactory()->getEditable('google_tag.container.ga4');
  $config->set('conditions.visitor_condition', ['id' => 'visitor_condition', 'negate' => FALSE])->save();
}
```

## Rubric

**Must** (1 point each):

1. Explains that the real ID and enabled state come from a `settings.php` override that is never stored, so an import cannot remove it.
2. Proposes checking the effective value with `config:get ... --include-overridden`, or the live page, before concluding tracking broke.
3. Identifies the update hook as what wrote the stored value, through a deployment that skipped config import.
4. Identifies that the hook appended `visitor_condition` after `request_path`, so the stored key order differs from the export.
5. States that a reordered mapping is reported as an "Update" even when the values are equal.
6. Concludes the import restored the exported order and that no change to the site is needed.
7. Recommends exporting configuration in the same commit as such update hooks, and keeping `config:status` clean.
8. Recommends that every deployment imports configuration and logs `config:status` before importing.

**Must not:**

- Run or recommend `config:import`, `config:export` or `config:set` on production as a diagnostic step.
- Claim the measurement ID was lost or tracking is broken without checking the effective value.
- Recommend putting the real measurement ID into `config/sync`.
