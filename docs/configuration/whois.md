# WHOIS Configuration

## Overview

Poweradmin includes WHOIS lookup functionality that allows administrators to query domain registration information directly from the interface. This feature helps with domain management and verification tasks.

## Configuration Options

WHOIS settings can be configured in the `config/settings.php` file under the `whois` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable WHOIS lookup functionality |
| `default_server` | `''` | Optional default WHOIS server (empty to use server from WHOIS database) |
| `socket_timeout` | `10` | Socket timeout in seconds for WHOIS queries |
| `restrict_to_admin` | `true` | Only allow administrators (user_is_ueberuser) to use WHOIS functionality |

## Configuration Example

```php
return [
    'whois' => [
        'enabled' => true,
        'default_server' => 'whois.internic.net',
        'socket_timeout' => 15,
        'restrict_to_admin' => true,
    ],
];
```

## Usage

When enabled, WHOIS lookups can be performed from:

1. **Zone management pages** - Lookup domain registration information
2. **Domain search results** - Quick WHOIS lookup for search results
3. **Administrative tools** - Bulk domain verification

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

## Troubleshooting

### Common Issues

1. **Connection timeouts**: Increase `socket_timeout` value
2. **Access denied**: Verify user has administrator privileges
3. **No results**: Check if domain exists and WHOIS server is correct

### Network Requirements

- Outbound connections on port 43 (WHOIS protocol)
- DNS resolution for WHOIS servers
- Firewall rules allowing WHOIS traffic

## Performance Considerations

- WHOIS queries are network-dependent and may be slow
- Consider caching results for frequently queried domains
- Set appropriate timeout values to prevent interface blocking