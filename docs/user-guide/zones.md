# Zone Management

Zones are the core objects in Poweradmin. Each zone corresponds to a DNS domain (or reverse network) managed by PowerDNS. This guide covers creating, editing, and managing zones.

![Zone List](/screenshots/zone-list.png)

## Zone Types

PowerDNS supports three zone types. Choose the type based on your DNS architecture:

- **Master** - the authoritative source for the zone. Changes are made here and replicated to slave servers. Use this when Poweradmin is your primary DNS management interface.
- **Slave** - a read-only copy that receives updates from a master server. Use this when another DNS server holds the primary data and you want PowerDNS to serve as a secondary.
- **Native** - zones that rely on native database replication instead of DNS-based zone transfers (AXFR/IXFR). Use this when all your PowerDNS servers share the same database backend.

> **Tip:** If you are running a single PowerDNS server, **Native** is the simplest option since no zone transfers are needed.

## Creating Zones

### Adding a Master Zone

![Add Master Zone](/screenshots/zone-add-master.png)

1. Navigate to **Zones** and click **Add master zone**
2. Enter the **Zone name** (e.g., `example.com`)
3. Select an **Owner** - the user who will manage this zone
4. Optionally select a **Zone template** to pre-populate records (SOA, NS, etc.)
5. Enable **DNSSEC** if you want the zone signed by PowerDNS
6. Click **Add zone**

The zone is created with the records defined in the selected template. If no template is chosen, only a SOA record is created.

### Adding a Slave Zone

1. Navigate to **Zones** and click **Add slave zone**
2. Enter the **Zone name**
3. Enter the **Master server IP** address that this slave will pull data from
4. Select an **Owner**
5. Click **Add zone**

Slave zones are populated automatically by PowerDNS through zone transfers from the configured master server.

### Zone Templates

Zone templates let you define a standard set of records that are added when creating a new zone. This is useful for ensuring every zone starts with consistent SOA values, nameserver records, and common entries like MX or SPF records. See [DNS Templates](dns-templates.md) for details on creating and managing templates.

## Zone Editor

![Zone Editor](/screenshots/zone-editor.png)

The zone editor is where you view and modify a zone's DNS records. It shows all records in a table with columns for name, type, content, TTL, and priority.

### Editing Records

- Click the **edit icon** next to a record to modify it inline
- Change the name, type, content, TTL, or priority fields directly in the table
- Click **Save** to apply changes or **Cancel** to discard

### Adding Records

Use the input row at the top of the record table to add new records:

1. Enter the record **Name** (just the hostname part, e.g., `www`)
2. Select the record **Type** (A, AAAA, CNAME, MX, TXT, etc.)
3. Enter the **Content** (e.g., an IP address for A records)
4. Set the **TTL** and **Priority** if applicable
5. Click **Add Record**

### Configurable Columns

Starting in v4.1.0, the zone editor supports configurable columns. You can show or hide columns such as Priority, TTL, or DNSSEC-related fields to reduce clutter depending on your workflow.

### Sorting

Starting in v4.1.0, you can sort records by clicking column headers. This helps when working with large zones to quickly find specific records.

## Bulk Operations

Starting in v4.0.0, you can add multiple records to a zone at once:

1. Open a zone in the zone editor
2. Click **Add multiple records**
3. Fill in several record rows in the bulk form
4. Click **Add Records** to create them all at once

This is particularly useful when setting up a new zone or adding a batch of similar records.

## CSV Export

Starting in v4.0.0, you can export a zone's records as a CSV file:

1. Open the zone in the zone editor
2. Click the **CSV export** button
3. The browser downloads a CSV file containing all records in the zone

This is useful for documentation, auditing, or migrating zone data to another system.

## Zone Ownership

Every zone has at least one owner. Ownership determines who can edit and manage the zone.

- **User ownership** - assign individual users as zone owners when creating or editing a zone
- **Group ownership** - assign zones to [Groups](groups.md) so all group members get access based on the group's access template

A zone can have both individual user owners and group owners simultaneously. Permissions from all sources are combined - if any ownership path grants a user access, they have it.

> **Note:** When creating a zone, you must select at least one owner. Administrators can reassign ownership later.

### Restricting Ownership Assignment

Starting in v4.4.0, the `dns.zone_ownership_mode` setting controls which ownership pickers are available on the zone creation form, the bulk registration form, the zone import form, and the zone ownership page:

- `both` (default) - users and groups can both be assigned as owners
- `users_only` - only individual users can be assigned; the group picker is hidden
- `groups_only` - only groups can be assigned; the user picker is hidden, and group membership is the sole way to grant zone access

Use `groups_only` to enforce group-based access management across the installation. The setting also applies to the API. API v2 supports group-only zones (pass `owner_user_id: null` together with `group_ids`); API v1 cannot create group-only zones and returns an error when `zone_ownership_mode` is set to `groups_only`.

## Disabled Records

Starting in v4.1.0, you can disable individual records without deleting them:

- In the zone editor, toggle the **disabled** checkbox on a record
- Disabled records remain in the database but are not served by PowerDNS
- Re-enable a record at any time by toggling it back on

This is useful for temporarily taking a record out of service during maintenance or troubleshooting, without losing the record configuration.

## Zone Deletion

To delete a zone, click the **delete icon** next to the zone in the zone list, or use the delete option from the zone editor.

Starting in v4.1.0, zone deletion uses two separate permissions:

- `zone_delete_own` - allows deleting zones you own
- `zone_delete_others` - allows deleting any zone, regardless of ownership

> **Warning:** Deleting a zone removes all its records permanently. This action cannot be undone. Make sure you have a backup or CSV export if you might need the data later.

See [Permissions](permissions.md) for a full list of available permissions and how to assign them through access templates.
