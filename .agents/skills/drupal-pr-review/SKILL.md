---
name: drupal-pr-review
description: Review a Drupal pull request or diff for correctness, security, caching and configuration regressions. Use for review requests; make fixes only when requested.
---

# Review a Drupal change

Follow [root guidance](../../../AGENTS.md) and the relevant project map.

**Scope:** read-only. Do not mutate a database or post an external review just to complete an assessment.

## Inputs

- Base/head or a supplied diff, the intended behavior, Drupal/PHP versions and available checks.

## Steps

1. **Establish scope.** Base/head, intended behavior, versions; preserve existing local changes.
2. **Read beyond the diff.** Affected callers, routes, services, plugins, templates and configuration. Do not assume installed or deployed versions match the lockfile.
3. **Trace concrete failure paths:**
   - route/entity access, ownership and CSRF where applicable
   - dependency injection and nullable values
   - output escaping
   - cache tags, contexts and max-age
   - translation
   - configuration dependencies and install-versus-update behavior, including update hooks that change exported config without an export in the same change
4. **Check JavaScript** behavior attachment and repeated AJAX execution where affected. A hidden frontend element is not access control.
5. **Run feasible checks.** Select existing project checks, run the non-destructive ones in the authorized environment, and record results.

## Output

Actionable findings by severity, each with path/location, triggering input, impact, evidence and a suggested fix or check. Skip stylistic findings unless a required standard fails. With no findings, state the reviewed scope and verification gaps; do not certify the whole site.
