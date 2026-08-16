# Basic Configuration

Poweradmin v4.x uses an array-based configuration format in `config/settings.php`.

**Note**: Upgrading from v3.x? The old flat `$variable` format was removed in 4.1.0. See [Legacy Configuration](legacy-configuration.md) to map the old names onto the keys below.

## Configuration File

Create `config/settings.php` with your custom settings. The file `config/settings.defaults.php` contains all defaults - do not edit it directly as changes will be overwritten during upgrades.

```php
<?php
return [
    'database' => [
        'host' => 'localhost',
        'name' => 'powerdns-db',
        'user' => 'poweradmin-db-user',
        'password' => 'poweradmin-db-user-password',
        'type' => 'mysql',
    ],

    'security' => [
        'session_key' => 'change_this_key',
    ],

    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
    ],
];
```

## Configuration Precedence

When using Docker, configuration is loaded in this order (later overrides earlier):

1. `config/settings.defaults.php` - Default values
2. `config/settings.php` - Your custom settings file
3. Environment variables (`PA_*`) - Docker/container settings
4. Docker secrets (`PA_*__FILE`) - Sensitive values from files

> **Note:** A secret and its plain environment variable are mutually exclusive, not layered. If both `PA_FOO` and `PA_FOO__FILE` are set, the container logs an error and exits rather than preferring one over the other.

## Configuration Sections

The configuration is organized into logical sections:

| Section | Description |
|---------|-------------|
| `database` | Database connection settings |
| `security` | Password policies, session management, MFA |
| `dns` | Nameserver details, SOA defaults, TLD checks |
| `interface` | UI preferences, themes, display options |
| `logging` | Logging configuration (file, syslog, database) |
| `pdns_api` | PowerDNS API integration |
| `mail` | Email configuration for notifications |
| `dnssec` | DNSSEC functionality |
| `ldap` | LDAP/Active Directory authentication |
| `oidc` | OpenID Connect authentication |
| `saml` | SAML authentication |
| `modules` | Optional modules: CSV export (`modules.csv_export`), zone import/export (`modules.zone_import_export`), secondary zone import over AXFR (`modules.secondary_zone_import`), WHOIS (`modules.whois`), RDAP (`modules.rdap`), DNS wizards (`modules.dns_wizards`), mail template previews (`modules.email_previews`) |
| `notifications` | Notification toggles, currently `notifications.zone_access_enabled` (default `false`) for zone access change emails |
| `api` | REST API configuration |
| `user_agreement` | User agreement system |
| `misc` | Timezone, conflict handling, etc. |

## Database Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `database.host` | - | Database server hostname |
| `database.port` | - | Database port (optional) |
| `database.user` | - | Database username |
| `database.password` | - | Database password |
| `database.name` | - | Database name |
| `database.type` | - | Database type: mysql, mysqli, pgsql, sqlite |
| `database.charset` | - | Connection charset (e.g., utf8) |
| `database.file` | - | SQLite database file path |
| `database.debug` | false | Log SQL queries |
| `database.pdns_db_name` | *(empty)* | Separate PowerDNS database, MySQL/MariaDB only (v3.8.0+) |

## Security Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `security.session_key` | change_this_key | Session encryption key (change this!) |
| `security.password_encryption` | bcrypt | Hash algorithm: bcrypt, argon2i, argon2id |
| `security.password_cost` | 12 | Bcrypt cost parameter |
| `security.login_token_validation` | true | CSRF protection for login |
| `security.global_token_validation` | true | CSRF protection globally |

For password policies and MFA settings, see [Security Policies](security-policies.md).

## Interface Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `interface.language` | en_EN | Default language |
| `interface.enabled_languages` | multiple* | Available languages |
| `interface.theme` | default | Theme name (`default`, `modern`, or your own directory under `theme_base_path`) |
| `interface.style` | light | UI style: `light` or `dark` |
| `interface.rows_per_page` | 10 | Rows per page in lists |
| `interface.session_timeout` | 1800 | Session timeout (seconds) |
| `interface.title` | Poweradmin | Application title |
| `interface.display_serial_in_zone_list` | false | Show serial in zone list |
| `interface.display_template_in_zone_list` | false | Show template in zone list |
| `interface.show_zone_comments` | true | Enable zone comments |
| `interface.show_record_comments` | false | Enable record comments |
| `interface.add_reverse_record` | true | Show PTR record checkbox |
| `interface.add_domain_record` | true | Show A/AAAA checkbox in reverse view |
| `interface.show_record_id` | false | Show record ID in edit form |
| `interface.position_record_form_top` | true | Add record form at top |
| `interface.position_save_button_top` | false | Save button at top |
| `interface.show_forward_zone_associations` | true | Show associated forward zones in reverse zone list (v4.0.5+) |
| `interface.display_hostname_only` | false | Show only hostname part in zone edit form (strips zone suffix). Site-wide default; from v4.4.0 each user can override this in their account preferences. |
| `interface.wide_layout` | false | Use the full browser width instead of a fixed-width page. Site-wide default; from v4.5.0 each user can override this in their account preferences. |

