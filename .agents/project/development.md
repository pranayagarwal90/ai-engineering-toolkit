# Development reference

Discover the project's document root, custom modules/themes, configuration directory, supported Drupal/PHP versions and existing checks. Inspect composer.json, CI and local environment configuration.

Some projects define composer quality; others do not. Run it only when that script exists. Otherwise select the actual PHPCS, static-analysis, PHPUnit, Twig or JavaScript commands from the project. Record missing prerequisites. Do not assume this toolkit includes Drupal or those tools.

For Drupal code, follow the project's existing conventions: dependency injection, access checks, render arrays and cache metadata. Never hand-edit Composer-managed dependencies (core, contrib or vendor).
