# Database Schema

This document describes the database tables used by Poweradmin and their relationships. Poweradmin extends the PowerDNS database schema with additional tables for user management, permissions, logging, and enhanced functionality.

## Database Requirements

Poweradmin requires **both** PowerDNS and Poweradmin database schemas to be installed:

1. **PowerDNS Schema**: Core DNS functionality (zones, records, cryptokeys)
2. **Poweradmin Schema**: User management, permissions, logging, and enhanced features

## PowerDNS Tables

These tables are created by the PowerDNS schema and store the core DNS data:

### `domains`
Stores DNS zones/domains.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(255) | Domain name |
| `master` | varchar(128) | Master server for slave zones |
| `last_check` | int | Last check timestamp |
| `type` | varchar(6) | Zone type (MASTER, SLAVE, NATIVE) |
| `notified_serial` | int | Last notified serial |
| `account` | varchar(40) | Account identifier |
| `options` | text | Zone options |
| `catalog` | varchar(255) | Catalog zone |

### `records`
Stores DNS records within zones.

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `name` | varchar(255) | Record name |
| `type` | varchar(10) | Record type (A, AAAA, CNAME, etc.) |
| `content` | varchar(65000) | Record content/value |
| `ttl` | int | Time to live |
| `prio` | int | Priority (for MX, SRV records) |
| `disabled` | tinyint | Record disabled flag |
| `ordername` | varchar(255) | DNSSEC ordering |
| `auth` | tinyint | Authoritative flag |

### `supermasters`
Stores supermaster configuration for automatic slave zone creation.

| Column | Type | Description |
|--------|------|-------------|
| `ip` | varchar(64) | Supermaster IP address |
| `nameserver` | varchar(255) | Nameserver hostname |
| `account` | varchar(40) | Account identifier |

### `comments`
Stores comments for DNS records.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `name` | varchar(255) | Record name |
| `type` | varchar(10) | Record type |
| `modified_at` | int | Modification timestamp |
| `account` | varchar(40) | Account identifier |
| `comment` | text | Comment text |

### `domainmetadata`
Stores domain metadata (DNSSEC settings, etc.).

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `kind` | varchar(32) | Metadata type |
| `content` | text | Metadata content |

### `cryptokeys`
Stores DNSSEC cryptographic keys.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `flags` | int | Key flags |
| `active` | tinyint | Key active status |
| `published` | tinyint | Key published status |
| `content` | text | Key content |

### `tsigkeys`
Stores TSIG keys for secure zone transfers.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(255) | Key name |
| `algorithm` | varchar(50) | Algorithm |
| `secret` | varchar(255) | Secret key |

## Poweradmin Core Tables

### `users`
Stores user accounts and authentication information.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `username` | varchar(64) | Username |
| `password` | varchar(128) | Encrypted password |
| `fullname` | varchar(255) | Full name |
| `email` | varchar(255) | Email address |
| `description` | varchar(1024) | User description |
| `perm_templ` | int | Permission template ID (FK to `perm_templ.id`) |
| `perm_templ_source` | varchar(20) | How `perm_templ` was assigned: `admin` (default; set by an administrator) or `sso` (assigned by OIDC/SAML provisioning) |
| `active` | int | Active status |
| `use_ldap` | int | Use LDAP authentication |
| `auth_method` | varchar(20) | Authentication method (sql, ldap, oidc, saml) |

### `perm_items`
Defines available permissions in the system.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(64) | Permission name |
| `descr` | varchar(1024) | Permission description |

### `perm_templ`
Defines permission templates (roles).

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(128) | Template name |
| `descr` | varchar(1024) | Template description |

### `perm_templ_items`
Links permission templates to specific permissions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `templ_id` | int | Foreign key to perm_templ.id |
| `perm_id` | int | Foreign key to perm_items.id |

### `zones`
Links zones to users for permission management. In API backend mode, also caches zone metadata from the PowerDNS API.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id (nullable in API mode) |
| `owner` | int | Foreign key to users.id |
| `comment` | varchar(1024) | Zone comment |
| `zone_templ_id` | int | Zone template ID |
| `zone_name` | varchar(255) | Zone name (cached from PowerDNS API, v4.3.0+) |
| `zone_type` | varchar(8) | Zone type: Master, Slave, Native (cached, v4.3.0+) |
| `zone_master` | varchar(255) | Master server for slave zones (cached, v4.3.0+) |

