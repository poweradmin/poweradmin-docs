# Database Configuration

Poweradmin's database settings are configured in the `config/settings.php` file under the `database` section.

## Configuration Options

- **type**: Database type. Options: 'mysql', 'pgsql', 'sqlite'. Default: 'mysql'
- **host**: Database server hostname. Default: 'localhost'
- **port**: Database server port. Default: '3306'
- **name**: Database name. Default: 'powerdns'
- **user**: Database username
- **password**: Database password
- **charset**: Database character set. Options: 'latin1', 'utf8'. Default: 'latin1'
- **file**: SQLite database file path (only for SQLite)
- **debug**: Enable SQL query debugging. Default: `false`

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
    ],
];
```

## Database Types

Poweradmin supports multiple database backends:

- MySQL/MariaDB (recommended)
- PostgreSQL
- SQLite

For detailed setup instructions for each database type, see:
- [MySQL/MariaDB Setup](../database/mysql.md)
- [PostgreSQL Setup](../database/postgresql.md)
- [SQLite Setup](../database/sqlite.md)
