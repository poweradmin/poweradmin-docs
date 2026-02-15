# Basic Configuration

Poweradmin v4.x uses an array-based configuration format in `config/settings.php`.

**Note**: For legacy v3.x variable format (`$variable`), see [Legacy Configuration](legacy-configuration.md).

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
| `whois` | WHOIS lookup settings |
| `rdap` | RDAP lookup settings |
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
| `database.pdns_db_name` | powerdns | Separate PowerDNS database (v3.8.0+) |

## Security Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `security.session_key` | p0w3r4dm1n | Session encryption key (change this!) |
| `security.password_encryption` | bcrypt | Hash algorithm: md5, md5salt, bcrypt, argon2i, argon2id |
| `security.password_encryption_cost` | 12 | Bcrypt cost parameter |
| `security.login_token_validation` | true | CSRF protection for login |
| `security.global_token_validation` | true | CSRF protection globally |

For password policies and MFA settings, see [Security Policies](security-policies.md).

## Interface Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `interface.lang` | en_EN | Default language |
| `interface.enabled_languages` | multiple* | Available languages |
| `interface.style` | ignite | Theme (ignite, spark for dark) |
| `interface.rowamount` | 10 | Records per page |
| `interface.expire` | 1800 | Session timeout (seconds) |
| `interface.title` | Poweradmin | Application title |
| `interface.zone_type_default` | MASTER | Default zone type |
| `interface.zonelist_serial` | false | Show serial in zone list |
| `interface.zonelist_template` | false | Show template in zone list |
| `interface.zone_comments` | true | Enable zone comments |
| `interface.record_comments` | false | Enable record comments |
| `interface.index` | cards | Display mode (cards/list) |
| `interface.add_reverse_record` | true | Show PTR record checkbox |
| `interface.add_domain_record` | true | Show A/AAAA checkbox in reverse view |
| `interface.edit_show_id` | true | Show record ID in edit form |
| `interface.edit_add_record_top` | false | Add record form at top |
| `interface.edit_save_changes_top` | false | Save button at top |
| `interface.show_forward_zone_associations` | true | Show associated forward zones in reverse zone list (v4.0.5+) |

\* Default languages: cs_CZ, de_DE, en_EN, es_ES, fr_FR, id_ID, it_IT, ja_JP, ko_KR, lt_LT, nb_NO, nl_NL, pl_PL, pt_PT, ru_RU, sv_SE, tr_TR, uk_UA, vi_VN, zh_CN

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
| `dns.soa` | 28800 7200 604800 86400 | SOA: refresh retry expire minimum |
| `dns.strict_tld_check` | false | Allow only official TLDs |
| `dns.top_level_tld_check` | false | Prevent top-level TLD creation |
| `dns.third_level_check` | false | Prevent third-level domain creation |
| `dns.txt_auto_quote` | false | Auto-quote TXT records |

For more DNS options, see [DNS Settings](dns-settings.md).

## Miscellaneous Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `misc.timezone` | UTC | Application timezone |
| `misc.display_stats` | false | Show memory/execution stats |
| `misc.display_errors` | false | Show PHP errors (disable in production) |
| `misc.show_generated_passwords` | true | Display generated passwords |
| `misc.edit_conflict_resolution` | last_writer_wins | Conflict strategy* |
| `misc.record_comments_sync` | false | Sync A/PTR record comments |

\* Conflict resolution strategies:
- `last_writer_wins` - Latest save overwrites previous
- `only_latest_version` - Reject if record was modified
- `3_way_merge` - Attempt automatic merge

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
