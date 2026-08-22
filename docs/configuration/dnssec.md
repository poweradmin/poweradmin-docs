# DNSSEC Configuration

## Overview

Poweradmin provides comprehensive support for DNSSEC (Domain Name System Security Extensions) through a well-structured implementation that follows domain-driven design principles. All DNSSEC operations go through the PowerDNS REST API - there is no command-line code path.

> **Note:** DNSSEC requires a configured PowerDNS API connection. If `pdns_api.url` and `pdns_api.key` are not both set, DNSSEC is inactive no matter what `dnssec.enabled` says.

The DNSSEC implementation enables you to:

- Secure and unsecure zones
- Manage cryptographic keys (create, activate, deactivate, delete)
- View DS (Delegation Signer) and DNSKEY records
- Manage DNSSEC key rollovers

Each zone gets a key management page listing its keys with their type, tag, algorithm and
active state, alongside actions to add, activate, export or delete a key, show the DS and
DNSKEY records, and unsign the zone.

![DNSSEC keys for a zone](../screenshots/dnssec-overview.png)

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

DNSSEC settings are configured in the `config/settings.php` file under the `dnssec` section.

| Setting | Default value | Description | Added in version |
|---------|---------------|-------------|-----------------|
| dnssec.enabled | false | Enable (true) or disable (false) DNSSEC support | 2.1.7 |
| dnssec.debug | false | Enable debug for DNSSEC operations | 2.1.9 |

## Enabling DNSSEC

To enable DNSSEC:

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

Working through the API means:

- No need to configure special permissions for the web server user
- More secure as it doesn't require shell access
- Better error handling and feedback
- Full support for all DNSSEC operations

> **Warning:** Leaving `pdns_api.url` or `pdns_api.key` empty does not fall back to a command-line tool. Poweradmin loads a no-op DNSSEC provider instead, and every DNSSEC action silently does nothing.

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

Importing requires the `zone_dnssec_manage_own` permission on the zone (ueberusers always pass). This is a separate permission from zone editing: full zone-edit rights without it are refused, and content-edit rights with it are accepted. The same gate applies to export.

### Exporting a Key

Each key row on the DNSSEC page now has an **Export** action. Clicking it returns the PEM block for the active private key so you can copy it into another server or store it offline. Treat the export the same way you would treat any private key - whoever holds it can sign records for the zone.

The export is always delivered as a file download (`Content-Type: application/x-pem-file`), named `<zone>-key-<id>.pem`. The PEM is never rendered inline in the page.

### Notes

- Imports and exports go through the PowerDNS API, so a working `pdns_api.url` and `pdns_api.key` are required.
- DS and DNSKEY records on the same page can be copied to clipboard with a single click. This is handy when handing the DS record to a registrar.
- The CSK guidance alert that used to sit on top of every DNSSEC page only appears on legacy pre-4.0 PowerDNS servers now. On 4.x+ the standard split-key advice no longer applies, and the alert was just adding noise.
- Sign and unsign actions are both recorded in the zone activity feed (sign was missing before 4.4.0).

## More Information

For more details on DNSSEC and PowerDNS:

- [PowerDNS DNSSEC Documentation](https://doc.powerdns.com/authoritative/dnssec/index.html)
- [PowerDNS API Documentation](https://doc.powerdns.com/authoritative/http-api/index.html)