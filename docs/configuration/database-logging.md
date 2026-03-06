# Database Logging

Poweradmin can log operations to the database for auditing and tracking purposes.

## Overview

Database logging records operations across three log tables:

- **User events** (`log_users`): login/logout, user creation/editing/deletion
- **Zone events** (`log_zones`): zone and record creation, modification, and deletion
- **Group events** (`log_groups`): group creation/editing/deletion, membership and zone assignment changes

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `logging.database_enabled` | false | Enable database logging |
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

- Login and logout
- User creation, editing, and deletion

### Zone Events

- Zone creation with initial settings
- Zone type changes (MASTER, NATIVE, SLAVE)
- Zone deletion
- Record creation, modification, and deletion

### Group Events

- Group creation, editing, and deletion
- User membership additions and removals
- Zone assignment additions and removals

## Viewing Logs

Administrators can view the change log through the web interface:

1. Navigate to **Logs** in the main menu
2. Filter by zone, user, or date range
3. Export logs if needed

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
DELETE FROM log_zones WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM log_groups WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

You can automate this with a cron job or scheduled task.

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
