# DNS Settings

DNS settings in Poweradmin can be configured through the `config/settings.php` file under the `dns` section or through individual variables in the legacy configuration format.

## Configuration Options

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $dns_hostmaster | dns.hostmaster | no default | The default email address to use for the SOA record (e.g., 'hostmaster.example.net'). | |
| $dns_ns1 | dns.ns1 | no default | The default primary nameserver. | |
| $dns_ns2 | dns.ns2 | no default | The default secondary nameserver. | |
| $dns_ns3 | dns.ns3 | no default | The third nameserver. | |
| $dns_ns4 | dns.ns4 | no default | The fourth nameserver. | |
| $dns_ttl | dns.ttl | 86400 | The default TTL for records (in seconds). | |
| $dns_soa | (see below) | 28800 7200 604800 86400 | SOA settings for refresh, retry, expire and minimum | 2.2.3 |
| - | dns.soa_refresh | 28800 | SOA refresh time | 2.2.3 |
| - | dns.soa_retry | 7200 | SOA retry time | 2.2.3 |
| - | dns.soa_expire | 604800 | SOA expire time | 2.2.3 |
| - | dns.soa_minimum | 86400 | SOA minimum TTL | 2.2.3 |
| $dns_strict_tld_check | dns.strict_tld_check | false | If enabled (true), allow official TLDs only. | |
| $dns_top_level_tld_check | dns.top_level_tld_check | false | Don't allow creation of top-level TLDs when true. | 2.1.7 |
| $dns_third_level_check | dns.third_level_check | false | Don't allow creation of third-level domains when true. | 2.1.7 |
| $dns_txt_auto_quote | dns.txt_auto_quote | false | Automatically quote TXT records when true. | 3.9.2 |
| $iface_zone_type_default | dns.zone_type_default | MASTER | Default zone type when creating new zones. | 2.1.9 |
| - | dns.prevent_duplicate_ptr | true | Prevent creation of multiple PTR records for same IP in batch operations. | 4.0.0 |
| - | dns.domain_record_types | null | Custom record types for domain zones (null uses defaults). | 4.0.0 |
| - | dns.reverse_record_types | null | Custom record types for reverse zones (null uses defaults). | 4.0.0 |

## SOA Record Settings

In the modern configuration format, the SOA settings are configured as individual parameters:

- **refresh**: The time interval before the zone should be refreshed. Default: `28800` (8 hours)
- **retry**: The time interval that should elapse before a failed refresh should be retried. Default: `7200` (2 hours)
- **expire**: The upper limit on the time interval that can elapse before the zone is no longer authoritative. Default: `604800` (1 week)
- **minimum**: The negative result TTL. Default: `86400` (24 hours)

In the legacy format, these are combined in the `$dns_soa` variable as a space-separated string.

## Record Type Configuration

You can customize which record types are available in the zone editing interface:

- **domain_record_types**: Array of record types for domain zones. Set to `null` to use defaults.
- **reverse_record_types**: Array of record types for reverse zones. Set to `null` to use defaults.

Example custom configuration:
```php
'dns' => [
    'domain_record_types' => ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'SRV', 'CAA'],
    'reverse_record_types' => ['PTR', 'NS', 'SOA', 'TXT', 'CNAME'],
],
```

## Modern Configuration Example

```php
return [
    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
        'ns3' => 'ns3.example.com',
        'ns4' => 'ns4.example.com',
        'ttl' => 86400,
        // SOA settings
        'soa_refresh' => 28800,
        'soa_retry' => 7200,
        'soa_expire' => 604800,
        'soa_minimum' => 86400,
        'zone_type_default' => 'MASTER',
        'strict_tld_check' => false,
        'top_level_tld_check' => false,
        'third_level_check' => false,
        'txt_auto_quote' => false,
        'prevent_duplicate_ptr' => true,
        'domain_record_types' => null, // Uses default types
        'reverse_record_types' => null, // Uses default types
    ],
];
```

## Legacy Configuration Example

```php
<?php
// DNS settings
$dns_hostmaster = 'hostmaster.example.com';
$dns_ns1 = 'ns1.example.com';
$dns_ns2 = 'ns2.example.com';
$dns_ns3 = 'ns3.example.com';
$dns_ns4 = 'ns4.example.com';
$dns_ttl = 86400;
$dns_soa = '28800 7200 604800 86400';
$dns_strict_tld_check = false;
$dns_top_level_tld_check = false;
$dns_third_level_check = false;
$dns_txt_auto_quote = false;
$iface_zone_type_default = 'MASTER';
```
