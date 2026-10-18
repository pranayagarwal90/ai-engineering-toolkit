# Operations reference

Record environment names, allowed evidence sources, timezone, deployed revision, service names and redacted log commands from the target project. Do not assume DDEV, Docker, Acquia, Redis or a CDN is present.

Use a bounded time range. Preserve correlation IDs while removing tokens, credentials and personal information. Do not dump environment variables or databases. Collect independent infrastructure evidence when Drupal cannot bootstrap. Restarts, cache flushes and config imports change state; investigation alone does not authorize them.
