# DNS Settings

DNS settings in Poweradmin are configured through the `config/settings.php` file under the `dns` section. These settings define various DNS-related defaults and behaviors.

## Basic Configuration

- **hostmaster**: The email address of the hostmaster (DNS administrator). Default: `hostmaster.example.com`
- **ns1**: Primary nameserver hostname. Default: `ns1.example.com`
- **ns2**: Secondary nameserver hostname. Default: `ns2.example.com`
- **ns3**: Third nameserver hostname. Default: none
- **ns4**: Fourth nameserver hostname. Default: none
- **ttl**: Default TTL for new records in seconds. Default: `86400` (24 hours)

## SOA Record Settings

- **soa_refresh**: The time interval before the zone should be refreshed. Default: `28800` (8 hours)
- **soa_retry**: The time interval that should elapse before a failed refresh should be retried. Default: `7200` (2 hours)
- **soa_expire**: The upper limit on the time interval that can elapse before the zone is no longer authoritative. Default: `604800` (1 week)
- **soa_minimum**: The negative result TTL. Default: `86400` (24 hours)

## Zone Settings

- **zone_type_default**: Default zone type for new zones. Options: 'MASTER', 'NATIVE'. Default: 'MASTER'

## Validation Settings

- **strict_tld_check**: Enable strict validation of TLDs. Default: `false`
- **top_level_tld_check**: Prevent creation of top-level domains. Default: `false`
- **third_level_check**: Prevent creation of third-level domains. Default: `false`
- **txt_auto_quote**: Automatically quote TXT records. Default: `false`

## Example Configuration

```php
return [
    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
        'ns3' => '',
        'ns4' => '',
        'ttl' => 86400,
        'soa_refresh' => 28800,
        'soa_retry' => 7200,
        'soa_expire' => 604800,
        'soa_minimum' => 86400,
        'zone_type_default' => 'MASTER',
        'strict_tld_check' => false,
        'top_level_tld_check' => false,
        'third_level_check' => false,
        'txt_auto_quote' => false,
    ],
];
```
