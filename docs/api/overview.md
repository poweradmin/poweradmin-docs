# API Overview

Poweradmin exposes a REST API that mirrors what the web interface can do for
zones, records, users, groups, permission templates, and zone templates. All
the same validation, ownership checks, and SOA serial bumping run on every
request, so anything you build on top of the API behaves the same as the UI.

For step-by-step setup, see the
[Headless / API-First Quickstart](../getting-started/headless-quickstart.md).
For the full list of configuration options and security recommendations, see
[API Configuration](../configuration/api.md).

## Two API versions

| Version | Base path | Status | When to use |
|---------|-----------|--------|-------------|
| **v2** | `/api/v2` | Recommended | All integrations. Consistent response envelope, RRset endpoints, bulk record creation, zone owners, zone templates, groups. |
| **v1** | `/api/v1` | Removed in 4.5.0 | Nothing new. Deprecated in 4.3.0, still present in 4.2.x-4.4.x. |

On 4.4.x and older, both versions ship together and share API keys and
authentication, so you can use v1 and v2 from the same client.

From 4.5.0 on, v1 is gone. Every `/api/v1` path answers `410 Gone` for every
HTTP method, with a `Link: </api/v2/>; rel="successor-version"` header and a
body of `{"error": true, "message": "..."}`. Migrate before upgrading.

Two v2 differences catch most v1 clients out: v2 wraps every response in the
envelope below, so list payloads are nested (`data.zones`, `data.users`,
`data.templates`, `data.records`) rather than a bare `data` array; and API keys
restricted to read-only or a narrow operation scope are now enforced on every
request, where v1 requests were exempt.

## Response envelope

API v2 wraps every response in a consistent envelope:

```json
{
  "success": true,
  "data": { ... }
}
```

On error:

```json
{
  "success": false,
  "data": null,
  "message": "Invalid record type"
}
```

The error message is a plain string at the top level. There is no nested `error` object and no
machine-readable error code, so branch on the HTTP status rather than on a code in the body.

Paginated list endpoints add a `pagination` block alongside `data`.

## What the API can do

- **Zones**: list, create, update, delete; manage owners (v4.2.0+); list RRsets
- **Records**: list per zone, create, update, delete, bulk create
- **Users**: full CRUD; user responses include the groups the user belongs to (v4.5.0+)
- **Zone metadata and DNSSEC**: read and write zone metadata, read DNSSEC status, sign and unsign zones
- **Dynamic DNS**: update a record from a dynamic DNS client
- **Groups**: full CRUD, manage members and zone assignments (v4.2.0+)
- **Permission templates**: full CRUD
- **Zone templates**: full CRUD, manage template records (v4.2.0+)
- **Permissions**: list available permission flags

The complete endpoint list, request/response schemas, and an interactive
explorer live at `/api/docs` on any instance with `api.docs_enabled = true`.

## What still requires the web UI

A small number of operator workflows are not exposed through the API today:

- Creating the first admin account (handled by the installer)
- Issuing and rotating API keys (Settings -> API Keys)
- Some global Poweradmin settings under Settings -> Configuration

If an endpoint you need is missing, please open an issue on the
[GitHub repository](https://github.com/poweradmin/poweradmin/issues).

## Companion projects

Four officially maintained integrations drive the Poweradmin API for you, so check these before
writing your own client:

| Project | Use it for | Distributed as |
|---|---|---|
| [terraform-provider-poweradmin](https://github.com/poweradmin/terraform-provider-poweradmin) | Managing zones, records, RRsets, users, groups and group zone assignments, permissions and zone templates as Terraform or OpenTofu resources | Terraform Registry |
| [external-dns-poweradmin-webhook](https://github.com/poweradmin/external-dns-poweradmin-webhook) | Using Poweradmin as a backend for Kubernetes ExternalDNS, so records follow your Ingresses and Services | Container image |
| [cert-manager-webhook-poweradmin](https://github.com/poweradmin/cert-manager-webhook-poweradmin) | DNS-01 ACME challenges in Kubernetes, for automated Let's Encrypt issuance through cert-manager | Helm chart, Artifact Hub |
| [certbot-dns-poweradmin](https://github.com/poweradmin/certbot-dns-poweradmin) | DNS-01 ACME challenges from Certbot outside Kubernetes | PyPI |

Each project publishes a compatibility table mapping its own releases to the Poweradmin versions it
supports. Check it before upgrading either side.

> **Note:** These integrations target the released 4.x line. Older versions of some of them can
> still be configured against API v1, which is removed in 4.5.0, so move to a v2-capable release
> before upgrading Poweradmin.

## Next steps

- [Authentication](authentication.md) - API keys, Basic Auth, request headers
- [Endpoints](endpoints.md) - endpoint reference and where to find the
  interactive explorer
- [API Configuration](../configuration/api.md) - enabling the API, web server
  setup, security
