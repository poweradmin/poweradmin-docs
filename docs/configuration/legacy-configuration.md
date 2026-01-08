# Legacy Configuration (v3.x LTS)

This page documents the legacy PHP variable configuration format used in Poweradmin v3.x and earlier versions.

**Note**: For Poweradmin v4.0.0 and later, use the [modern array-based configuration](basic.md) format instead.

## Configuration File

Legacy configuration uses individual PHP variables in `inc/config.inc.php`:

```php
<?php
$db_host = 'localhost';
$db_name = 'powerdns-db';
$db_user = 'poweradmin-db-user';
$db_pass = 'poweradmin-db-user-password';
$db_type = 'mysql';

$session_key = 'generate-some-random-text-here';

$dns_hostmaster = 'hostmaster.example.net';
$dns_ns1 = 'ns1.example.net';
$dns_ns2 = 'ns2.example.net';
```

## Database Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$db_host` | - | Database host | - |
| `$db_port` | - | Database port | - |
| `$db_user` | - | Database username | - |
| `$db_pass` | - | Database password | - |
| `$db_name` | - | Database name | - |
| `$db_type` | - | Database type: mysql, mysqli, pgsql, sqlite | mysqli 2.1.5, sqlite 2.1.6 |
| `$db_charset` | - | Database charset (e.g., utf8) | 2.1.8 |
| `$db_file` | - | SQLite database file path | 2.1.6 |
| `$db_debug` | false | Show executed SQL queries | 2.1.6 |
| `$pdns_db_name` | powerdns | Separate PowerDNS database name | 3.8.0 |

## Security Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$session_key` | p0w3r4dm1n | Session encryption key | 2.1.6 |
| `$password_encryption` | bcrypt | Password hash: md5, md5salt, bcrypt, argon2i, argon2id | 2.1.6 |
| `$password_encryption_cost` | 12 | Bcrypt cost parameter | 2.1.8 |
| `$login_token_validation` | true | Enable login token validation | 3.9.0 |
| `$global_token_validation` | true | Enable global token validation | 3.9.0 |

## Interface Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$iface_lang` | en_EN | Interface language | - |
| `$iface_enabled_languages` | multiple* | Enabled languages | 3.8.0 |
| `$iface_style` | ignite | CSS theme (ignite, spark for dark) | - |
| `$iface_templates` | templates | HTML templates directory | 2.2.3 |
| `$iface_rowamount` | 10 | Maximum rows per page | - |
| `$iface_expire` | 1800 | Session timeout (seconds) | - |
| `$iface_zonelist_serial` | false | Show zone serial in listing | - |
| `$iface_zonelist_template` | false | Show zone template in listing | - |
| `$iface_title` | Poweradmin | Application title | 2.1.5 |
| `$iface_add_reverse_record` | true | Show reverse record checkbox | 2.1.7 |
| `$iface_add_domain_record` | true | Show A/AAAA record checkbox in reverse view | - |
| `$iface_zone_type_default` | MASTER | Default zone type | 2.1.9 |
| `$iface_zone_comments` | true | Show zone comments | 2.2.3 |
| `$iface_record_comments` | false | Show record comments | 3.9.0 |
| `$iface_index` | cards | Display mode (cards or list) | 3.2.0 |
| `$iface_search_group_records` | false | Group records in search | 3.8.0 |
| `$iface_edit_show_id` | true | Show record ID in edit form | 3.9.0 |
| `$iface_edit_add_record_top` | false | Add record form on top | 3.9.0 |
| `$iface_edit_save_changes_top` | false | Save button on top | 3.9.0 |
| `$iface_migrations_show` | false | Show migrations menu (experimental) | - |

\* Default enabled languages: cs_CZ, de_DE, en_EN, fr_FR, it_IT, ja_JP, lt_LT, nb_NO, nl_NL, pl_PL, ru_RU, tr_TR, zh_CN

