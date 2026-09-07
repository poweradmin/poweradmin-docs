# Database Configuration

Poweradmin's database settings are configured in the `config/settings.php` file under the `database` section. This guide covers the general configuration options. For database-specific setup instructions, refer to the links at the bottom of this page.

## Configuration Options

- **type**: Database type. Options: 'mysql', 'pgsql', 'sqlite'. Default: 'mysql'
- **host**: Database server hostname. Default: 'localhost'
- **port**: Database server port. Default: '3306' for MySQL, '5432' for PostgreSQL
- **name**: Database name. Default: 'powerdns'
- **user**: Database username
- **password**: Database password
- **charset**: Database character set. Default: 'latin1'. Only the literal value `utf8` affects the connection: on MySQL/MariaDB it appends `charset=utf8` to the DSN. Any other value, `utf8mb4` included, leaves the connection on the server's default character set. The installer offers the driver's full charset list (about 38 values for MySQL) and uses that choice when creating the tables, which is a separate thing from the connection charset
- **file**: SQLite database file path (only for SQLite)
- **debug**: Enable SQL query debugging. Default: `false`
- **pdns_db_name**: Separate database name for PowerDNS (added in v3.8.0). MySQL/MariaDB only - ignored (and rejected by config validation) on PostgreSQL and SQLite. Default: same as 'name'

## Example Configuration

```php
return [
    'database' => [
        'host' => 'localhost',
        'port' => '3306',
        'name' => 'poweradmin',
        'user' => 'poweradmin',
        'password' => 'your_secure_password',
        'type' => 'mysql',
        'charset' => 'latin1',
        'file' => '',
        'debug' => false,
        'pdns_db_name' => 'powerdns', // Optional, MySQL/MariaDB only: Use when PowerDNS tables are in a separate database
    ],
];
```

## Moving Poweradmin Tables to Their Own Database

Many older installations keep the Poweradmin tables in the PowerDNS database.
On MySQL/MariaDB you can split them without re-importing anything, because
`RENAME TABLE` moves a table between databases on the same server atomically
and keeps its data.

1. Bring the schema up to date first. Run any missing update scripts against the
   shared database (see [Which update scripts have already run?](../upgrading/index.md#which-update-scripts-have-already-run)).
2. Take a dump of the shared database.
3. Create the new database and grant the Poweradmin user access to it:

    ```sql
    CREATE DATABASE poweradmin CHARACTER SET utf8mb4;
    GRANT ALL ON poweradmin.* TO 'poweradmin'@'%';
    ```

4. Generate the rename statements. Everything in the shared database that is not
   one of PowerDNS's own tables belongs to Poweradmin:

    ```sql
    SELECT CONCAT('RENAME TABLE `powerdns`.`', table_name, '` TO `poweradmin`.`', table_name, '`;')
    FROM information_schema.tables
    WHERE table_schema = 'powerdns'
      AND table_name NOT IN ('domains', 'records', 'supermasters', 'comments',
                             'domainmetadata', 'cryptokeys', 'tsigkeys');
    ```

    Review the output, then run it.

5. Point Poweradmin at the new layout in `config/settings.php`:

    ```php
    'database' => [
        'name' => 'poweradmin',
        'pdns_db_name' => 'powerdns',
        // ...
    ],
    ```

6. Log in and open the zone list, users, and zone templates pages.

A name server that replicates the database can now replicate only `powerdns`.
Future update scripts run against the `poweradmin` database. The 4.3.0 script
reads the PowerDNS `domains` table; its header explains how to qualify that
name when `pdns_db_name` is set.

PostgreSQL and SQLite do not support `pdns_db_name`. To separate the databases
there, switch to [API backend mode](powerdns-api.md#migrating-from-sql-to-api-backend),
which needs only the Poweradmin tables.

## Database Types

Poweradmin supports multiple database backends:

- **MySQL/MariaDB** (recommended): Offers good performance and wide compatibility
- **PostgreSQL**: Provides advanced features and strict SQL standard compliance
- **SQLite**: Lightweight option for small deployments or testing

Poweradmin uses PowerDNS's own database tables for zones and records. It directly queries the PowerDNS tables like domains and records, while maintaining its own tables for user permissions and metadata. The system will display all zones in the PowerDNS database, regardless of how they were created (through Poweradmin UI or via REST API).

```
┌─────────────────────┐            ┌─────────────────────┐
│                     │            │                     │
│    Poweradmin       │            │     PowerDNS        │
│    Application      │            │     Server          │
│                     │            │                     │
└──────────┬──────────┘            └──────────┬──────────┘
           │                                  │
           │                                  │
           │                                  │
           │      ┌────────────────────┐      │
           │      │                    │      │
           └─────►│ Database Server    │◄─────┘
                  │                    │
                  │ ┌──────────────┐   │
                  │ │ PowerDNS     │   │
                  │ │ Tables       │   │
                  │ │ - domains    │   │
                  │ │ - records    │   │
                  │ │ - ...        │   │
                  │ └──────────────┘   │
                  │                    │
                  │ ┌──────────────┐   │
                  │ │ Poweradmin   │   │
                  │ │ Tables       │   │
                  │ │ - users      │   │
                  │ │ - permissions│   │
                  │ │ - ...        │   │
                  │ └──────────────┘   │
                  │                    │
                  └────────────────────┘
```

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
