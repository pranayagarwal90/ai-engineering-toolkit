---
description: Deploy an application image by digest with backups, migrations, config import and verification.
---

Read [shared rules](../../.agents/RULES.md) and [pinned image deployment](../../.agents/skills/pinned-image-deployment/SKILL.md). Use [Release Engineer](../agents/release-engineer.agent.md) as role guidance.

Task inputs: target (tag, commit or digest), environment, the project's deployment script, and explicit approval to deploy.
Use the project's script where it exists. Confirm a backup exists before migrations, pin the digest where restarts read it, and verify that the running digest and the pin equal the target. Report what ran, the backup location and anything left for a person.
