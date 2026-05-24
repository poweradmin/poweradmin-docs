# Manual Installation

This page describes how to install Poweradmin **without** running the web installer wizard. The manual path is useful for automated deployments (Ansible, Salt, Terraform), restricted environments where the wizard cannot be reached, or operators who want to keep the install directory out of the document root entirely.

If you would rather have the wizard walk you through the setup interactively, see [Web Installer Wizard](wizard.md).

## Prerequisites

Verify that your setup meets the application requirements. For detailed requirements, including PHP version, required extensions, and supported databases, see [System Requirements](../getting-started/requirements.md).

## Installation Steps

### 1. Prepare the Environment

Unpack the Poweradmin archive in a location accessible via your web server. Ensure unpacked files are readable by the user that your web server/PHP runs as.

### 2. Import Database Structure

Import the Poweradmin database structure as a database superuser. The schema bundles the tables Poweradmin needs alongside the PowerDNS tables your authoritative server already uses.

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

> **Note:** Unlike the web installer, importing the schema does not create an admin user automatically. You will create the `admin` account by hand in step 4. Until then, there is no way to log in.

### 3. Create Database User

After importing the schema, create a database user with SELECT, INSERT, UPDATE, DELETE rights on the database. Grant the runtime user only what it needs - never reuse the superuser credentials from step 2 in `config/settings.php`.

#### For MySQL/MariaDB:
```sql
CREATE USER 'poweradmin'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON powerdns.* TO 'poweradmin'@'localhost';
FLUSH PRIVILEGES;
```

#### For PostgreSQL:
Run these as the `postgres` superuser inside the target database (`\c powerdns` in `psql`). The `ALTER DEFAULT PRIVILEGES` step is required so that any tables added by future schema updates are automatically covered:

```sql
CREATE USER poweradmin WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE powerdns TO poweradmin;
GRANT USAGE ON SCHEMA public TO poweradmin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO poweradmin;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO poweradmin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO poweradmin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO poweradmin;
```

### 4. Create the Admin User

The web installer normally creates the built-in `admin` account for you. Since you are skipping the installer, insert it by hand. The wizard hashes the password with PHP's `password_hash()` and bcrypt by default - do the same for compatibility:

```sh
php -r 'echo password_hash("your_admin_password", PASSWORD_BCRYPT, ["cost" => 12]) . "\n";'
```

Copy the resulting hash (it will start with `$2y$`) and insert the row, pointing `perm_templ` at the seeded Administrator template (id `1`):

```sql
INSERT INTO users
    (username, password, fullname, email, description, perm_templ, active, use_ldap, auth_method)
VALUES
    ('admin', '<PASTE_HASH_HERE>', 'Administrator', 'admin@example.net', 'Administrator with full rights.', 1, 1, 0, 'sql');
```

> **Note:** Administrative rights come from the `perm_templ` column on the `users` row, not from a separate join table. Permission template `id = 1` is the seeded "Administrator template with full rights".

### 5. Create Configuration File

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
        'user' => 'poweradmin', // Database user created in step 3
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

### 6. Secure the Installation

- Restrict permissions on `config/settings.php` so only the web server user can read it.
- Remove or rename the `install/` directory so the wizard cannot be re-run.
- Confirm you can log in at `/login` as `admin` with the password you hashed in step 4, then rotate it from the web interface if it was a temporary placeholder.

## Web Server Configuration

### Apache Configuration

Apache requires `mod_rewrite` to be enabled for Poweradmin to function correctly. Starting with v4.1.0, all pages use clean URLs (e.g., `/login`, `/zones`) which depend on URL rewriting.

1. Enable the required Apache modules:

```bash
a2enmod rewrite headers
```

2. Configure your VirtualHost. If you are using PHP-FPM instead of `mod_php`, also include the `SetHandler` block shown below to forward `.php` requests to the FPM socket:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/poweradmin

    <Directory /path/to/poweradmin>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Only needed when using PHP-FPM (not mod_php).
    # Adjust the socket path to your installed PHP version.
    <FilesMatch \.php$>
        SetHandler "proxy:unix:/var/run/php/php8.2-fpm.sock|fcgi://localhost"
    </FilesMatch>

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
