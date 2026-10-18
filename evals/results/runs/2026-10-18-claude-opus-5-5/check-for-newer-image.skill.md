Yes, there's a newer image. The running blog is at revision `1b9eae8` and `registry.example/blog:main` now points to `8b3182f`, which is three commits ahead. I only checked; nothing was pulled, pinned or deployed.

**What the evidence shows**

| | Reference | Revision |
|---|---|---|
| Running (`app-1`) | `registry.example/blog@sha256:aaa1...` | `1b9eae8` |
| Pinned (what a restart would use) | `registry.example/blog@sha256:aaa1...` | same as running |
| Target (`:main` in the registry) | `sha256:bbb2...` | `8b3182f` |

- The running image and the pin match, so a restart today would bring back the same version.
- The target has a different digest, so there is something to deploy.
- The CI "Docker Image" run for `8b3182f` succeeded.

**Commits between running and target**

```
8b3182f Merge pull request #86 from develop
9646ab7 Update Drupal core, contrib, and dev tools; fix security advisories
610bf0a Updated agents.
```

`9646ab7` fixes security advisories, so this update is worth doing soon. It also updates Drupal core and contributed modules, so a deploy will almost certainly need database updates and a config import.

**Unverified (likely, but not confirmed)**

- **The digests are truncated.** `aaa1...` and `bbb2...` differ, but I'd compare the full values before deploying.
- **CI and the digest aren't linked yet.** The CI run succeeded, but nothing here shows it produced `sha256:bbb2...`. The registry's revision label (`8b3182f`) suggests it did. To confirm, compare the digest in the CI run's output with `docker buildx imagetools inspect registry.example/blog:main`.
- **The fallback pin is a different version.** The Compose default is `registry.example/blog:sha-3401e9d`. Since Compose resolves to `@sha256:aaa1...`, `IMAGE_VAR` must currently be set in the Compose environment. I didn't read that file because it may hold secrets. If the variable were lost, a restart would fall back to `sha-3401e9d`. That's a tag, not a digest, and its revision isn't `1b9eae8`, so it would silently change the version. When you deploy, I'd also change the default to a digest or a current tag.

**If you ask me to deploy later**, I would:
1. Pull `registry.example/blog@sha256:bbb2...` and check its revision label is `8b3182f`.
2. Back up the database and uploaded files.
3. Set `IMAGE_VAR` to the new digest in the Compose environment file.
4. Recreate only the app service.
5. Run `drush config:status`, then `drush updatedb` and `drush config:import`.
6. Check that the running image and the pin both point to `bbb2...`.

That needs a separate go-ahead from you.
