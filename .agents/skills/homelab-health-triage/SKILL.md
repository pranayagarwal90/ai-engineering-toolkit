---
name: homelab-health-triage
description: Read-only, outside-in health sweep of a self-hosted server (scheduler, VM/WSL, containers, port forwarding, reverse proxy, tunnels, public relays, backups) when something "isn't working", after a reboot, or when asked for status.
---

# Triage a homelab

Follow [shared rules](../../RULES.md) and the project's [infrastructure](../../project/infrastructure.md) page, which records the layers, request paths and allowed commands.

**Scope:** read-only. Restarting services or VMs, changing port forwarding, reconnecting VPN/tunnel clients or rebooting needs explicit approval, and often an elevated shell the assistant does not have; give the user the exact command instead. Do not read secret files or print environment variables.

## Inputs

- The symptom: which URL, app, job or access path fails, from where (LAN, VPN, public internet), and since when.
- Recent changes: reboots, updates, configuration edits.

## Steps

1. **Run the project's sweep** if one exists; otherwise check each layer below in one pass. Report only failing and warning lines, plus one line saying the rest is fine.
2. **Work from the outside in.** The first broken hop is usually the cause; later failures are symptoms of it.

   | Layer | Read-only checks |
   | --- | --- |
   | Host scheduler and lifecycle | Expected scheduled tasks/timers ran, last result codes, startup/shutdown logs, any shared lock held by a stuck job |
   | VM or WSL | Running, its current IP (it can change after a reboot), uptime |
   | Containers | Expected services running and healthy; restart loops; dependency chain |
   | Host services outside containers | systemd units or native apps the stack depends on |
   | Port forwarding and firewall | Forwarding rules still point at the current VM IP; the port answers locally but not from the LAN means forwarding |
   | Reverse proxy and private DNS | Proxy running and bound to the right interface; certificates; names resolve to the right host |
   | Tunnels and public relays | Tunnel connections registered; **test each relay or edge separately**, since one healthy path hides a broken one and devices on the private network bypass the public path entirely |
   | Storage and backups | Free space, last backup result and age |

3. **Check known failures.** Look up the symptom in the project's troubleshooting notes before investigating from scratch.
4. **Narrow down with evidence.** Compare the same request from inside the host, from the LAN and from outside to locate the failing hop. Read the failing component's recent logs, bounded to the incident window.
5. **Propose the fix.** The smallest action that addresses the first broken hop, its blast radius (what else restarts or disconnects, including the assistant's own session) and how to verify it. Run it only with approval.
6. **Record new failures.** After a new kind of failure is fixed, add a dated entry to the project's troubleshooting notes.

## Output

A short table of failing and warning checks, the first broken hop with evidence, the proposed fix with its blast radius, and what the user must run themselves.

See [public URL down through one relay](https://github.com/pranayagarwal90/ai-engineering-toolkit/blob/main/examples/public-url-one-relay-down.md) for a real case.
