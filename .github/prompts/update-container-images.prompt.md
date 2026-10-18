---
description: Find and apply container image updates safely, in batches, with backups.
---

Read [shared rules](../../.agents/RULES.md) and [container-image-updates](../../.agents/skills/container-image-updates/SKILL.md). Use [Homelab Operator](../agents/homelab-operator.agent.md) as role guidance.

Task inputs: which services (or all), whether to apply or only report, and the backup procedure.
Report outdated images first. Recreate only with approval, in batches, checking logs after each. Treat major versions as separate migrations. Never delete volumes or prune.
