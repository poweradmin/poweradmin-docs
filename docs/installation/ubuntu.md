# Ubuntu Installation

This guide will help you install Poweradmin on Ubuntu systems.

## Prerequisites

Ensure you have the following PHP extensions installed:

```bash
apt install php php-intl php-php-gettext php-tokenizer php-xml php-fpm
```

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

> **Note:** `php-fpm` is required only if you plan to use Nginx or choose not to use `mod_php` with Apache.

## Web Server Configuration

### Apache (Default on Ubuntu)

Apache is usually pre-installed and configured on Ubuntu systems. You'll need to:

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
- `fastcgi_pass` - Adjust PHP-FPM socket path as needed (e.g., `unix:/var/run/php/php8.2-fpm.sock`)

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

Download the latest release from [GitHub Releases](https://github.com/poweradmin/poweradmin/releases):

```bash
# For latest 4.0.x stable release
wget https://github.com/poweradmin/poweradmin/archive/refs/tags/v4.0.5.zip
unzip v4.0.5.zip
```

Or download directly from your browser and transfer the files to your server.

### Deploy to Web Server

Move the Poweradmin files to your web server's document root:

```bash
cp -r poweradmin-4.0.5/* /var/www/html/
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
