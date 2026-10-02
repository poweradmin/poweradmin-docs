# Migrating from Other Tools

These pages cover moving to Poweradmin from another PowerDNS web interface. None of these tools has an
import tool. Each guide describes a manual migration. Try it on a test copy first.

## How Hard Is It?

What you have to move depends on where the old tool keeps the DNS data.

| Where the records live | Tools | What you migrate |
|---|---|---|
| In PowerDNS, written over the PowerDNS API | [PowerDNS-Admin](powerdns-admin.md), [Opera DNS UI](opera-dns-ui.md), [nsedit](nsedit.md) | Users, permissions and zone ownership. The records are already in place |
| In the PowerDNS database, written with SQL | [PDNS Manager](pdns-manager.md) | Users, permissions and zone ownership, plus the tool's own tables in the PowerDNS database |
| In the tool's own database, exported to PowerDNS | NicTool | The zones themselves, see [below](#tools-with-their-own-zone-store) |

When the records are already in PowerDNS, connect Poweradmin to the same PowerDNS server and the zones show up.
What is left is recreating users and deciding who may edit which zone. The old tool and Poweradmin can run side by
side while you do this, since both write to the same PowerDNS.

## Supported Tools

| Tool | Last activity | Talks to PowerDNS through | Guide |
|---|---|---|---|
| PowerDNS-Admin | Active, CalVer releases since 2026.08 | API | [Migrating from PowerDNS-Admin](powerdns-admin.md) |
| Opera DNS UI (dns-ui) | Occasional commits, last release v0.2.8 (2023) | API | [Migrating from Opera DNS UI](opera-dns-ui.md) |
| nsedit | Occasional commits, last in 2025 | API | [Migrating from nsedit](nsedit.md) |
| PDNS Manager (pdnsmanager.org) | No commits since 2021 | SQL, MySQL/MariaDB only | [Migrating from PDNS Manager](pdns-manager.md) |

Most other PowerDNS web interfaces have had no commits for years. If yours stores its data in PowerDNS, the
[PowerDNS-Admin guide](powerdns-admin.md) is a good template: the Poweradmin side of the steps is the same.

## Common Steps

Every migration in this section follows the same outline:

1. Export a list of users, their rights and the zones each can reach from the old tool.
2. Install Poweradmin and connect it to the existing PowerDNS. See [Installation](../installation/index.md) and
   [PowerDNS API](../configuration/powerdns-api.md).
3. Recreate rights as [permission templates](../user-guide/users-roles.md), then users and
   [groups](../user-guide/groups.md).
4. Assign zone ownership. Zones that Poweradmin did not create have no owner, so users who may only see their own
   zones cannot see them. The [Database Consistency Check](../maintenance/consistency-check.md) lists them under "zones without
   owners".
5. Move scripts and dynamic DNS clients, then switch users over.

## Tools with Their Own Zone Store

Some tools, such as [NicTool](https://www.nictool.com/), keep zones in their own database. NicTool's PowerDNS
export writes BIND zone files for the PowerDNS bind backend, so the zones never reach a database Poweradmin can
manage. For these tools, the zones are the migration. Set up PowerDNS with a database backend, then either:

- load the exported zone files with [Zone Import](../configuration/zone-import-export.md), or
- transfer each zone from the running server with [Secondary Zone Import](../user-guide/secondary-zone-import.md)
  and convert it to a primary zone. This needs Poweradmin 4.5.0 or newer in API backend mode.

Stop the export to the old server once a zone has moved. Users and permissions are recreated by hand, as in the
other guides.
