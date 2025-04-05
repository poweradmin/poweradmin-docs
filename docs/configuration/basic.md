# Basic Configuration

Poweradmin supports two configuration formats: legacy (individual PHP variables) and modern (array-based configuration).

## Configuration Files

With any new installation, the file `config/settings.defaults.php` (or in legacy versions, `inc/config-defaults.inc.php`) is distributed. You should not edit this file as your changes will likely be overwritten during upgrades.

Instead:
- Modern format: Create `config/settings.php`
- Legacy format: Create `inc/config.inc.php`

Your custom settings will override the defaults. This way, new configuration options can be added with sensible defaults without breaking your existing configuration.

## Legacy Configuration Format

This is the traditional format, still supported for backwards compatibility:

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

## Modern Configuration Format

The recommended modern format uses a PHP array structure:

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

## Configuration Sections

The modern configuration format is organized into logical sections:

- **database**: Database connection settings
- **security**: Security-related settings including password policies and session management
- **dns**: DNS-specific configurations including nameserver details
- **interface**: UI and display preferences
- **logging**: Logging configuration
- **pdns_api**: PowerDNS API integration settings

## Configuration Variables

The following configuration variables are available in the legacy format, with their modern array format equivalents:

### Database Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $db_host | database.host | no default | The host to connect to for access to the database. | |
| $db_port | database.port | no default | The port to use for database connection. | |
| $db_user | database.user | no default | The username to use to access the database. | |
| $db_pass | database.password | no default | The password to use to access the database. | |
| $db_name | database.name | no default | The name of the database of PowerDNS. | |
| $db_type | database.type | no default | The type of the database of PowerDNS. Poweradmin currently has support for 'mysql', 'mysqli', 'pgsql' and 'sqlite'. | mysqli - 2.1.5, sqlite - 2.1.6 |
| $db_charset | database.charset | no default | The charset set which is used for communication with database (for example - 'utf8' for MySQL) | 2.1.8 |
| $db_file | database.file | no default | Used only for SQLite, provide full path to database file | 2.1.6 |
| $db_debug | database.debug | false | Show all executed SQL queries (if true) | 2.1.6 |
| $pdns_db_name | database.pdns_name | powerdns | Used for a separate database for PowerDNS (experimental feature) | 3.8.0 |

### API Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $pdns_api_url | pdns_api.url | no default | The endpoint for establishing a connection to the PowerDNS API. | 3.7.0 |
| $pdns_api_key | pdns_api.key | no default | The authentication key required for establishing a connection with the PowerDNS API. | 3.7.0 |

### Security Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $session_key | security.session_key | p0w3r4dm1n | The key used for session data encryption | 2.1.6 |
| $password_encryption | security.password_encryption | "bcrypt" | The type of encryption used for keeping user passwords in database. Other possible values - md5, md5salt (compatible with WHMCS), argon2i, argon2id | 2.1.6 |
| $password_encryption_cost | security.password_encryption_cost | 12 | The algorithmic cost (needed for bcrypt) | 2.1.8 |
| $login_token_validation | security.login_token_validation | true | Enable or disable login token validation | 3.9.0 |
| $global_token_validation | security.global_token_validation | true | Enable or disable global token validation | 3.9.0 |

### Interface Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $iface_lang | interface.lang | en_EN | The language for the interface. | |
| $iface_enabled_languages | interface.enabled_languages | multiple* | Languages enabled in the interface. | 3.8.0 |
| $iface_style | interface.style | ignite | The CSS template to use as skin of web interface. See "style/" directory. If you want a dark theme, use 'spark'. | |
| $iface_templates | interface.templates | templates | The HTML templates to use for web interface. See "templates/" directory. | 2.2.3 |
| $iface_rowamount | interface.rowamount | 10 | The maximum number of rows that should be shown (usefull if you have a large number of zones or records). | |
| $iface_expire | interface.expire | 1800 | Session time-out in seconds. After this timeout, you are automagically logged out. | |
| $iface_zonelist_serial | interface.zonelist_serial | false | Enable (true) or disable (false) display of zone's serial in the zone listing. | |
| $iface_zonelist_template | interface.zonelist_template | false | Enable (true) or disable (false) display of zone's template in the zone listing. | |
| $iface_title | interface.title | Poweradmin | The title which is showed in header | 2.1.5 |
| $iface_add_reverse_record | interface.add_reverse_record | true | Displays a checkbox for adding a reverse record | 2.1.7 |
| $iface_add_domain_record | interface.add_domain_record | true | Displays a checkbox for adding an A/AAAA record from the reverse zone view | |
| $iface_zone_type_default | interface.zone_type_default | MASTER | Default zone type when creating new zones | 2.1.9 |
| $iface_zone_comments | interface.zone_comments | true | Show or hide zone comments | 2.2.3 |
| $iface_record_comments | interface.record_comments | false | Show or hide record comments | 3.9.0 |
| $iface_index | interface.index | cards | Interface display mode (cards or list) | 3.2.0 |
| $iface_search_group_records | interface.search_group_records | false | Group records by name and content in search results | 3.8.0 |
| $iface_edit_show_id | interface.edit_show_id | true | Show or hide record ID in edit form | 3.9.0 |
| $iface_edit_add_record_top | interface.edit_add_record_top | false | Add new record fields on top of the list | 3.9.0 |
| $iface_edit_save_changes_top | interface.edit_save_changes_top | false | Save changes button on top of the list | 3.9.0 |
| $iface_migrations_show | interface.migrations_show | false | Show or hide migrations in the menu (experimental) | |

