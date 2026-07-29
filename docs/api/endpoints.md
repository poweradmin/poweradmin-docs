# API Endpoints

The fastest way to discover the full set of endpoints with request and
response schemas is the interactive OpenAPI explorer that ships with
Poweradmin. This page is a high-level map; the explorer is the source of
truth.

## Interactive API documentation

When `api.docs_enabled = true` in `config/settings.php`, every Poweradmin
instance hosts its own Swagger UI:

```
https://your-poweradmin-host/api/docs
```

From there you can:

- Browse every endpoint grouped by tag (Zones, Records, Users, ...)
- See the exact JSON request and response schemas
- Paste in an API key via the **Authorize** button
- Issue real requests against the running instance and inspect the response

For production deployments, leave `docs_enabled` off and use a staging
instance for exploration.

## High-level endpoint map (API v2)

API v2 is the recommended version. All paths are prefixed with `/api/v2`.

### Zones

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/zones` | List zones |
| `POST` | `/zones` | Create zone |
| `GET` | `/zones/{id}` | Get zone |
| `PUT` | `/zones/{id}` | Update zone |
| `DELETE` | `/zones/{id}` | Delete zone |
| `GET` | `/zones/{id}/owners` | List zone owners (v4.2.0+) |
| `POST` | `/zones/{id}/owners` | Add owner(s), supports batch (v4.2.0+) |
| `DELETE` | `/zones/{id}/owners/{user_id}` | Remove owner (v4.2.0+) |

### Records

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/zones/{id}/records` | List records in a zone |
| `POST` | `/zones/{id}/records` | Create record |
| `PUT` | `/zones/{id}/records/{record_id}` | Update record |
| `DELETE` | `/zones/{id}/records/{record_id}` | Delete record |
| `POST` | `/zones/{id}/records/bulk` | Bulk create records (v4.2.0+) |
| `GET` | `/zones/{id}/rrsets` | List RRsets (v4.2.0+) |
| `GET` | `/zones/{id}/rrsets/{name}/{type}` | Get a specific RRset (v4.2.0+) |

When `ttl` is omitted on a record create call, Poweradmin applies the
configured default (`dns.ttl_reverse` for PTR records in reverse zones when
set, `dns.ttl` otherwise). See
[DNS settings](../configuration/dns-settings.md) for details.

Records in **Secondary** and **Consumer** zones are read-only - they replicate
from a primary. Create, update, delete, and bulk-write calls against such a
zone return `403` with a message stating the zone is read-only (rather than a
permission error). Edit the records on the primary instead.

