# Migrating from PowerDNS-Admin

PowerDNS-Admin and Poweradmin are two separate projects with similar names. PowerDNS-Admin is a Python/Flask
application. Poweradmin is a PHP application. Both are web interfaces for the PowerDNS authoritative server.
Poweradmin supports PowerDNS 4.0.0 and newer, see [System Requirements](../getting-started/requirements.md).

There is no import tool. This page describes a manual migration. Try it on a test copy first.

## What Carries Over

Records live in PowerDNS. Neither tool stores them itself, so there is nothing to export or convert. Point
Poweradmin at the same PowerDNS and the zones are there.

PowerDNS-Admin keeps a copy of the zone list in its own database and refreshes it from the PowerDNS API. It also
stores users, accounts, roles, zone-to-user mappings, API keys, settings and history there. None of that carries
over. The migration is mostly about users and permissions.

| Stays in PowerDNS | Must be recreated in Poweradmin |
|---|---|
| Zones and records | Users |
| DNSSEC keys and zone metadata | Accounts, as groups |
| | Roles, as permission templates |
| | API keys |
| | Login setup (LDAP, OIDC, SAML) |
| | Settings, domain templates |

History is not migrated.

## Before You Start

Export a list of users, their roles, and which zones each user can reach. This is your worklist. The query below
runs against the PowerDNS-Admin database. Quote `user` as `"user"` on PostgreSQL.

```sql
-- users and roles
SELECT u.username, u.email, r.name AS role
FROM user u JOIN role r ON r.id = u.role_id;

-- zones a user can reach directly
SELECT u.username, d.name AS zone
FROM domain_user du
JOIN user u ON u.id = du.user_id
JOIN domain d ON d.id = du.domain_id;

-- account members and the zones of each account
SELECT a.name AS account, u.username, d.name AS zone
FROM account a
JOIN account_user au ON au.account_id = a.id
JOIN user u ON u.id = au.user_id
LEFT JOIN domain d ON d.account_id = a.id;
```

Also write down:

- API keys that scripts use, and which zones or accounts each key is limited to.
- Hosts that send dynamic DNS updates to PowerDNS-Admin.

Back up the PowerDNS database and the PowerDNS-Admin database.

## Steps

### 1. Install Poweradmin

Pick a method from the [Installation](../installation/index.md) section, for example [Docker](../installation/docker.md)
or the [Web Installer Wizard](../installation/wizard.md). Poweradmin creates its own tables for users, groups and
permissions. Do not point it at the PowerDNS-Admin database.

### 2. Connect It to the Same PowerDNS

PowerDNS-Admin only ever talks to PowerDNS over the HTTP API. Poweradmin can work in two modes:

- SQL mode (default). Poweradmin reads and writes the PowerDNS database (MySQL/MariaDB, PostgreSQL or SQLite) and
  uses the PowerDNS API for DNSSEC, zone transfers and metadata. Configure the database as described in
  [Database Configuration](../configuration/database.md) and set `pdns_api.url` and `pdns_api.key`.
