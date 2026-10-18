I haven't run anything. I can't reach your host from here, so nothing below has been executed. Because you asked to update everything, I'll recreate the routine updates. Two things in the evidence change how I'd go about it.

**Two items I won't do as part of "update everything":**
- **Postgres 16 → 17 is a major version upgrade.** Changing the pin isn't enough: version 17 can't read version 16's data directory, so the data has to be dumped and restored or run through `pg_upgrade`. That needs its own planned migration. Keeping `postgres:16` still picks up 16.x patch releases. I'd check whether the pull brought a newer 16.x image and apply it only if it did.
- **I won't prune the 40 GB of unused images.** Some of those are the old images we'd roll back to. Pruning can wait until you've confirmed everything works.

**There are no recent backups, so I'll take one first.** The photo app's migrations will change its database, and rolling back an app with migrations means restoring the database too.

## Plan and commands

**1. Health check before changing anything**, so problems that already exist don't get blamed on the update:
```bash
docker compose ps -a
docker compose logs --since 30m --tail 50
```
If anything is already unhealthy, I'd stop and report it before going on.

**2. Backup**, into a dated folder that routine backup cleanup won't delete:
```bash
B=/srv/backups/manual/2026-10-18-pre-update; mkdir -p "$B"
docker compose exec -T postgres pg_dumpall -U <db_user> > "$B/postgres.sql"
# Also copy the photo app's data volume (its database-related state; also the upload library if space allows):
docker run --rm -v <photos_volume>:/src:ro -v "$B":/dst alpine tar czf /dst/photos-data.tgz -C /src .
```
I'd check that the dump isn't empty (`head`, `ls -lh`) before going on.

**3. Read the photos v1.121.0 release notes** for breaking changes and any required Postgres or extension versions. If something requires manual steps, I'd stop and ask you.

**4. Recreate in batches, checking logs after each one:**
```bash
# a. stateless
docker compose up -d --no-deps dashboard && docker compose logs --tail 50 dashboard
# b. data stores (the photo app will blink briefly)
docker compose up -d --no-deps redis && docker compose exec redis redis-cli ping
#    postgres: only if the pulled postgres:16 image ID differs from the running one
# c. app with migrations: change the pin to photos:v1.121.0 in compose, then
docker compose up -d --no-deps photos
docker compose logs -f photos | grep -iE 'migrat|error'
# d. tunnel last
docker compose up -d --no-deps tunnel && docker compose logs --tail 50 tunnel   # look for "Registered tunnel connection"
```
The tunnel goes last because it's your public access path. If it fails to reconnect, nothing else has changed, and the old image is still there to roll back to.

**5. Finish:** run the health check again and confirm no container is running an older image than its tag points to. Then commit the photos pin change on a branch.

## Rollback
- **dashboard, redis, tunnel:** retag the old image ID, then `docker compose up -d --no-deps <svc>`.
- **photos:** once its migrations have run, going back to the old image also means restoring `postgres.sql` from step 2.

## Expected result
| Service | Old | New | Result |
| --- | --- | --- | --- |
| dashboard | old image ID | new image ID | not run yet |
| redis | 7.4.1 | 7.4.2 | not run yet |
| postgres | 16.4 | newer 16.x if available | 17 deferred to a planned migration |
| photos | v1.120.1 | v1.121.0 | not run yet, after backup and release notes |
| tunnel | old | new | not run yet, last |

**Still needs a decision from you:** the Postgres 17 migration, and pruning old images after you've confirmed everything works. If you run these steps yourself, send me the output from the backup and the photos migration logs and I'll check them.
