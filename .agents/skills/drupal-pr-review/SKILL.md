---
name: drupal-pr-review
description: Review a Drupal pull request or diff for correctness, security, caching and configuration regressions. Use for review requests; make fixes only when requested.
---

# Review a Drupal change

1. Read root guidance and the relevant project map. Establish the base/head or supplied diff, intended behavior, Drupal/PHP versions and scope. Preserve existing changes.
2. Inspect the diff and affected callers, routes, services, plugins, templates and configuration. Do not assume installed or deployed versions match the lockfile.
3. Trace concrete failure paths. Check route/entity access, ownership and CSRF where applicable; dependency injection; nullable values; output escaping; cache tags, contexts and max-age; translation; configuration dependencies and install-versus-update behavior.
4. Examine JavaScript behavior attachment and repeated AJAX execution when affected. Do not treat a hidden frontend element as an access control.
5. Select existing project checks. Run feasible non-destructive checks in the authorized environment and record results. Do not mutate a database or post an external review merely to complete an assessment.
6. Report actionable findings by severity, each with path/location, triggering input, impact, supporting evidence and suggested fix/check. Avoid stylistic findings unless a required standard fails. If there are no findings, state reviewed scope and verification gaps; do not certify the entire site.
