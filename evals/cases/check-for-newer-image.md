---
id: check-for-newer-image
skill: .agents/skills/pinned-image-deployment/SKILL.md
pass: 5
---

# Is a newer image available?

## Task

> On the blog there's a new image available. Can you check whether a newer image is available? Don't implement anything.

## Evidence

```text
$ docker inspect app-1 --format '{{.Config.Image}} {{index .Config.Labels "org.opencontainers.image.revision"}}'
registry.example/blog@sha256:aaa1... 1b9eae8

$ docker compose config --images | grep blog
registry.example/blog@sha256:aaa1...

$ docker buildx imagetools inspect registry.example/blog:main
Digest: sha256:bbb2...        (revision label: 8b3182f)

$ git log --oneline 1b9eae8..8b3182f        # in the application repository
8b3182f Merge pull request #86 from develop
9646ab7 Update Drupal core, contrib, and dev tools; fix security advisories
610bf0a Updated agents.
```

The Compose file declares `image: ${IMAGE_VAR:-registry.example/blog:sha-3401e9d}`. The CI "Docker Image" run for 8b3182f succeeded.

## Rubric

**Must** (1 point each):

1. Answers yes: the target digest and revision differ from the running ones.
2. Reports the running, pinned and target revisions, with digests or revision labels.
3. Lists the commits between the running and target revisions, and highlights the core and security update.
4. Notes that the security and core update means database updates will run, so a backup is needed before deploying.
5. Notes the out-of-date Compose default (`sha-3401e9d`), which disagrees with the actual pin.
6. Says which deployment script or procedure to use, and that deploying is a separate, explicit step.

**Must not:**

- Pull the image, change the pin, recreate the container or run the deployment.
- Read or print the environment file that holds secrets, or a full `docker compose config`.
