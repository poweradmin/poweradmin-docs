# Debian Installation

This guide will help you install Poweradmin on Debian systems (Debian 12 or later recommended).

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

### Apache (Default on Debian)

Apache is usually pre-installed and configured on Debian systems. You'll need to:

1. Enable the required Apache modules:

```bash
a2enmod rewrite
```

2. Either place Poweradmin in the default webroot (`/var/www/html/`) or create a virtual host configuration.

### Nginx Configuration

If you prefer Nginx, create a configuration file like this:

```nginx
server {
    listen 80;
    server_name localhost; # Replace with your domain

    root /var/www/html; # Path to Poweradmin files
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Deny access to .htaccess and .htpasswd files for security reasons
    location ~ /\.ht {
        deny all;
    }
}
```

Save this configuration to `/etc/nginx/sites-available/poweradmin` and enable it:

```bash
ln -s /etc/nginx/sites-available/poweradmin /etc/nginx/sites-enabled/
nginx -t  # Test the configuration
systemctl reload nginx
```

## Installing Poweradmin

### Obtain Poweradmin Source Code

Download the latest release (v3.9.3) from [GitHub Releases](https://github.com/poweradmin/poweradmin/releases):

```bash
wget https://github.com/poweradmin/poweradmin/archive/refs/tags/v3.9.3.zip
unzip v3.9.3.zip
```

Or download directly from your browser and transfer the files to your server.

### Deploy to Web Server

Move the Poweradmin files to your web server's document root:

```bash
cp -r poweradmin-3.9.3/* /var/www/html/
chown -R www-data:www-data /var/www/html/
```

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