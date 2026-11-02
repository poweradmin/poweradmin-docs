# Debugging Poweradmin

To help diagnose issues, you can enable various debug settings in your Poweradmin configuration. Below are the available debug settings and how to enable them.

## Configuration Location

Debugging settings should be added to your `config/settings.php` file. The legacy `inc/config.inc.php` format and its migration script were removed in 4.1.0, so `config/settings.php` is the only configuration file on current releases.

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

### 4. Show Errors in the Interface

`misc.display_errors` (default `false`) makes error pages and PowerDNS API and DNSSEC errors carry the upstream detail, and turns on strict Twig templates. Use it for troubleshooting only and turn it off again in production:

```php
return [
    // Other settings...

    'misc' => [
        'display_errors' => true,
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

Installers before 4.5.0 wrote a broken `config/settings.php` when a database, LDAP or SMTP password contained a single quote (`'`) or a backslash (`\`). From 4.5.0 the web installer escapes both.

**Symptoms (older installers, or a hand-written `settings.php`):**

- Installation fails with PHP parse errors
- Configuration file cannot be parsed
- "Access denied for user" errors after successful installation test

**Example Error:**

```
Parse error: syntax error, unexpected 'password' in config/settings.php on line 42
```

**Solution:**

- In a hand-written `settings.php`, write `\'` for a single quote and `\\` for a backslash inside single-quoted strings. Double quotes need no escaping there.
- On an installer older than 4.5.0, avoid single quotes, backslashes and line breaks in these passwords, or fix the generated file by hand.
- Use `var_dump(ConfigurationManager::getInstance()->getAll())` to inspect parsed configuration values.

### PowerDNS Answers REFUSED for Public Names

Names inside your zones resolve, but `dig @your-server example.com` or any other
public name returns `REFUSED`. This is how PowerDNS Authoritative Server works:
it answers only for the zones it holds and never recurses. No Poweradmin setting
changes that, and neither do secondary zones or supermasters; a secondary zone
transfers one zone in, and a supermaster only auto-creates secondary zones when a
listed primary sends a NOTIFY.

If clients need both your zones and the public internet, run a resolver in front
(PowerDNS Recursor, Unbound, BIND), point the clients at it, and forward only your
own zones to the authoritative server. The old `recursor=` option in `pdns.conf`
was removed in PowerDNS Authoritative 4.1.
