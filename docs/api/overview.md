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
| **v2** | `/api/v2` | Recommended | All new integrations. Consistent response envelope, RRset endpoints, bulk record creation, zone owners, zone templates, groups. |
| **v1** | `/api/v1` | Legacy, still supported | Existing integrations that have not migrated yet. |

Both versions ship together. You can use v1 and v2 from the same client; the
API keys and authentication are shared.

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
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid record type",
    "details": { "field": "type", "value": "INVALID" }
  }
}
```

Paginated list endpoints add a `pagination` block alongside `data`.

## What the API can do

- **Zones**: list, create, update, delete; manage owners (v4.2.0+); list RRsets
- **Records**: list per zone, create, update, delete, bulk create (v4.2.0+)
- **Users**: full CRUD, list groups
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

Two officially maintained projects already drive the Poweradmin API for you:

- [terraform-provider-poweradmin](https://github.com/poweradmin/terraform-provider-poweradmin) -
  manage zones, records, users, and templates from Terraform.
- [external-dns-poweradmin-webhook](https://github.com/poweradmin/external-dns-poweradmin-webhook) -
  use Poweradmin as a backend for Kubernetes ExternalDNS.

## Next steps

- [Authentication](authentication.md) - API keys, Basic Auth, request headers
- [Endpoints](endpoints.md) - endpoint reference and where to find the
  interactive explorer
- [API Configuration](../configuration/api.md) - enabling the API, web server
  setup, security
