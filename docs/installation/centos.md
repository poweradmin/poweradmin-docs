# CentOS/RHEL Installation

This guide will help you install Poweradmin on RHEL-based distributions like Rocky Linux 9 or AlmaLinux 9. CentOS Stream 9 is also supported provided PHP 8.2 or newer is enabled.

## Prerequisites

### Install PowerDNS

Poweradmin is a frontend for an existing PowerDNS authoritative server - it does not install or run PowerDNS itself. If you do not already have PowerDNS running, install it first and configure a database backend (MySQL/MariaDB, PostgreSQL, or SQLite). See the [PowerDNS installation guide](https://doc.powerdns.com/authoritative/installation.html) for details.

### Enable a PHP 8.2+ Stream

Rocky Linux 9, AlmaLinux 9, and RHEL 9 ship PHP 8.0 by default, which does not meet Poweradmin's PHP 8.2 minimum. Switch to a newer stream before installing PHP packages:

```bash
dnf module reset php -y
dnf module enable php:8.2 -y   # or php:8.3
```

Alternatively, install PHP from the [Remi repository](https://rpms.remirepo.net/) if you need an even newer release.

### Install PHP and Extensions

```bash
dnf install -y php php-cli php-intl php-gettext php-mbstring php-xml php-pdo php-fpm
```

### Database Support

Install the appropriate PHP database driver based on your preferred database:

```bash
# For MySQL/MariaDB
dnf install -y php-mysqlnd

# For PostgreSQL
dnf install -y php-pgsql
```

> **Note:** SQLite support is built into `php-pdo` on RHEL-family distributions - there is no separate `php-sqlite3` package in the default AppStream repositories. If you plan to use SQLite, `php-pdo` alone is sufficient.

## Web Server Configuration

### Apache

**1. Install Apache if not already installed:**

```bash
dnf install -y httpd
```

**2. Enable and start the Apache service:**

```bash
systemctl enable httpd
systemctl start httpd
```

**3. Configure SELinux if it's enabled:**

```bash
# Allow Apache to connect to the database
setsebool -P httpd_can_network_connect_db 1

# If using a non-standard directory, set the correct context
semanage fcontext -a -t httpd_sys_content_t "/path/to/poweradmin(/.*)?"
restorecon -Rv /path/to/poweradmin
```

**4. Configure your firewall:**

```bash
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https  # If using HTTPS
firewall-cmd --reload
```

**5.** Ensure `AllowOverride All` is set in your Apache configuration to allow the `.htaccess` file to function properly. The `.htaccess` file handles URL routing, API support, and security rules automatically.

### Nginx Configuration

If you prefer Nginx, use the configuration example provided in the Poweradmin repository. The configuration includes API routing, CORS support, security rules, and clean URL handling.

**1. Install Nginx:**

```bash
dnf install -y nginx
```

**2.** Download the appropriate configuration file:

**Version-specific configuration files:**

- **Poweradmin 4.0.x**: Use [nginx.conf.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/nginx.conf.example)
- **Poweradmin 4.1.x+**: Use [nginx.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example) (includes subfolder deployment support)

**3.** Save the configuration to `/etc/nginx/conf.d/poweradmin.conf` and adjust:

- `server_name` - Set to your domain name
- `root` - Set to your Poweradmin installation path
- `fastcgi_pass` - Use `unix:/var/run/php-fpm/www.sock` for RHEL/CentOS

**4. Enable and start Nginx and PHP-FPM:**

```bash
systemctl enable nginx php-fpm
systemctl start nginx php-fpm
```

**5.** Configure SELinux and firewall as with Apache.

### Caddy Configuration

For Caddy servers, use the configuration example from the repository:

- **Poweradmin 4.0.x**: Use [Caddyfile.example from release/4.0.x](https://github.com/poweradmin/poweradmin/blob/release/4.0.x/Caddyfile.example)
- **Poweradmin 4.1.x+**: Use [caddy.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) (includes subfolder deployment support)

## Installing Poweradmin

### Obtain Poweradmin Source Code

Download the latest release from the [stable line](https://github.com/poweradmin/poweradmin/releases) (currently the 4.2.x series). Always check the releases page for the most recent version - the example below uses v4.2.3:

```bash
VERSION=4.2.3
curl -Lo v${VERSION}.zip https://github.com/poweradmin/poweradmin/archive/refs/tags/v${VERSION}.zip
unzip v${VERSION}.zip
```

If you don't have curl or unzip installed:

```bash
dnf install -y curl unzip
```

### Deploy to Web Server

Move the Poweradmin files to your web server's document root:

```bash
# For Apache (default directory)
cp -r poweradmin-${VERSION}/* /var/www/html/
chown -R apache:apache /var/www/html/

# For Nginx (if using a different directory)
cp -r poweradmin-${VERSION}/* /usr/share/nginx/html/
chown -R nginx:nginx /usr/share/nginx/html/
```

## Complete the Installation

1. Visit http://your-server/install/ in your browser
2. Follow the installation steps
3. Once installation is complete, remove the `install` directory for security
4. Log in with the admin username and password created during installation

## Troubleshooting

If you encounter issues:

- Check PHP error logs: `/var/log/php-fpm/www-error.log`
- Check web server logs: `/var/log/httpd/error_log` or `/var/log/nginx/error.log`
- Ensure SELinux permissions are properly set if SELinux is enabled
- Verify all required PHP extensions are installed and enabled
- Check that file permissions are correct for your web server user
- For API issues, ensure CORS headers and Authorization header forwarding are configured (see the example configs)
