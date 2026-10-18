# Infrastructure reference

Record these facts from the target environment before using the deployment or homelab workflows. Leave a field "unknown" rather than guessing; never put credentials or private addresses in a public copy.

- **Layers and request paths:** for each way in (LAN, VPN, public tunnel or relay), the hops from client to container, and which component owns each hop.
- **Hosts:** operating systems, VM/WSL setup, how its IP is assigned, what starts at boot and in what order.
- **Service definitions:** Compose files (always-on and on-demand), where image pins live, and which services hold data or run migrations.
- **Repeated facts:** every place a service's name, port or domain appears (forwarding rules, proxy routes, DNS, dashboard, monitoring, docs) and the check that keeps them consistent.
- **Commands:** the read-only health sweep, log locations, the supported way to start, stop and recreate services, and the deployment script.
- **Privileges:** which actions need an elevated shell or another person, and which would disconnect a remote session (VPN, VM or host restarts).
- **Safety:** files never to read (secrets), commands never to run (volume deletion, prune), and the backup and restore procedure.
