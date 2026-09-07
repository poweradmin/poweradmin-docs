# Health Checks *(v4.5.0+)*

Poweradmin can expose two endpoints that a monitoring system reads without logging in, so
you find out that the database or the PowerDNS API has gone away before a user does.

Both are **disabled by default**. They answer without a session and without an API key, so
turn on only the one you need and restrict it at your reverse proxy.

These endpoints report on **Poweradmin itself**. For PowerDNS server statistics, see the
[PowerDNS Server Status](../configuration/powerdns-api.md) page instead.

## Enabling

In `config/settings.php`:

```php
'health' => [
    'enabled' => true,        // GET /api/health
    'ping_enabled' => true,   // GET /ping
    'db_timeout' => 2,        // seconds; how long the database check waits to connect
    'pdns_timeout' => 2,      // seconds; how long the PowerDNS check waits
],
```

In Docker, set `PA_HEALTH_ENABLED=true` and `PA_HEALTH_PING_ENABLED=true`. See
[Docker Installation](../installation/docker.md).

Neither endpoint depends on `api.enabled`. You can run a health check with the API key
system switched off entirely.

While a flag is off its endpoint returns `404`, indistinguishable from a build that never
had the feature.

## `GET /ping` - liveness

Answers if the PHP process can serve a request. It touches nothing else, so it still
answers while the database is down. Use it to decide whether to restart a container or
pull an instance out of a load balancer.

```console
$ curl -i https://dns.example.com/ping
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8
Cache-Control: no-store

ok
```

## `GET /api/health` - readiness

Reports whether Poweradmin can reach its dependencies. Use it to decide whether an
instance should receive traffic.

```console
$ curl -s https://dns.example.com/api/health
{"status":"ok","checks":{"database":"ok","pdns_api":"ok"}}
```

Returns `200` when healthy and `503` when any check failed:

```console
$ curl -s -o /dev/null -w '%{http_code}\n' https://dns.example.com/api/health
503
```

```json
{"status":"error","checks":{"database":"down","pdns_api":"ok"}}
```

### Checks

| Check | Meaning |
|-------|---------|
| `database` | `ok` if Poweradmin can open a connection and run a statement, otherwise `down` |
| `pdns_api` | `ok` if the PowerDNS API answered, `down` if it did not, `skipped` if no PowerDNS API is configured |

`skipped` is normal for installs using the database backend, where Poweradmin talks to the
PowerDNS database directly and never calls the API. A `skipped` check never causes a `503`.

If `dns.backend` is set to `api` and no PowerDNS API is configured, the check reports `down`
rather than `skipped`. On that backend an unconfigured API means no zone operation can work,
so the instance is not ready.

### What the response does not contain

The endpoint is unauthenticated, so a check either passed or it did not. The response
carries no version number, hostname, database driver, or error text.

The reason a check failed goes to the application's diagnostic log instead. That log is
off by default, so set `logging.type` to `native` (`PA_LOGGING_TYPE=native` in Docker) to
have connection errors written to the PHP error log:

```php
'logging' => [
    'type' => 'native',
],
```

With diagnostic logging left at its `null` default, a failing check is reported as `down`
and nothing is written anywhere. That is deliberate: an endpoint scraped every few seconds
would otherwise fill the log with one line per scrape for as long as the outage lasts.

### Response time

Both checks are bounded so an unreachable dependency cannot hold the request open for the
operating system's TCP timeout. The database connect is capped by `health.db_timeout` and
the PowerDNS call by `health.pdns_timeout`, both 2 seconds by default. The PowerDNS request
retries once, so its worst case is roughly twice that value. Set your monitoring timeout
above the sum.

## Restricting access

Anyone who can reach these paths can call them. Deny them at the proxy and allow only your
monitoring system.

**nginx**

```nginx
location ~ ^/(ping|api/health)$ {
    allow 10.0.0.0/8;
    deny all;
    try_files $uri /index.php$is_args$args;
}
```

**Apache**

```apache
<LocationMatch "^/(ping|api/health)$">
    Require ip 10.0.0.0/8
</LocationMatch>
```

## Docker

The image ships a `HEALTHCHECK` that requests `/`, which succeeds even when the database is
down. To make the container status reflect real readiness, enable the endpoint and override
the healthcheck:

```yaml
services:
  poweradmin:
    image: poweradmin/poweradmin:4.5.0
    environment:
      - PA_HEALTH_ENABLED=true
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

## Kubernetes

Use `/ping` for liveness and `/api/health` for readiness. A failing dependency should stop
traffic reaching the pod, not restart it:

```yaml
env:
  - name: PA_HEALTH_ENABLED
    value: "true"
  - name: PA_HEALTH_PING_ENABLED
    value: "true"
livenessProbe:
  httpGet:
    path: /ping
    port: 80
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /api/health
    port: 80
  periodSeconds: 30
  timeoutSeconds: 5
```

## Related documentation

- [Maintenance and Monitoring](../maintenance/index.md)
- [Reverse Proxy](../installation/reverse-proxy.md)
- [Settings Reference](../configuration/settings-reference.md)