### `zone_templ`
Defines zone templates for bulk zone creation.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(128) | Template name |
| `descr` | varchar(1024) | Template description |
| `owner` | int | Foreign key to users.id |
| `created_by` | int | Foreign key to users.id (creator) |

### `zone_templ_records`
Stores record templates within zone templates.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `zone_templ_id` | int | Foreign key to zone_templ.id |
| `name` | varchar(255) | Record name template |
| `type` | varchar(6) | Record type |
| `content` | varchar(2048) | Record content template |
| `ttl` | int | Time to live |
| `prio` | int | Priority |

### `records_zone_templ`
Links records to zone templates.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `record_id` | int | Foreign key to records.id |
| `zone_templ_id` | int | Foreign key to zone_templ.id |

## Security Tables

### `login_attempts`
Tracks login attempts for security purposes.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id (nullable) |
| `ip_address` | varchar(45) | IP address |
| `timestamp` | int | Attempt timestamp (Unix) |
| `successful` | tinyint | Success flag |

### `api_keys`
Stores API keys for authentication.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(255) | Key name |
| `secret_key` | varchar(255) | Hashed API key |
| `created_by` | int | Foreign key to users.id |
| `created_at` | timestamp | Creation timestamp |
| `last_used_at` | timestamp | Last usage timestamp |
| `disabled` | tinyint | Disabled flag |
| `expires_at` | timestamp | Expiration timestamp |

### `user_mfa`
Stores multi-factor authentication settings.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `enabled` | tinyint | MFA enabled flag |
| `secret` | varchar(255) | MFA secret |
| `recovery_codes` | text | Recovery codes |
| `type` | varchar(20) | MFA type (app, email) |
| `last_used_at` | datetime | Last usage timestamp |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Update timestamp |
| `verification_data` | text | Verification data |

### `password_reset_tokens`
Stores password reset tokens.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `email` | varchar(255) | User email |
| `token` | varchar(64) | Reset token |
| `expires_at` | timestamp | Expiration timestamp |
| `created_at` | timestamp | Creation timestamp |
| `used` | tinyint | Token used flag |
| `ip_address` | varchar(45) | Request IP address |

### `username_recovery_requests`
Tracks username recovery requests for rate limiting.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `email` | varchar(255) | Email address |
| `ip_address` | varchar(45) | Request IP address |
| `created_at` | timestamp | Request timestamp |

## Authentication Provider Tables

### `oidc_user_links`
Links users to OpenID Connect providers.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `provider_id` | varchar(50) | OIDC provider identifier |
| `oidc_subject` | varchar(255) | OIDC subject claim |
| `username` | varchar(255) | Username from provider |
| `email` | varchar(255) | Email from provider |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

### `saml_user_links`
Links users to SAML providers.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `provider_id` | varchar(50) | SAML provider identifier |
| `saml_subject` | varchar(255) | SAML NameID |
| `username` | varchar(255) | Username from provider |
| `email` | varchar(255) | Email from provider |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

## User Data Tables

### `user_preferences`
Stores user preferences and settings.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `preference_key` | varchar(100) | Preference key |
| `preference_value` | text | Preference value |

### `user_agreements`
Tracks user agreement acceptance.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `agreement_version` | varchar(50) | Agreement version |
| `accepted_at` | timestamp | Acceptance timestamp |
| `ip_address` | varchar(45) | IP address |
| `user_agent` | text | Browser user agent |

## Zone Management Tables

### `zone_template_sync`
Tracks zone template synchronization.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `zone_id` | int | Foreign key to zones.id |
| `zone_templ_id` | int | Foreign key to zone_templ.id |
| `last_synced` | timestamp | Last sync timestamp |
| `template_last_modified` | timestamp | Template modification time |
| `needs_sync` | tinyint | Sync needed flag |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

## Logging Tables

