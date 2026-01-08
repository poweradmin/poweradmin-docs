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
| `perm_templ` | int | Permission template ID |
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
Links zones to users for permission management.

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Primary key |
| `domain_id` | int | Foreign key to domains.id |
| `owner` | int | Foreign key to users.id |
| `comment` | varchar(1024) | Zone comment |
| `zone_templ_id` | int | Zone template ID |

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

1. **Zone Ownership**: `zones.domain_id` → `domains.id`, `zones.owner` → `users.id`
2. **DNS Records**: `records.domain_id` → `domains.id`
3. **User Permissions**: `users.perm_templ` → `perm_templ.id`
4. **Permission Templates**: `perm_templ_items.templ_id` → `perm_templ.id`, `perm_templ_items.perm_id` → `perm_items.id`
5. **Zone Templates**: `zone_templ_records.zone_templ_id` → `zone_templ.id`
6. **API Keys**: `api_keys.created_by` → `users.id`
7. **MFA**: `user_mfa.user_id` → `users.id`
8. **User Preferences**: `user_preferences.user_id` → `users.id`
9. **OIDC Links**: `oidc_user_links.user_id` → `users.id`
10. **SAML Links**: `saml_user_links.user_id` → `users.id`

## Version History

| Version | Changes |
|---------|---------|
| 4.2.0 | Added `oidc_user_links`, `saml_user_links`, `username_recovery_requests`; Added `auth_method` to users; Added zone deletion permissions |
| 4.1.0 | Performance indexes added |
| 4.0.0 | Added `login_attempts`, `api_keys`, `user_mfa`, `user_preferences`, `zone_template_sync`, `password_reset_tokens`, `user_agreements` |

## Backup Considerations

When backing up Poweradmin, ensure you backup:

1. **PowerDNS Tables**: Contains your DNS data
2. **Poweradmin Tables**: Contains users, permissions, and configuration
3. **Configuration Files**: `config/settings.php` and related files

For more information about database setup and migration, see:
- [Database Configuration](./mysql-configuration.md)
- [Upgrading to v4.0.0](../upgrading/v4.0.0.md)
