# Dynamic DNS Overview

## Requirements

Before setting up Dynamic DNS, ensure you have:

- PowerDNS server with Poweradmin interface
- User account with appropriate permissions
- One of the following clients:
  - Bash shell environment
  - Python 3.x with requests module
  - Perl with LWP::UserAgent module

## Features

- IPv4 and IPv6 support (dual-stack)
- Multiple IP management capabilities:
  - Support for comma-separated IP lists
  - Simultaneous management of multiple A/AAAA records
  - Selective record type updating
- Intelligent record synchronization:
  - Automatic cleanup of outdated records
  - Database and DNS zone consistency maintenance
  - Optional full sync with dual-stack support
- Automatic SOA serial updates
- Support for both Basic HTTP Authentication and query parameters
- TTL management (default 60 seconds)
- Verbose response mode for debugging
- Backward compatibility with legacy clients

## Available Scripts

### Backend Components

- `dynamic_update.php` - Main server-side script for processing DNS updates, supporting:
  - Single or multiple IPv4/IPv6 addresses
  - Automatic IP detection using 'whatismyip'
  - Comma-separated IP lists
  - Dual-stack updates
- `addons/clientip.php` - Server-side script that provides the client's public IP address

### Client Tools

Official client scripts:
- `addons/dynamic_dns_client.sh` - Bash client script for updating IP addresses
- `addons/dynamic_dns_client.py` - Python client script for updating IP addresses
- `addons/dynamic_dns_client.pl` - Perl client script for updating IP addresses

You can also use cURL or any HTTP client to update DNS records. See the [Using cURL](using-curl.md) guide for examples and best practices.

## Security Features

- Basic HTTP Authentication
- Permission-based access control
- User activity validation
- IP address validation
- Domain ownership verification

For detailed configuration steps, see the [Configuration](configuration.md) section.