### `log_users`
Logs user-related activities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `event` | varchar(2048) | Event description |
| `created_at` | timestamp | Event timestamp |
| `priority` | int | Log priority level |

### `log_zones`
Logs zone-related activities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `event` | varchar(2048) | Event description |
| `created_at` | timestamp | Event timestamp |
| `priority` | int | Log priority level |
| `zone_id` | int | Related zone ID |

### `log_api`
Logs API requests handled by the public API.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `event` | varchar(2048) | Event description |
| `created_at` | timestamp | Event timestamp |
| `priority` | int | Log priority level |

### `log_groups`
Logs user-group lifecycle events (create / rename / membership changes).

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `event` | varchar(2048) | Event description |
| `created_at` | timestamp | Event timestamp |
| `priority` | int | Log priority level |
| `group_id` | int | Related `user_groups.id` (nullable) |

### `log_record_changes`
Structured before/after snapshots for record mutations. Powers the diff-style change-log UI and email digests. Complements `log_zones` (which is a free-text activity feed) with machine-readable detail.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `zone_id` | int | Related zone (nullable) |
| `record_id` | text | Record identifier (numeric for SQL mode, encoded for API mode) |
| `action` | varchar(32) | `create`, `update`, `delete` |
| `user_id` | int | Acting user (nullable) |
| `username` | varchar(64) | Acting username (denormalized so log survives user deletion) |
| `before_state` | text | JSON snapshot prior to mutation (null for creates) |
| `after_state` | text | JSON snapshot after mutation (null for deletes) |
| `client_ip` | varchar(64) | Source IP |
| `created_at` | timestamp | Event timestamp |

## Group Tables

### `user_groups`
Named groups that bundle a permission template and a set of members. Underpins group-based ownership of zones.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int unsigned | Primary key |
| `name` | varchar(255) | Group name (unique) |
| `description` | text | Free-form description |
| `perm_templ` | int | FK to `perm_templ.id` - the permission template applied to members |
| `created_by` | int | FK to `users.id` (nullable; `SET NULL` on user deletion) |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Last update timestamp |

### `user_group_members`
Membership join table between users and groups.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int unsigned | Primary key |
| `group_id` | int unsigned | FK to `user_groups.id` (cascade delete) |
| `user_id` | int | FK to `users.id` (cascade delete) |
| `created_at` | timestamp | Membership added at |

### `zones_groups`
Maps zones to groups for group-based ownership. A zone can be owned directly via `zones.owner` and/or via one or more rows in this table.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int unsigned | Primary key |
| `domain_id` | int | Zone identifier (matches PowerDNS `domains.id`) |
| `group_id` | int unsigned | FK to `user_groups.id` (cascade delete) |
| `created_at` | timestamp | Assignment timestamp |

## Defaults and Application State

### `record_type_defaults`
Per-record-type default TTL values used when adding new records via the UI.

| Column | Type | Description |
|--------|------|-------------|
| `record_type` | varchar(20) | DNS record type (e.g. `A`, `AAAA`, `MX`); primary key |
| `ttl` | int | Default TTL in seconds |
| `created_at` | timestamp | Created at |
| `updated_at` | timestamp | Updated at |

### `app_settings`
Key/value store for settings that can be changed at runtime from the admin UI (without editing `config/settings.php`).

| Column | Type | Description |
|--------|------|-------------|
| `setting_key` | varchar(128) | Setting identifier (primary key) |
| `setting_value` | text | Stored value (always serialized to string) |
| `value_type` | varchar(16) | One of `string`, `int`, `bool`, `array` - tells callers how to deserialize `setting_value` |
| `created_at` | timestamp | Created at |
| `updated_at` | timestamp | Updated at |

### `records_zone_templ_api`
API-mode equivalent of `records_zone_templ`. Tracks which template a record was created from when Poweradmin is talking to PowerDNS via the API (record identifiers are opaque strings, not numeric IDs).

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Zone identifier |
| `record_id` | varchar(255) | API-mode record identifier |
| `zone_templ_id` | int | FK to `zone_templ.id` |

## Record Comment Tables

### `record_comment_links`
Bridge table that maps a record identifier to a PowerDNS `comments.id`. Record-level comment **text** lives in PowerDNS's own `comments` table; Poweradmin only stores the link so that comments survive record edits in the UI / API.

