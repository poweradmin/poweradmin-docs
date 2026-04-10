# WHOIS Configuration

## Overview

Poweradmin includes WHOIS lookup functionality that allows administrators to query domain registration information directly from the interface. This feature helps with domain management and verification tasks.

## Configuration Options

WHOIS settings can be configured in the `config/settings.php` file under the `whois` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable WHOIS lookup functionality |
| `default_server` | `''` | Optional default WHOIS server (empty to use server from WHOIS database) |
| `custom_servers` | `[]` | Custom TLD-to-server mapping for TLDs not in the built-in database |
| `socket_timeout` | `10` | Socket timeout in seconds for WHOIS queries |
| `restrict_to_admin` | `true` | Only allow administrators (user_is_ueberuser) to use WHOIS functionality |

## Configuration Example

```php
return [
    'whois' => [
        'enabled' => true,
        'default_server' => '',
        'custom_servers' => [
            'za' => 'whois.registry.net.za',
            'co.za' => 'whois.registry.net.za',
        ],
        'socket_timeout' => 15,
        'restrict_to_admin' => true,
    ],
];
```

### Custom Server Mapping

The `custom_servers` option allows you to define WHOIS servers for specific TLDs that may not be in the built-in database. Custom servers take priority over the built-in server list.

```php
'custom_servers' => [
    'za' => 'whois.registry.net.za',    // South Africa
    'co.za' => 'whois.registry.net.za', // South African SLD
],
```

**Docker environment variable:**

```
PA_MODULE_WHOIS_CUSTOM_SERVERS=za=whois.registry.net.za,co.za=whois.registry.net.za
```

**Lookup priority:**

1. Custom servers (from `custom_servers` config)
2. Built-in WHOIS server database
3. `default_server` (global fallback, if set)

## Usage

When enabled, WHOIS lookups can be performed from:

1. **Zone management pages** - Lookup domain registration information
2. **Domain search results** - Quick WHOIS lookup for search results
3. **Administrative tools** - Bulk domain verification

### How to Use WHOIS Lookup

1. Navigate to any zone in Poweradmin
2. Click the **WHOIS** button or icon next to the domain name
3. View the registration information returned by the WHOIS server

### WHOIS Information Displayed

The WHOIS lookup returns information including:

- **Registrar**: The domain registrar
- **Registration dates**: Created, updated, expiration dates
- **Name servers**: Configured DNS servers
- **Registrant info**: Contact information (if not privacy-protected)
- **Status**: Domain status codes (e.g., clientTransferProhibited)

### When to Use WHOIS vs RDAP

| Feature | WHOIS | RDAP |
|---------|-------|------|
| Protocol | Legacy text-based | Modern JSON/REST |
| Format | Unstructured text | Structured JSON |
| Internationalization | Limited | Full Unicode support |
| Use case | Quick lookups | Programmatic access |

For structured data and better internationalization support, consider using [RDAP](rdap.md) instead.

## Supported TLDs

The WHOIS functionality supports lookups for:

- Generic TLDs (.com, .net, .org, etc.)
- Country code TLDs (.uk, .de, .jp, etc.)
- New gTLDs (.xyz, .tech, .app, etc.)

## Security Considerations

- **Admin restriction**: By default, only users with administrator privileges can use WHOIS functionality
- **Rate limiting**: Consider implementing rate limiting for WHOIS queries to prevent abuse
- **Timeout settings**: Adjust socket timeout based on your network conditions
- **Logging**: WHOIS queries may be logged depending on your logging configuration

## Performance Considerations

- WHOIS queries are network-dependent and may be slow
- Consider caching results for frequently queried domains
- Set appropriate timeout values to prevent interface blocking