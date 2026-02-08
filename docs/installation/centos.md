# CentOS/RHEL Installation

This guide will help you install Poweradmin on CentOS, RHEL, and other RHEL-based distributions like Rocky Linux or AlmaLinux.

## Prerequisites

Ensure you have the following PHP extensions installed:

```bash
dnf install -y php php-intl php-gettext php-pdo php-xml php-fpm
```

### Database Support

Install the appropriate PHP database driver based on your preferred database:

```bash
# For MySQL/MariaDB
dnf install -y php-mysqlnd

# For PostgreSQL
dnf install -y php-pgsql

# For SQLite (if available in your repositories)
dnf install -y php-sqlite3
```

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

- **Poweradmin 4.0.x**: Use [nginx.conf.example from release/4.x](https://github.com/poweradmin/poweradmin/blob/release/4.x/nginx.conf.example)
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

- **Poweradmin 4.0.x**: Use [Caddyfile.example from release/4.x](https://github.com/poweradmin/poweradmin/blob/release/4.x/Caddyfile.example)
- **Poweradmin 4.1.x+**: Use [caddy.conf.example from master](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) (includes subfolder deployment support)

## Installing Poweradmin

### Obtain Poweradmin Source Code

Download the latest release from [GitHub Releases](https://github.com/poweradmin/poweradmin/releases):

```bash
# For latest 4.0.x stable release
curl -Lo v4.0.5.zip https://github.com/poweradmin/poweradmin/archive/refs/tags/v4.0.5.zip
unzip v4.0.5.zip
```

If you don't have curl or unzip installed:

```bash
dnf install -y curl unzip
```

### Deploy to Web Server

Move the Poweradmin files to your web server's document root:

```bash
# For Apache (default directory)
cp -r poweradmin-4.0.5/* /var/www/html/
chown -R apache:apache /var/www/html/

# For Nginx (if using a different directory)
cp -r poweradmin-4.0.5/* /usr/share/nginx/html/
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
