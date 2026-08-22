# Architecture and Ports

What Poweradmin connects to, and over which ports. Useful when writing firewall rules, planning a
split deployment, or answering a security review.

Poweradmin is a PHP web application. It has no daemon or background worker of its own - everything
happens inside a request from a browser or an API client, so there are no outbound connections
except the ones listed here.

## Components

| Component | What it is |
|---|---|
| Browser / API client | Talks to Poweradmin over HTTP |
| Poweradmin | The PHP application, served by Apache, nginx + php-fpm, Caddy, or the bundled FrankenPHP container |
| Poweradmin database | Users, permissions, templates, logs. May be the same database as PowerDNS or a separate one |
| PowerDNS database | Zones and records, in PowerDNS's own schema |
| PowerDNS Authoritative Server | Answers DNS queries; optionally exposes its HTTP API |

## Connections

| From | To | Port | Protocol | Notes |
|---|---|---|---|---|
| Browser / API client | Poweradmin | 80 / 443 | HTTP(S) | Whatever your web server listens on. Put TLS in front of it - see [Reverse Proxy](reverse-proxy.md) |
| Poweradmin | Poweradmin database | 3306 (MySQL/MariaDB), 5432 (PostgreSQL) | TCP | SQLite instead uses a local file, so there is no network hop |
| Poweradmin | PowerDNS database | same as above | TCP | Only when `dns.backend = 'sql'` |
| Poweradmin | PowerDNS API | 8081 | HTTP | Only when the API is configured. Authenticated with an `X-API-Key` header |
| PowerDNS | PowerDNS database | same as above | TCP | PowerDNS's own connection; nothing to do with Poweradmin |
| Resolvers / secondaries | PowerDNS | 53 | UDP + TCP | Normal DNS traffic |

Ports are the defaults. `database.port` is empty by default, in which case Poweradmin uses 3306 for
MySQL/MariaDB and 5432 for PostgreSQL. PowerDNS's API port comes from its own `webserver-port`
setting, which defaults to 8081.

## The two data paths

`dns.backend` decides how Poweradmin reads and writes zone data, and it changes which connections
exist. This is the single most important thing to know before drawing firewall rules.

### SQL backend (`dns.backend = 'sql'`, the default)

Poweradmin writes zones and records straight into the PowerDNS database.

```
Browser ──443──▶ Poweradmin ──3306/5432──▶ PowerDNS database ◀──3306/5432── PowerDNS ──53──▶ Resolvers
                     │
                     └──8081──▶ PowerDNS API   (optional: DNSSEC, server status)
```

The API connection is optional here but not merely cosmetic: DNSSEC operations go through it
exclusively, and without `pdns_api.url` and `pdns_api.key` every DNSSEC action silently does
nothing. See [DNSSEC Configuration](../configuration/dnssec.md).

### API backend (`dns.backend = 'api'`)

Poweradmin does not touch the PowerDNS database at all. Zone and record operations become API
calls, and its own database holds only users, permissions, templates and logs.

```
Browser ──443──▶ Poweradmin ──8081──▶ PowerDNS ──53──▶ Resolvers
                     │                    │
                     │                    └──3306/5432──▶ PowerDNS database
                     └──3306/5432──▶ Poweradmin database
```

This mode was added in 4.3.0 and is still marked experimental. It is the right choice when
Poweradmin has no network route to the PowerDNS database - see
[Remote Setup](remote-setup-guide.md) and [PowerDNS API](../configuration/powerdns-api.md).

## Hardening notes

- **The PowerDNS API is unauthenticated apart from the API key**, and the key grants full control of
  every zone. Bind `webserver-address` to an address Poweradmin can reach and no one else can, and
  restrict `webserver-allow-from` to Poweradmin's address. See
  [Enabling the API](https://doc.powerdns.com/authoritative/http-api/index.html#enabling-the-api).
- **Port 8081 should never be reachable from the internet.** It is a plain HTTP endpoint; if
  Poweradmin and PowerDNS are on different hosts, put the connection on a private network or tunnel
  it.
- **The database ports do not need to be public either.** A single-host install can bind both the
  database and the PowerDNS API to `127.0.0.1` and expose only 80/443 and 53.
- If Poweradmin sits behind a proxy, configure `security.trusted_proxies` so client addresses in the
  logs and in rate limiting are the real ones - see [Reverse Proxy](reverse-proxy.md).

## Related Documentation

- [Installation Overview](index.md)
- [Remote Setup](remote-setup-guide.md) - Poweradmin and PowerDNS on separate hosts
- [PowerDNS API Configuration](../configuration/powerdns-api.md)
- [Database Configuration](../configuration/database.md)
- [Reverse Proxy](reverse-proxy.md)
