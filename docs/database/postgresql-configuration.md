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

        // SSL/TLS Settings (optional, added in 4.1.0)
        'ssl' => false,               // Enable SSL/TLS connection
        'ssl_verify' => false,        // Verify server certificate (requires ssl=true)
        'ssl_ca' => '',               // Path to CA certificate file (sslrootcert)
        'ssl_key' => '',              // Path to client private key (sslkey)
        'ssl_cert' => '',             // Path to client certificate (sslcert)
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

## SSL/TLS Configuration

*Added in version 4.1.0*

Poweradmin supports SSL/TLS encrypted connections to PostgreSQL servers using the `sslmode` DSN parameter.

### SSL Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `ssl` | Enable SSL/TLS connection | `false` |
| `ssl_verify` | Verify server certificate (requires `ssl=true`) | `false` |
| `ssl_ca` | Path to CA certificate file (sslrootcert) | Empty |
| `ssl_key` | Path to client private key (sslkey) | Empty |
| `ssl_cert` | Path to client certificate (sslcert) | Empty |

### SSL Mode Mapping

Poweradmin maps the settings to PostgreSQL `sslmode` values:

| ssl | ssl_verify | PostgreSQL sslmode |
|-----|------------|-------------------|
| `false` | - | `prefer` (try SSL, fall back to non-SSL) |
| `true` | `false` | `require` (require SSL, no cert verification) |
| `true` | `true` | `verify-full` (require SSL + verify cert + hostname) |

### Example: SSL with Certificate Verification

```php
'database' => [
    'type' => 'pgsql',
    'host' => 'postgres.example.com',
    'port' => '5432',
    'user' => 'poweradmin',
    'password' => 'your_password',
    'name' => 'powerdns',
    'ssl' => true,
    'ssl_verify' => true,
    'ssl_ca' => '/path/to/ca-cert.pem',
],
```

### Example: SSL without Verification

```php
'database' => [
    'type' => 'pgsql',
    'host' => 'postgres.example.com',
    'port' => '5432',
    'user' => 'poweradmin',
    'password' => 'your_password',
    'name' => 'powerdns',
    'ssl' => true,
    'ssl_verify' => false,
],
```

### Backwards Compatibility Note

By default (`ssl=false`), Poweradmin uses `sslmode=prefer`, which attempts SSL connections but falls back to non-SSL if the server doesn't support it. This maintains backwards compatibility with existing configurations.
