# PowerDNS API Configuration

## Overview

Poweradmin can interact with PowerDNS through its API for advanced operations like DNSSEC management and automatic zone changes. This document explains how to configure the PowerDNS API integration.

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

## Security Considerations

- Always use HTTPS for production environments
- Restrict API access to trusted IP addresses
- Use a strong API key and rotate it regularly
- Consider using a reverse proxy for additional security
- Keep PowerDNS and Poweradmin updated to the latest versions