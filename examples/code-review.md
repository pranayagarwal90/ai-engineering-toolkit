# Reviewing a personalized greeting: a cache leak hiding in five lines

Status: **synthetic walkthrough.** The module, route and code are invented to show the review method; no real pull request or test run is described.

## The request

> Review this PR. It adds a greeting block to the dashboard page.

The [PR review skill](../.agents/skills/drupal-pr-review/SKILL.md) applies, read-only. It says to read beyond the diff: the route, the service wiring and how the output is cached, not only the changed method.

## The change

`site_greeting.routing.yml`:

```yaml
site_greeting.dashboard:
  path: '/dashboard'
  defaults:
    _controller: '\Drupal\site_greeting\Controller\DashboardController::page'
  requirements:
    _permission: 'access content'
```

`src/Controller/DashboardController.php`:

```php
public function page(): array {
  return [
    '#markup' => 'Hello ' . $this->currentUser->getDisplayName(),
    '#cache' => ['max-age' => 3600],
  ];
}
```

`$this->currentUser` is injected through `create()`, so dependency injection is fine.

## Tracing the failure paths

**Who sees the page?** Everyone with `access content`, which on most sites includes anonymous visitors and every editor.

**How is it cached?** The render array declares only `max-age`, no cache contexts. Drupal's Dynamic Page Cache stores the whole response and varies it only by the contexts the page declares, plus defaults such as theme, language and the user's permission set (`user.permissions`). Nothing here says "this output depends on which user is logged in".

**Concrete trigger:**
1. Editor Alice opens `/dashboard`. The response "Hello Alice" is cached.
2. Editor Bob has the same roles, so the same permission hash. He opens `/dashboard` within the hour and receives the cached "Hello Alice".

**Escaping:** the display name is concatenated into `#markup`. Drupal filters `#markup` for XSS, so a script tag would be stripped, but some HTML is allowed through, and names are user-controlled. Display names should be rendered as plain text.

## Findings

| Severity | Location | Finding | Trigger | Fix |
| --- | --- | --- | --- | --- |
| **High** | `DashboardController::page()` | Personalized output cached without the `user` cache context; one user's name is served to others. | Two users with the same roles visit within `max-age`. | Add `'contexts' => ['user']` to `#cache`. The `max-age` can then be dropped; the user context already varies the cache. |
| Medium | Same | User-controlled display name concatenated into `#markup`. | A display name containing HTML. | Use a translatable string with a placeholder, which escapes it: `$this->t('Hello @name', ['@name' => ...])`. |
| Question | Routing | Should anonymous visitors see a greeting? With `access content` they see "Hello Anonymous". | Anonymous visit. | Confirm the intent; restrict to `user.role:authenticated` or hide the greeting for anonymous users. |

Suggested change:

```php
public function page(): array {
  return [
    '#markup' => $this->t('Hello @name', ['@name' => $this->currentUser->getDisplayName()]),
    '#cache' => ['contexts' => ['user']],
  ];
}
```

## Verification plan

These are checks to run, not results:

- Log in as two users with the same roles and load `/dashboard` in turn. Each must see their own name. The `X-Drupal-Dynamic-Cache` header shows whether the page came from cache.
- Set a display name to `<em>Bob</em>` and confirm it shows literally, not in italics.
- Load the page anonymously and confirm the agreed behavior.
- Add a functional test that logs in two users and asserts each greeting, so the cache context cannot be removed silently later.

## Why this example matters

The code is short, correct-looking, and passes linting and a single-user manual test. The defect appears only when cache metadata is traced against **who** sees the output. That is why the skill asks for the route and cache behavior, not just the diff, and for a concrete trigger behind each finding.
