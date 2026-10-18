**Yes, a newer image is available.** The running container is two commits plus a merge behind `:main`, and one of those commits contains security fixes.

| | Image | Revision |
|---|---|---|
| Running (`app-1`) | `registry.example/blog@sha256:aaa1...` | `1b9eae8` |
| Registry `:main` | `sha256:bbb2...` | `8b3182f` |

**What the newer image adds** (`1b9eae8..8b3182f`):
- `9646ab7` Update Drupal core, contrib, and dev tools; **fix security advisories**
- `610bf0a` Updated agents
- `8b3182f` Merge PR #86 from develop

The CI "Docker Image" run for `8b3182f` succeeded, so the image was built and pushed normally.

**About your Compose file:**
- `docker compose config` resolves to the pinned digest `@sha256:aaa1...`, not the default `blog:sha-3401e9d`. That means `IMAGE_VAR` is set somewhere, probably in `.env` or the shell environment, and it pins the current image.
- Because of that pin, `docker compose pull` will **not** pick up the new image. Updating means changing `IMAGE_VAR`.
- The fallback default `sha-3401e9d` is a third revision. It's probably stale, but it isn't what's running.

**Checks I'd run before updating** (read-only):
```sh
# Confirm an immutable tag exists for the new revision and matches :main
docker buildx imagetools inspect registry.example/blog:sha-8b3182f

# Find where IMAGE_VAR is set
grep -n IMAGE_VAR .env; docker compose config --environment | grep IMAGE_VAR

# Confirm 8b3182f is a descendant of the running revision
git merge-base --is-ancestor 1b9eae8 8b3182f && echo ahead
```

I'd pin to the `sha-8b3182f` tag or the full `bbb2...` digest rather than the mutable `:main` tag. As you asked, I haven't changed anything.
