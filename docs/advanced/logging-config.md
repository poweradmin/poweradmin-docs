# Advanced Logging Configuration

This guide provides detailed information about PowerAdmin's advanced logging capabilities and configuration options. For basic logging setup, see the [Basic Logging Configuration](../configuration/logging.md).

## Log Types in Detail

PowerAdmin supports several logging methods that can be combined for comprehensive monitoring:

### 1. Native Logging

Uses PHP's `error_log()` function to write logs to the configured PHP error log destination.

```php
'logging' => [
    'type' => 'native',
    'level' => 'info',
    // other settings...
],
```

### 2. Null Logging

Disables all application logging (except database logging if enabled separately).

```php
'logging' => [
    'type' => 'null',
    // other settings...
],
```

### 3. Database Logging

Logs user actions and zone changes to the PowerAdmin database. This is independent of the main logger type.

```php
'logging' => [
    // Can be combined with any type
    'database_enabled' => true, 
    // other settings...
],
```

### 4. Syslog Logging

Logs authentication and security events to the system's syslog.

```php
'logging' => [
    'syslog_enabled' => true,
    'syslog_identity' => 'poweradmin',    // Program identifier in syslog
    'syslog_facility' => LOG_USER,        // Standard PHP syslog facility constant
    // other settings...
],
```

## Environment-Specific Configurations

### Production Environment Configuration

For a standard production environment:

```php
'logging' => [
    'type' => 'native',
    'level' => 'warning',        // Only log warning and above
    'database_enabled' => true,  // Track user actions and zone changes
    'syslog_enabled' => true,    // Log security events to syslog
    'syslog_identity' => 'poweradmin',
    'syslog_facility' => LOG_LOCAL0,
],
```

### Development Environment Configuration

For a development environment:

```php
'logging' => [
    'type' => 'native',
    'level' => 'debug',         // Log everything including debug messages
    'database_enabled' => true, // Track changes for debugging
    'syslog_enabled' => false,  // Usually not needed in development
],
```

### Minimal Logging Configuration

For minimal performance impact:

```php
'logging' => [
    'type' => 'null',            // Disable application logging
    'database_enabled' => false, // Disable database logging
    'syslog_enabled' => true,    // Keep security logging
    'syslog_identity' => 'poweradmin',
    'syslog_facility' => LOG_USER,
],
```

## Best Practices

1. **Production environments**: Use `warning` or `error` levels to avoid excessive logging
2. **Debug temporary issues**: Temporarily enable `debug` level, then return to normal settings
3. **Database logging**: Useful for audit trails but may impact performance on high-traffic systems
4. **Syslog logging**: Recommended for security events to integrate with system monitoring

## Advanced Configuration

### Custom Log Paths

If using `native` logging, you can control the log file location by configuring PHP's `error_log` setting in your php.ini file.

### Log Rotation

For production systems, ensure log rotation is configured at the system level:
- For syslog: Configure logrotate for your syslog files
- For PHP error logs: Configure logrotate for your PHP error log files
- For database logs: Implement periodic pruning of old log entries

### Database Log Tables

When `database_enabled` is true, logs are stored in:
- `log_users` table: Authentication and user management events
- `log_zones` table: DNS zone and record changes