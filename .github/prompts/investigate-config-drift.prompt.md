---
description: Investigate unexpected Drupal configuration differences or import changes without changing configuration.
---

Read [root guidance](../../AGENTS.md) and [drupal-config-drift](../../.agents/skills/drupal-config-drift/SKILL.md). Use [drupal-maintenance](../agents/drupal-maintenance.agent.md) as role guidance.

Task inputs: configuration names (from config:status or an import preview), environment, recent deployments and update hooks, and the revision being deployed. Investigation only.
Use supplied inputs first; ask only for blocking missing details. Report stored, effective and sync values (redacted), the likely writer, the recommended direction and prevention steps. Do not import, export or set configuration without explicit scope.
