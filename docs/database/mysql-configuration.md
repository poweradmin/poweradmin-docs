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

## Optimization Guidelines

### Server Configuration

For better performance with MySQL, consider these settings in your MySQL server configuration:

```ini
# my.cnf or my.ini
[mysqld]
innodb_buffer_pool_size = 128M       # Increase for better performance (adjust based on server RAM)
max_connections = 100                # Maximum number of connections
wait_timeout = 28800                 # Timeout for idle connections (in seconds)
character_set_server = utf8mb4       # For complete Unicode support
collation_server = utf8mb4_general_ci # Case-insensitive collation
innodb_flush_log_at_trx_commit = 1   # 1 = Most durable but slower, 2 = Good compromise
```

### InnoDB Migration

Poweradmin works best with InnoDB tables. If you're using an older installation with MyISAM tables, consider migrating to InnoDB. See `sql/InnoDB-migration.md` for detailed migration steps.

## Performance Considerations

1. **Indexes**: Ensure indexes are properly set up, especially on frequently queried fields

2. **Query optimization**: When experiencing slow performance, enable debug mode to review and optimize SQL queries

3. **Connection pooling**: For high-traffic installations, consider implementing connection pooling

4. **Regular maintenance**: 
   - Run `OPTIMIZE TABLE` periodically on tables with frequent deletions
   - Consider setting up a maintenance plan for database backups

## Troubleshooting

### Common Issues

1. **Connection errors**: Verify the host, port, user and password settings

2. **Character set issues**: Make sure the charset in settings matches the database charset

3. **Permission problems**: Ensure the database user has appropriate privileges

4. **Performance issues**:
   - Increase buffer pool size
   - Check slow query log
   - Ensure proper indexing