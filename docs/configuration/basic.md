# Basic Configuration

Poweradmin supports two configuration formats: legacy (individual PHP variables) and modern (array-based configuration). Both formats are stored in the `config/settings.php` file.

## Legacy Configuration Format

This is the traditional format, still supported for backwards compatibility:

```php
<?php
$db_host = 'localhost';
$db_name = 'powerdns-db';
$db_user = 'poweradmin-db-user';
$db_pass = 'poweradmin-db-user-password';
$db_type = 'mysql';

$session_key = 'generate-some-random-text-here';

$dns_hostmaster = 'hostmaster.example.net';
$dns_ns1 = 'ns1.example.net';
$dns_ns2 = 'ns2.example.net';
```

## Modern Configuration Format

The recommended modern format uses a PHP array structure:

```php
<?php
return [
    'database' => [
        'host' => 'localhost',
        'name' => 'powerdns-db',
        'user' => 'poweradmin-db-user',
        'password' => 'poweradmin-db-user-password',
        'type' => 'mysql',
    ],

    'security' => [
        'session_key' => 'change_this_key',
    ],

    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
    ],
];
```

## Configuration Sections

The modern configuration format is organized into logical sections:

- **database**: Database connection settings
- **security**: Security-related settings including password policies and session management
- **dns**: DNS-specific configurations including nameserver details
- **interface**: UI and display preferences
- **logging**: Logging configuration
- **pdns_api**: PowerDNS API integration settings

For detailed information about specific settings, see:
- [Database Configuration](database.md)
- [DNS Settings](dns-settings.md)
- [Security Policies](security-policies.md)

## Important Notes

1. When using the modern format, all settings should be included in the array structure
2. The legacy format is maintained for backward compatibility but new installations should use the modern format
3. Never commit sensitive information like passwords to version control
4. Always change default values, especially the `session_key`, in production environments
5. Make sure to set appropriate file permissions on your configuration file
