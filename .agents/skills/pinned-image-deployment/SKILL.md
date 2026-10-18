---
name: pinned-image-deployment
description: Check for and deploy a newer container image of an application by digest, with backups, migrations, config import and verification; also explains a deploy that "succeeded" but left the old version running.
---

# Deploy a pinned container image

Follow [shared rules](../../RULES.md) and the project's [infrastructure](../../project/infrastructure.md) and [operations](../../project/operations.md) pages for hosts, Compose files and service names.

**Scope:** "is there a newer image?" is read-only. A deployment changes production: run it only when explicitly asked, and prefer the project's existing deployment script over ad-hoc commands. Never read or print environment files that hold secrets; change the image pin only through a tool that edits that one line.

## Inputs

- The application image repository and the target: a branch tag (for example `main`), an immutable commit tag (`sha-<7>`), a commit SHA or a digest.
- Where the running service's image reference is defined (Compose file, environment file, orchestrator manifest) and how the project deploys.

## Steps

1. **Read the current state.**
   - Running image reference and its revision label (`org.opencontainers.image.revision`).
   - The pinned reference the next restart would use, from the Compose/env source of truth. Use `docker compose config --images`, never a full `config` that prints interpolated secrets.
   - If they differ, report it: a restart would change the running version.
2. **Resolve the target without pulling.** Read the registry digest and revision label (for example `docker buildx imagetools inspect <ref>`). A moving tag is not a version; record the digest.
3. **Decide whether there is anything to deploy.**
   - Target digest equals the running one: stop with "nothing to deploy". Fix only a stale pin if needed.
   - Otherwise list the commits between the running and target revisions, and confirm the CI build for the target succeeded.
   - For "check only" requests, report here and stop.
4. **Prepare.**
   - Pull by digest and confirm the pulled revision label matches the registry and any requested commit.
   - Back up the application database and uploaded files, and record old and new image references next to the backup.
5. **Pin where restarts read it.** Write the digest to the single source of truth (for example the image variable in the Compose environment file), then confirm Compose resolves to it. A variable typed in a shell is not exported and does not change the file; a temporary override file is lost on the next `up` or reboot.
6. **Apply.**
   - Recreate only the application service (`up -d --no-deps --force-recreate <service>`), never the database.
   - Wait for it to answer, then run the application's migrations and its configuration import every time. Log what the import will change first (for Drupal, `config:status`).
   - If the deploy fails before migrations start, restore the previous pin and container. After migrations, do not roll back code automatically: report the backup and the rollback procedure.
7. **Verify.** Pending migrations and configuration status, key pages, the running digest equals the target, and the pin equals the target.

## Output

Running, pinned and target revisions (with digests); the commits deployed; backup location; migration and configuration-import results; verification results; anything left to a person. For a check-only request: up to date, or update available with the commit list.

## When a deploy "succeeded" but nothing changed

Compare the running revision with the intended one before debugging application code. Common causes:

- The target was set as an unexported shell variable or a one-off override, so Compose used the old pin.
- A moving tag was pulled once and is cached locally; nothing re-resolved it.
- The image was rebuilt from a local `build:` section instead of pulled.
- The script verified the configuration it read, not the container that is running.

See the [deployment that reported success](https://github.com/pranayagarwal90/ai-engineering-toolkit/blob/main/examples/deploy-reported-success.md) for a real case.
