# Remote Poweradmin Setup Guide

This guide details how to set up Poweradmin on a separate server from your PowerDNS installation, allowing you to
maintain a dedicated admin interface without needing to install PowerDNS on the same machine.

## Prerequisites

- A server for Poweradmin (referred to as "admin server")
- A server running PowerDNS (referred to as "DNS server")
- MySQL/MariaDB, PostgreSQL, or SQLite database access from the admin server to the PowerDNS database
- Network connectivity between both servers
- PHP 7.4+ with required extensions on the admin server
- Web server software (Apache, Nginx, etc.) on the admin server

## Architecture Overview

In a remote setup:

1. Poweradmin is installed on the admin server
2. PowerDNS runs on the DNS server
3. Poweradmin connects to the PowerDNS database remotely
4. For DNSSEC operations, Poweradmin uses the PowerDNS API

```
┌────────────────┐        ┌────────────────┐
│                │        │                │
│  Admin Server  │        │   DNS Server   │
│                │        │                │
│  ┌──────────┐  │        │  ┌──────────┐  │
│  │Poweradmin│  │◄──────►│  │ PowerDNS │  │
│  └──────────┘  │  API   │  └──────────┘  │
│                │        │                │
└───────┬────────┘        └───────┬────────┘
        │                         │
        │    ┌──────────────┐     │
        └───►│ PowerDNS DB  │◄────┘
             └──────────────┘
```

## Step 1: Install Poweradmin on the Admin Server

1. Clone or download Poweradmin:

```bash
git clone https://github.com/poweradmin/poweradmin.git
cd poweradmin
```

2. Install dependencies:

```bash
composer install --no-dev
```

3. Configure your web server to serve Poweradmin (directory configuration examples for Apache/Nginx not shown here).

## Step 2: Configure Database Connection

1. Create a database user on your PowerDNS database server with appropriate permissions:

```sql
-- For MySQL/MariaDB (execute on DNS server's database)
CREATE
USER 'poweradmin'@'admin_server_ip' IDENTIFIED BY 'secure_password';
GRANT
SELECT,
INSERT
,
UPDATE,
DELETE
ON powerdns.* TO 'poweradmin'@'admin_server_ip';
FLUSH
PRIVILEGES;
```

2. Configure Poweradmin to connect to the remote database:
    - Copy `config/settings.defaults.php` to `config/settings.php`
    - Edit the database connection settings:

```php
'database' => [
    'host' => 'dns_server_ip',  // IP address of your PowerDNS server
    'port' => '3306',           // Database port (MySQL default: 3306, PostgreSQL: 5432)
    'user' => 'poweradmin',     // The database user created in step 1
    'password' => 'secure_password',
    'name' => 'powerdns',       // The PowerDNS database name
    'type' => 'mysql',          // mysql, pgsql, or sqlite
],
```

## Step 3: Configure PowerDNS API Access

For DNSSEC management and certain operations, Poweradmin requires access to the PowerDNS API:

1. Enable the API on your PowerDNS server by editing `/etc/powerdns/pdns.conf`:
```
api=yes
api-key=your_secure_api_key
webserver=yes
webserver-address=0.0.0.0  # Or restrict to admin_server_ip
webserver-port=8081
webserver-allow-from=admin_server_ip/32
```

2. Configure Poweradmin to use the API by editing your `settings.php`:

```php
'pdns_api' => [
    'url' => 'http://dns_server_ip:8081',  // PowerDNS API URL
    'key' => 'your_secure_api_key',        // PowerDNS API key
],
```

## Step 4: Configure DNSSEC (Optional)

If you're using DNSSEC, enable it in your settings:

```php
'dnssec' => [
    'enabled' => true,
    'debug' => false,  // Set to true for troubleshooting
],
```

Note: The PowerDNS API method is strongly recommended over the legacy pdnsutil method. When configured with the API
settings above, Poweradmin will automatically use the API for DNSSEC operations.

## Step 5: Network Security Considerations

Since you're running Poweradmin on a separate server:

1. PowerDNS Server Configuration:
    - Edit your PowerDNS configuration to allow external connections:

```conf
# In /etc/powerdns/pdns.conf
webserver-address=0.0.0.0  # Allow connections from any IP (consider restricting to admin_server_ip)
webserver-allow-from=admin_server_ip/32  # Replace with your admin server's IP
```

- By default, PowerDNS API only binds to localhost (127.0.0.1), so this change is necessary

2. Firewall Configuration:
    - Allow connections from the admin server to the DNS server on:
        - Database port (MySQL: 3306, PostgreSQL: 5432)
        - PowerDNS API port (typically 8081)
    - Consider using SSH tunneling or VPN for additional security
    - Example with UFW (Ubuntu):

```bash
# On PowerDNS server
sudo ufw allow from admin_server_ip to any port 8081 proto tcp
sudo ufw allow from admin_server_ip to any port 3306 proto tcp
```

3. TLS/SSL:
    - Consider using SSL/TLS for database connections
    - Use HTTPS for Poweradmin's web interface
    - Consider using HTTPS for the PowerDNS API

## Step 6: Test the Connection

1. Complete the Poweradmin installation wizard if running for the first time
2. Log in to Poweradmin
3. Verify you can view and modify zones
4. Test DNSSEC operations if enabled

## Security Best Practices

1. Use a dedicated database user with minimum required permissions
2. Implement IP restrictions for database and API access
3. Use strong, unique passwords for all components
4. Keep both Poweradmin and PowerDNS updated to the latest versions
5. Regularly audit access logs on both servers