\* Default enabled languages: cs_CZ, de_DE, en_EN, fr_FR, it_IT, ja_JP, lt_LT, nb_NO, nl_NL, pl_PL, ru_RU, tr_TR, zh_CN

### DNS Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $dns_hostmaster | dns.hostmaster | no default | The default emailaddress to use for the RP in the SOA record. For example: 'hostmaster.example.net'. | |
| $dns_ns1 | dns.ns1 | no default | The default primary nameserver. | |
| $dns_ns2 | dns.ns2 | no default | The default secondary nameserver. | |
| $dns_ns3 | dns.ns3 | no default | The third secondary nameserver. | |
| $dns_ns4 | dns.ns4 | no default | The fourth secondary nameserver. | |
| $dns_ttl | dns.ttl | 86400 | The default TTL for records (in seconds of course). | |
| $dns_soa | dns.soa | 28800 7200 604800 86400 | SOA settings for refresh, retry, expire and minimum | 2.2.3 |
| $dns_strict_tld_check | dns.strict_tld_check | false | If enabled (true), allow  official TLD's only. | |
| $dns_top_level_tld_check | dns.top_level_tld_check | false | Don't allow to create top level TLDs | 2.1.7 |
| $dns_third_level_check | dns.third_level_check | false | Don't allow to create third level domains | 2.1.7 |
| $dns_txt_auto_quote | dns.txt_auto_quote | false | Automatically quote TXT records | 3.9.2 |

### Timezone Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $timezone | timezone | UTC | Set timezone (for php 5.1.0+). See http://www.php.net/manual/en/timezones.php for list of supported timezones. | |

### Logging Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $logger_type | logging.type | null | Logger type (null, native) | 3.9.0 |
| $logger_level | logging.level | info | Logging level (debug, info, notice, warning, error, critical, alert, emergency) | 3.9.0 |
| $syslog_use | logging.syslog.use | false | Enable (true) or disable (false) logging of authentication attempts and other operations to syslog | 2.1.6 |
| $syslog_ident | logging.syslog.ident | poweradmin | Specifies program name which is added to syslog message | 2.1.6 |
| $syslog_facility | logging.syslog.facility | LOG_USER | Specifies what type of program is logging the message | 2.1.6 |
| $dblog_use | logging.dblog.use | false | Enable (true) or disable (false) logging to database | 3.2.0 |

### DNSSEC Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $pdnssec_use | dnssec.use | false | Enable (true) or disable (false) DNSSEC support | 2.1.7 |
| $pdnssec_debug | dnssec.debug | false | Enable debug for DNSSEC operations | 2.1.9 |
| $pdnssec_command | dnssec.command | /usr/bin/pdnsutil | Full path to pdnsutil utility (will be deprecated in the future) | 2.1.7 |

### LDAP Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $ldap_use | ldap.use | false | Authenticate against directory service (LDAP/Active Directory) | 2.1.7 |
| $ldap_debug | ldap.debug | false | Enable debug for LDAP connection | 2.1.7 |
| $ldap_uri | ldap.uri | ldap://domaincontroller.example.com | LDAP URI | 2.1.7 |
| $ldap_basedn | ldap.basedn | ou=users,dc=example,dc=com | The top level of the LDAP directory tree | 2.1.7 |
| $ldap_search_filter | ldap.search_filter | no default | Filter for LDAP search | 2.1.7 |
| $ldap_binddn | ldap.binddn | cn=admin,dc=example,dc=com | LDAP user | 2.1.7 |
| $ldap_bindpw | ldap.bindpw | some_password | password for LDAP user | 2.1.7 |
| $ldap_user_attribute | ldap.user_attribute | uid | username attribute used in LDAP search filter | 2.1.7 |
| $ldap_proto | ldap.proto | 3 | LDAP protocol version | 2.1.7 |

LDAP search filter examples:
```
$ldap_search_filter = '(memberOf=cn=powerdns,ou=groups,dc=poweradmin,dc=org)';
$ldap_search_filter = '(objectClass=account)';
$ldap_search_filter = '(objectClass=person)(memberOf=cn=admins,ou=groups,dc=poweradmin,dc=org)';
$ldap_search_filter = '(cn=*admin*)';
```

### Other Settings

| Legacy variable | Modern equivalent | Default value | Description | Added in version |
|----------------|-------------------|---------------|-------------|-----------------|
| $display_stats | display_stats | false | Displays the memory consumption and execution time of an application | |
| $experimental_edit_conflict_resolution | edit_conflict_resolution | last_writer_wins | Controls how concurrent updates are handled (last_writer_wins, only_latest_version, 3_way_merge) | |
| $record_comments_sync | record_comments_sync | false | Enable bidirectional comment synchronization between A and PTR records | 3.9.0 |

For detailed information about specific settings, see:

- [Database Configuration](database.md)
- [DNS Settings](dns-settings.md)
- [Security Policies](security-policies.md)
- [PowerDNS API](powerdns-api.md)
- [LDAP Integration](ldap.md)
- [Logging Setup](logging.md)

## Important Notes

1. When using the modern format, all settings should be included in the array structure
2. The legacy format is maintained for backward compatibility but new installations should use the modern format
3. Never commit sensitive information like passwords to version control
4. Always change default values, especially the `session_key`, in production environments
5. Make sure to set appropriate file permissions on your configuration file
