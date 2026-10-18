# Public URL down after a reboot while private access worked

Status: **real use, sanitized.** This happened on a personal home server in October 2026. It publishes a media server to the internet through a VPN provider's public relay ("funnel") feature. Hostnames and addresses are placeholders.

## The problem

After a Windows host reboot, friends outside the private network got "Unable to reach server" from `https://media.example.ts.net`. On the owner's own devices, which were on the VPN, everything worked, and a quick external fetch from one location also succeeded.

## Diagnosis

Using [homelab-health-triage](../.agents/skills/homelab-health-triage/SKILL.md):

- **Outside-in:** the containers, the native media server and its local port all answered, and devices on the VPN reached it. That pointed to the public relay layer.
- **Why it looked fine:** devices on the VPN never use the public path, and a single external request can reach a different, healthy regional relay.
- **Testing each relay separately:** the relay addresses came from public DNS. Some had to be resolved through a public resolver, because the host's own resolver returned the private VPN address. Each was tested with `curl --resolve host:443:<relay-ip> https://host/`. The broken relays accepted TCP, then dropped the connection after the TLS ClientHello. The VPN client's ingress peers showed zero traffic.

## Fix

Disconnecting and reconnecting the VPN client fixed every relay within about a minute. A service restart would also have worked, but it needed an elevated shell the session did not have.

## Prevention

- The startup script now tests every relay the same way after boot and reconnects the VPN client if any fails.
- The project's triage sweep checks each relay, and the troubleshooting notes record the symptom and the fix.

## Takeaways

- Test **every** public path; one healthy relay hides a broken one.
- Devices on the private network bypass the public layer entirely, so they can't confirm it works.
- A disruptive fix such as reconnecting the VPN can cut off a remote session. Say so and ask before running it.
