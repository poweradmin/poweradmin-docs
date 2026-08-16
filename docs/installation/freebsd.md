# FreeBSD Installation

This guide will help you install Poweradmin on FreeBSD. FreeBSD 14.4 and the 15.x series are the recommended targets, using PHP 8.4 from the ports tree.

> **Note:** This guide is not tested by the maintainer on every release and may only work with help from the community. Corrections are welcome.

## Prerequisites

### Install PowerDNS

Poweradmin is a frontend for an existing PowerDNS authoritative server - it does not install or run PowerDNS itself. If you do not already have PowerDNS running, install it first and configure a database backend (MySQL/MariaDB, PostgreSQL, or SQLite). The `powerdns` package provides it, and its service is enabled with `sysrc pdns_enable=YES`. See the [PowerDNS installation guide](https://doc.powerdns.com/authoritative/installation.html) for details.

### Install PHP and Extensions

FreeBSD has no `php` meta-package - install a versioned package explicitly. PHP 8.4 is the current ports default:

```bash
pkg install php84 php84-intl php84-gettext php84-pdo
```

Then create a `php.ini`, which the package does not install for you:

```bash
cp /usr/local/etc/php.ini-production /usr/local/etc/php.ini
```

> **Note:** `openssl` is compiled into the `php84` package itself and has no separate port, unlike older PHP versions. Confirm it is present with `php -m | grep openssl`.

> **Note:** `lang/php82` is deprecated and is scheduled for removal from the ports tree on 2026-12-31. Use `php84` (or `php83`/`php85`, substituting the version throughout this guide) rather than installing PHP 8.2 on a new system.

### Database Support

Install the appropriate PHP database driver based on your preferred database:

```bash
# For MySQL/MariaDB
pkg install php84-pdo_mysql

# For PostgreSQL
pkg install php84-pdo_pgsql

# For SQLite
pkg install php84-pdo_sqlite
```

## Web Server Configuration

Poweradmin's files live under `/usr/local/www/` on FreeBSD, and the web server runs as the `www` user and group. Web server configuration lives under `/usr/local/etc/`, not `/etc/`.

### Apache

Install Apache and the PHP module:

```bash
pkg install apache24 mod_php84
```

Then:

1. Tell Apache to hand PHP files to the module by adding this to `/usr/local/etc/apache24/httpd.conf`:

    ```apache
    <FilesMatch "\.php$">
        SetHandler application/x-httpd-php
    </FilesMatch>
    <FilesMatch "\.phps$">
        SetHandler application/x-httpd-php-source
    </FilesMatch>
    ```

2. Ensure `mod_rewrite` and `mod_headers` are enabled in `httpd.conf` - Poweradmin requires URL rewriting.

3. Ensure `AllowOverride All` is set for your document root so the `.htaccess` file functions properly.

4. Enable and start Apache:

    ```bash
    sysrc apache24_enable=YES
    service apache24 start
    ```

The `.htaccess` file included with Poweradmin handles URL routing, API support, and security rules automatically.

### Nginx Configuration

If you prefer Nginx, install it along with PHP-FPM, which ships inside the `php84` package rather than as a separate port:

```bash
pkg install nginx
sysrc php_fpm_enable=YES
sysrc nginx_enable=YES
service php_fpm start
service nginx start
```

Use the configuration example provided in the Poweradmin repository. The configuration includes API routing, CORS support, security rules, and clean URL handling.

**Version-specific configuration files:**

- **Poweradmin 4.0.x**: Use [nginx.conf.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/nginx.conf.example)
- **Poweradmin 4.1.x+**: Use [nginx.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example) (includes subfolder deployment support)

Save the configuration under `/usr/local/etc/nginx/` and adjust:

- `server_name` - Set to your domain name
- `root` - Set to your Poweradmin installation path, for example `/usr/local/www/poweradmin`
- `fastcgi_pass` - The example ships the Debian socket path `unix:/var/run/php/php8.2-fpm.sock`, which does not exist on FreeBSD. PHP-FPM listens on `127.0.0.1:9000` by default here, so use `fastcgi_pass 127.0.0.1:9000;` or change `listen` in `/usr/local/etc/php-fpm.d/www.conf` to a socket path and point `fastcgi_pass` at it.

The PHP-FPM pool's `user` and `group` in `/usr/local/etc/php-fpm.d/www.conf` should match the web server user, `www`.

Then test and reload:

```bash
nginx -t
service nginx reload
```

### Caddy Configuration

For Caddy servers, install the package and use the configuration example from the repository:

```bash
pkg install caddy
```

- **Poweradmin 4.0.x**: Use [Caddyfile.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/Caddyfile.example)
- **Poweradmin 4.1.x+**: Use [caddy.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) (includes subfolder deployment support)

Save it as `/usr/local/etc/caddy/Caddyfile`. As with Nginx, the example's `php_fastcgi unix//run/php/php-fpm.sock` and `root * /srv/www` are Linux paths - point them at `127.0.0.1:9000` and your FreeBSD web root instead.

## Installing Poweradmin

### Obtain Poweradmin Source Code

Download the latest release from the [stable line](https://github.com/poweradmin/poweradmin/releases) (currently the 4.3.x series). Always check the releases page for the most recent version - the example below uses v4.3.4. `fetch` is in the base system, but `unzip` is not:

```bash
pkg install unzip
VERSION=4.3.4
fetch https://github.com/poweradmin/poweradmin/archive/refs/tags/v${VERSION}.zip
unzip v${VERSION}.zip
```

Or download directly from your browser and transfer the files to your server.

### Deploy to Web Server

Move the Poweradmin files into the web root and give them to the web server user:

```bash
mkdir -p /usr/local/www/poweradmin
cp -r poweradmin-${VERSION}/* /usr/local/www/poweradmin/
chown -R www:www /usr/local/www/poweradmin
```

Point your virtual host's document root at `/usr/local/www/poweradmin`.

## Complete the Installation

1. Visit http://your-server/install/ in your browser
2. Follow the installation steps
3. Once installation is complete, remove the `install` directory for security
4. Log in with the admin username and password created during installation

## Troubleshooting

If you encounter issues:

- Check the web server error log - the path set by `ErrorLog` in `/usr/local/etc/apache24/httpd.conf`, or `/var/log/nginx/error.log` for Nginx
- Confirm PHP loaded the extensions it needs with `php -m`, and that `/usr/local/etc/php.ini` exists
- If PHP files download instead of executing, the handler configuration or `fastcgi_pass` target is wrong
- Verify file ownership is `www:www` under `/usr/local/www/poweradmin`
- For API issues, ensure CORS headers and Authorization header forwarding are configured (see the example configs)
