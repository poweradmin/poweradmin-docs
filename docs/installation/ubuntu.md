# Ubuntu Installation

This guide will help you install Poweradmin on Ubuntu systems. Tested on Ubuntu 24.04 LTS (PHP 8.3) and Ubuntu 22.04 LTS (requires PHP 8.2+ via the [ondrej/php PPA](https://launchpad.net/~ondrej/+archive/ubuntu/php) since 22.04 ships PHP 8.1).

## Prerequisites

### Install PowerDNS

Poweradmin is a frontend for an existing PowerDNS authoritative server - it does not install or run PowerDNS itself. If you do not already have PowerDNS running, install it first and configure a database backend (MySQL/MariaDB, PostgreSQL, or SQLite). See the [PowerDNS installation guide](https://doc.powerdns.com/authoritative/installation.html) for details.

### Install PHP and Extensions

Install PHP and the extensions Poweradmin requires:

```bash
apt install php php-cli php-intl php-mbstring php-xml php-curl php-fpm
```

> **Note:** `gettext` and `tokenizer` are built into `php-cli` on Ubuntu and do not need separate packages. `php-fpm` is required only if you plan to use Nginx or choose not to use `mod_php` with Apache.

### Database Support

Install the appropriate PHP database driver based on your preferred database:

```bash
# For MySQL/MariaDB
apt install php-mysql

# For PostgreSQL
apt install php-pgsql

# For SQLite
apt install php-sqlite3
```

## Web Server Configuration

### Apache

Install Apache if it is not already present:

```bash
apt install apache2 libapache2-mod-php
```

Then:

1. Enable the required Apache modules:

```bash
a2enmod rewrite headers
```

2. Either place Poweradmin in the default webroot (`/var/www/html/`) or create a virtual host configuration.

3. Ensure `AllowOverride All` is set in your Apache configuration to allow the `.htaccess` file to function properly.

The `.htaccess` file included with Poweradmin handles URL routing, API support, and security rules automatically.

### Nginx Configuration

If you prefer Nginx, first install it:

```bash
apt install nginx
```

Then use the configuration example provided in the Poweradmin repository. The configuration includes API routing, CORS support, security rules, and clean URL handling.

**Version-specific configuration files:**

- **Poweradmin 4.0.x**: Use [nginx.conf.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/nginx.conf.example)
- **Poweradmin 4.1.x+**: Use [nginx.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example) (includes subfolder deployment support)

Save the configuration to `/etc/nginx/sites-available/poweradmin` and adjust:

- `server_name` - Set to your domain name
- `root` - Set to your Poweradmin installation path
- `fastcgi_pass` - Adjust PHP-FPM socket path to match your installed PHP version (e.g., `unix:/var/run/php/php8.3-fpm.sock` on Ubuntu 24.04, `unix:/var/run/php/php8.2-fpm.sock` on Debian 12)

Then enable the site:

```bash
ln -s /etc/nginx/sites-available/poweradmin /etc/nginx/sites-enabled/
nginx -t  # Test the configuration
systemctl reload nginx
```

### Caddy Configuration

For Caddy servers, use the configuration example from the repository:

- **Poweradmin 4.0.x**: Use [Caddyfile.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/Caddyfile.example)
- **Poweradmin 4.1.x+**: Use [caddy.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) (includes subfolder deployment support)

## Installing Poweradmin

### Obtain Poweradmin Source Code

Download the latest release from the [stable line](https://github.com/poweradmin/poweradmin/releases) (currently the 4.3.x series). Always check the releases page for the most recent version - the example below uses v4.3.4:

```bash
VERSION=4.3.4
wget https://github.com/poweradmin/poweradmin/archive/refs/tags/v${VERSION}.zip
unzip v${VERSION}.zip
```

Or download directly from your browser and transfer the files to your server.

### Deploy to Web Server

Move the Poweradmin files to your web server's document root:

```bash
cp -r poweradmin-${VERSION}/* /var/www/html/
chown -R www-data:www-data /var/www/html/
```

> **Note:** You can safely remove the default index.html (or derivative) if it exists.

## Complete the Installation

1. Visit http://your-server/install/ in your browser
2. Follow the installation steps
3. Once installation is complete, remove the `install` directory for security
4. Log in with the admin username and password created during installation

## Troubleshooting

If you encounter issues:

- Check PHP error logs: `/var/log/apache2/error.log` or `/var/log/nginx/error.log`
- Ensure all required PHP extensions are installed and enabled
- Verify file permissions are set correctly for your web server user
- For API issues, ensure CORS headers and Authorization header forwarding are configured (see the example configs)
