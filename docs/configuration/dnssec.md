# DNSSEC Configuration

## Overview

Poweradmin provides comprehensive support for DNSSEC (Domain Name System Security Extensions) through a well-structured implementation that follows domain-driven design principles. The system offers two implementation methods:

1. **PowerDNS API Integration** (Recommended): Uses the PowerDNS REST API for DNSSEC operations
2. **pdnsutil Command-line Tool** (Legacy): Uses the pdnsutil command-line utility 

The DNSSEC implementation enables you to:
- Secure and unsecure zones
- Manage cryptographic keys (create, activate, deactivate, delete)
- View DS (Delegation Signer) and DNSKEY records
- Manage DNSSEC key rollovers

## Basic Concepts

- **Zone Signing Keys (ZSK)**: Used to sign the actual DNS records
- **Key Signing Keys (KSK)**: Used to sign the ZSK and establish trust
- **DS Records**: Delegation Signer records that help establish the trust chain
- **Key Rotation**: Regular update of keys for enhanced security

## Prerequisites

- PowerDNS version 4.0.0 or higher
- PowerDNS with DNSSEC support
- Proper database configuration
- API access configured (see [PowerDNS API Configuration](./powerdns-api.md))

## Configuration Options

DNSSEC settings can be configured in the `config/settings.php` file under the `dnssec` section or through individual variables in the legacy configuration format.

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $pdnssec_use | dnssec.enabled | false | Enable (true) or disable (false) DNSSEC support | 2.1.7 |
| $pdnssec_debug | dnssec.debug | false | Enable debug for DNSSEC operations | 2.1.9 |
| $pdnssec_command | dnssec.command | /usr/bin/pdnsutil | Full path to pdnsutil utility (will be deprecated in the future) | 2.1.7 |

## Implementation Methods

### Option 1: PowerDNS API Method (Recommended)

To enable DNSSEC using the PowerDNS API:

1. Configure your PowerDNS server with API access
2. Update your Poweradmin configuration file with the following settings:

```php
return [
    'dnssec' => [
        'enabled' => true,
        'debug' => false,
    ],
    'pdns_api' => [
        'url' => 'http://localhost:8081',
        'key' => 'your-api-key',
    ],
];
```

The API method provides several advantages:
- No need to configure special permissions for the web server user
- More secure as it doesn't require shell access
- Better error handling and feedback
- Full support for all DNSSEC operations

### Option 2: pdnsutil Method (Legacy)

If you can't use the API method, you can still use the legacy pdnsutil approach:

```php
return [
    'dnssec' => [
        'enabled' => true,
        'debug' => false,
        'command' => '/usr/bin/pdnsutil',
    ],
    'pdns_api' => [
        'url' => '',
        'key' => '',
    ],
];
```

Configure permissions for the web server user to run pdnsutil:

For example, on Ubuntu with Apache:
```bash
# Add the web server user to the root group
adduser www-data root

# Make pdns.conf readable by the web server user
chmod 640 /etc/powerdns/pdns.conf
```

**Important Note**: The pdnsutil method requires the web server user to have access to the PowerDNS configuration file, which poses security risks. The API method is strongly recommended.

## PowerDNS Configuration

Make sure to enable DNSSEC in your PowerDNS configuration:

```conf
dnssec=yes
api=yes
api-key=your_api_key
```

## Verification

Check DNSSEC status using:

```bash
dig +dnssec example.com SOA
```

## Troubleshooting

Common issues:

1. **API connection problems**: Ensure the API URL is correct and the API key has the necessary permissions

2. **pdnsutil permission errors**: Check that the web server user can access pdns.conf and has permission to execute pdnsutil

3. **DNSSEC operations failing**: Check the PowerDNS logs for detailed error messages

4. Check that both PowerDNS API and DNSSEC are enabled

5. Verify the pdnsutil command path is correct

6. Enable debug mode temporarily to get more detailed logs

## Migration

If you're currently using the pdnsutil method, it's recommended to migrate to the API method:

1. Configure the PowerDNS API (see PowerDNS documentation)
2. Update your Poweradmin configuration with API settings
3. No data migration is needed - the same DNSSEC keys will be accessible through both methods

## More Information

For more details on DNSSEC and PowerDNS:
- [PowerDNS DNSSEC Documentation](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [PowerDNS API Documentation](https://doc.powerdns.com/authoritative/http-api/index.html)