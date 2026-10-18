---
description: Check whether a newer application image is available, without deploying.
---

Read [root guidance](../../AGENTS.md) and [pinned image deployment](../../.agents/skills/pinned-image-deployment/SKILL.md). Use [Release Engineer](../agents/release-engineer.agent.md) as role guidance.

Task inputs: image repository, target tag (default: the release branch), and where the running service's image is pinned. Check only.
Report the running, pinned and target revisions with digests, and the commits in between. Do not pull, back up, change the pin or recreate anything.
