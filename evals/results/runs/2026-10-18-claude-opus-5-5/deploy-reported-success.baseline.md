The deploy ran successfully, but it **redeployed the old image** (`sha256:aaa1...`) instead of your new one (`sha256:bbb2...`).

## What went wrong

```text
$ IMAGE_VAR=registry.example/blog@sha256:bbb2...
$ bash scripts/deploy.sh
Image: registry.example/blog@sha256:aaa1...
```

Two things kept your value from reaching the deploy:

1. **The variable was never exported.** `IMAGE_VAR=...` on its own line sets a shell-local variable. `bash scripts/deploy.sh` starts a child process that can't see it. (`IMAGE_VAR=... bash scripts/deploy.sh` on one line, or `export IMAGE_VAR=...`, would pass it.)
2. **The script reads `IMAGE_VAR` from the Compose environment file anyway.** Even an exported value may be ignored or overridden, depending on how the script loads that file. The file still contains `aaa1`.

The rest of the output fits this:

- `Image is up to date ... aaa1` means it pulled the image that was already running.
- `No pending updates.` means the database update step ran against the old code, so the Drupal core update never ran.
- `Site responded with HTTP 200` is the only success check. It shows the site is up, not which release is live, so the script said "complete" with the old version.

One thing to look at: `google_tag.container.ga4 | Update` shows a config import changed something on the old code. It's probably harmless, but it may be a config change meant for the new release being applied early, or something being reverted. Check it after redeploying.

## How to fix it

1. Check what the env file and the running container actually contain:
   ```bash
   grep IMAGE_VAR .env          # or whichever env file deploy.sh / compose uses
   docker compose ps
   docker compose images
   ```
2. Update the env file to the new digest. Editing the file is the reliable fix, since that's what the script reads:
   ```bash
   sed -i 's|^IMAGE_VAR=.*|IMAGE_VAR=registry.example/blog@sha256:bbb2...|' .env
   ```
   Use the full digest, not the truncated one.
3. Redeploy and check that the `Image:` line shows `bbb2...`:
   ```bash
   bash scripts/deploy.sh
   ```
   This time `updatedb` should list pending core updates rather than "No pending updates."
4. Confirm the new release is live:
   ```bash
   docker compose exec <drupal-service> drush status --field=drupal-version
   ```

Because the release includes a core update with database updates, take a DB backup before step 3 if the script doesn't do that already.

## Preventing this next time

I'd suggest a small change to `deploy.sh`: fail if the image digest it resolved doesn't match an expected digest passed in as an argument, and check the Drupal version after deploy instead of relying only on HTTP 200. Either check would have stopped this run. I can draft that if you'd like.
