The most likely problem is that your friends' traffic and yours take different routes. Your phone and laptop are on the VPN, so they connect straight to the server and never touch the public relays. Friends come in from the internet through one of the **three** relay addresses that public DNS returns. A website checker usually tests just one of them. So if one relay is broken and the others work, everything looks fine to you and the checker, while some friends fail.

I haven't run anything, and I followed your instruction to read only those two files. That means I skipped the project's infrastructure page and troubleshooting notes, which may already describe this exact failure.

## What we know

| Check | Result | Meaning |
| --- | --- | --- |
| Media server locally (`localhost:8096/health`) | ✅ `200` | The app itself is fine |
| Funnel status | ✅ "enabled" | It's turned on in the settings. That doesn't prove each relay can reach the server |
| Owner devices | ✅ work | They're on the VPN, so they skip the public path. This tells us nothing about it |
| Website checker | ✅ up | Probably tested only one relay |
| Public relays (203.0.113.10, 203.0.113.20, 198.51.100.30) | ⚠️ **not tested individually** | Most likely where it breaks |

**Best guess:** after the reboot, the tunnel client didn't fully reconnect to every public relay, so one or two of them can't reach the server. That's the first broken hop, and the "Unable to reach server" message is a symptom of it. This still needs confirming.

## Next step: test each relay separately

Run this from a device **off the VPN**, like your phone on mobile data with the VPN off, or a friend's computer. I'm connected over the same VPN, so my results wouldn't prove anything about the public path.

```bash
for ip in 203.0.113.10 203.0.113.20 198.51.100.30; do
  curl -sS -o /dev/null --connect-timeout 10 \
    -w "$ip -> %{http_code} in %{time_total}s\n" \
    --resolve media.example.ts.net:443:$ip \
    https://media.example.ts.net/health || echo "$ip -> FAILED"
done
```

If one or two fail and the rest return `200`, the guess is confirmed. Then, on the server, run these read-only checks and send me the output (remove any keys or IP addresses you don't want to share):

```bash
tailscale status
tailscale funnel status
tailscale netcheck
journalctl -u tailscaled --since "today 12:00" --no-pager | tail -n 200
```

## Likely fix (only if the test confirms it)

Restart the tunnel client so it reconnects to all the relays. I don't have admin rights, so you'd run it yourself:

```bash
sudo systemctl restart tailscaled
```

- **What it disrupts:** every VPN connection drops for a few seconds, including your phone and laptop and **my session**, so I'll be offline until it reconnects. The media server keeps running; it just can't be reached for a moment.
- **How to check it worked:** run the loop above again from off the VPN. All three addresses should return `200`. Then ask a friend to try.

If all three relays already return `200` from off the VPN, this guess is wrong. In that case I'd want to know where your friends are connecting from, which app they use (TV app or browser), and the exact URL they enter.

Once it's fixed, add a dated entry to the troubleshooting notes, something like "after reboot, one public relay stopped reaching the server; test each relay with `curl --resolve`".
