# API Endpoints

This page is a task-shaped map of the API, not the complete list. The
[API Reference](reference.md) is generated from the source and documents every
operation with its full request and response schemas - use that when you need
the authoritative answer, and this page when you want to find the right
endpoint for a job.

A running instance can also serve the same specification interactively.

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
| `GET` | `/zones` | List zones; `id` is the identifier the other zone endpoints take (from v4.6.0, `canonical_id` carries the same value) |
| `POST` | `/zones` | Create zone |
| `GET` | `/zones/{id}` | Get zone |
| `PUT` | `/zones/{id}` | Update zone |
| `DELETE` | `/zones/{id}` | Delete zone |
| `GET` | `/zones/{id}/owners` | List zone owners (v4.2.0+) |
| `POST` | `/zones/{id}/owners` | Add owner(s), supports batch (v4.2.0+) |
| `DELETE` | `/zones/{id}/owners/{user_id}` | Remove owner (v4.2.0+) |

From v4.2.6, v4.3.5, v4.4.1 and v4.5.0, changing a zone's `name`, `type` or `master` through
`PUT /zones/{id}` requires the zone metadata permission (`zone_meta_edit_own` or
`zone_meta_edit_others`), the same gate as the web edit form; record content permissions alone
return `403`. A value that matches what is stored is not treated as a change, so clients that
resend every field on update keep working.

