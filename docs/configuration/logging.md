# Basic Logging Configuration

Poweradmin has two independent logging systems. This guide covers the basic configuration options. For advanced settings and best practices, see the [Advanced Logging Configuration](../advanced/logging-config.md) guide.

## Two Logging Systems

Poweradmin uses two separate logging systems that serve different purposes:

### 1. Audit Logging (who did what)

Controlled by `database_enabled` and `syslog_enabled`. Tracks user, zone, and group changes - create/edit/delete operations, login/logout, group membership changes.

- **database_enabled**: writes audit events to `log_users`, `log_zones`, and `log_groups` tables
- **syslog_enabled**: writes audit events to syslog

### 2. Diagnostic Logging (application errors and debug info)

Controlled by `type` and `level`. Used for troubleshooting application issues such as password reset flows, MFA, OIDC/SAML errors. Writes to PHP's `error_log`. Not related to audit logging.

## Configuration Options

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $logger_type | logging.type | null | Diagnostic logger type: null (disabled), native (PHP error_log) | 3.9.0 |
| $logger_level | logging.level | info | Diagnostic logging level (debug, info, notice, warning, error, critical, alert, emergency) | 3.9.0 |
| $dblog_use | logging.database_enabled | false | Enable audit logging to database (log_users, log_zones, log_groups tables) | 3.2.0 |
| $syslog_use | logging.syslog_enabled | false | Enable audit logging to syslog | 2.1.6 |
| $syslog_ident | logging.syslog_identity | poweradmin | Specifies program name which is added to syslog message | 2.1.6 |
| $syslog_facility | logging.syslog_facility | LOG_USER | Specifies what type of program is logging the message | 2.1.6 |

## Diagnostic Log Levels

Available logging levels for the diagnostic logger (`type`/`level`), in order of increasing severity:

1. DEBUG: Detailed debug information
2. INFO: Interesting events
3. NOTICE: Normal but significant events
4. WARNING: Exceptional occurrences that are not errors
5. ERROR: Runtime errors that do not require immediate action
6. CRITICAL: Critical conditions
7. ALERT: Action must be taken immediately
8. EMERGENCY: System is unusable

When you set a specific log level, you will receive logs of that level and all higher severity levels. For example, setting `level` to `warning` will log warnings, errors, critical issues, alerts, and emergencies, but not info or debug messages.

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

For more advanced logging configuration, environment-specific examples, and best practices, see:
- [Advanced Logging Configuration](../advanced/logging-config.md)
