# DNS Record Type Customization

## Overview

Poweradmin 4.0.0 allows you to customize which DNS record types are available when creating or editing records in both domain (forward) zones and reverse zones. This feature helps simplify the user interface by showing only the record types relevant to your specific DNS needs.

## Configuration Options

The record type customization is configured in the `dns` section of your `settings.php` file with two key settings:

```php
'dns' => [
    // Other DNS settings...
    
    // Record Type Settings
    'domain_record_types' => null,  // For forward zones (A, AAAA, MX, etc.)
    'reverse_record_types' => null, // For reverse zones (PTR, etc.)
]
```

### Default Behavior

By default, both settings are set to `null`, which means Poweradmin will display all supported record types for the respective zone type.

## Customizing Domain (Forward) Zone Record Types

To customize which record types are available when editing forward zones:

```php
'domain_record_types' => ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'SRV', 'CAA'],
```

This example shows a typical configuration with common record types. You can add or remove types based on your requirements.

## Customizing Reverse Zone Record Types

Similarly, you can customize which record types are available when editing reverse zones:

```php
'reverse_record_types' => ['PTR', 'NS', 'SOA', 'TXT', 'CNAME'],
```

## Zone Templates

When editing zone templates, Poweradmin will automatically show the combined list of both `domain_record_types` and `reverse_record_types` to ensure all potential record types for template use are available.

## Supported Record Types

Poweradmin supports the following DNS record types that can be included in your customized lists:

| Record Type | Description | Typically Used In |
|-------------|-------------|------------------|
| A | Maps a domain name to an IPv4 address | Domain zones |
| AAAA | Maps a domain name to an IPv6 address | Domain zones |
| CNAME | Creates an alias for another domain name | Both |
| MX | Specifies mail servers for the domain | Domain zones |
| NS | Specifies name servers for the domain | Both |
| PTR | Maps an IP address to a domain name (reverse lookup) | Reverse zones |
| SOA | Start of Authority, contains administrative information | Both |
| SRV | Specifies location of services (like SIP, XMPP) | Domain zones |
| TXT | Contains text information (often used for verification) | Both |
| CAA | Specifies which Certificate Authorities can issue certificates | Domain zones |
| DNSKEY | Public key for DNSSEC | Both |
| DS | Delegation Signer, contains hash of DNSKEY record | Both |
| NAPTR | Name Authority Pointer for ENUM and other transformations | Domain zones |
| SSHFP | SSH Public Key Fingerprint | Domain zones |
| TLSA | TLS Authentication association | Domain zones |

## Use Cases

1. **Simplifying the Interface**: Hide rarely used record types to make the interface cleaner
2. **Preventing Errors**: Limit available record types to prevent misconfiguration
3. **Specialized Deployments**: Tailor the interface for specific DNS use cases

## Example Configurations

### Basic Web Server Configuration
```php
'domain_record_types' => ['A', 'AAAA', 'CNAME', 'MX', 'TXT'],
'reverse_record_types' => ['PTR', 'NS', 'SOA'],
```

### DNSSEC-Focused Configuration
```php
'domain_record_types' => ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'DNSKEY', 'DS'],
'reverse_record_types' => ['PTR', 'NS', 'SOA'],
```

### Full-Featured Configuration
```php
'domain_record_types' => [
    'A', 'AAAA', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'SRV', 'CAA', 
    'DNSKEY', 'DS', 'NAPTR', 'SSHFP', 'TLSA'
],
'reverse_record_types' => ['PTR', 'NS', 'SOA', 'TXT', 'CNAME'],
```