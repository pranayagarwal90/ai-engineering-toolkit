## Most likely cause

Your phone and laptop aren't a valid test, because they're on the VPN. They resolve `media.example.ts.net` to the server's private tailnet address and connect directly. Your friends aren't on the VPN, so they go through the public Funnel relays (the three addresses in public DNS). That relay path is what broke after the reboot. The media server itself is fine: `localhost:8096/health` returns `200`.

The website checker doesn't rule this out. Many checkers count any TLS handshake or HTTP response as "up", including a 502 from the relay. The checker may also have hit a different relay than your friends.

"Funnel enabled" in status only means the node is allowed to use Funnel. It doesn't prove the proxy rule that forwards public traffic to `http://localhost:8096` came back after the reboot. Common reasons it doesn't:

- **The rule was started in the foreground** (`tailscale funnel 8096` without `--bg`). A foreground rule vanishes when that process dies, so it doesn't survive a reboot.
- **tailscaled started before the media server** and the relay path got stuck in an error state.
- **The rule points at the wrong target**, such as a different port or `https://` instead of `http://`.

## How I'd confirm it

From my session I can test the public path directly by forcing each relay IP. That skips VPN DNS, and it doesn't need admin rights:

```bash
for ip in 203.0.113.10 203.0.113.20 198.51.100.30; do
  echo "== $ip"
  curl -sS -o /dev/null -w '%{http_code}\n' --max-time 10 \
    --resolve media.example.ts.net:443:$ip \
    https://media.example.ts.net/health
done
```

- `200` from all three means the relays work, and the problem is on your friends' side (e.g., a stale server address saved in their app).
- `502`, a timeout or a TLS error means the relay can't reach your server's proxy rule.
- Mixed results mean one relay is unhealthy, which would also explain the checker saying "up".

I'd also run `tailscale funnel status` and `tailscale serve status` and look for a line like `https://media.example.ts.net (Funnel on)` → `proxy http://127.0.0.1:8096`. If there's no proxy target, the rule is gone.

## Fix (needs admin, so you'll have to run it)

```bash
sudo tailscale funnel --bg 8096     # recreate the rule persistently
tailscale funnel status             # confirm it shows proxy http://127.0.0.1:8096
```

If the rule already looks correct, restart the daemon now that the media server is up:

```bash
sudo systemctl restart tailscaled
```

Then rerun the `curl --resolve` loop above. You can also test from your phone with Wi-Fi and the VPN both turned off. If it works there, it'll work for your friends.
