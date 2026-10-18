---
name: container-image-updates
description: Find and safely apply container image updates for a self-hosted Compose stack - floating tags and version pins - with backups, batch ordering, migration checks and rollback; also for designing safe automatic updates.
---

# Update container images

Follow [root guidance](../../../AGENTS.md) and the project's [infrastructure](../../../architecture/infrastructure.md) page.

**Scope:** finding updates is read-only. Recreating always-on services needs approval; an explicit "update everything" counts. Major versions of databases and apps with migrations are planned migrations, not routine updates. Never delete volumes or prune images as part of an update.

## Inputs

- The Compose files and how services are pinned (floating tags such as `latest`/`stable`, or explicit versions).
- Which services hold data or run migrations, and the backup procedure.

## Steps

1. **Start healthy.** Run the [triage](../homelab-health-triage/SKILL.md) sweep first, so pre-existing failures are not blamed on the update.
2. **Find what is outdated.**
   - Floating tags: pull without recreating, then compare each running container's image ID with the image its tag now points to.
   - Pinned versions: list newer tags from the registry. Patch releases are routine; majors are separate migrations.
   - A pin changed in Compose shows as unchanged until the container is recreated.
   - Stopped on-demand apps pick up new images on their next start.
3. **Read release notes** for anything that runs migrations (photo libraries, cloud suites, document managers, workflow tools, databases) and for every major-version jump.
4. **Back up first.** Database dumps, plus data volumes for apps with migrations, in a dated folder that the routine backup retention will not delete.
5. **Recreate in batches, checking logs after each:**
   1. Stateless services.
   2. Data stores (Redis, MariaDB, Postgres). Dependent apps blink briefly.
   3. Apps with migrations. Search their logs for migration messages and errors.
   4. Apps with their own upgrade tooling (for example Nextcloud `occ status`): check maintenance mode and pending upgrades before and after.
   5. Tunnels and proxies last, confirming their connections register again.
6. **Leave special cases to their own path:** locally built images (rebuild them), application images deployed by digest ([pinned image deployment](../pinned-image-deployment/SKILL.md)), and native or host-installed apps.
7. **Finish.** Run triage again; confirm no running container is behind its tag; record pin changes in version control on a branch. Keep the old images until the user confirms, as the rollback path.

## Automatic updates

Automate only services that are stateless and run no migrations; opt them in explicitly (for example with a label). Each automatic update should:
- take only minor and patch versions for pinned services
- health-check the new container, wait a soak period and probe its HTTP endpoint
- roll back to the previous pin on failure, and stop updating anything else that run if a rollback fails
- commit the pin bump only after success, and notify a person of the outcome

## Output

A table of service, old version, new version and result; backups taken; migrations observed; anything left for a person, such as majors and services with their own path.
