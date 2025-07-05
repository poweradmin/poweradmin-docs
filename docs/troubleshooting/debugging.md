# Debugging Poweradmin

To help diagnose issues, you can enable various debug settings in your Poweradmin configuration. Below are the available debug settings and how to enable them.

## Configuration Location

Debugging settings should be added to your `config/settings.php` file. If you're still using the legacy configuration in `inc/config.inc.php`, consider migrating to the new configuration format using the provided script:

```bash
php scripts/migrate-config.php
```

## Available Debug Settings

### 1. PHP Error Reporting

To display PHP errors directly in the browser, add the following lines to your `index.php` or any other entry point file:

```php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
```

### 2. Logger Settings

Configure the logging settings in your `config/settings.php`:

```php
return [
    // Other settings...
    
    'logging' => [
        'type' => 'native',    // Options: 'null', 'native'
        'level' => 'debug',    // Options: 'debug', 'info', 'notice', 'warning', 'error', 'critical', 'alert', 'emergency'
        // Other logging settings...
    ],
    
    // Other settings...
];
```

These settings are primarily used for logging authentication issues and other system events.

### 3. Database Debugging

Enable or disable database debugging to log detailed database operations and errors:

```php
return [
    // Other settings...
    
    'database' => [
        // Other database settings...
        'debug' => true,    // Show all SQL queries
    ],
    
    // Other settings...
];
```

### 4. DNSSEC Debugging

Enable or disable DNSSEC debugging to log detailed DNSSEC operations and errors:

```php
return [
    // Other settings...
    
    'dnssec' => [
        // Other DNSSEC settings...
        'debug' => true,    // Enable DNSSEC debug logging
    ],
    
    // Other settings...
];
```

### 5. LDAP Debugging

Enable or disable LDAP debugging to log detailed LDAP operations and errors:

```php
return [
    // Other settings...
    
    'ldap' => [
        // Other LDAP settings...
        'debug' => true,    // Enable LDAP debug logging
    ],
    
    // Other settings...
];
```

## Display Statistics

To see memory usage and execution time at the bottom of each page, enable the display_stats option:

```php
return [
    // Other settings...
    
    'misc' => [
        // Other miscellaneous settings...
        'display_stats' => true,    // Display memory usage and execution time
    ],
    
    // Other settings...
];
```

By enabling these settings, you can gain more insight into the application's behavior and troubleshoot issues more effectively.

## Common Configuration Issues

### Password Character Issues

If you experience PHP syntax errors when generating configuration files during installation, check your passwords for problematic characters:

**Symptoms:**
- Installation fails with PHP parse errors
- Configuration file cannot be parsed
- "Access denied for user" errors after successful installation test

**Solution:**
Avoid these characters in database, LDAP, and SMTP passwords:
- Single quotes (`'`)
- Double quotes (`"`)
- Backslashes (`\`)
- Line breaks

**Example Error:**
```
Parse error: syntax error, unexpected 'password' in config/settings.php on line 42
```

**Debugging Steps:**
1. Check your password for the problematic characters listed above
2. Use `var_dump((new AppConfiguration())->getAll())` to inspect parsed configuration values
3. Look for missing quotes or escape characters in the output
4. Change the password to use only alphanumeric characters and basic symbols

This issue occurs because the configuration file generator does not properly escape special PHP characters in password values during installation.