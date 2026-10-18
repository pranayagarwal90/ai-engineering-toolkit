---
name: homelab-service-change
description: Add, remove, rename, re-port or re-domain a self-hosted service while keeping every repeated fact (Compose, port forwarding, proxy routes, DNS, dashboard, monitoring, docs) in sync.
---

# Change a homelab service

Follow [shared rules](../../RULES.md) and the project's [infrastructure](../../project/infrastructure.md) page, which lists where service facts are repeated.

**Scope:** editing files in the repository is local work. Applying the change (recreating services, forwarding ports, reloading the proxy, editing runtime dashboards or monitors) affects running systems; ask first, and hand elevated steps to the user as exact commands.

## Inputs

- The change: service, port, domain, always-on or on-demand, and whether it is added, removed or renamed.
- The project's list of places that repeat service facts, and its consistency checks, if any.

## Steps

1. **Take a baseline.** Run the project's consistency (drift) check before editing, and report drift that already exists rather than silently fixing it.
2. **Edit each copy the change touches:**
   - service definition (always-on or on-demand Compose file) and any on-demand controller list
   - port-forwarding or firewall exceptions; prefer generating them from Compose over hand-kept lists
   - reverse-proxy routes and DNS records
   - dashboard cards and monitoring
   - documentation: URL lists, service tables and counts
3. **Regenerate generated files** (proxy config, dashboard fragments) with the project's tools instead of editing them by hand.
4. **Verify in the repository:** Compose `config --quiet`, the drift check again and the project's tests.
5. **List the steps outside Git** for the user, with exact commands: recreate the service, apply forwarding (often elevated), reload the proxy the supported way, update the live dashboard from the repo, add or remove monitors.
6. **When retiring a service,** keep its data for rollback, remove its forwarding and routes, and record it as retired so nobody debugs it later.
7. **After it is applied,** run the [triage](../homelab-health-triage/SKILL.md) sweep.

## Output

The files changed, consistency and test results, and the outside-Git steps with their commands and who runs them.