## DNS Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$dns_hostmaster` | - | Default hostmaster email (e.g., hostmaster.example.net) | - |
| `$dns_ns1` | - | Primary nameserver | - |
| `$dns_ns2` | - | Secondary nameserver | - |
| `$dns_ns3` | - | Third nameserver | - |
| `$dns_ns4` | - | Fourth nameserver | - |
| `$dns_ttl` | 86400 | Default TTL (seconds) | - |
| `$dns_soa` | 28800 7200 604800 86400 | SOA: refresh retry expire minimum | 2.2.3 |
| `$dns_strict_tld_check` | false | Allow only official TLDs | - |
| `$dns_top_level_tld_check` | false | Prevent top-level TLD creation | 2.1.7 |
| `$dns_third_level_check` | false | Prevent third-level domain creation | 2.1.7 |
| `$dns_txt_auto_quote` | false | Auto-quote TXT records | 3.9.2 |

## PowerDNS API Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$pdns_api_url` | - | PowerDNS API endpoint URL | 3.7.0 |
| `$pdns_api_key` | - | PowerDNS API authentication key | 3.7.0 |

## Logging Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$logger_type` | null | Logger type (null, native) | 3.9.0 |
| `$logger_level` | info | Log level: debug, info, notice, warning, error, critical, alert, emergency | 3.9.0 |
| `$syslog_use` | false | Enable syslog logging | 2.1.6 |
| `$syslog_ident` | poweradmin | Syslog program name | 2.1.6 |
| `$syslog_facility` | LOG_USER | Syslog facility | 2.1.6 |
| `$dblog_use` | false | Enable database logging | 3.2.0 |

## DNSSEC Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$pdnssec_use` | false | Enable DNSSEC support | 2.1.7 |
| `$pdnssec_debug` | false | Enable DNSSEC debug | 2.1.9 |
| `$pdnssec_command` | /usr/bin/pdnsutil | Path to pdnsutil (deprecated) | 2.1.7 |

## LDAP Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$ldap_use` | false | Enable LDAP authentication | 2.1.7 |
| `$ldap_debug` | false | Enable LDAP debug | 2.1.7 |
| `$ldap_uri` | ldap://domaincontroller.example.com | LDAP server URI | 2.1.7 |
| `$ldap_basedn` | ou=users,dc=example,dc=com | LDAP base DN | 2.1.7 |
| `$ldap_search_filter` | - | LDAP search filter | 2.1.7 |
| `$ldap_binddn` | cn=admin,dc=example,dc=com | LDAP bind DN | 2.1.7 |
| `$ldap_bindpw` | - | LDAP bind password | 2.1.7 |
| `$ldap_user_attribute` | uid | Username attribute | 2.1.7 |
| `$ldap_proto` | 3 | LDAP protocol version | 2.1.7 |

### LDAP Search Filter Examples

```php
$ldap_search_filter = '(memberOf=cn=powerdns,ou=groups,dc=poweradmin,dc=org)';
$ldap_search_filter = '(objectClass=account)';
$ldap_search_filter = '(objectClass=person)(memberOf=cn=admins,ou=groups,dc=poweradmin,dc=org)';
$ldap_search_filter = '(cn=*admin*)';
```

## Other Settings

| Variable | Default | Description | Added |
|----------|---------|-------------|-------|
| `$timezone` | UTC | PHP timezone | - |
| `$display_stats` | false | Show memory/execution stats | - |
| `$experimental_edit_conflict_resolution` | last_writer_wins | Conflict handling strategy | - |
| `$record_comments_sync` | false | Sync A/PTR record comments | 3.9.0 |

## Migrating to v4.x

When upgrading to Poweradmin v4.0.0 or later, you can migrate your configuration using:

```bash
php config/migrate-config.php
```

This will convert your legacy `inc/config.inc.php` to the modern `config/settings.php` format.

See [Basic Configuration](basic.md) for the modern configuration format.
