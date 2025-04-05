# Logging Configuration

Poweradmin's logging system can be configured through the `config/settings.php` file under the `logging` section, or through individual variables in the legacy configuration format.

## Configuration Options

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $logger_type | logging.type | null | Logger type (null, native) | 3.9.0 |
| $logger_level | logging.level | info | Logging level (debug, info, notice, warning, error, critical, alert, emergency) | 3.9.0 |
| $syslog_use | logging.syslog_enabled | false | Enable (true) or disable (false) logging of authentication attempts and other operations to syslog | 2.1.6 |
| $syslog_ident | logging.syslog_identity | poweradmin | Specifies program name which is added to syslog message | 2.1.6 |
| $syslog_facility | logging.syslog_facility | LOG_USER | Specifies what type of program is logging the message | 2.1.6 |
| $dblog_use | logging.database_enabled | false | Enable (true) or disable (false) logging to database | 3.2.0 |

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

## Modern Configuration Example

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

## Legacy Configuration Example

```php
<?php
// Logging settings
$logger_type = 'native';
$logger_level = 'warning';
$syslog_use = true;
$syslog_ident = 'poweradmin';
$syslog_facility = LOG_USER;
$dblog_use = true;
```

For more advanced logging configuration and analysis, see:
- [Log Configuration](../advanced/logging-config.md)
