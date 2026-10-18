## The deploy reinstalled the old image

**What the log shows:**

- You set `IMAGE_VAR=registry.example/blog@sha256:bbb2...` in your shell, but the script printed `Image: registry.example/blog@sha256:aaa1...`. It pulled `aaa1`, which was "up to date", and recreated the container from that same image.
- The script reads `IMAGE_VAR` from the Compose environment file, not from your shell. A plain `VAR=...` on its own line isn't exported, so the script never saw it. Even `export` wouldn't have changed the file, so the next `up` or reboot would still use `aaa1`.
- `No pending updates.` fits this. The Drupal core update is in `bbb2`, so the old code had no new database updates to run.
- "Site responded with HTTP 200" only shows the site is up. The script never checked that the running image was the one you meant to deploy, so it reported "complete" anyway.

**Something else to check:** `config:status` showed `google_tag.container.ga4 | Update`. Your active config differs from the exported config in code, probably because someone changed it in the admin UI. The log doesn't show whether a config import ran. When you redeploy, the import will overwrite that GA4 setting with the version in code, so first decide which version you want to keep.

**Not yet confirmed:** that `bbb2` is the build with the core update and that its CI build passed. I haven't run anything.

## Checks to run first (read-only)

```bash
# What the running container actually uses
docker inspect --format '{{.Image}} {{index .Config.Labels "org.opencontainers.image.revision"}}' <drupal-container>

# What the next restart would use (images only, no secrets printed)
docker compose config --images

# The target's digest and revision, without pulling
docker buildx imagetools inspect registry.example/blog@sha256:bbb2...

# The GA4 difference
drush config:status
drush config:diff google_tag.container.ga4   # if config_diff is available
```

I expect the first two to show `aaa1`. If the third shows a revision that includes the core update and CI passed for it, `bbb2` is safe to deploy.

## How to fix it (when you ask me to deploy)

Redeploying changes production, so I'll wait for your go-ahead. The steps would be:

1. Back up the database and uploaded files, and note `aaa1` and `bbb2` next to the backup.
2. Change only the `IMAGE_VAR` line in the env file. I'd use a one-line in-place edit (for example `sed -i 's|^IMAGE_VAR=.*|IMAGE_VAR=registry.example/blog@sha256:bbb2...|' <env-file>`) so I never open or print the file. Then confirm `docker compose config --images` shows `bbb2`.
3. Run `bash scripts/deploy.sh`. This time `drush updatedb` should run the core update.
4. Check that the running container's digest and the pin are both `bbb2`, that there are no pending updates, that the config status is clean, and that the key pages load.

I'd also suggest a small change to `scripts/deploy.sh`: fail the deploy if the running container's digest doesn't match the intended one. That would stop it saying "complete" after redeploying the old image.

Do you want me to go ahead with the redeploy, and should the GA4 setting come from code or from what's live now?
