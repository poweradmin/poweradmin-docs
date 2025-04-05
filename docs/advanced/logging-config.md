# PowerAdmin Logging Configuration Guide

PowerAdmin includes a flexible logging system that supports multiple output methods and log levels. This guide explains how to configure various types of logging in your PowerAdmin installation.

## Logging Configuration

Logging settings are defined in your `config/settings.php` file. The defaults are provided in `config/settings.defaults.php`:

```php
'logging' => [
    'type' => 'null',                          // Options: 'null', 'native'
    'level' => 'info',                         // Options: 'debug', 'info', 'notice', 'warning', 'error', 'critical', 'alert', 'emergency'
    'database_enabled' => false,               // Enable logging zone and record changes to the database
    
    // Syslog Settings
    'syslog_enabled' => false,                 // Write authentication attempts to syslog
    'syslog_identity' => 'poweradmin',         // Syslog identity
    'syslog_facility' => LOG_USER,             // Syslog facility
],
```

## Log Types

PowerAdmin supports several logging methods:

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

## Log Levels

PowerAdmin supports the standard PSR-3 log levels, from highest to lowest severity:

1. `emergency`: System is unusable
2. `alert`: Action must be taken immediately
3. `critical`: Critical conditions
4. `error`: Error conditions
5. `warning`: Warning conditions
6. `notice`: Normal but significant conditions
7. `info`: Informational messages (default)
8. `debug`: Debug-level messages

When you set a specific log level, you will receive logs of that level and all higher severity levels. For example, setting `level` to `warning` will log warnings, errors, critical issues, alerts, and emergencies, but not info or debug messages.

## Practical Examples

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