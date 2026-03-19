# PowerDNS API Configuration

## Overview

Poweradmin can interact with PowerDNS through its REST API in two ways:

1. **Supplementary mode** (default): The API enhances a traditional SQL-based setup with DNSSEC management, zone transfers, and metadata access. Poweradmin still queries the PowerDNS database directly for zone and record operations.

2. **API backend mode** (v4.3.0+): The API is the sole communication channel with PowerDNS. Poweradmin does not need access to the PowerDNS database at all. This is ideal for cloud-hosted PowerDNS, network-restricted environments, or API-first architectures.

This document explains how to configure both modes.

## Prerequisites

- PowerDNS server with API enabled
- API key generated on PowerDNS server
- Network connectivity between Poweradmin and PowerDNS API endpoint

## Configuration Options

PowerDNS API settings can be configured in the `config/settings.php` file under the `pdns_api` section or through individual variables in the legacy configuration format.

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $pdns_api_url | pdns_api.url | no default | The endpoint for establishing a connection to the PowerDNS API | 3.7.0 |
| $pdns_api_key | pdns_api.key | no default | The authentication key required for establishing a connection with the PowerDNS API | 3.7.0 |
| - | pdns_api.display_name | PowerDNS | PowerDNS name to identify server in the interface | 4.0.0 |
| - | pdns_api.server_name | localhost | PowerDNS server name used in API calls | 4.0.0 |
| - | dns.backend | sql | Backend mode: `sql` (database) or `api` (API only) | 4.3.0 |

## Modern Configuration Example

```php
return [
    'pdns_api' => [
        'display_name' => 'Production PowerDNS',
        'url' => 'http://localhost:8081',
        'key' => 'YOUR_API_KEY',
        'server_name' => 'localhost',
    ],
];
```

## Legacy Configuration Example

```php
<?php
// PowerDNS API settings
$pdns_api_url = 'http://localhost:8081';
$pdns_api_key = 'YOUR_API_KEY';
```

## PowerDNS Server Setup

To enable the API in your PowerDNS configuration, add the following to your PowerDNS configuration file:

```conf
# Enable API and webserver
api=yes
api-key=YOUR_API_KEY
webserver=yes
webserver-port=8081
webserver-address=127.0.0.1  # Restrict to localhost for security
```

For production environments, it's recommended to secure the API with HTTPS:

```conf
webserver-port=8081
webserver-address=0.0.0.0
webserver-allow-from=192.168.0.0/24,127.0.0.1
webserver-password=YOUR_PASSWORD
webserver-loglevel=none
```

## Testing Connection

You can verify the API connection by running:

```bash
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8081/api/v1/servers/localhost
```

If the connection is successful, you should receive a JSON response with server information.

## Functionality Enabled by API

With the PowerDNS API properly configured, Poweradmin gains the following capabilities:

- DNSSEC management (key creation, rotation, DS record handling)
- Real-time zone transfers
- Metadata management
- Direct server statistics access

## API Backend Mode (v4.3.0+)

API backend mode eliminates the need for Poweradmin to access the PowerDNS database. All DNS operations go through the PowerDNS REST API.

### When to Use API Backend Mode

- PowerDNS database is not accessible from the Poweradmin server
- Running PowerDNS as a managed/cloud service
- Network policies prevent direct database access
- You prefer API-first integration

### Configuration

Set `dns.backend` to `api` in your `config/settings.php`:

```php
return [
    'dns' => [
        'backend' => 'api',
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
    ],

    'pdns_api' => [
        'url' => 'http://powerdns-server:8081',
        'key' => 'YOUR_API_KEY',
        'server_name' => 'localhost',
    ],

    // Poweradmin's own database (still required)
    'db_host' => 'localhost',
    'db_port' => 3306,
    'db_user' => 'poweradmin',
    'db_pass' => 'password',
    'db_name' => 'poweradmin',
    'db_type' => 'mysql',

    // PowerDNS database settings are NOT needed in API mode
];
```

### New Installation with API Backend

The installer (Step 4) offers a choice between "Database" and "API" backend. Selecting API will:

- Prompt for the PowerDNS API URL and key
- Skip PowerDNS database configuration
- Set `dns.backend` to `api` in the generated configuration

### Migrating from SQL to API Backend

1. Ensure the PowerDNS API is enabled and accessible
2. Run the v4.3.0 database migration (adds required columns to `zones` table)
3. Change `dns.backend` from `sql` to `api` in `config/settings.php`
4. Add `pdns_api` settings if not already configured
5. Load any page - the zone sync service automatically populates cached zone metadata

All existing zone ownership, group assignments, and permissions are preserved. The migration is reversible by changing `dns.backend` back to `sql`.

### Zone Sync Service

In API backend mode, a sync service keeps the local `zones` table in sync with PowerDNS:

- **Automatic**: Runs on zone list page loads, throttled to once per 5 minutes per session
- **Adds** zones created directly in PowerDNS (assigned no owner - admin must assign access)
- **Removes** local entries for zones deleted from PowerDNS
- **Updates** cached zone type and master when changed

### Docker

For Docker deployments, set the backend via environment variable:

```yaml
environment:
  PA_DNS_BACKEND: api
  PA_PDNS_API_URL: http://powerdns:8081
  PA_PDNS_API_KEY: your-api-key
```

## Security Considerations

- Always use HTTPS for production environments
- Restrict API access to trusted IP addresses
- Use a strong API key and rotate it regularly
- Consider using a reverse proxy for additional security
- Keep PowerDNS and Poweradmin updated to the latest versions
- In API backend mode, the API key grants full control over PowerDNS - protect it accordingly