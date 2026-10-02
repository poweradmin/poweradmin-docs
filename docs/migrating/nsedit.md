# Migrating from nsedit

[nsedit](https://github.com/tuxis-ie/nsedit) is a small PHP editor for PowerDNS. It talks to PowerDNS only over
the HTTP API and keeps its users in an SQLite file. See [Migrating from Other Tools](index.md) for the
general approach.

There is no import tool. This page describes a manual migration. Try it on a test copy first.

## What Carries Over

Records live in PowerDNS. Point Poweradmin at the same PowerDNS and the zones are there, including record comments
and the `SOA-EDIT` and `SOA-EDIT-API` metadata nsedit sets on new zones.

nsedit records the owner of each zone in two places: the zone's `account` field in PowerDNS, and the `zones` table
of its SQLite database. When the `account` field is set, nsedit uses it. Poweradmin can read that field, so zone
ownership can carry over without retyping it on Poweradmin 4.6.0 and newer, see
[step 4](#4-assign-zone-ownership).

| Stays in PowerDNS | Must be recreated in Poweradmin |
|---|---|
| Zones and records, record comments | Users |
| DNSSEC keys and zone metadata | Admin flag, as a permission template |
| Zone owner, in the `account` field | Zone ownership in Poweradmin (can be adopted from `account`) |
| | Zone templates |
| | Settings in `includes/config.inc.php` |

The nsedit log is not migrated.

## Before You Start

Find the nsedit user database. Its path is `$authdb` in `includes/config.inc.php`, by default
`../etc/pdns.users.sqlite3`, or `/app/pdns.users.sqlite3` in the Docker image. Then export the worklist:

```sql
-- users; "emailaddress" is the login name, not necessarily an email address
SELECT id, emailaddress AS username, isadmin FROM users ORDER BY emailaddress;

-- zone owners as nsedit's own table records them
SELECT z.zone, u.emailaddress AS owner
FROM zones z JOIN users u ON u.id = z.owner
ORDER BY z.zone;
```

Compare the second list with the `account` field in PowerDNS. With a database backend:

```sql
SELECT name, account FROM domains ORDER BY name;
```

nsedit's table stores zone names with a trailing dot, PowerDNS does not. A zone whose `account` is empty is owned
by the user in nsedit's table. A zone whose `account` differs from that table was changed outside nsedit; the
`account` value is what nsedit acted on.

If logging is on, export the log from **Logs** in nsedit (JSON). Back up the SQLite file and the PowerDNS database.

## Steps

### 1. Install Poweradmin

Pick a method from the [Installation](../installation/index.md) section. Poweradmin needs its own database for
users and permissions, separate from the nsedit SQLite file.

### 2. Connect It to the Same PowerDNS

nsedit uses only the PowerDNS API. Poweradmin can do the same in API backend mode: set `dns.backend` to `api`,
plus `pdns_api.url` and `pdns_api.key`. The API URL and key are the `$apiproto`, `$apiip`, `$apiport` and
`$apipass` values from nsedit's config. Some features are limited in this mode, see
[API Backend Mode](../configuration/powerdns-api.md#api-backend-mode-v430).

If Poweradmin can reach the PowerDNS database, SQL mode (the default) has the full feature set. See
[PowerDNS API](../configuration/powerdns-api.md) for both modes.

Sign in as the administrator and open the zone list. You should see the existing zones.

### 3. Recreate Users

nsedit has two kinds of user: administrators (`isadmin = 1`) and normal users. Whether a normal user may add and
delete zones is the global `$allowzoneadd` setting.

In Poweradmin, create a [permission template](../user-guide/users-roles.md) for normal users. Include zone
creation if `$allowzoneadd` was on. An nsedit administrator maps to a Poweradmin user with the `user_is_ueberuser`
permission. The full list of permissions is in [User Permissions](../user-guide/permissions.md).

Create each user under **Users**, or with the `/api/v2/users` endpoint. **Use exactly the same username as in
nsedit**, including case, so that zone ownership can be adopted in the next step. Poweradmin also requires an
email address for each user.

nsedit stores passwords as SHA-512 crypt hashes (`$6$...`). Poweradmin cannot verify these, so users set new
passwords. Users who signed in through WeFact need a password or another login method; Poweradmin supports
[LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md) and [SAML](../configuration/saml.md).

### 4. Assign Zone Ownership

Zones that Poweradmin did not create have no owner. Non-administrators cannot see them until they get one.

On Poweradmin 4.6.0 and newer:

1. Set `dns.adopt_zone_owner_from_account` to `true` in `config/settings.php` (Docker:
   `PA_DNS_ADOPT_ZONE_OWNER_FROM_ACCOUNT=true`).
2. Set `interface.enable_consistency_checks` to `true`, then open the
   [Database Consistency Check](../maintenance/consistency-check.md) (`/tools/database-consistency`).
3. Under "zones without owners", choose **Assign all to me**. Each zone goes to the user whose username matches its
   `account` field exactly. Zones with no match go to you. Zones whose `account` is `admin`, nsedit's default, go
   to the Poweradmin user `admin` if there is one.
4. Fix the zones from [Before You Start](#before-you-start) whose `account` was empty, on the zone's ownership page
   or with `/api/v2/zones/{id}/owners`.

On 4.5.0 and earlier, **Assign all to me** gives every zone to you. Reassign them on each zone's ownership page, or
script it with `/api/v2/zones/{id}/owners` from the list in [Before You Start](#before-you-start).

In API backend mode the zone sync also applies the setting, so zones may already have their owners when you open
the check. The setting never replaces an existing owner. Leave it on if you want zones that keep arriving with an
`account`, for example from an autoprimary, to get an owner too. See
[Supermasters and Autoprimaries](../user-guide/supermasters.md).

nsedit allows one owner per zone. In Poweradmin a zone can have several user owners and group owners, see
[Zone Ownership](../user-guide/zones.md#zone-ownership).

### 5. Recreate Templates

nsedit templates come from `$templates` in its config and from JSON files in `templates.d/`. Recreate the ones you
use as [DNS templates](../user-guide/dns-templates.md). Replace nsedit's `[zonename]` placeholder with Poweradmin's
`[ZONE]`. NS records in an nsedit template filled the nameserver fields; in Poweradmin they are ordinary template
records, and `[NS1]`, `[NS2]` and so on insert the configured nameservers. To copy an existing zone, use
[Save as Template](../user-guide/dns-templates.md#saving-an-existing-zone-as-a-template).

The default nameservers and TTL from nsedit's `$defaults` correspond to Poweradmin's `dns.ns1` to `dns.ns4` and
`dns.ttl`, see [DNS Settings](../configuration/dns-settings.md).

### 6. Replace Scripts

nsedit's "API" is the `zones.php` endpoint, called with `$adminapikey` from an address in `$adminapiips`. Scripts
that use it must be rewritten for Poweradmin's REST API at `/api/v2`, see [API Overview](../api/overview.md) and
[API Authentication](../api/authentication.md).

### 7. Switch Over

1. Ask a few users to sign in and check that they see their zones.
2. Stop making changes in nsedit. Both tools write to PowerDNS, so a record changed in one shows up in the other.
   Zones created in Poweradmin carry no nsedit owner, so nsedit shows them as owned by `admin`.
3. Shut nsedit down. Keep the SQLite file and the exported log if you need the history.

## Concept Mapping

| nsedit | Poweradmin |
|---|---|
| Admin user (`isadmin = 1`) | User with `user_is_ueberuser` |
| Normal user | User with a [permission template](../user-guide/users-roles.md) |
| `$allowzoneadd` | Zone creation permissions in the template |
| Zone owner (`account` field) | [Zone ownership](../user-guide/zones.md#zone-ownership), adopted with `dns.adopt_zone_owner_from_account` (4.6.0+) |
| Template (`$templates`, `templates.d/`) | [DNS template](../user-guide/dns-templates.md) |
| Zone import (zone data on creation) | [Zone Import](../configuration/zone-import-export.md) |
| Zone clone | [Save the zone as a template](../user-guide/dns-templates.md#saving-an-existing-zone-as-a-template), then create the new zone from it |
| Log | [Record change log](../user-guide/record-change-log.md) and the zone logs at `/zones/logs`, not migrated |
| WeFact login | No equivalent; [LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md) or [SAML](../configuration/saml.md) |
| `zones.php` with `$adminapikey` | [REST API](../api/overview.md) with an API key |
