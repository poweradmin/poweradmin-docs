# Manual Installation

This page describes the manual installation procedure for Poweradmin. While using the installer is recommended for most users, manual installation can be useful for automated deployments or advanced users.

## Prerequisites

Verify that your setup meets the application requirements. For detailed requirements, including PHP version, required extensions, and supported databases, see [System Requirements](../getting-started/requirements.md).

## Installation Steps

### 1. Prepare the Environment

Unpack the Poweradmin archive in a location accessible via your web server. Ensure unpacked files are readable by the user that your web server/PHP runs as.

### 2. Create Database User

Create a database user with SELECT, INSERT, UPDATE, DELETE rights on your PowerDNS database:

#### For MySQL/MariaDB:
```sql
CREATE USER 'poweradmin'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON powerdns.* TO 'poweradmin'@'localhost';
FLUSH PRIVILEGES;
```

#### For PostgreSQL:
```sql
CREATE USER poweradmin WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO poweradmin;
```

### 3. Import Database Structure

Import the Poweradmin database structure:

#### For MySQL/MariaDB:
```bash
mysql -u root -p powerdns < sql/poweradmin-mysql-db-structure.sql
```

#### For PostgreSQL:
```bash
psql -U postgres -d powerdns -f sql/poweradmin-pgsql-db-structure.sql
```

#### For SQLite:
```bash
sqlite3 /path/to/your/powerdns.db < sql/poweradmin-sqlite-db-structure.sql
```

!!! danger "Default Credentials"
    The default login credentials are:
    
    * Username: `admin`
    * Password: `admin`
    
    You **must** change these credentials immediately after your first login for security reasons.

### 4. Create Configuration File

Create a `config/settings.php` file using the template below. A full list of configuration options can be found in `config/settings.defaults.php`.

```php
<?php
/**
 * Poweradmin Custom Settings Configuration File
 */

return [
    /**
     * Database Settings
     */
    'database' => [
        'host' => 'localhost',
        'user' => 'poweradmin', // Database user created in step 2
        'password' => 'secure_password',
        'name' => 'powerdns',  // PowerDNS database name
        'type' => 'mysql',     // Options: 'mysql', 'pgsql', 'sqlite'
        // 'file' => '',       // Only for SQLite, provide full path to database file
    ],

    /**
     * Security Settings
     */
    'security' => [
        'session_key' => 'generate_a_random_string_here', // IMPORTANT: Change this!
    ],

    /**
     * DNS Settings
     */
    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
    ],
];
```

For detailed configuration options, see [Basic Configuration](../configuration/basic.md) and [Database Configuration](../configuration/database.md).

### 5. Secure the Installation

* Set appropriate permissions on configuration files
* Remove the `install` directory after installation
* Change the default admin password immediately after first login
## Post-Installation Steps

1. Configure web server permissions
2. Set up proper DNS settings (see [DNS Settings](../configuration/dns-settings.md))
3. Configure additional features as needed:
    * [LDAP Integration](../configuration/ldap.md)
    * [PowerDNS API](../configuration/powerdns-api.md)
    * [DNSSEC](../configuration/dnssec.md)

## Troubleshooting

For common installation issues and solutions, see [Common Issues](../troubleshooting/common-issues.md).