From v4.5.0, in API backend mode, `POST /zones/{id}/owners` answers `409` with "Owners cannot be added to this
zone: its ID is shared with another zone" when the id belongs to two zones. See
[Zone IDs Shared by Two Zones](../configuration/powerdns-api.md#zone-ids-shared-by-two-zones).

#### Setting the serial policy on create (v4.5.0+)

`POST /zones` accepts an optional `soa_edit_api` string that sets the zone's
SOA-EDIT-API serial policy:

```json
{
  "name": "example.com",
  "type": "MASTER",
  "soa_edit_api": "INCREASE"
}
```

Omit the field, or send an empty string, to apply the `dns.soa_edit_api`
configuration default. Send `OFF` to disable the policy for this zone
specifically; in API backend mode that also clears the default PowerDNS applies.

The accepted values are `DEFAULT`, `INCREASE`, `EPOCH`, `SOA-EDIT`,
`SOA-EDIT-INCREASE` and `OFF`, narrowed to whatever the `dns.soa_edit_api_options`
configuration list allows. A value outside that set returns `400`, and so does a
non-string value. This differs deliberately from the add-zone form, which silently
drops an unoffered value and falls back to the default.

Two limits worth knowing before scripting against it. The field is create-only:
`PUT /zones/{id}` does not accept it, and an existing zone's policy is changed
through `PUT /zones/{id}/metadata/SOA-EDIT-API` instead. And a SLAVE zone takes
its serial from the primary, so a value accepted there is validated but never
applied.

### Zone metadata and DNSSEC

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/zones/{id}/metadata` | List all metadata kinds for a zone (v4.3.0+) |
| `GET` | `/zones/{id}/metadata/{kind}` | Get one metadata kind (v4.3.0+) |
| `PUT` | `/zones/{id}/metadata/{kind}` | Set one metadata kind (v4.3.0+) |
| `DELETE` | `/zones/{id}/metadata/{kind}` | Remove one metadata kind (v4.3.0+) |
| `GET` | `/zones/{id}/dnssec` | Get DNSSEC status and keys (v4.5.0+) |
| `POST` | `/zones/{id}/dnssec` | Sign or unsign the zone (v4.5.0+) |
| `GET` | `/zones/{id}/dnssec/keys` | List the zone's keys with their DNSKEY and DS (v4.5.0+) |
| `POST` | `/zones/{id}/dnssec/keys` | Add a key (`type`, `algorithm`, `bits`, optional `active`) (v4.5.0+) |
| `POST` | `/zones/{id}/dnssec/keys/import` | Import a key from a BIND-format private key (`type`, `privatekey`, optional `active`) (v4.6.0+) |
| `GET` | `/zones/{id}/dnssec/keys/{key_id}` | Get one key (v4.5.0+) |
| `PATCH` | `/zones/{id}/dnssec/keys/{key_id}` | Activate or deactivate a key (v4.5.0+) |
| `DELETE` | `/zones/{id}/dnssec/keys/{key_id}` | Delete a key (v4.5.0+) |
| `POST` | `/zones/{id}/dnssec/rectify` | Rectify a signed primary zone (v4.5.0+) |

Reading keys needs view access to the zone; the other key endpoints need `zone_dnssec_manage_own`
on the zone (or administrator rights) and the PowerDNS API. From 4.6.0, adding, importing,
updating and deleting keys also needs view access to the zone, as on the web DNSSEC pages, and
answers `403` without it. For API key scopes, adding a key is a
`create` operation and rectifying is an `update`. New keys are created inactive unless `active` is
`true`, as in the web UI. A key's `type` is the role PowerDNS derives on every read (`ksk` or
`zsk` only while an active SEP and an active non-SEP key share an algorithm, otherwise `csk`); from
4.6.0 the `sep` field reports the stored secure-entry-point flag. Rectify is refused for Secondary
and Consumer zones. When PowerDNS
cannot be reached, the status, sign/unsign, key and rectify endpoints answer `502` rather than
reporting the zone as unsigned.

An imported key must use an algorithm offered for new keys on the connected PowerDNS version.
Any other algorithm answers `400` with "The private key uses an unsupported algorithm (one of:
...)", listing the accepted ones.

### Server status (v4.5.0+)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/server/status` | PowerDNS version, uptime and statistics, for monitoring |

Requires the `server_status_view` permission (administrators have it implicitly) and the
PowerDNS API to be configured. It works with read-only keys; keys restricted to specific zones
get `403` because the status is not tied to a zone. The endpoint does not depend on
`interface.show_pdns_status`.

- `?metrics=uptime,udp-queries` returns only the named metrics
- `?include=slaves` also probes the configured autoprimary servers, which is slower. It needs
  `supermaster_view` as well, since it lists their addresses
- `501` means the PowerDNS API is not configured, `503` means PowerDNS is not reachable, so a
  monitoring check can rely on the status code alone

```json
{
  "success": true,
  "message": "Server status retrieved successfully",
  "data": {
    "running": true,
    "server_id": "localhost",
    "daemon_type": "authoritative",
    "version": "4.9.4",
    "uptime_seconds": 86400,
    "metrics": { "udp-queries": "1234", "uptime": "86400" }
  }
}
```

### Dynamic DNS

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/dynamic-dns` | Update a record from a dynamic DNS client (v4.5.0+) |

This is the API v2 equivalent of the standalone `dynamic_update.php` script
described in [Dynamic DNS](../user-guide/ddns/overview.md). Both remain
supported; the standalone script keeps the dyndns2-compatible query-string
interface that routers expect.

### Change requests (v4.6.0+)

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/zones/{id}/change-requests` | File a change request for a zone |
| `GET` | `/change-requests` | List change requests in the caller's review scope plus the caller's own |
| `GET` | `/change-requests/{id}` | Get a change request with its stale actions |
| `POST` | `/change-requests/{id}/approve` | Approve and apply a change request |
| `POST` | `/change-requests/{id}/reject` | Reject a change request |
| `DELETE` | `/change-requests/{id}` | Cancel the caller's own pending change request |

All of them answer `404` while `approval.enabled` is off. When the caller's changes to a
zone are routed through review, the record write endpoints below answer `403` with
"Changes to this zone require approval; create a change request instead". See
[Change Requests](../user-guide/change-requests.md#api-v2).

### Records

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/zones/{id}/records` | List records in a zone |
| `POST` | `/zones/{id}/records` | Create record |
| `GET` | `/zones/{id}/records/{recordId}` | Fetch a single record |
| `PUT` | `/zones/{id}/records/{recordId}` | Update record |
| `DELETE` | `/zones/{id}/records/{recordId}` | Delete record |
| `POST` | `/zones/{id}/records/bulk` | Bulk create, update and delete records |
| `GET` | `/zones/{id}/rrsets` | List RRsets |
| `GET` | `/zones/{id}/rrsets/{name}/{type}` | Get a specific RRset |

When `ttl` is omitted on a record create call, Poweradmin applies the
configured default (`dns.ttl_reverse` for PTR records in reverse zones when
set, `dns.ttl` otherwise). See
[DNS settings](../configuration/dns-settings.md) for details. A `ttl` of `0`
is accepted (do not cache); negative values and fractional strings such as
`"0.5"` are refused with `400`.

Records in **Secondary** and **Consumer** zones are read-only - they replicate
from a primary. Create, update, delete, and bulk-write calls against such a
zone return `403` with a message stating the zone is read-only (rather than a
permission error). Edit the records on the primary instead.

#### PowerDNS refusals in API backend mode (v4.6.0+)

In API backend mode, when PowerDNS answers a write with 400 or 422, the API returns `422` with the
usual message followed by the PowerDNS reason, for example `Failed to create record: RRset
www.example.com. IN LUA: update of Lua records is not allowed`. This covers record create, update
and delete, bulk operations, RRset replace and delete, zone create from a template (`Failed to create LUA
record for zone: <reason>`) and change request approval. When PowerDNS is unreachable or fails, the
status stays `500` with the old message. Before 4.6.0 every one of these answered `500`. See the
[LUA record note](../configuration/powerdns-api.md#known-issue-lua-records-refused-on-powerdns-auth-51).

#### Record comments (v4.6.0+)

Record responses (list, single `GET`, `POST` and `PUT`) include `comment`, a string or `null`.
`GET /zones/{id}/records` accepts a `comment` filter, a case-insensitive substring match like
`name` and `content`. Records without a comment never match it, and `q` does not search comments.

With the SQL backend the value is the record's linked comment, else the comment stored for its
name and type. In API backend mode it is the RRset comment, so every record in an RRset returns
the same one. A `PUT` without `comment` leaves the stored comment alone; an empty string clears it.

#### Bulk operations

`POST /zones/{id}/records/bulk` takes an `operations` array. Each operation has an `action` of
`create`, `update` or `delete`, plus the fields of the matching single-record call (bulk
`update` has no `update_ptr`).

- `comment` on a `create` or `update` operation sets the record comment. The top-level `comment`
  is the change reason; on its own it satisfies the require-reason setting.
- `create_ptr` on a `create` operation (A and AAAA records only) also creates the PTR record in
  the matching reverse zone. A PTR that cannot be created does not fail the batch; the reason is
  added to `data.warnings`, which is always present and empty when there is nothing to report.
  That includes a reverse zone outside the API key's zone list and one where the user must file
  change requests: the PTR is skipped there, as with `create_ptr` and `update_ptr` on the
  single-record calls.
- With the SQL backend the batch is one transaction and the PTR records roll back with it. In API
  backend mode there is no transaction: operations already applied, PTR records included, stay
  when a later operation fails.

Set `dry_run` to `true` at the top level to run every check without writing anything. The zone
scope, permissions, change-approval refusal, operation cap and required reason apply as for a real
call, and the summary comes back with `"dry_run": true`. No records, comments, PTR records, serial
change, log entry or change request is kept.

```bash
curl -X POST -H "X-API-Key: your-api-key-here" -H "Content-Type: application/json" \
     -d '{"dry_run": true, "comment": "move the web tier", "operations": [
           {"action": "create", "name": "www", "type": "A", "content": "192.0.2.10",
            "comment": "web server", "create_ptr": true}]}' \
     "https://poweradmin.example.com/api/v2/zones/42/records/bulk"
