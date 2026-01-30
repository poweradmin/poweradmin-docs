# MySQL Configuration for Poweradmin

## Overview

This guide explains how to configure Poweradmin to use MySQL or MariaDB as your database backend.

## Requirements

- MySQL 5.7+ or MariaDB 10.3+
- PHP with PDO MySQL extension enabled
- MySQL user with appropriate privileges

## Configuration Steps

1. Create a configuration file at `/config/settings.php` based on the example below:

```php
<?php
/**
 * Poweradmin MySQL Configuration
 */
return [
    /**
     * Database Settings
     */
    'database' => [
        'type' => 'mysql',            // Set database type to MySQL
        'host' => 'localhost',        // MySQL server hostname
        'port' => '3306',             // Default MySQL port
        'user' => 'poweradmin',       // Database username
        'password' => 'your_password', // Database password (change this!)
        'name' => 'powerdns',         // Database name
        'charset' => 'utf8mb4',       // Recommended: utf8mb4 for full Unicode support
        'file' => '',                 // Not used for MySQL
        'debug' => false,             // Set to true to see SQL queries for debugging

        // SSL/TLS Settings (optional, added in 4.1.0)
        'ssl' => false,               // Enable SSL/TLS connection
        'ssl_verify' => false,        // Verify server certificate (requires ssl=true)
        'ssl_ca' => '',               // Path to CA certificate file
        'ssl_key' => '',              // Path to client private key (for mTLS)
        'ssl_cert' => '',             // Path to client certificate (for mTLS)
    ],

    // Other configuration sections remain the same as in settings.defaults.php
];
```

## Database Creation

### Creating the Database

```sql
CREATE DATABASE powerdns CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'poweradmin'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON powerdns.* TO 'poweradmin'@'localhost';
FLUSH PRIVILEGES;
```

### Schema Installation

The SQL schema files are located in the `sql/` directory:

- For a new installation: Use `sql/poweradmin-mysql-db-structure.sql`
- For PowerDNS schema: Check the appropriate version in `sql/pdns/[version]/schema.mysql.sql`

```bash
mysql -u poweradmin -p powerdns < sql/poweradmin-mysql-db-structure.sql
mysql -u poweradmin -p powerdns < sql/pdns/[version]/schema.mysql.sql
```

## SSL/TLS Configuration

*Added in version 4.1.0*

Poweradmin supports SSL/TLS encrypted connections to MySQL/MariaDB servers.

### SSL Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `ssl` | Enable SSL/TLS connection | `false` |
| `ssl_verify` | Verify server certificate (requires `ssl=true`) | `false` |
| `ssl_ca` | Path to CA certificate file | Empty |
| `ssl_key` | Path to client private key (for mutual TLS) | Empty |
| `ssl_cert` | Path to client certificate (for mutual TLS) | Empty |

### Example: SSL with Certificate Verification

```php
'database' => [
    'type' => 'mysql',
    'host' => 'mysql.example.com',
    'port' => '3306',
    'user' => 'poweradmin',
    'password' => 'your_password',
    'name' => 'powerdns',
    'charset' => 'utf8mb4',
    'ssl' => true,
    'ssl_verify' => true,
    'ssl_ca' => '/path/to/ca-cert.pem',
],
```

### Example: SSL without Verification (Self-Signed Certificates)

```php
'database' => [
    'type' => 'mysql',
    'host' => 'mysql.example.com',
    'port' => '3306',
    'user' => 'poweradmin',
    'password' => 'your_password',
    'name' => 'powerdns',
    'charset' => 'utf8mb4',
    'ssl' => true,
    'ssl_verify' => false,
],
```

### Backwards Compatibility Note

By default (`ssl=false`), Poweradmin disables SSL certificate verification to maintain backwards compatibility with servers that don't use SSL or use self-signed certificates. This addresses issues with newer MariaDB connector libraries that enforce SSL verification by default.
