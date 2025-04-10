# PostgreSQL Configuration for Poweradmin

## Overview

This guide explains how to configure Poweradmin to use PostgreSQL as your database backend.

## Requirements

- PostgreSQL 10.0+
- PHP with PDO PostgreSQL extension enabled
- PostgreSQL user with appropriate privileges

## Configuration Steps

1. Create a configuration file at `/config/settings.php` based on the example below:

```php
<?php
/**
 * Poweradmin PostgreSQL Configuration
 */
return [
    /**
     * Database Settings
     */
    'database' => [
        'type' => 'pgsql',            // Set database type to PostgreSQL
        'host' => 'localhost',        // PostgreSQL server hostname
        'port' => '5432',             // Default PostgreSQL port
        'user' => 'poweradmin',       // Database username
        'password' => 'your_password', // Database password (change this!)
        'name' => 'powerdns',         // Database name
        'charset' => 'UTF8',          // PostgreSQL uses uppercase charset names
        'file' => '',                 // Not used for PostgreSQL
        'debug' => false,             // Set to true to see SQL queries for debugging
    ],
    
    // Other configuration sections remain the same as in settings.defaults.php
];
```

## Database Creation

### Creating the Database

```sql
CREATE DATABASE powerdns ENCODING 'UTF8';
CREATE USER poweradmin WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE powerdns TO poweradmin;
\c powerdns
GRANT ALL ON SCHEMA public TO poweradmin;
```

### Schema Installation

The SQL schema files are located in the `sql/` directory:

- For a new installation: Use `sql/poweradmin-pgsql-db-structure.sql`
- For PowerDNS schema: Check the appropriate version in `sql/pdns/[version]/schema.pgsql.sql`

```bash
psql -U poweradmin -d powerdns -f sql/poweradmin-pgsql-db-structure.sql
psql -U poweradmin -d powerdns -f sql/pdns/[version]/schema.pgsql.sql
```

## Optimization Guidelines

### Server Configuration

For better performance with PostgreSQL, consider these settings in your PostgreSQL server configuration:

```ini
# postgresql.conf
max_connections = 100                # Maximum number of connections
shared_buffers = 128MB               # Start with 25% of RAM for small servers
effective_cache_size = 4GB           # Set to about 50-75% of available RAM
work_mem = 4MB                       # Memory for query operations
maintenance_work_mem = 64MB          # Memory for maintenance operations
random_page_cost = 4                 # Lower for SSD (1.1-2.0), higher for HDD
timezone = 'UTC'                     # Database timezone
```

## PostgreSQL-Specific Considerations

### Sequences

PostgreSQL uses sequences for auto-incrementing primary keys. If you're migrating from MySQL or experiencing issues with IDs, you may need to reset sequences:

```sql
SELECT setval('sequence_name', (SELECT MAX(id) FROM table_name));
```

### Case Sensitivity

PostgreSQL is case-sensitive for identifiers unless quoted. All table and column names in Poweradmin should be accessed in lowercase.

### Performance Tuning

1. **VACUUM**: Schedule regular `VACUUM ANALYZE` operations to maintain database health

2. **Indexing**: Consider additional indexes for query patterns specific to your installation

3. **Statement Timeout**: For web applications, consider setting `statement_timeout` to prevent long-running queries

## Troubleshooting

### Common Issues

1. **Connection errors**: 
   - Verify the host, port, user and password settings
   - Check pg_hba.conf for client authorization settings

2. **Permission problems**: 
   - Ensure the database user has appropriate privileges
   - Check both database and schema-level permissions

3. **Performance issues**:
   - Run EXPLAIN ANALYZE on slow queries
   - Check for missing indexes
   - Ensure autovacuum is properly configured

## SQL Compatibility Notes

When developing custom queries or extensions for Poweradmin with PostgreSQL, note these differences from MySQL:

1. PostgreSQL uses `SERIAL` instead of `AUTO_INCREMENT`
2. String concatenation uses `||` instead of `CONCAT()` or `+`
3. Use `IS NULL` and `IS NOT NULL` instead of `= NULL` or `!= NULL`
4. Date functions differ significantly between MySQL and PostgreSQL
5. PostgreSQL is generally stricter about SQL syntax and type casting