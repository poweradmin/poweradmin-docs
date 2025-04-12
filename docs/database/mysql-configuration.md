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

## Troubleshooting

### Common Issues

1. **Connection errors**: Verify the host, port, user and password settings

2. **Character set issues**: Make sure the charset in settings matches the database charset

3. **Permission problems**: Ensure the database user has appropriate privileges

