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

## Web Server Configuration

### Apache Configuration
For a basic Apache configuration, you can use the following settings:

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

### Nginx Configuration
For Nginx servers, use the following configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/poweradmin;
    index index.php index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # For DDNS update functionality
    location ~ ^/update {
        rewrite ^/update(.*)$ /dynamic_update.php last;
    }
    
    location ~ ^/nic/update {
        rewrite ^/nic/update(.*)$ /dynamic_update.php last;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
    }
}
```

### Caddy Configuration
The following Caddy configuration has been suggested by community members. Note that this configuration is not actively used by the maintainers but has been reported to work:

```caddy
:80 {
    log {
        output file /var/log/caddy/caddy.log {
        }
    }

    # Set this path to your site's directory.
    root * /srv/www

    rewrite /update /dynamic_update.php
    rewrite /nic/update /dynamic_update.php

    php_fastcgi * unix//run/php/php-fpm.sock {
    }

    file_server * {
    }
}
```

## Post-Installation Steps

1. Configure web server permissions
2. Set up proper DNS settings (see [DNS Settings](../configuration/dns-settings.md))
3. Configure additional features as needed:
    * [LDAP Integration](../configuration/ldap.md)
    * [PowerDNS API](../configuration/powerdns-api.md)
    * [DNSSEC](../configuration/dnssec.md)

## Troubleshooting

For common installation issues and solutions, see [Common Issues](../troubleshooting/common-issues.md).
