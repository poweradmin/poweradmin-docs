# Migrating from PDNS Manager

[PDNS Manager](https://pdnsmanager.org/) is a PHP and Angular interface for PowerDNS. It writes the PowerDNS
database directly with SQL and supports MySQL/MariaDB only. It has had no commits since 2021. See
[Migrating from Other Tools](index.md) for the general approach.

There is no import tool. This page describes a manual migration. Try it on a copy of the database first.

## What Carries Over

PDNS Manager stores zones and records in the standard PowerDNS `domains` and `records` tables. Poweradmin reads the
same tables, so the zones are there as soon as it is connected.

PDNS Manager also keeps its own tables in the PowerDNS database:

| Table | Holds |
|---|---|
| `users` | Users: `name`, `type` (`admin` or `user`), `backend`, `password` |
| `permissions` | Which user may edit which zone (`domain_id`, `user_id`) |
| `remote` | Dynamic DNS credentials, one per record |
| `options` | PDNS Manager's schema version |

Poweradmin also has a table named `users`. The two cannot share a database, see [step 2](#2-keep-the-tables-apart).

| Stays in PowerDNS | Must be recreated in Poweradmin |
|---|---|
| Zones and records | Users (passwords can be copied, see [step 4](#4-recreate-users)) |
| | User type, as a permission template |
| | Zone permissions, as zone ownership |
| | Dynamic DNS credentials |

## Before You Start

Export the worklist from the PowerDNS database:

```sql
-- users; "native" users have a password hash, others log in through a plugin
SELECT id, name, type, backend, password IS NOT NULL AS has_password
FROM users ORDER BY name;

-- which user may edit which zone; admins may edit every zone
SELECT u.name AS user, d.name AS zone
FROM permissions p
JOIN users u ON u.id = p.user_id
JOIN domains d ON d.id = p.domain_id
ORDER BY u.name, d.name;

-- dynamic DNS credentials to move
SELECT r.name, r.type, rm.description, rm.type AS auth_type
FROM remote rm JOIN records r ON r.id = rm.record;

-- zones without an SOA record
SELECT d.name FROM domains d
WHERE d.type IN ('MASTER', 'NATIVE')
  AND NOT EXISTS (SELECT 1 FROM records r WHERE r.domain_id = d.id AND r.type = 'SOA');
```

PDNS Manager creates a zone without an SOA record and expects you to set one afterwards. The last query finds
zones where that never happened.

Back up the whole database.

## Steps

### 1. Check the PowerDNS Schema

A fresh PDNS Manager install creates the PowerDNS tables itself, from the PowerDNS 4.1 schema. If PowerDNS has been
upgraded since, check that the schema upgrades from the PowerDNS upgrade notes were applied. For example,
PowerDNS 4.3 added `cryptokeys.published`, and 4.7 added `domains.options` and `domains.catalog`. PowerDNS and
Poweradmin both expect the schema of the PowerDNS version you run.

### 2. Keep the Tables Apart

Install Poweradmin from the [Installation](../installation/index.md) section, in one of two ways.

**Separate database (recommended).** Create a new MySQL database for Poweradmin, for example `poweradmin`, and load
the Poweradmin schema there. Then point Poweradmin at both:

```php
'database' => [
    'type' => 'mysql',
    'host' => 'localhost',
    'name' => 'poweradmin',        // Poweradmin's own tables
    'pdns_db_name' => 'powerdns',  // the database PowerDNS and PDNS Manager use
    'user' => 'poweradmin',
    'password' => '...',
],
```

The database user needs access to both databases. See [Database Configuration](../configuration/database.md).

**Same database.** Rename PDNS Manager's `users` table before loading the Poweradmin schema:

```sql
RENAME TABLE users TO pdnsmanager_users;
```

PDNS Manager stops working at this point, so export the worklist first. The foreign keys from `permissions` follow
the rename. In the queries on this page, use `pdnsmanager_users` for
PDNS Manager's users and `users` for Poweradmin's, without the database prefixes.

Leave PowerDNS's configuration as it is. Sign in to Poweradmin as the administrator and open the zone list. You
should see the existing zones.

### 3. Recreate User Types as Permission Templates

PDNS Manager has two user types. An `admin` maps to a Poweradmin user with the `user_is_ueberuser` permission. A
`user` may edit the records of the zones granted to them. Create a [permission template](../user-guide/users-roles.md)
for them with `zone_content_view_own` and `zone_content_edit_own`, plus any other rights they should have. The full
list is in [User Permissions](../user-guide/permissions.md).

### 4. Recreate Users

Create each user under **Users**, or with the `/api/v2/users` endpoint, using the same username and a temporary
password. Poweradmin also requires an email address.

PDNS Manager stores `native` users' passwords as PHP bcrypt hashes (`$2y$...`), a format Poweradmin verifies. To
let users keep their passwords, copy the hashes after creating the users. This is a manual database change with no
tool support, so test it on a copy first. With the separate database from step 2:

```sql
UPDATE poweradmin.users pa
JOIN powerdns.users pm ON CONVERT(pm.name USING utf8mb4) = pa.username
SET pa.password = pm.password
WHERE pm.backend = 'native'
  AND pm.password IS NOT NULL
  AND pa.auth_method = 'sql';
```

Poweradmin rehashes a password at the next login if its own settings call for a different algorithm or cost.

Users from a `config` backend have no hash in the database. They set a new password, or sign in through
[LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md) or [SAML](../configuration/saml.md). PDNS
Manager logins of the form `prefix/username` become plain usernames.

### 5. Assign Zone Ownership

Zones that Poweradmin did not create have no owner, so users who may only see their own zones cannot see them. Give
each zone the owners from the `permissions` export:

- On the zone's ownership page (`/zones/{id}/ownership`), or with `/api/v2/zones/{id}/owners`.
- For many zones with the same users, through a [group](../user-guide/groups.md): create the group, add the users,
  and move the zones to it on the group's zones page.

Since Poweradmin 4.6.0 there is a shortcut for zones with exactly one user. Write the username into the zone's
`account` field, set `dns.adopt_zone_owner_from_account` to `true`, and run **Assign all to me** under "zones
without owners" in the [Database Consistency Check](../maintenance/consistency-check.md). The check is off by
default; set `interface.enable_consistency_checks` to `true`. Each zone goes to the
user its `account` names; the rest go to you.

```sql
-- only for zones with a single user and no account yet
UPDATE powerdns.domains d
JOIN (SELECT domain_id, MIN(user_id) AS user_id FROM powerdns.permissions
      GROUP BY domain_id HAVING COUNT(*) = 1) one ON one.domain_id = d.id
JOIN powerdns.users u ON u.id = one.user_id
SET d.account = u.name
WHERE d.account IS NULL OR d.account = '';
```

### 6. Fix Zones Without SOA

The [Database Consistency Check](../maintenance/consistency-check.md) lists zones with no SOA record under "Zones
without SOA". **Fix** creates a placeholder SOA, `ns1.<zone> hostmaster.<zone>` with a serial from today's date.
It does not use the `dns.*` settings, so edit each SOA afterwards to name your real primary nameserver and contact.
For many zones it is quicker to insert the SOA records with SQL.

### 7. Move Dynamic DNS Clients

PDNS Manager updates one record by its numeric ID, through its `remote/updatepw` endpoint with a per-record
password, or `remote/updatekey` with a signed request. Poweradmin updates a record by hostname, see
[Dynamic DNS](../user-guide/ddns/overview.md):

- `/dynamic_update.php`, a dyndns2-style endpoint for stock clients such as ddclient, with a Poweradmin username
  and password.
- `POST /api/v2/dynamic-dns`, with an API key.

Create a user or API key for each client and give it only the zones it updates. There is no equivalent of the
signed-key method.

### 8. Switch Over and Clean Up

1. Ask a few users to sign in and check that they see their zones.
2. Stop PDNS Manager. Both tools write the same tables, so a change in one shows up in the other, but zones created
   in Poweradmin have no PDNS Manager permissions.
3. Remove PDNS Manager's tables:

    ```sql
    -- separate database: run in the PowerDNS database, never in Poweradmin's
    DROP TABLE permissions, remote, users, options;

    -- same database: users is now Poweradmin's table, so drop the renamed one
    DROP TABLE permissions, remote, pdnsmanager_users, options;
    ```

    Do not skip this. On installs upgraded from older PDNS Manager versions, the foreign keys from `permissions`
    and `remote` do not cascade, so deleting a zone or record that still has a row there fails. Check with
    `SHOW CREATE TABLE permissions;` if in doubt.

## Concept Mapping

| PDNS Manager | Poweradmin |
|---|---|
| User type `admin` | User with `user_is_ueberuser` |
| User type `user` | User with a [permission template](../user-guide/users-roles.md) |
| `permissions` row | [Zone ownership](../user-guide/zones.md#zone-ownership) by user or group |
| `native` user, bcrypt hash | Local user, hash can be copied |
| `config` backend user | Local user with a new password, or LDAP, OIDC, SAML |
| Remote update by password | `/dynamic_update.php` or `POST /api/v2/dynamic-dns` |
| Remote update by signed key | No equivalent |
| SOA set after zone creation | SOA created with the zone; "Zones without SOA" fix for old zones |
