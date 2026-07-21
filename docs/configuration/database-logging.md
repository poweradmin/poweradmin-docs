# Database Logging

Poweradmin can log operations to the database for auditing and tracking purposes.

## Overview

Database logging records operations across four log tables:

- **User events** (`log_users`): login/logout, user creation/editing/deletion, MFA, password resets
- **API events** (`log_api`): API key management, plus optional per-request public API audit entries and permission violations (401/403)
- **Zone events** (`log_zones`): zone and record creation, modification, and deletion
- **Group events** (`log_groups`): group creation/editing/deletion, membership and zone assignment changes

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `logging.database_enabled` | false | Enable database logging |
| `logging.api_request_logging` | false | Log every public API request to `log_api` (requires `database_enabled`); permission violations are logged regardless (added in v4.5.0) |
| `logging.api_log_retention_days` | 0 | Days to keep `log_api` rows; 0 = keep forever (added in v4.5.0) |
| `logging.dblog.use` | false | Legacy setting (v3.x) |

## Modern Configuration

```php
return [
    'logging' => [
        'database_enabled' => true,
    ],
];
```

## Legacy Configuration

```php
$dblog_use = true;
```

## Docker Configuration

```yaml
environment:
  PA_LOGGING_DATABASE_ENABLED: "true"
```

## Log Tables

### log_users

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Auto-increment ID |
| `event` | text | Description of the event |
| `priority` | int | Syslog priority level |
| `created_at` | timestamp | When the event occurred |

### log_api

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Auto-increment ID |
| `event` | text | Description of the event |
| `priority` | int | Syslog priority level |
| `created_at` | timestamp | When the event occurred |

### log_zones

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Auto-increment ID |
| `zone_id` | int | Affected zone ID |
| `event` | text | Description of the event |
| `priority` | int | Syslog priority level |
| `created_at` | timestamp | When the event occurred |

### log_groups

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Auto-increment ID |
| `group_id` | int | Affected group ID |
| `event` | text | Description of the event |
| `priority` | int | Syslog priority level |
| `created_at` | timestamp | When the event occurred |

## What Gets Logged

### User Events

- Login and logout (includes `auth_method` - sql, ldap, oidc, saml)
- User creation, editing, and deletion
- MFA enable/disable/verify
- Password changes and resets
- Username recovery

### API Events

- API key creation, editing, and deletion
- API key regeneration and toggling (enable/disable)
- Permission violations (401/403 responses) on the public API - logged whenever `database_enabled` is on
- Per-request public API calls (method, path, status, key id, user, client IP) - only when `api_request_logging` is enabled, since this is high volume

### Zone Events

- Zone creation with initial settings
- Zone type changes (MASTER, NATIVE, SLAVE)
- Zone deletion
- Record creation, modification, and deletion
- DNSSEC sign and unsign events (sign events added in v4.4.0; before that only unsign was recorded)

### Group Events

- Group creation, editing, and deletion
- User membership additions and removals
- Zone assignment additions and removals

## Viewing Logs

Administrators can view logs through the web interface:

- **Users** > **User logs** - user and authentication events
- **Tools** > **API Logs** - API key management, per-request API activity, and permission violations
- **Zones** > **Zone logs** - zone and record events
- **Groups** > **Group logs** - group membership and zone assignment events

Each log page supports filtering by user, event type, and date range, with CSV/JSON export.

From v4.4.0, zone owners can read the audit log for the zones they own (directly or via group ownership) without being administrators. They see only entries for their own zones - the filter is applied server-side. Administrators continue to see everything.

## Querying Logs

You can query logs directly from the database:

```sql
-- Recent user events
SELECT * FROM log_users
ORDER BY created_at DESC
LIMIT 100;

-- Recent zone events
SELECT * FROM log_zones
ORDER BY created_at DESC
LIMIT 100;

-- Events for a specific zone
SELECT * FROM log_zones
WHERE zone_id = 42
ORDER BY created_at DESC;

-- Recent group events
SELECT * FROM log_groups
ORDER BY created_at DESC
LIMIT 100;

-- Events in date range
SELECT * FROM log_users
WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31';
```

## Log Retention

Database logs can grow large over time. Consider implementing a retention policy:

```sql
-- Delete logs older than 90 days
DELETE FROM log_users WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM log_api WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM log_zones WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM log_groups WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

You can automate this with a cron job or scheduled task.

The `log_api` table has built-in retention: set `logging.api_log_retention_days` to a positive number of days and Poweradmin prunes older API log rows automatically (opportunistically, during API request logging). Leave it at `0` to keep API logs forever and manage them manually as above. This applies only to `log_api`; the other log tables have no built-in pruning.

## Performance Considerations

1. **Index optimization**: Ensure indexes on `zone_id`, `group_id`, and `created_at` columns
2. **Log rotation**: Implement retention policies for large deployments
3. **Disk space**: Monitor database size, especially with high change volume

## Combining with Syslog

For comprehensive auditing, combine database logging with syslog:

```php
'logging' => [
    'database_enabled' => true,
    'syslog_enabled' => true,
    'syslog_identity' => 'poweradmin',
    'syslog_facility' => LOG_USER,
],
```

This provides both persistent database records and real-time syslog events.

## Related Documentation

- [Logging Setup](logging.md)
- [Security Policies](security-policies.md)
