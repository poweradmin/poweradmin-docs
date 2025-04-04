# PowerDNS API Configuration

## Overview

Poweradmin can interact with PowerDNS through its API for advanced operations like DNSSEC management and automatic zone changes. This document explains how to configure the PowerDNS API integration.

## Prerequisites

- PowerDNS server with API enabled
- API key generated on PowerDNS server
- Network connectivity between Poweradmin and PowerDNS API endpoint

## Configuration Options

The PowerDNS API settings are configured in the `config/settings.php` file under the `pdns_api` section:

- **url**: PowerDNS API URL, e.g., 'http://127.0.0.1:8081'. Default: empty
- **key**: PowerDNS API key. Default: empty

## Example Configuration

```php
return [
    'pdns_api' => [
        'url' => 'http://localhost:8081',
        'key' => 'YOUR_API_KEY',
    ],
];
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