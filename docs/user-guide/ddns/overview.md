# Dynamic DNS Overview

Dynamic DNS (DDNS) allows you to automatically update DNS records when your IP address changes. This is essential for:

- Hosting services on connections with dynamic IP addresses
- Maintaining DNS records for home servers or networks
- Providing consistent domain name access to systems with changing IP addresses
- Enabling remote access to home networks or IoT devices

Poweradmin's Dynamic DNS implementation offers a flexible API that can be integrated with various automation tools and scripts to keep DNS records up to date. It supports both IPv4 and IPv6 addresses through various update methods.

## Requirements

Before setting up Dynamic DNS, ensure you have:

- PowerDNS server with Poweradmin interface
- User account with appropriate permissions
- One of the following clients:
    - Bash shell environment
    - Python 3.x with requests module
    - Perl with LWP::UserAgent module
    - cURL or any HTTP client tool

## Features

- **IPv4 and IPv6 support** (dual-stack)
- **Multiple IP management**:
    - Support for comma-separated IP lists
    - Simultaneous management of multiple A/AAAA records
    - Selective record type updating
- **Intelligent record synchronization**:
    - Automatic cleanup of outdated records
    - Database and DNS zone consistency maintenance
    - Optional full sync with dual-stack support
- **Automatic SOA serial updates**
- **Flexible authentication** (Basic HTTP Authentication and query parameters)
- **TTL management** (default 60 seconds)
- **Debugging support** with verbose response mode
- **Backward compatibility** with legacy clients

## Implementation Components

### Endpoints

Two server endpoints accept dynamic updates:

- **`/dynamic_update.php`** - dyndns2-compatible endpoint authenticated with the user's Poweradmin username and password (HTTP Basic Auth or query parameters). Designed for stock clients like `ddclient` and `inadyn`. See [Client Setup](client-setup.md).
- **`POST /api/v2/dynamic-dns`** - JSON / form-encoded endpoint authenticated with an API key (`X-API-Key` header). Returns the result as a structured JSON document. Recommended for any client you control or any automation where storing a Poweradmin login password would be undesirable. Request body:

    ```json
    {
      "hostname": "host.example.com",
      "ipv4": "192.0.2.1",
      "ipv6": "2001:db8::1",
      "dualstack": false
    }
    ```

    Successful response:

    ```json
    {
      "success": true,
      "message": "Dynamic DNS record updated",
      "data": {
        "hostname": "host.example.com",
        "zone_id": 3,
        "applied_ipv4": ["192.0.2.1"],
        "applied_ipv6": [],
        "changed": true
      }
    }
    ```

    The API endpoint enforces the same DDNS permission gate as `dynamic_update.php` (dedicated user with `zone_content_edit_own` or `zone_content_edit_own_as_client`). Administrator API keys are rejected with `403`.

### Server-Side Components

- `dynamic_update.php` - Main script for processing DNS updates, supporting:
    - Single or multiple IPv4/IPv6 addresses
    - Automatic IP detection using 'whatismyip'
    - Comma-separated IP lists
    - Dual-stack updates
- `addons/clientip.php` - Script that provides the client's public IP address

### Client-Side Tools

Official client scripts:

- `addons/dynamic_dns_client.sh` - Bash client script
- `addons/dynamic_dns_client.py` - Python client script
- `addons/dynamic_dns_client.pl` - Perl client script

You can also use cURL or any HTTP client to update DNS records. See the [Using cURL](using-curl.md) guide for examples.

## Security Features

- Basic HTTP Authentication
- Permission-based access control
- User activity validation
- IP address validation
- Domain ownership verification

## Getting Started

To set up and use Dynamic DNS with Poweradmin:

1. [Configure Dynamic DNS](configuration.md) - Set up user permissions and DNS zones
2. [Set up clients](client-setup.md) - Configure update clients on your devices
3. [Using cURL](using-curl.md) - For manual updates or custom implementations