\* Default languages: ar_SA, bg_BG, bs_BA, cs_CZ, da_DK, de_DE, el_GR, en_EN, es_ES, et_EE, fa_IR, fi_FI, fr_FR, ga_IE, he_IL, hi_IN, hr_HR, hu_HU, id_ID, it_IT, ja_JP, ko_KR, lt_LT, lv_LV, ms_MY, nb_NO, nl_NL, pl_PL, pt_BR, pt_PT, ro_RO, ru_RU, sk_SK, sl_SI, sq_AL, sr_RS, sv_SE, th_TH, tr_TR, uk_UA, vi_VN, zh_CN, zh_TW (et_EE, fi_FI, hr_HR, hu_HU, lv_LV, ro_RO, sk_SK, sr_RS added in v4.4.0)

> **Tip:** If you experience slow loading or timeout errors on the reverse zones page, set `show_forward_zone_associations` to `false`. This disables the lookup of associated forward zones which can be slow with many PTR records.

For UI customization, see [UI Customization](ui/overview.md).

## DNS Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `dns.hostmaster` | - | Default hostmaster (e.g., hostmaster.example.net) |
| `dns.ns1` | - | Primary nameserver |
| `dns.ns2` | - | Secondary nameserver |
| `dns.ns3` | - | Third nameserver (optional) |
| `dns.ns4` | - | Fourth nameserver (optional) |
| `dns.ttl` | 86400 | Default TTL (seconds) |
| `dns.soa_refresh` | 28800 | SOA refresh (seconds) |
| `dns.soa_retry` | 7200 | SOA retry (seconds) |
| `dns.soa_expire` | 604800 | SOA expire (seconds) |
| `dns.soa_minimum` | 86400 | SOA minimum (seconds) |
| `dns.zone_type_default` | MASTER | Default zone type: `MASTER` or `NATIVE` |
| `dns.strict_tld_check` | false | Allow only official TLDs |
| `dns.top_level_tld_check` | false | Prevent top-level TLD creation |
| `dns.third_level_check` | false | Prevent third-level domain creation |
| `dns.txt_auto_quote` | false | Auto-quote TXT records |

For more DNS options, see [DNS Settings](dns-settings.md).

## Miscellaneous Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `misc.timezone` | UTC | Application timezone, used for SOA serial generation (e.g. `Europe/Berlin`, `Asia/Shanghai`) |
| `misc.display_stats` | false | Show memory/execution stats |
| `misc.display_errors` | false | Show PHP errors (disable in production) |
| `misc.show_generated_passwords` | true | Display generated passwords |
| `misc.edit_conflict_resolution` | last_writer_wins | Conflict strategy* |
| `misc.record_comments_sync` | false | Sync A/PTR record comments |
| `misc.template_cache` | false | Cache compiled Twig templates on disk for faster rendering (v4.5.0+) |
| `misc.template_cache_path` | *(empty)* | Directory for compiled templates; empty uses `var/cache/twig` (v4.5.0+) |

\* Conflict resolution strategies:
- `last_writer_wins` - Latest save overwrites previous
- `only_latest_version` - Reject if record was modified
- `3_way_merge` - Attempt automatic merge

### Template caching

Enabling `misc.template_cache` compiles Twig templates to PHP once and reuses them, which takes the
compile step out of every request. The cache directory must be writable by the web server user. If
it cannot be created or written, Poweradmin logs a warning and falls back to uncached rendering
rather than failing the request.

Compiled templates are revalidated against their source files, so an upgrade that ships new
templates takes effect without clearing the cache by hand.

## Related Documentation

- [Database Configuration](database.md)
- [DNS Settings](dns-settings.md)
- [Security Policies](security-policies.md)
- [PowerDNS API](powerdns-api.md)
- [LDAP Integration](ldap.md)
- [OIDC Authentication](oidc.md)
- [SAML Authentication](saml.md)
- [Logging Setup](logging.md)
- [Mail Configuration](mail.md)
- [API Configuration](api.md)
- [Legacy Configuration (v3.x)](legacy-configuration.md)
