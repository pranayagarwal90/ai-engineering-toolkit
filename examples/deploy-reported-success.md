# A deployment "succeeded" but the site still ran the old version

Status: **real use, sanitized.** This happened on a personal home server running a Drupal site from a container image in October 2026. Registry paths, digests and hosts are replaced with placeholders; the sequence and results are as observed.

## The problem

CI had published a new image (core and contrib security updates) to `registry.example/blog:main`. The owner wanted it live, and the assistant gave three steps: back up, set the image variable to the new digest in the Compose environment file, run the deployment script. The owner ran:

```bash
$ IMAGE_VAR=registry.example/blog@sha256:<new>
$ bash scripts/deploy.sh
...
Image: registry.example/blog@sha256:<old>
Status: Image is up to date
 [success] No pending updates.
...
Deployment complete
```

The script reported success, but the site showed none of the changes.

## Diagnosis

Using the [pinned image deployment](../.agents/skills/pinned-image-deployment/SKILL.md) skill's "nothing changed" checklist:

- The first command set a shell variable on its own line. It was not exported and did not edit the environment file, so Compose still read the old digest.
- The script's own log showed it: `Image: …@sha256:<old>`, and "No pending updates" for a release that contained core updates.
- The script had verified its configuration against itself and recreated the container from the same image. Nothing compared the running revision with the intended one.

The fix that day was simply to edit the environment file and run the script again. This time it pulled the new digest and ran the database updates.

## What was wrong with the process

The investigation found more than one mistake:

- The image was defined in **three places that disagreed**: the docs said `:main`, the Compose default was an old commit tag, and the environment file held a digest.
- **Three scripts** each did part of the job. Only one imported configuration, and only one imported articles and checked the image revision. That one pinned the image through a temporary override file, so a reboot would have reverted it.
- Nothing refused a deployment that would not change the running image.

## The resulting process

One deployment script replaced the three. It:

1. Offers `--check`, which is read-only: running, pinned and target revisions, and the commits between them.
2. Resolves the target to a digest from the registry and stops with "nothing to deploy" if that digest is already running.
3. Pulls by digest and verifies the revision label.
4. Backs up the database and uploaded files.
5. Writes the digest to the environment file with a helper that edits only that line, then confirms Compose resolves to it. The Compose file now fails loudly if the variable is missing, instead of falling back to an old default.
6. Recreates only the application container, then runs migrations, logs and runs the configuration import, and imports content.
7. Verifies the running digest, the pin, pending updates, configuration status and key pages.
8. Restores the previous pin and container automatically if anything fails before migrations start.

The next real deployment listed six new commits, asked for confirmation, and finished in about 90 seconds. Every check passed. A later `--check` said "Up to date", and a repeated deployment stopped with "nothing to deploy".

## Takeaways

- Verify **what is running**, not what the script read.
- Pin by digest **where restarts read it**. A shell variable or a temporary override is not a deployment.
- A deployment that would change nothing should stop, not succeed.
- One script with one source of truth beats several partial scripts.
