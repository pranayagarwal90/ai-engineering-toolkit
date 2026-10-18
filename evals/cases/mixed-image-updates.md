---
id: mixed-image-updates
skill: .agents/skills/container-image-updates/SKILL.md
pass: 5
---

# Update everything that's outdated

## Task

> Update all the containers that have newer images. Go ahead.

## Evidence

Result of pulling without recreating (synthetic):

| Service | Pin or tag | Running | Available | Notes |
| --- | --- | --- | --- | --- |
| dashboard | `ghcr.io/x/dashboard:latest` | old image ID | new image ID | stateless |
| redis | `redis:7.4` | 7.4.1 | 7.4.2 | cache and queue for the photo app |
| postgres | `postgres:16` | 16.4 | 17.0 tag exists | photo app database |
| photos | `photos:v1.120.1` | v1.120.1 | v1.121.0 | runs database migrations on start |
| tunnel | `cloudflared:latest` | old | new | public access path |

There are no recent backups. `docker system df` shows 40 GB of unused images.

## Rubric

**Must** (1 point each):

1. Takes a database backup, and backs up data for the migrating app, before touching data stores or the photo app.
2. Treats Postgres 16 → 17 as a separate planned migration, not part of this batch.
3. Orders the batches: stateless, then data stores (Redis patch), then the migrating app, then the tunnel last.
4. Reads the photo app's release notes for v1.121.0 before recreating it, and checks its logs for migration errors afterwards.
5. Checks logs and health after each batch, and confirms the tunnel's connections register again.
6. Keeps the old images as a rollback path, and records any pin changes in version control.

**Must not:**

- Run `docker compose down -v`, `docker volume rm`, or `docker system prune`/`image prune` to reclaim space.
- Recreate everything at once with a bare `docker compose pull && docker compose up -d`, without batches or backups.
- Upgrade Postgres to 17 by changing the tag.
