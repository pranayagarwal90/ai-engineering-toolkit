# Illustrative code review

Status: intentionally simplified fixture, not production code or an actual PR transcript.

Request: “Review this change. The controller renders an account-specific greeting on a publicly accessible route.”

```php
public function greeting() {
  return [
    '#markup' => 'Hello ' . $this->currentUser->getDisplayName(),
    '#cache' => ['max-age' => 3600],
  ];
}
```

Read the code-review profile and PR-review skill. Inspect the actual route, controller injection and response/cache behavior before concluding.

Questions to resolve: does the render output vary by user; is the greeting escaped safely; what access is intended; does cache metadata bubble correctly? A complete review requires surrounding source, not this snippet alone.

Expected finding, if surrounding code adds no user context: cached personalized output lacks a user cache context and can be reused incorrectly. Propose appropriate escaping/rendering and user variation, then verify behavior for two accounts and anonymous requests. This is an illustrative expected finding, not an executed regression test.
