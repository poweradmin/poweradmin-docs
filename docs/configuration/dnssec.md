# DNSSEC Configuration

## Introduction

DNSSEC (Domain Name System Security Extensions) provides authentication and integrity to DNS data. This guide explains how to configure DNSSEC in Poweradmin.

## Basic Concepts

- **Zone Signing Keys (ZSK)**: Used to sign the actual DNS records
- **Key Signing Keys (KSK)**: Used to sign the ZSK and establish trust
- **DS Records**: Delegation Signer records that help establish the trust chain
- **Key Rotation**: Regular update of keys for enhanced security

## Prerequisites

- PowerDNS with DNSSEC support
- Proper database configuration
- API access configured (see [PowerDNS API Configuration](./powerdns-api.md))

## Configuration Options

The DNSSEC settings are configured in the `config/settings.php` file under the `dnssec` section:

- **enabled**: Enable DNSSEC functionality. Default: `false`
- **debug**: Enable DNSSEC debug logging. Default: `false`
- **command**: Path to pdnsutil command. Default: `/usr/bin/pdnsutil`

## Example Configuration

```php
return [
    'dnssec' => [
        'enabled' => true,
        'debug' => false,
        'command' => '/usr/bin/pdnsutil',
    ],
];
```

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

If you encounter issues with DNSSEC:

1. Check that both PowerDNS API and DNSSEC are enabled
2. Verify the pdnsutil command path is correct
3. Check PowerDNS logs for any DNSSEC-related errors
4. Enable debug mode temporarily to get more detailed logs