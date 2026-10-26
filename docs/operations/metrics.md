# Prometheus Metrics *(v4.6.0+)*

Poweradmin can serve counts about itself at `/api/metrics` in the Prometheus text format, so
the monitoring system that already scrapes your other services can graph Poweradmin too.

These metrics describe **Poweradmin itself**: how many zones and users it manages and whether
it can reach the DNS backend. For PowerDNS server statistics, see the
[PowerDNS Server Status](../configuration/powerdns-api.md) page. For a yes/no check that the
database and the PowerDNS API are reachable, use the [Health Checks](health-checks.md).

## Enabling

The endpoint is **disabled by default** and needs the API to be enabled. In
`config/settings.php`:

```php
'api' => [
    'enabled' => true,
],
'metrics' => [
    'enabled' => true,
    'require_auth' => true,     // default; scrapes authenticate with an API key
    'count_records' => false,   // default; see "Counting records" below
],
```

In Docker, set `PA_API_ENABLED=true` and `PA_METRICS_ENABLED=true`, plus
`PA_METRICS_REQUIRE_AUTH` and `PA_METRICS_COUNT_RECORDS` if you need to change them. See
[Docker Installation](../installation/docker.md).

While `metrics.enabled` is off the endpoint returns `404` to everyone, without asking for
credentials.

## Authentication

With `require_auth` on (the default), a scrape must authenticate as a user who holds the
`server_status_view` permission:

1. Create a monitoring user and give it a permission template with `server_status_view`.
   It needs no zone permissions. See [Permissions](../user-guide/permissions.md).
2. Create an API key for that user and store the secret on the Prometheus host.

A key restricted to specific zones is refused with `403`, because the counts cover the whole
installation. A user without `server_status_view` also gets `403`, and a request without
credentials gets `401`. HTTP Basic Auth of the same user works as well.

With `require_auth` set to `false` the endpoint is public, like `/api/health`. Restrict it at
your reverse proxy if you do that.

A scrape never starts a session, so it sets no cookie.

## Prometheus scrape config

```yaml
scrape_configs:
  - job_name: poweradmin
    metrics_path: /api/metrics
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/poweradmin-api-key
    static_configs:
      - targets: ["poweradmin.example.com"]
```

The API key can also be sent as an `X-API-Key` header.

## Metrics

All metrics are gauges, computed on every scrape. None of them is labelled by zone or user
name, so each has only a handful of series.

| Metric | Labels | Meaning |
|--------|--------|---------|
| `poweradmin_info` | `version`, `backend` (`sql` or `api`) | Always 1; carries the Poweradmin version and the DNS backend mode |
| `poweradmin_up` | | 1 when the zone counts could be read from the DNS backend, 0 when not |
| `poweradmin_zones` | `type` (for example `master`, `native`, `slave`) | Zones by type |
| `poweradmin_zones_dnssec_signed` | | Zones with an active DNSSEC key, or presigned |
| `poweradmin_users` | `active` (`true` or `false`) | Poweradmin users by state |
| `poweradmin_records` | | All records, including SOA and NS; only with `count_records` |
| `poweradmin_metrics_collect_duration_seconds` | | How long collecting the metrics took |

When the DNS backend cannot be reached, the scrape still succeeds: `poweradmin_up` is 0 and
the zone metrics are left out. In API backend mode the PowerDNS API is asked with the short
`health.pdns_timeout` (2 seconds by default), so a down PowerDNS stays inside Prometheus's
default scrape timeout. A suitable alert:

```yaml
- alert: PoweradminBackendDown
  expr: poweradmin_up == 0
  for: 5m
```

With the SQL backend, a database that is down fails the whole request with `500`, as it does
for every API endpoint; Prometheus then reports the target as down.

### Where the counts come from

- **SQL backend:** the PowerDNS `domains`, `cryptokeys` and `domainmetadata` tables, and the
  Poweradmin `users` table.
- **API backend:** one zone list request to the PowerDNS API, which also carries the DNSSEC
  flag. On installations with many zones this is the main cost of a scrape.

### Counting records

`count_records` adds `poweradmin_records`. It runs `COUNT(*)` over the whole records table on
every scrape, which can be slow on large installations, so it is off by default. It is
available with the SQL backend only.

## Grafana dashboard

A ready-made dashboard ships in the Poweradmin repository at
`addons/grafana/poweradmin-dashboard.json`. Import it in Grafana and pick the Prometheus data
source that scrapes Poweradmin.