```

With the SQL backend a dry run executes the operations inside the transaction and rolls it back,
so the result is exact. In API backend mode it only validates each operation against the zone as
it is now, and tracks deletes, re-keying updates and duplicate creates inside the batch. It does
not see a create followed by an update of that record, AAAA addresses spelled differently, a
second `create_ptr` for the same address, or a CNAME added next to other data in the same batch.
PowerDNS's own checks, such as the LUA record gate, are not run.


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
exists, the request fails rather than granting administrator rights. This applies from
v4.2.6, v4.3.5, v4.4.1 and v4.5.0 - on earlier releases, omitting the field created an
administrator, so check any client that relies on the old default.

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

From v4.2.6, v4.3.5, v4.4.1 and v4.5.0, adding or updating a template record validates the
content against the record type and returns `400` with the validator message when it fails.
See [Record validation](../user-guide/dns-templates.md#record-validation) for the rules,
including where MX and SRV priority belongs.

From the same releases, `GET /zone-templates` and `GET /zone-templates/{id}/records` are also
readable with `zone_master_add` or `zone_slave_add`, matching the add-zone form, which offers
templates to anyone who may add a zone. Writing a template still needs the template permissions.

## Health endpoints (v4.5.0+)

These sit outside the versioned API and outside the API key model. They take no
credentials, are **disabled by default**, and return `404` while disabled. Paths are
absolute, not relative to `/api/v2`.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/health` | Readiness: database and PowerDNS API reachability. `200` healthy, `503` otherwise |
| `GET` | `/ping` | Liveness: returns `ok` and checks nothing else |

