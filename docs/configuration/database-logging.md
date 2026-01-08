# Database Logging

Poweradmin can log zone and record changes to the database for auditing and tracking purposes.

## Overview

Database logging records all modifications to DNS zones and records, including:

- Zone creation, modification, and deletion
- Record creation, modification, and deletion
- User who made the change
- Timestamp of the change

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

## Log Table Structure

Changes are stored in the `log_changes` table:

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Auto-increment ID |
| `user_id` | int | User who made the change |
| `zone_id` | int | Affected zone ID |
| `record_id` | int | Affected record ID (if applicable) |
| `action` | varchar | Action type (create, update, delete) |
| `old_value` | text | Previous value (for updates) |
| `new_value` | text | New value |
| `created_at` | timestamp | When the change occurred |

## What Gets Logged

### Zone Changes

- Zone creation with initial settings
- Zone type changes (MASTER, NATIVE, SLAVE)
- Zone deletion
- Zone template assignments

### Record Changes

- New record creation
- Record content modifications
- TTL changes
- Record deletion

## Viewing Logs

Administrators can view the change log through the web interface:

1. Navigate to **Logs** in the main menu
2. Filter by zone, user, or date range
3. Export logs if needed

## Querying Logs

You can query logs directly from the database:

```sql
-- Recent changes
SELECT * FROM log_changes
ORDER BY created_at DESC
LIMIT 100;

-- Changes by user
SELECT * FROM log_changes
WHERE user_id = 1
ORDER BY created_at DESC;

-- Changes to specific zone
SELECT * FROM log_changes
WHERE zone_id = 42
ORDER BY created_at DESC;

-- Changes in date range
SELECT * FROM log_changes
WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31';
```

## Log Retention

Database logs can grow large over time. Consider implementing a retention policy:

```sql
-- Delete logs older than 90 days
DELETE FROM log_changes
WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

You can automate this with a cron job or scheduled task.

## Performance Considerations

1. **Index optimization**: Ensure indexes on `zone_id`, `user_id`, and `created_at`
2. **Log rotation**: Implement retention policies for large deployments
3. **Disk space**: Monitor database size, especially with high change volume

## Combining with Syslog

For comprehensive auditing, combine database logging with syslog:

```php
'logging' => [
    'database_enabled' => true,
    'syslog' => [
        'use' => true,
        'ident' => 'poweradmin',
        'facility' => LOG_USER,
    ],
],
```

This provides both persistent database records and real-time syslog events.

## Related Documentation

- [Logging Setup](logging.md)
- [Security Policies](security-policies.md)
