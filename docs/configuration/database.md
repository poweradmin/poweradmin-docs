# Database Configuration

Poweradmin's database settings are configured in the `config/settings.php` file under the `database` section. This guide covers the general configuration options. For database-specific setup instructions, refer to the links at the bottom of this page.

## Configuration Options

- **type**: Database type. Options: 'mysql', 'pgsql', 'sqlite'. Default: 'mysql'
- **host**: Database server hostname. Default: 'localhost'
- **port**: Database server port. Default: '3306' for MySQL, '5432' for PostgreSQL
- **name**: Database name. Default: 'powerdns'
- **user**: Database username
- **password**: Database password
- **charset**: Database character set. Options: 'latin1', 'utf8', 'utf8mb4'. Default: 'latin1'
- **file**: SQLite database file path (only for SQLite)
- **debug**: Enable SQL query debugging. Default: `false`
- **pdns_db_name**: Separate database name for PowerDNS (added in v3.8.0). Default: same as 'name'

## Example Configuration

```php
return [
    'database' => [
        'host' => 'localhost',
        'port' => '3306',
        'name' => 'powerdns',
        'user' => 'poweradmin',
        'password' => 'your_secure_password',
        'type' => 'mysql',
        'charset' => 'latin1',
        'file' => '',
        'debug' => false,
        'pdns_db_name' => 'powerdns', // Optional: Use when PowerDNS tables are in a separate database
    ],
];
```

## Database Types

Poweradmin supports multiple database backends:

- **MySQL/MariaDB** (recommended): Offers good performance and wide compatibility
- **PostgreSQL**: Provides advanced features and strict SQL standard compliance
- **SQLite**: Lightweight option for small deployments or testing

## Database-Specific Setup Guides

For detailed setup instructions for each database type, including schema creation, permissions, and optimization tips, see:

- [MySQL/MariaDB Setup](../database/mysql-configuration.md)
- [PostgreSQL Setup](../database/postgresql-configuration.md)
- [SQLite Setup](../database/sqlite.md)

These guides provide comprehensive information about:
- Creating users and databases
- Setting up permissions
- Installing schema files
- Performance optimization
- Troubleshooting common issues