They are not part of the OpenAPI specification, and they answer regardless of whether
`api.enabled` is set. See [Health Checks](../operations/health-checks.md).

## API v1 endpoints

**Removed in 4.5.0.** On 4.5.0 and later, every `/api/v1` path answers
`410 Gone` and points at `/api/v2`.

On 4.2.x-4.4.x, v1 is still available under `/api/v1`. The endpoint surface is
similar but the response envelope is less consistent and several v2 features
(RRsets, bulk records, zone owners, groups, zone templates) are not available.
See [API Configuration](../configuration/api.md#api-v1-endpoints-legacy-removed-in-450) for
the v1 endpoint list, and migrate to v2 before upgrading to 4.5.0.

## Paging, sorting and filtering

From 4.6.0, the v2 list endpoints in the table below accept `page` and `per_page`, and most
also take `sort` and a few filters. Before 4.6.0 only `/zones` and `/users` paged, and none
sorted or filtered. Short lists such as `/zones/{id}/owners` always come back whole.

### Paging

```bash
GET /api/v2/zones?page=2&per_page=50
```

Without `per_page` (or with `per_page=0`) the whole list comes back and there is no
`pagination` object. With it, `page` starts at 1 (a smaller value is read as 1), `per_page`
is capped at 10000, and the response carries a `pagination` object at the top level, next to
`data`:

```json
{
  "success": true,
  "data": { "zones": [ ... ] },
  "pagination": { "current_page": 2, "per_page": 50, "total": 150, "last_page": 3 }
}
```

A page past the end returns an empty list together with the `pagination` object, so a client
can stop when `current_page` reaches `last_page`.

> **Warning:** The parameter is `per_page`, not `limit`. An unrecognised
> parameter is ignored rather than rejected, so `?limit=50` silently returns
> every row.

From 4.6.0, a query parameter sent as an array, such as `?type[]=A`, answers `400` with
"Query parameter 'type' must be a single value". This applies to every v2 endpoint and to the
internal API.

### Sorting

`sort` takes comma-separated field names, each with an optional `:asc` or `:desc` suffix
(ascending by default), up to five fields:

```bash
GET /api/v2/zones/42/records?sort=type,name:desc
```

A field the endpoint does not offer, a field given twice, or a direction other than `asc` or
`desc` answers `400` with a message that lists the allowed fields.

Without `sort`, most lists come in the database order of their name column; the exceptions are
noted in the table below. Lists that are sorted in memory (records, RRsets, groups, templates,
permissions) compare text fields case-insensitively in natural order, so `host2` sorts before
`host10`. `/zones` applies that natural order only for `sort=name`, where numeric prefixes are
compared as numbers. `/users` sorts case-insensitively but not naturally.

### Filters

Every filter is a query parameter and combines with `sort`, `page` and `per_page`. The
`pagination.total` counts the filtered list. `q` is a case-insensitive substring match.

| Endpoint | Sort fields | Filters |
|----------|-------------|---------|
| `GET /zones` | `name`, `type`, `id` | `name` (exact zone name), `q` (zone name) |
| `GET /zones/{id}/records` | `name`, `type`, `content`, `ttl`, `priority` | `type` (record type), `name`, `content`, `comment`, `q` (name or content). Default order: type, then name (as PowerDNS returns them in API backend mode) |
| `GET /zones/{id}/rrsets` | `name`, `type`, `ttl` | `type` (record type), `name`, `content`, `q` (name or content); `content` and `q` keep an RRset when any of its records matches. Default order: type, then name (as PowerDNS returns them in API backend mode) |
| `GET /users` | `id`, `username`, `fullname`, `email` | `q` (username, full name, email or description), `username` and `email` (exact lookups, see below). Default order: `id` |
| `GET /groups` | `id`, `name`, `member_count`, `zone_count`, `created_at` | `q` (name or description) |
| `GET /groups/{id}/members` | `user_id`, `username`, `fullname`, `email`, `joined_at` | `q` (username, full name or email). Default order: newest member first |
| `GET /groups/{id}/zones` | `zone_id`, `zone_name`, `zone_type`, `created_at` | `q` (zone name). Default order: newest assignment first |
| `GET /zone-templates` | `id`, `name`, `zones_linked` | `q` (name or description) |
| `GET /zone-templates/{id}/records` | `name`, `type`, `content`, `ttl`, `priority` | `type` (record type, case-insensitive), `name`, `content`, `q` (name or content) |
| `GET /permissions` | `id`, `name` | `q` (name or description) |
| `GET /permission-templates` | `id`, `name`, `template_type` | `q` (name or description), `type` (`user` or `group`; anything else answers `400`) |
| `GET /change-requests` | none | `status` (`pending` by default; `approved`, `rejected`, `cancelled`, `failed` or `all`; anything else answers `400`), `zone_id`. Default order: newest first |

`name` and `content` (and `comment` on the zone record list) are case-insensitive substring matches like `q`;
`q` searches both columns at once.

`GET /users?username=alice` and `GET /users?email=alice@example.com` look up one user. The
list then holds that user or is empty, `page`, `per_page` and `q` are ignored, `sort` is
checked but not applied, no `pagination` object is returned, and `username` wins when both are
given.

`GET /change-requests` ignores `sort`; it always lists newest first. Without `per_page` it
returns at most 10000 requests, and when more match, the response carries a `pagination`
object (`per_page` 10000, `last_page` above 1) so the client knows to page on with
`per_page` and `page`.

### Examples

The second page of 50 zones, newest id first:

```bash
curl -H "X-API-Key: your-api-key-here" \
     "https://poweradmin.example.com/api/v2/zones?sort=id:desc&page=2&per_page=50"
```

The A records of a zone that mention `mail`, by name:

```bash
curl -H "X-API-Key: your-api-key-here" \
     "https://poweradmin.example.com/api/v2/zones/42/records?type=A&q=mail&sort=name"
```

Group permission templates, ordered by name:

```bash
curl -H "X-API-Key: your-api-key-here" \
     "https://poweradmin.example.com/api/v2/permission-templates?type=group&sort=name"
```

## Related documentation

- [Overview](overview.md) - what the API can do, response envelope
- [Authentication](authentication.md) - API keys and Basic Auth
- [API Configuration](../configuration/api.md) - enabling the API, web server
  requirements, security, request/response examples
- [Dynamic DNS with cURL](../user-guide/ddns/using-curl.md) - the separate,
  simpler `dynamic_update.php` endpoint for IP-update scripts
