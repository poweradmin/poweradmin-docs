# Logging Configuration

Poweradmin's logging system can be configured through the `config/settings.php` file under the `logging` section.

## Basic Configuration

- **type**: The logging handler to use
  - `null`: Disable logging
  - `native`: Use PHP's native error logging
- **level**: The minimum logging level (see below for options)
- **database_enabled**: Enable logging zone and record changes to database. Default: `false`

## Syslog Configuration

- **syslog_enabled**: Write authentication attempts to syslog. Default: `false`
- **syslog_identity**: Syslog identity string. Default: 'poweradmin'
- **syslog_facility**: Syslog facility to use. Default: LOG_USER

## Log Levels

Available logging levels, in order of increasing severity:

1. DEBUG: Detailed debug information
2. INFO: Interesting events
3. NOTICE: Normal but significant events
4. WARNING: Exceptional occurrences that are not errors
5. ERROR: Runtime errors that do not require immediate action
6. CRITICAL: Critical conditions
7. ALERT: Action must be taken immediately
8. EMERGENCY: System is unusable

## Example Configuration

```php
return [
    'logging' => [
        'type' => 'native',
        'level' => 'warning',
        'database_enabled' => true,
        'syslog_enabled' => true,
        'syslog_identity' => 'poweradmin',
        'syslog_facility' => LOG_USER,
    ],
];
```

For more advanced logging configuration and analysis, see:
- [Log Configuration](../advanced/logging-config.md)
- [Log Analysis](../advanced/log-analysis.md)
