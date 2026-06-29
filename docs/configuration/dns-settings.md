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
| - | dns.ttl_reverse | null | Default TTL for PTR records in reverse zones. When `null`, falls back to `dns.ttl`. When configured, the value pre-fills the TTL field on the reverse-zone add-record form, applies to batch PTR creation, and is used for PTRs auto-created alongside a forward record (the matched forward record's TTL is overridden). The same default is applied server-side by the v1/v2 record APIs, RRSets, bulk records, and the DNS wizard when the request omits a `ttl` field. | 4.4.0 (UI), 4.5.0 (APIs + wizard) |
| $dns_soa | (see below) | 28800 7200 604800 86400 | SOA settings for refresh, retry, expire and minimum | 2.2.3 |
| - | dns.soa_refresh | 28800 | SOA refresh time | 2.2.3 |
| - | dns.soa_retry | 7200 | SOA retry time | 2.2.3 |
| - | dns.soa_expire | 604800 | SOA expire time | 2.2.3 |
| - | dns.soa_minimum | 86400 | SOA minimum TTL | 2.2.3 |
| $dns_strict_tld_check | dns.strict_tld_check | false | If enabled (true), allow official TLDs only. | |
| $dns_top_level_tld_check | dns.top_level_tld_check | false | Don't allow creation of top-level TLDs when true. | 2.1.7 |
| $dns_third_level_check | dns.third_level_check | false | Don't allow creation of third-level domains when true. | 2.1.7 |
| - | dns.parent_zone_ownership_check | true | Block creating a zone that overlaps an existing zone owned by another user, in either direction (a subdomain of, or a parent of, the other zone). Covers forward and reverse zones. Ueberusers are exempt. | 4.5.0 |
| $dns_txt_auto_quote | dns.txt_auto_quote | false | Automatically quote TXT records when true. | 3.9.2 |
| $iface_zone_type_default | dns.zone_type_default | MASTER | Default zone type when creating new zones. | 2.1.9 |
| - | dns.default_zone_template | null | Default zone template pre-selected on the add-zone form. Accepts a template id (int) or name (string). The DB-backed default (set in the template list UI) wins when both are present. | 4.4.0 |
| - | dns.zone_ownership_mode | both | Controls how zone ownership can be assigned on creation and ownership pages. Options: `both`, `users_only`, `groups_only`. | 4.4.0 |
| - | dns.prevent_duplicate_ptr | true | Prevent creation of multiple PTR records for same IP in batch operations. | 4.0.0 |
| - | dns.domain_record_types | null | Custom record types for domain zones (null uses defaults). | 4.0.0 |
| - | dns.reverse_record_types | null | Custom record types for reverse zones (null uses defaults). | 4.0.0 |
| - | dns.top_record_types | null | Pin selected record types to the top of record type selectors, in the given order. Null = alphabetical only. | 4.4.0 |
| - | dns.custom_tlds | [] | Custom TLDs to allow in zone names (when `strict_tld_check` is on) and in CNAME targets (e.g., `['dn42', 'home']`). | 3.x |

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
- **top_record_types** (4.4.0): Array of record types to pin to the top of record type selectors, in the given order. Remaining types follow alphabetically. Set to `null` to keep the original alphabetical order.

Example custom configuration:
```php
'dns' => [
    'domain_record_types' => ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'SRV', 'CAA'],
    'reverse_record_types' => ['PTR', 'NS', 'SOA', 'TXT', 'CNAME'],
    'top_record_types' => ['A', 'AAAA', 'CNAME', 'TXT', 'MX'],
],
```

## Custom TLD Whitelist

The `custom_tlds` option lets you whitelist non-IANA TLDs so they pass validation. It applies in two places:

- **CNAME targets** are normally restricted to alphabetic TLDs, which rejects experimental networks like DN42 (`.dn42`).
- **Zone names** are normally restricted to the official IANA list plus reserved special-use names when `strict_tld_check` is enabled. With `strict_tld_check` off (the default), any alphabetic TLD is accepted and this whitelist is not consulted.

```php
'dns' => [
    'strict_tld_check' => true,
    'custom_tlds' => ['dn42', 'home', 'lan', 'corp'],
],
```

With this configuration, both a zone named `office.lan` and a CNAME target like `ns1.example.dn42` pass validation. Matching is case-insensitive.

**Note**: Standard alphabetic TLDs (like `.com`, `.org`, `.net`) always work regardless of this setting.

### Pre-whitelisted special-use TLDs

Even with `strict_tld_check` enabled, the following reserved TLDs are always accepted and do not need to be added to `custom_tlds`:

| TLD | Reference | Typical use |
|-----|-----------|-------------|
| `test`, `example`, `invalid`, `localhost` | RFC 2606 | Testing and documentation |
| `local` | RFC 6762 | Multicast DNS |
| `onion` | RFC 7686 | Tor hidden services |
| `alt` | RFC 9476 | Alternative DNS namespaces |
| `internal` | ICANN reserved (2024) | Private-use applications |

If you use one of these for an internal zone, no extra configuration is required. Other common homelab TLDs such as `.lan`, `.home`, and `.corp` are not on this list and require either `strict_tld_check = false` or an entry in `custom_tlds`.

## Zone Overlap Protection

`parent_zone_ownership_check` (added in 4.5.0, **enabled by default**) stops a user from creating a zone that overlaps a zone owned by **another** user. Because PowerDNS serves the most-specific zone, an overlapping zone would otherwise shadow the other owner's data.

It blocks both directions:

- **subdomain of another owner's zone** - e.g. user B cannot create `b.a.com` when `a.com` is owned by user A;
- **parent of another owner's zone** - e.g. user B cannot create `a.com` when `b.a.com` is owned by user A.

Notes:

- Applies to forward and reverse zones.
- Creating a sub-zone of a zone **you already own** is allowed (legitimate delegation).
- Ueberusers (super-admins) are exempt.
- The check runs only at creation time; it does not retroactively flag zones that already overlap.

To allow cross-owner overlapping zones, set it to `false`:

```php
'dns' => [
    'parent_zone_ownership_check' => false,
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
        'ttl_reverse' => null, // PTR-specific default; null falls back to dns.ttl (added in 4.4.0)
        // SOA settings
        'soa_refresh' => 28800,
        'soa_retry' => 7200,
        'soa_expire' => 604800,
        'soa_minimum' => 86400,
        'zone_type_default' => 'MASTER',
        'default_zone_template' => null, // template id (int) or name (string); null for "none"
        'zone_ownership_mode' => 'both', // 'both', 'users_only', or 'groups_only'
        'strict_tld_check' => false,
        'top_level_tld_check' => false,
        'third_level_check' => false,
        'parent_zone_ownership_check' => true, // block overlapping zones across owners (added in 4.5.0)
        'txt_auto_quote' => false,
        'prevent_duplicate_ptr' => true,
        'domain_record_types' => null, // Uses default types
        'reverse_record_types' => null, // Uses default types
        'custom_tlds' => [], // Custom TLDs for CNAME validation
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