| Column        | Type                                                     | Description                                                          |
|---------------|----------------------------------------------------------|----------------------------------------------------------------------|
| `record_id`   | VARCHAR(3072) on MySQL / VARCHAR(4096) on PostgreSQL & SQLite | Record identifier (numeric `records.id` in SQL mode, encoded string in API mode). Primary key. |
| `comment_id`  | int                                                      | Reference to PowerDNS `comments.id`. Unique.                         |

## Default Permission Templates

Poweradmin includes default permission templates:

| Template | Description |
|----------|-------------|
| Administrator | Full access (user_is_ueberuser) |
| Zone Manager | Full management of own zones |
| DNS Editor | Edit records (no SOA/NS) |
| Read Only | View-only access |
| No Access | No permissions |

## Table Relationships

### Key Relationships

1. **Direct zone ownership**: `zones.domain_id` → `domains.id`; `zones.owner` → `users.id`
2. **Group zone ownership**: `zones_groups.domain_id` → `domains.id`; `zones_groups.group_id` → `user_groups.id`
3. **Group membership**: `user_group_members.group_id` → `user_groups.id`; `user_group_members.user_id` → `users.id`
4. **DNS records**: `records.domain_id` → `domains.id`
5. **User permissions**: `users.perm_templ` → `perm_templ.id`; `user_groups.perm_templ` → `perm_templ.id`
6. **Permission templates**: `perm_templ_items.templ_id` → `perm_templ.id`; `perm_templ_items.perm_id` → `perm_items.id`
7. **Zone templates**: `zone_templ_records.zone_templ_id` → `zone_templ.id`; `records_zone_templ.zone_templ_id` → `zone_templ.id` (SQL mode); `records_zone_templ_api.zone_templ_id` → `zone_templ.id` (API mode)
8. **API keys**: `api_keys.created_by` → `users.id`
9. **MFA**: `user_mfa.user_id` → `users.id`
10. **User preferences**: `user_preferences.user_id` → `users.id`
11. **OIDC / SAML links**: `oidc_user_links.user_id` → `users.id`; `saml_user_links.user_id` → `users.id`
12. **Comment bridge**: `record_comment_links.comment_id` → PowerDNS `comments.id`

## Version History

| Version            | Changes |
|--------------------|---------|
| 4.5.0 *(develop)*  | Added `log_record_changes` (structured before/after record snapshots), `records_zone_templ_api` (template tracking in API mode), `record_type_defaults` (per-type default TTLs), and `app_settings` (admin-managed runtime key/value store). `zones.zone_templ_id` now defaults to `0`. |
| 4.4.0 *(master)*   | Added `is_default` to `zone_templ` for marking a system-wide default template. |
| 4.3.0              | Added `log_api` and migrated API key log entries into it; added `zone_name`, `zone_type`, `zone_master` to `zones`; widened `record_comment_links.record_id` to VARCHAR. |
| 4.2.0              | Introduced group-based ownership (`user_groups`, `user_group_members`, `zones_groups`, `log_groups`); added `template_type` to `perm_templ`; made `zones.owner` nullable. Introduced `record_comment_links`. Renamed default permission templates (DNS Editor → Editor, Read Only → Viewer, No Access → Guest). |
| 4.1.0              | Added `oidc_user_links`, `saml_user_links`, `username_recovery_requests`; added `auth_method` to `users` (with backfill from `use_ldap`); performance indexes added. |
| 4.0.0              | Major rework: added `login_attempts`, `api_keys`, `user_mfa`, `user_preferences`, `zone_template_sync`, `password_reset_tokens`, `user_agreements`. |

## Backup Considerations

When backing up Poweradmin, ensure you backup:

1. **PowerDNS Tables**: Contains your DNS data
2. **Poweradmin Tables**: Contains users, permissions, and configuration
3. **Configuration Files**: `config/settings.php` and related files

For more information about database setup and migration, see:
- [Database Configuration](./mysql-configuration.md)
- [Upgrading to v4.0.0](../upgrading/v4.0.0.md)
