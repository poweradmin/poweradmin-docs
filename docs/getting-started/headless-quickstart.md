# Headless / API-First Quickstart

If you want to drive PowerDNS from scripts, CI, or your own tooling without
clicking through a web UI, Poweradmin can run in an API-first mode. The web
interface stays available for the few things that need it (creating the first
admin user, issuing API keys), but day-to-day zone and record management can
happen entirely over the REST API.

This page gets you from zero to a scripted record update in about five minutes.

## What you get

- A REST API (`/api/v1` and `/api/v2`) with predictable JSON responses
- Per-user API keys that can be revoked or rotated
- Interactive OpenAPI/Swagger docs at `/api/docs`
- The same validation Poweradmin applies in the web UI (record types,
  hostnames, TTL bounds, SOA serial bumps)

## 1. Start Poweradmin with the API enabled

The Docker image is the fastest path. Set `PA_API_ENABLED=true` so the API is
exposed, and `PA_API_DOCS_ENABLED=true` so you can explore endpoints
interactively.

```bash
docker run -d --name poweradmin -p 8080:80 \
  -e PA_API_ENABLED=true \
  -e PA_API_DOCS_ENABLED=true \
  poweradmin/poweradmin:latest
```

The default image uses SQLite with a pre-seeded admin account
(`admin` / `testadmin`). For a production setup, point at MySQL or PostgreSQL
with the `DB_*` variables described in
[Docker Installation](../installation/docker.md).

## 2. Create an API key

API keys are issued through the web UI. This is a one-time step — once the key
exists, you can do everything else from scripts.

1. Open [http://localhost:8080](http://localhost:8080) and log in.
2. Go to **Settings -> API Keys** (`/settings/api-keys`).
3. Click **Add API Key**, give it a name (e.g. `ci-deploy`), and copy the key.
   The full key is only shown once.

Store it somewhere your scripts can read it:

```bash
export PA_API_KEY="paste-the-key-here"
export PA_URL="http://localhost:8080"
```

## 3. Verify the key works

```bash
curl -H "X-API-Key: $PA_API_KEY" "$PA_URL/api/v2/zones"
```

You should get back a JSON envelope with an empty `data` array (or your existing
zones if any).

## 4. Create a zone

```bash
curl -X POST \
  -H "X-API-Key: $PA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example.com",
    "type": "MASTER"
  }' \
  "$PA_URL/api/v2/zones"
```

The response includes the zone `id` you will use for subsequent requests.

## 5. Add a record

```bash
ZONE_ID=1  # from the previous response

curl -X POST \
  -H "X-API-Key: $PA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "www.example.com",
    "type": "A",
    "content": "192.0.2.10",
    "ttl": 3600
  }' \
  "$PA_URL/api/v2/zones/$ZONE_ID/records"
```

Poweradmin validates the record, writes it to PowerDNS, and bumps the SOA
serial so secondaries pick up the change.

## 6. Explore the rest interactively

With `PA_API_DOCS_ENABLED=true` the full OpenAPI explorer is available at:

```
http://localhost:8080/api/docs
```

You can paste your API key into the "Authorize" dialog and try every endpoint
from the browser.

## When to use this mode

This setup is a good fit when:

- You are scripting record updates from CI, Terraform, or config management
- You want PowerDNS managed by an infrastructure team but exposed to developers
  as an API
- You do not want end users in a web UI at all, but still need Poweradmin's
  validation and audit logging
- You are integrating with the
  [terraform-provider-poweradmin](https://github.com/poweradmin/terraform-provider-poweradmin)
  or the
  [external-dns-poweradmin-webhook](https://github.com/poweradmin/external-dns-poweradmin-webhook)

The web UI remains available for operators who prefer it; nothing about
enabling the API turns it off.

## What is *not* covered by the API yet

The REST API focuses on zones, records, users, groups, permission templates,
and zone templates. A few operator workflows still live only in the web UI:

- Initial admin user creation (handled by the installer)
- API key issuance and rotation (Settings -> API Keys)
- Some global settings under Settings -> Configuration

If a missing endpoint blocks you, please open an issue on the
[GitHub repository](https://github.com/poweradmin/poweradmin/issues).

## Next steps

- [API Configuration](../configuration/api.md) - full list of API settings,
  web server requirements, security recommendations
- [PowerDNS API Configuration](../configuration/powerdns-api.md) - connecting
  Poweradmin to PowerDNS itself, including the API-only backend mode
  (`dns.backend = api`) added in 4.3.0
- [Dynamic DNS with cURL](../user-guide/ddns/using-curl.md) - a separate,
  simpler endpoint for IP-update scripts
