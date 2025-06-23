# RDAP Configuration

## Overview

RDAP (Registration Data Access Protocol) is the modern replacement for WHOIS. Poweradmin supports RDAP lookups for domain registration information with structured JSON responses and better internationalization support.

## Configuration Options

RDAP settings can be configured in the `config/settings.php` file under the `rdap` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable RDAP lookup functionality |
| `default_server` | `''` | Optional default RDAP server URL (empty to use server from RDAP database) |
| `request_timeout` | `10` | HTTP request timeout in seconds for RDAP queries |
| `restrict_to_admin` | `true` | Only allow administrators (user_is_ueberuser) to use RDAP functionality |

## Configuration Example

```php
return [
    'rdap' => [
        'enabled' => true,
        'default_server' => 'https://rdap.verisign.com/com/v1/',
        'request_timeout' => 15,
        'restrict_to_admin' => true,
    ],
];
```

## RDAP vs WHOIS

| Feature | WHOIS | RDAP |
|---------|-------|------|
| Protocol | Plain text | JSON over HTTPS |
| Security | No encryption | HTTPS encryption |
| Internationalization | Limited | Full Unicode support |
| Machine readable | No | Yes |
| Rate limiting | Basic | Standardized |
| Authentication | None | OAuth2 support |

## Usage

When enabled, RDAP lookups provide:

1. **Structured data** - JSON responses with consistent formatting
2. **Enhanced security** - HTTPS-based queries
3. **Better performance** - HTTP-based protocol with caching support
4. **Internationalization** - Full Unicode domain support

## Supported TLDs

RDAP supports lookups for:

- All major gTLDs (.com, .net, .org, .info, etc.)
- Many ccTLDs with RDAP servers
- New gTLDs with RDAP implementation

## Security Features

- **HTTPS encryption** - All queries use encrypted connections
- **Admin restriction** - Access limited to administrators by default
- **Rate limiting compliance** - Respects RDAP server rate limits
- **Input validation** - Domain names are validated before queries

## Configuration Best Practices

### Production Environment

```php
'rdap' => [
    'enabled' => true,
    'default_server' => '', // Use automatic server detection
    'request_timeout' => 30, // Longer timeout for reliability
    'restrict_to_admin' => true,
],
```

### Development Environment

```php
'rdap' => [
    'enabled' => true,
    'default_server' => 'https://rdap.verisign.com/com/v1/',
    'request_timeout' => 10,
    'restrict_to_admin' => false, // Allow all users for testing
],
```

## RDAP Server Bootstrap

RDAP uses a bootstrap mechanism to determine the correct server for each TLD:

1. **Automatic detection** - Queries IANA bootstrap registry
2. **Cached mappings** - Server mappings are cached for performance
3. **Fallback servers** - Default server used if bootstrap fails

## Troubleshooting

### Common Issues

1. **SSL certificate errors**: Verify RDAP server certificates
2. **Timeout issues**: Increase `request_timeout` value
3. **Access denied**: Check administrator privileges
4. **Server not found**: Verify TLD supports RDAP

### Network Requirements

- Outbound HTTPS connections (port 443)
- DNS resolution for RDAP servers
- Valid SSL/TLS certificates

## Performance Optimization

- **Caching**: RDAP responses can be cached
- **Connection pooling**: Reuse HTTP connections
- **Timeout tuning**: Balance between reliability and performance
- **Error handling**: Graceful fallback to WHOIS if RDAP fails