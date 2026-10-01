---
name: drupal-custom-module-development
description: Design and implement a requested Drupal custom module or feature using the target repository's conventions, access rules, configuration and verification workflow.
---

# Develop a custom Drupal module

1. Read root guidance, project architecture and related implementation. Establish the requested behavior, acceptance criteria, Drupal/PHP versions, document root and enabled dependencies. Ask only for decisions that materially block implementation.
2. Reuse an existing module when appropriate. Choose services, routes/forms, plugins, configuration or entities based on behavior, not a fixed skeleton. Explain significant dependencies and tradeoffs.
3. Plan access, validation, translation, cacheability and configuration lifecycle. Keep secrets outside exported configuration. Decide how an existing installation receives changes; install defaults alone do not update it.
4. Implement the smallest complete feature within the user's scope. Use dependency injection and Drupal APIs. Include permissions, schema and libraries only where required. Preserve unrelated work.
5. Select meaningful existing checks and add regression tests only for behavior that warrants them. Verify denied-access and invalid-input paths alongside the successful path where relevant. Run database/config operations only on the intended authorized environment.
6. Report changed behavior, file responsibilities, checks actually run, setup/update steps and limitations. Do not deploy, publish or claim production validation without evidence and scope.
