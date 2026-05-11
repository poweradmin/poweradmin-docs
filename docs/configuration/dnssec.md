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

## Migration

If you're currently using the pdnsutil method, it's recommended to migrate to the API method:

1. Configure the PowerDNS API (see PowerDNS documentation)
2. Update your Poweradmin configuration with API settings
3. No data migration is needed - the same DNSSEC keys will be accessible through both methods

## Importing and Exporting PEM Keys

PowerDNS 4.7 and newer expose endpoints for importing PEM-encoded private keys into a zone and exporting the active ones back out. Poweradmin wires both into the zone's DNSSEC page so you can move signed zones between servers without dropping out to `pdnsutil`.

The buttons only appear when the connected PowerDNS reports version 4.7 or newer. On older servers (or when capability detection couldn't reach the API), they stay hidden - you can still sign and unsign zones, but not import or export key material.

### Importing a Key

Open the zone's DNSSEC page and use the **Import key** form:

1. Pick the key type - **KSK**, **ZSK**, or **CSK**.
2. Pick the algorithm. The dropdown only shows algorithms the connected PowerDNS supports, so what you see is what will actually work. Common picks are `ecdsa256` and `ed25519`; legacy zones often use `rsasha256`.
3. Paste the full PEM block, including the `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` lines.
4. Submit.

If PowerDNS rejects the format (wrong algorithm for the key, malformed PEM, etc.) the error from the API is shown above the form. Successful imports are recorded in the zone activity log as a key-add event.

You need full edit permission on the zone to import. Read-only or content-only roles cannot.

### Exporting a Key

Each key row on the DNSSEC page now has an **Export** action. Clicking it returns the PEM block for the active private key so you can copy it into another server or store it offline. Treat the export the same way you would treat any private key - whoever holds it can sign records for the zone.

There is no export-to-file download by default; the PEM is shown inline so you can paste it where you need it. If you want a file, save it from the page.

### Notes

- Imports and exports go through the PowerDNS API. The pdnsutil method does not currently expose PEM import/export through Poweradmin - if you're on the legacy method, switch the connection to API mode first.
- DS and DNSKEY records on the same page can be copied to clipboard with a single click. This is handy when handing the DS record to a registrar.
- The CSK guidance alert that used to sit on top of every DNSSEC page only appears on legacy pre-4.0 PowerDNS servers now. On 4.x+ the standard split-key advice no longer applies, and the alert was just adding noise.
- Sign and unsign actions are both recorded in the zone activity feed (sign was missing before 4.4.0).

## More Information

For more details on DNSSEC and PowerDNS:
- [PowerDNS DNSSEC Documentation](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [PowerDNS API Documentation](https://doc.powerdns.com/authoritative/http-api/index.html)