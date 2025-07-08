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

## Poweradmin Tables

These tables are added by the Poweradmin schema and provide user management, permissions, logging, and enhanced functionality:

### `users`
Stores user accounts and authentication information.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `username` | varchar(16) | Username |
| `password` | varchar(255) | Encrypted password |
| `fullname` | varchar(255) | Full name |
| `email` | varchar(255) | Email address |
| `description` | text | User description |
| `perm_templ` | tinyint | Permission template ID |
| `active` | tinyint | Active status |
| `use_ldap` | tinyint | Use LDAP authentication |

### `perm_items`
Defines available permissions in the system.

| Column | Type | Description |
|--------|------|-------------|
| `id` | tinyint | Primary key |
| `name` | varchar(64) | Permission name |
| `descr` | varchar(1024) | Permission description |

### `perm_templ`
Defines permission templates (roles).

| Column | Type | Description |
|--------|------|-------------|
| `id` | tinyint | Primary key |
| `name` | varchar(128) | Template name |
| `descr` | varchar(1024) | Template description |

### `perm_templ_items`
Links permission templates to specific permissions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `templ_id` | tinyint | Foreign key to perm_templ.id |
| `perm_id` | tinyint | Foreign key to perm_items.id |

### `zones`
Links zones to users for permission management.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `owner` | int | Foreign key to users.id |
| `comment` | text | Zone comment |
| `zone_templ_id` | int | Zone template ID |

### `zone_templ`
Defines zone templates for bulk zone creation.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `name` | varchar(128) | Template name |
| `descr` | varchar(1024) | Template description |
| `owner` | int | Foreign key to users.id |

### `zone_templ_records`
Stores record templates within zone templates.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `zone_templ_id` | int | Foreign key to zone_templ.id |
| `name` | varchar(255) | Record name template |
| `type` | varchar(6) | Record type |
| `content` | varchar(255) | Record content template |
| `ttl` | int | Time to live |
| `prio` | int | Priority |

### `records_zone_templ`
Links records to zone templates.

| Column | Type | Description |
|--------|------|-------------|
| `domain_id` | int | Foreign key to domains.id |
| `record_id` | int | Foreign key to records.id |
| `zone_templ_id` | int | Foreign key to zone_templ.id |

## Version 4.0.0 New Tables

The following tables were added in Poweradmin v4.0.0:

### `login_attempts`
Tracks login attempts for security purposes.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `username` | varchar(255) | Username attempted |
| `ip_address` | varchar(45) | IP address |
| `attempted_at` | timestamp | Attempt timestamp |
| `successful` | tinyint | Success flag |

### `migrations`
Tracks database migrations.

| Column | Type | Description |
|--------|------|-------------|
| `version` | varchar(180) | Migration version |
| `migration_name` | varchar(100) | Migration name |
| `start_time` | timestamp | Start time |
| `end_time` | timestamp | End time |
| `breakpoint` | tinyint | Breakpoint flag |

### `api_keys`
Stores API keys for authentication.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `name` | varchar(255) | Key name |
| `key_hash` | varchar(255) | Hashed API key |
| `last_used_at` | timestamp | Last usage timestamp |
| `expires_at` | timestamp | Expiration timestamp |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

### `user_mfa`
Stores multi-factor authentication settings.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `secret` | varchar(255) | MFA secret |
| `recovery_codes` | text | Recovery codes |
| `enabled` | tinyint | MFA enabled flag |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

### `user_preferences`
Stores user preferences and settings.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `preference_key` | varchar(255) | Preference key |
| `preference_value` | text | Preference value |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

### `zone_template_sync`
Tracks zone template synchronization.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `zone_templ_id` | int | Foreign key to zone_templ.id |
| `domain_id` | int | Foreign key to domains.id |
| `last_sync` | timestamp | Last sync timestamp |
| `sync_status` | varchar(50) | Sync status |
| `created_at` | timestamp | Creation timestamp |
| `updated_at` | timestamp | Update timestamp |

### `password_reset_tokens`
Stores password reset tokens.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `token` | varchar(255) | Reset token |
| `expires_at` | timestamp | Expiration timestamp |
| `used` | tinyint | Token used flag |
| `created_at` | timestamp | Creation timestamp |

### `user_agreements`
Tracks user agreement acceptance.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Foreign key to users.id |
| `agreement_version` | varchar(50) | Agreement version |
| `accepted_at` | timestamp | Acceptance timestamp |
| `ip_address` | varchar(45) | IP address |

## Logging Tables

### `log_users`
Logs user-related activities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `timestamp` | timestamp | Activity timestamp |
| `user_id` | int | Foreign key to users.id |
| `action` | varchar(255) | Action performed |
| `data` | text | Action data |

### `log_zones`
Logs zone-related activities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `timestamp` | timestamp | Activity timestamp |
| `user_id` | int | Foreign key to users.id |
| `domain_id` | int | Foreign key to domains.id |
| `action` | varchar(255) | Action performed |
| `data` | text | Action data |

## Table Relationships

### Key Relationships

1. **Zone Ownership**: `zones.domain_id` → `domains.id`, `zones.owner` → `users.id`
2. **DNS Records**: `records.domain_id` → `domains.id`
3. **User Permissions**: `users.perm_templ` → `perm_templ.id`
4. **Permission Templates**: `perm_templ_items.templ_id` → `perm_templ.id`, `perm_templ_items.perm_id` → `perm_items.id`
5. **Zone Templates**: `zone_templ_records.zone_templ_id` → `zone_templ.id`
6. **API Keys**: `api_keys.user_id` → `users.id`
7. **MFA**: `user_mfa.user_id` → `users.id`
8. **User Preferences**: `user_preferences.user_id` → `users.id`

### Database Constraints

- **Foreign Key Constraints**: Ensure referential integrity between related tables
- **Unique Constraints**: Prevent duplicate usernames, domain names, etc.
- **Index Constraints**: Optimize query performance on frequently accessed columns

## Backup Considerations

When backing up Poweradmin, ensure you backup:

1. **PowerDNS Tables**: Contains your DNS data
2. **Poweradmin Tables**: Contains users, permissions, and configuration
3. **Configuration Files**: `config/settings.php` and related files

## Migration Notes

- Always backup your database before running migrations
- Use the provided SQL migration files for version upgrades
- Test migrations in a staging environment first
- Verify all tables exist after migration using the verification queries in the upgrade documentation

For more information about database setup and migration, see:
- [Database Configuration](./mysql-configuration.md)
- [Upgrading to v4.0.0](../upgrading/v4.0.0.md)