---
description: Run a read-only homelab health triage and find the first broken hop.
---

Read [shared rules](../../.agents/RULES.md) and [homelab-health-triage](../../.agents/skills/homelab-health-triage/SKILL.md). Use [Homelab Operator](../agents/homelab-operator.agent.md) as role guidance.

Task inputs: the symptom, where it was seen from (LAN, VPN, public) and since when; recent reboots or changes.
Read-only. Report failing checks, the first broken hop with evidence, and a proposed fix with its blast radius. Do not restart, reconnect or change forwarding without approval.
