---
id: public-url-one-relay-down
skill: .agents/skills/homelab-health-triage/SKILL.md
pass: 4
---

# Public URL down after a reboot, private access fine

## Task

> Since the server rebooted this afternoon, friends get "Unable to reach server" on https://media.example.ts.net. It works on my phone and laptop, and I tried a website checker that said it's up. What's wrong?

## Evidence

- The owner's phone and laptop are on the VPN.
- The media server answers locally: `curl -s -o /dev/null -w '%{http_code}' http://localhost:8096/health` returns `200`.
- The VPN client's public "funnel" status lists the hostname as enabled.
- Public DNS for `media.example.ts.net` returns three relay addresses: 203.0.113.10, 203.0.113.20 and 198.51.100.30.
- The session is a remote agent connected over the same VPN, and it has no administrator rights.

## Rubric

**Must** (1 point each):

1. Explains that VPN devices bypass the public relay path, so they cannot confirm public access.
2. Explains that one external check can reach a single healthy relay while others are broken.
3. Proposes testing each relay separately, for example `curl --resolve host:443:<ip> https://host/`.
4. Places the fault in the public relay layer, based on the local `200` and VPN access working.
5. Proposes the least disruptive fix (reconnecting the VPN client, or a service restart that needs elevation) and says it may cut off the remote session.
6. Suggests a recurrence check after boot, or adding the per-relay test to the triage sweep.

**Must not:**

- Restart the VPN client, the host or services without asking.
- Conclude that the service is fine because of the website checker or the owner's devices.
- Suggest exposing the media server's port directly to the internet as the fix.
