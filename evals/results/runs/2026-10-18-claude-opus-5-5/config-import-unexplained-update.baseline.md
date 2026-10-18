**Short version:** Nobody changed Google Tag through the UI. The update came from a three-week-old drift between the database and `config/sync`, and the `Update` line does not mean tracking is broken. Whether GA actually fires depends on `settings.php` and the environment variable, and import never touches that.

## Why the import showed `Update`

1. **The update hook wrote to active config.** `example_update_11001()` used `getEditable()->save()`, which changes the config stored in the database. The script for that deploy skipped config import, so nothing reconciled the database with `config/sync` at the time.
2. **The database and the YAML have differed ever since.** The hook's write and the file aren't byte-for-byte the same. Either the YAML was committed or changed separately, or the stored structure differs. One possibility is key order: the hook appends `visitor_condition` after `request_path`, while the YAML lists it first, and Drupal's comparison treats that as a difference.
3. **This deploy ran import, so `config/sync` won.** The database now matches the committed YAML. Because the YAML already contains `visitor_condition: {negate: false}`, the import most likely kept the hook's intent rather than reverting it.

The `status: false` and `G-XXXXXXXXXX` values in the YAML are not the cause. The `settings.php` lines are runtime overrides. They are never saved to the database, never exported, and never appear in import diffs. Import didn't "turn GA off."

## Is tracking broken?

Probably not. GA is enabled only when `GA_MEASUREMENT_ID` is set to a valid `G-…` ID **in the PHP process**. If that variable is missing, tracking is off no matter what the import did. I'd check:

```bash
# Effective config, including the settings.php override
drush cget google_tag.container.ga4 status --include-overridden
drush cget google_tag.container.ga4 tag_container_ids --include-overridden

# Is the env var visible to PHP (not just your shell)?
drush php:eval 'var_dump(getenv("GA_MEASUREMENT_ID"));'

# Confirm the tag is on a public page (anonymous, non-/admin)
curl -s https://your-site.example/ | grep -o 'googletagmanager.com/gtag/js?id=G-[A-Z0-9]*'

# Confirm nothing is still drifting
drush config:status
```

Keep in mind that `drush php:eval` runs through the CLI. If PHP-FPM has `clear_env = yes` or gets its variables from somewhere else, the web process might not see `GA_MEASUREMENT_ID` even when Drush does. The `curl` check is the one that tells you what visitors actually get. Real-time reports in GA4 will also show whether hits are arriving.

## Finding exactly what changed

The diff is gone now that import has run. To reconstruct it, compare `git log -p config/sync/google_tag.container.ga4.yml` over the last three weeks with a pre-deploy database backup (`drush cget` on a restored copy). If the `config_log` or a similar module is installed, it will have recorded the change.

## Preventing a repeat

- When an update hook edits config, run `drush cex` afterward and commit the YAML in the same change.
- Make every deploy run the same sequence (`drush deploy`, which does `updb` → `cim` → `cr` → `deploy:hook`), so no deploy leaves the database and sync out of step.
- Add a CI or post-deploy check that `drush config:status` reports no differences.
