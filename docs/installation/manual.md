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

> **Warning:** The default login credentials are `admin` / `admin`. You **must** change these credentials immediately after your first login for security reasons.

### 4. Create Configuration File

Create a `config/settings.php` file using the template below. A full list of configuration options can be found in `config/settings.defaults.php`.

> **Warning:** When creating passwords for database, LDAP, or SMTP authentication, avoid using single quotes (`'`), double quotes (`"`), backslashes (`\`), and line breaks. These characters can cause configuration file generation to fail during installation with cryptic PHP syntax errors.

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

- Set appropriate permissions on configuration files
- Remove the `install` directory after installation
- Change the default admin password immediately after first login

## Web Server Configuration

### Apache Configuration

Apache requires `mod_rewrite` to be enabled for Poweradmin to function correctly. Starting with v4.1.0, all pages use clean URLs (e.g., `/login`, `/zones`) which depend on URL rewriting.

1. Enable the required Apache modules:

```bash
a2enmod rewrite headers
```

2. Configure your VirtualHost:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/poweradmin

    <Directory /path/to/poweradmin>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # For DDNS update functionality
    RewriteEngine On
    RewriteRule ^/update(.*)$ /dynamic_update.php [L]
    RewriteRule ^/nic/update(.*)$ /dynamic_update.php [L]
</VirtualHost>
```

> **Warning:** If you see 404 errors when accessing Poweradmin (e.g., on `/login`), check that: (1) `mod_rewrite` is enabled: `a2enmod rewrite && systemctl restart apache2`, (2) `AllowOverride All` is set in your VirtualHost or Apache configuration, (3) The `.htaccess` file is present in the Poweradmin root directory.

    You can verify `mod_rewrite` is loaded with: `apache2ctl -M | grep rewrite`

### Important: Apache .htaccess File

The `.htaccess` file in the root directory is **essential** for Poweradmin to work properly. Starting with v4.1.0, it handles all URL routing (not just API requests).

**Version-specific .htaccess files:**

- **For Poweradmin 4.0.x**: Use the [.htaccess from release/4.0.x branch](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/.htaccess)
- **For Poweradmin 4.1.x and later**: Use the latest [.htaccess from master branch](https://github.com/poweradmin/poweradmin/blob/master/.htaccess)

`AllowOverride All` **must** be set in your Apache configuration to allow the `.htaccess` file to function.

### Nginx Configuration
For Nginx servers, use the complete configuration example provided in the Poweradmin repository.

**Version-specific nginx configuration files:**

- **For Poweradmin 4.0.x with API support**: Use the [nginx.conf.example from release/4.0.x branch](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/nginx.conf.example)
- **For other Poweradmin 4.x versions**: Use the latest [nginx.conf.example from master branch](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example)


Make sure to adjust the following settings for your environment:

- `server_name` - Set to your domain name
- `root` - Set to your Poweradmin installation path
- `fastcgi_pass` - Adjust PHP-FPM socket/TCP configuration as needed

### Caddy Configuration
For Caddy servers, use the comprehensive configuration example provided in the Poweradmin repository. This configuration is actively used in the production Docker image and includes advanced security, API support, and performance optimizations.

**Version-specific Caddy configuration files:**

- **For Poweradmin 4.0.x with API support**: Use the [Caddyfile.example from release/4.0.x branch](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/Caddyfile.example)
- **For Poweradmin 4.1.x+**: Use the latest [Caddyfile.example from master branch](https://github.com/poweradmin/poweradmin/blob/master/Caddyfile.example)

Make sure to adjust the following settings for your environment:

- Replace `your-domain.com` with your actual domain name for automatic HTTPS
- `root` - Set to your Poweradmin installation path
- `php_fastcgi` - Adjust PHP-FPM socket/TCP configuration as needed (default: `localhost:9000`)

## Post-Installation Steps

1. Configure web server permissions
2. Set up proper DNS settings (see [DNS Settings](../configuration/dns-settings.md))
3. Configure additional features as needed:
    * [LDAP Integration](../configuration/ldap.md)
    * [PowerDNS API](../configuration/powerdns-api.md)
    * [DNSSEC](../configuration/dnssec.md)

## Troubleshooting

For common installation issues and solutions, see [Debugging](../troubleshooting/debugging.md).