### Users

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/users` | List users |
| `POST` | `/users` | Create user |
| `GET` | `/users/{id}` | Get user |
| `PUT` | `/users/{id}` | Update user |
| `DELETE` | `/users/{id}` | Delete user |

Writing `perm_templ` is gated separately from the write itself, and a rejected
assignment returns `403`:

- Callers holding `user_is_ueberuser` may assign any template.
- Callers holding `user_edit_templ_perm` may assign any template that does **not**
  grant `user_is_ueberuser`, and may not change their own account's template unless
  they also hold `user_edit_others`.
- Everyone else may not send `perm_templ` at all.

Omitting `perm_templ` on create assigns the least-privileged non-superuser template,
whoever the caller is; it no longer falls back to template id 1. If no such template
exists, the request fails rather than granting administrator rights.

#### Permission template and groups on reads (v4.5.0+)

User reads carry the assigned permission template by ID and by name, plus the
groups the user belongs to:

```json
{
  "user_id": 5,
  "username": "svc-acme",
  "perm_templ": 2,
  "perm_templ_name": "Zone Manager",
  "groups": [{ "id": 3, "name": "dns-operators" }]
}
```

`perm_templ_name` is `null` when the stored template no longer exists or is a
group template rather than a user template.

#### Assigning groups on create (v4.5.0+)

`POST /users` accepts an optional `groups` array holding integer group IDs,
exact group names, or a mix of both:

```json
{
  "username": "svc-acme",
  "password": "...",
  "perm_templ": 2,
  "groups": [3, "dns-operators"]
}
```

The response lists the memberships that were actually created, so a caller does
not have to assume the request took full effect:

```json
{ "user_id": 5, "groups": [{ "id": 3, "name": "dns-operators" }] }
```

Rules worth knowing before you script against it:

- Sending `groups` requires `user_is_ueberuser`, because a group carries its own
  permission template. Callers without it get `403`, even when they may otherwise
  create users.
- Names are matched exactly, including case and accents. `"Viewers"` resolves,
  `"viewers"` does not. This is deliberate: MySQL's default collation would
  otherwise accept variants that PostgreSQL and SQLite reject.
- Numeric strings are treated as names, not IDs. Send `3` to reference group 3;
  `"3"` is looked up as a group named `3` and will normally fail.
- If any entry does not resolve to a group, the whole request returns `400` and
  no user is created.
- Naming the same group more than once, whether by ID and by name or by
  repeating one value, still creates a single membership.
- The array may hold up to 50 groups. A longer list returns `400` and creates
  nothing.

Membership changes after creation go through
`POST`/`DELETE /groups/{id}/members`; `PUT /users/{id}` does not accept `groups`.

### Groups (v4.2.0+)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/groups` | List groups |
| `POST` | `/groups` | Create group |
| `GET` | `/groups/{id}` | Get group |
| `PUT` | `/groups/{id}` | Update group |
| `DELETE` | `/groups/{id}` | Delete group |
| `GET` | `/groups/{id}/members` | List group members |
| `POST` | `/groups/{id}/members` | Add member |
| `DELETE` | `/groups/{id}/members/{user_id}` | Remove member |
| `GET` | `/groups/{id}/zones` | List zones assigned to group |
| `POST` | `/groups/{id}/zones` | Assign zone to group |
| `DELETE` | `/groups/{id}/zones/{zone_id}` | Remove zone from group |

### Permission templates

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/permission-templates` | List templates |
| `POST` | `/permission-templates` | Create template |
| `GET` | `/permission-templates/{id}` | Get template |
| `PUT` | `/permission-templates/{id}` | Update template |
| `DELETE` | `/permission-templates/{id}` | Delete template |
| `GET` | `/permissions` | List available permission flags |
| `GET` | `/permissions/{id}` | Get permission flag details |

### Zone templates (v4.2.0+)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/zone-templates` | List zone templates |
| `POST` | `/zone-templates` | Create zone template |
| `GET` | `/zone-templates/{id}` | Get zone template |
| `PUT` | `/zone-templates/{id}` | Update zone template |
| `DELETE` | `/zone-templates/{id}` | Delete zone template |
| `GET` | `/zone-templates/{id}/records` | List template records |
| `POST` | `/zone-templates/{id}/records` | Add template record |
| `PUT` | `/zone-templates/{template_id}/records/{id}` | Update template record |
| `DELETE` | `/zone-templates/{template_id}/records/{id}` | Delete template record |

## API v1 endpoints

**Removed in 4.5.0.** On 4.5.0 and later, every `/api/v1` path answers
`410 Gone` and points at `/api/v2`.

On 4.2.x-4.4.x, v1 is still available under `/api/v1`. The endpoint surface is
similar but the response envelope is less consistent and several v2 features
(RRsets, bulk records, zone owners, groups, zone templates) are not available.
See [API Configuration](../configuration/api.md#api-v1-endpoints-legacy) for
the v1 endpoint list, and migrate to v2 before upgrading to 4.5.0.

## Pagination

List endpoints for zones and users accept `page` and `limit` query
parameters:

```bash
GET /api/v2/zones?page=1&limit=50
```

Omitting both returns all results (added in v4.0.1). Paginated responses
include a `pagination` block:

```json
{
  "pagination": { "total": 150, "page": 1, "limit": 50, "pages": 3 }
}
```

## Related documentation

- [Overview](overview.md) - what the API can do, response envelope
- [Authentication](authentication.md) - API keys and Basic Auth
- [API Configuration](../configuration/api.md) - enabling the API, web server
  requirements, security, request/response examples
- [Dynamic DNS with cURL](../user-guide/ddns/using-curl.md) - the separate,
  simpler `dynamic_update.php` endpoint for IP-update scripts