- API backend mode. Set `dns.backend` to `api`, plus `pdns_api.url` and `pdns_api.key`. Poweradmin then needs no
  access to the PowerDNS database. This is the closest match to how PowerDNS-Admin works, but some features are
  limited in this mode. See
  [Restrictions with the PowerDNS API backend](../user-guide/zones.md#restrictions-with-the-powerdns-api-backend).

SQL mode has the full feature set. Use API backend mode when Poweradmin cannot reach the PowerDNS database. See
[PowerDNS API](../configuration/powerdns-api.md) for the settings in both modes.

One Poweradmin installation manages one PowerDNS server, the one named by `pdns_api.server_name`.

Sign in as the administrator and open the zone list. You should see the existing zones.

### 3. Recreate Roles as Permission Templates

PowerDNS-Admin has three roles: Administrator, Operator and User. Whether a User may create or delete zones, or
view history, is a global setting there. In Poweradmin these are individual permissions grouped into a
[permission template](../user-guide/users-roles.md). Create one template for each role you use, and more if some
users need different rights. The full list of permissions is in [User Permissions](../user-guide/permissions.md).

An Administrator in PowerDNS-Admin maps to a Poweradmin user with the `user_is_ueberuser` permission.

### 4. Recreate Users

Create users under **Users**, or use the `/api/v2/users` endpoint. Give each user a permission template, or put the
permissions on a group instead (next step). The `permissions.show_user_access_templates` and
`permissions.show_group_access_templates` settings control which of the two is shown in the interface, see
[Permissions Settings](../configuration/permissions.md).

Poweradmin does not import password hashes. Users set new passwords, or sign in through an external system.
Poweradmin supports [LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md) and
[SAML](../configuration/saml.md). PowerDNS-Admin also offers Google, GitHub and Azure login. These have no direct
equivalent; check whether your provider offers OIDC or SAML.

Two-factor login is off by default, set `mfa.enabled`. Each user enrolls again, see [MFA](../user-guide/mfa.md).

### 5. Recreate Accounts as Groups and Assign Zones

A PowerDNS-Admin account is a set of zones shared by its member users. Each zone belongs to at most one account.
The matching concept in Poweradmin is a [group](../user-guide/groups.md):

1. Create a group for each account and give it a permission template.
2. Add the account's members to the group.
3. On the group's zones page, move the account's zones from **Available Zones** to **Owned Zones**. You can select
   several zones at once.

Zones that a user reaches directly (the `domain_user` table) become user ownership in Poweradmin. Open the zone,
then its ownership page (`/zones/{id}/ownership`), and add the user. A zone can have user owners and group owners at
the same time. See [Zone Ownership](../user-guide/zones.md#zone-ownership).

There is no "change owner" action for several zones on the zone list. For many zones, assign them through a group
or script it with the API: `/api/v2/zones/{id}/owners` for users and `/api/v2/groups/{id}/zones` for groups.

### 6. Recreate API Keys

PowerDNS-Admin API keys carry a role and are limited to a set of zones or accounts. Poweradmin API keys belong to
a user and can do what that user can do. To keep a key limited to some zones, create a service user for the script,
give it a permission template and make it owner of those zones (or a member of a group that owns them), then create
the key under that user.

Enable the API (`api.enabled = true`) and create keys under **Settings -> API Keys** (`/settings/api-keys`), see
[API Authentication](../api/authentication.md). A regular user can hold up to `api.max_keys_per_user` keys
(default 5). Administrators have no limit.

The API itself is different. Poweradmin's API is `/api/v2`, authenticated with the `X-API-Key` header, see
[API Overview](../api/overview.md). Scripts that use PowerDNS-Admin's own endpoints (`/api/v1/pdnsadmin/...`)
must be rewritten. PowerDNS-Admin also passes `/api/v1/servers/...` calls through to PowerDNS. Scripts that use
those can usually be pointed at the PowerDNS API directly, with a PowerDNS API key.

### 7. Move Dynamic DNS Clients

PowerDNS-Admin accepts dynamic updates at `/nic/update` with the user's login as HTTP Basic Auth. Poweradmin has two
endpoints, see [Dynamic DNS](../user-guide/ddns/overview.md):

- `/dynamic_update.php`, a dyndns2-style endpoint for stock clients such as ddclient, authenticated with the
  Poweradmin username and password.
- `POST /api/v2/dynamic-dns`, authenticated with an API key.

Change the URL in each client. Users who authenticate with a password need their new Poweradmin password.

### 8. Optional Features

- [DNS templates](../user-guide/dns-templates.md) replace PowerDNS-Admin domain templates. Recreate them by hand.
- [DNSSEC](../user-guide/dnssec.md) management is off by default, set `dnssec.enabled`. See
  [DNSSEC configuration](../configuration/dnssec.md). Existing keys stay in PowerDNS.
- [Change requests](../user-guide/change-requests.md) add a review step before changes are applied. Off by default,
  set `approval.enabled`. PowerDNS-Admin has nothing like this.

PowerDNS-Admin stores its settings in its database. Poweradmin reads them from `config/settings.php`, see
[Settings Reference](../configuration/settings-reference.md).

### 9. Switch Over

1. Ask a few users to sign in and check that they see their zones and can do what their role allowed before.
2. Stop making changes in PowerDNS-Admin. Both tools write to PowerDNS, so a record changed in one shows up in the
   other, but each keeps its own list of who owns what. Zones created in Poweradmin appear in PowerDNS-Admin only
   after it syncs its zone list.
3. Keep PowerDNS-Admin reachable for a while so you can look up its history and settings.
4. Move scripts, dynamic DNS clients and users to Poweradmin, then shut PowerDNS-Admin down.

## Concept Mapping

| PowerDNS-Admin | Poweradmin |
|---|---|
| Account | [Group](../user-guide/groups.md) |
| User | User |
| Role: Administrator | User with `user_is_ueberuser` |
| Role: Operator, User | [Permission template](../user-guide/users-roles.md) |
| Domain-user mapping | [Zone ownership](../user-guide/zones.md#zone-ownership) by user |
| API key with role and zone scope | [API key](../api/authentication.md) owned by a user |
| Domain template | [DNS template](../user-guide/dns-templates.md) |
| History | [Record change log](../user-guide/record-change-log.md) and the zone logs at `/zones/logs`, not migrated |
| LDAP, OIDC, SAML login | [LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md), [SAML](../configuration/saml.md) |
| Google, GitHub, Azure login | No direct equivalent |
| TOTP two-factor login | [MFA](../user-guide/mfa.md), users enroll again |
| `/nic/update` | `/dynamic_update.php` or `POST /api/v2/dynamic-dns`, see [Dynamic DNS](../user-guide/ddns/overview.md) |
| Settings in database | `config/settings.php`, see [Settings Reference](../configuration/settings-reference.md) |
