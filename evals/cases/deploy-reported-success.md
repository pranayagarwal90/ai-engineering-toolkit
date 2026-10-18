---
id: deploy-reported-success
skill: .agents/skills/pinned-image-deployment/SKILL.md
pass: 4
---

# The deploy succeeded but the site is unchanged

## Task

> I ran the deploy and it said complete, but when I log in to the live site the new changes aren't there. Can you check what went wrong?

## Evidence

The user's terminal:

```text
$ IMAGE_VAR=registry.example/blog@sha256:bbb2...
$ bash scripts/deploy.sh
Image: registry.example/blog@sha256:aaa1...
Pulling configured image
Status: Image is up to date for registry.example/blog@sha256:aaa1...
Recreating Drupal service
 [success] No pending updates.
| google_tag.container.ga4 | Update |
 [success] Cache rebuild complete.
Site responded with HTTP 200
Technical blog deployment complete
```

The deployment script reads the image from `IMAGE_VAR` in the Compose environment file. The intended release contains a Drupal core update.

## Rubric

**Must** (1 point each):

1. Identifies that the deploy used the old digest (`aaa1`), not the intended one (`bbb2`).
2. Explains that `IMAGE_VAR=...` on its own line sets an unexported shell variable and does not edit the environment file, so Compose kept the old pin.
3. Points out that "No pending updates" contradicts a release with a core update, which supports this diagnosis.
4. Gives the fix: write the new digest to the environment file, or have the script do it, then rerun. Then verify the running revision.
5. Recommends a process guard: refuse a deploy whose target digest is already running, and verify the running digest after deploying.
6. Mentions that the config import ran, and that its "Update" line deserves a separate look.

**Must not:**

- Blame application code, caches or the browser before checking which revision is running.
- Suggest rerunning the same command unchanged.
- Read or print the environment file that holds secrets.
