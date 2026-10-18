I'll update most of these now, but I'm handling three differently.

**Postgres: not upgrading to 17.** Your pin is `postgres:16`, so a pull won't move you to 17. Moving would mean changing the major version, and Postgres 17 can't read a 16 data directory. That needs a dump and restore or `pg_upgrade`, and with no backup a mistake could destroy the photo database. Postgres stays on 16.4 unless you ask for a planned major upgrade.

**Photos: backup first, then update.** v1.121.0 runs database migrations on start, and those usually can't be undone. Since there are no backups, I'll dump the database before recreating it.

**Unused images: not pruning yet.** The 40 GB includes the old images, which are your fastest way to roll back. I'll prune once everything has run well for a day or two.

### What I'd run

```bash
# 1. Back up the photo database (needed before the photos migration)
mkdir -p ~/backups
docker compose exec -T postgres pg_dumpall -U postgres | gzip > ~/backups/pg-$(date +%F-%H%M).sql.gz
ls -lh ~/backups/   # confirm the file exists and isn't tiny
# (If photos has an upload/library volume, snapshot or rsync it too if you can)

# 2. Note current image IDs so we can roll back
docker compose images > ~/backups/images-before-$(date +%F).txt

# 3. Low-risk updates
docker compose up -d dashboard
docker compose up -d redis          # 7.4.1 -> 7.4.2 patch; brief queue/cache blip

# 4. Photos, after the backup is confirmed
docker compose up -d photos
docker compose logs -f photos       # watch the migrations finish cleanly

# 5. Tunnel last
docker compose up -d cloudflared
docker compose logs --tail=50 cloudflared   # confirm "Registered tunnel connection"
```

The tunnel goes last because it's your public access path. If you're connected through it and the new version fails to come up, you'll lose remote access. Run step 5 from the local network or over a separate SSH path if you can.

### If photos breaks after migrating
Re-pin `photos:v1.120.1`, restore the dump into a fresh Postgres volume, and bring it back up. Don't just roll back the image, because the old version may not work with a database that has already been migrated.

When this is done, I'd strongly suggest a scheduled nightly `pg_dumpall` so the next update doesn't start without a backup. I can set that up if you'd like.
