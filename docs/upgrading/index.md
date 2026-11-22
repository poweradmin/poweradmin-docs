# Upgrading Poweradmin

Coming from another PowerDNS web interface, such as PowerDNS-Admin, Opera DNS UI, nsedit or PDNS Manager? See
[Migrating from Other Tools](../migrating/index.md).

> **Need help with the upgrade?** Paid upgrade assistance, from planning to doing the upgrade with you,
> is available through [Support & Sponsorship](https://www.poweradmin.org/p/support-and-sponsorship),
> or write to [support@poweradmin.org](mailto:support@poweradmin.org).

## Quick Path to a Supported Version

Find the version you run and follow its row. 4.4.x and 3.9.x are LTS until December 2027; see
[Version Support](../getting-started/lifecycle.md).

| You run | Upgrade to | How |
|---------|------------|-----|
| 2.x | 4.4.3 | [Upgrading from 2.x](from-2x.md) |
| 3.0.0 - 3.9.13 | 3.9.14 (stay on 3.x) | [Within 3.x](#within-3x-to-3914) |
| 3.x | 4.4.3 | [From 3.x to 4.4.3](#from-3x-to-443) |
| 4.0.0 - 4.3.x | 4.4.3 | [From 4.0 - 4.3 to 4.4.3](#from-40-43-to-443) |
| 4.4.0 - 4.4.2 | 4.4.3 | [Patch upgrade](#patch-version-upgrades-eg-44x-44y): replace the files, no SQL |

What each target needs:

| Target | PHP | Configuration file | URL rewriting |
|--------|-----|--------------------|---------------|
| 3.9.14 | 8.1 or later | `inc/config.inc.php` | not needed |
| 4.4.3 | 8.2 or later | `config/settings.php` | required (shipped `.htaccess` with `AllowOverride All`, or `nginx.conf.example`) |

3.3.x ran on PHP 7.2 and 3.4.x on PHP 7.4, so on those versions upgrade PHP first.

Run each update script with the client for your database, in the order listed, and stop at the
first error. Most scripts are not wrapped in a transaction, so if one stops halfway, restore the
backup, fix the cause and run the scripts again from that point:

```bash
# MySQL / MariaDB
mysql -u poweradmin -p poweradmin < sql/poweradmin-mysql-update-to-X.sql
# PostgreSQL (ON_ERROR_STOP makes psql stop and exit non-zero on an error)
psql -v ON_ERROR_STOP=1 -U poweradmin -d poweradmin -f sql/poweradmin-pgsql-update-to-X.sql
# SQLite
sqlite3 /path/to/pdns.db < sql/poweradmin-sqlite-update-to-X.sql
```

After copying the new files, delete the `install/` directory. Both 3.9.14 and 4.4.3 refuse to
show the login page while it exists.

### Within 3.x (to 3.9.14)

1. Back up the database and the installation directory.
2. Replace the files with the [3.9.14 release](https://github.com/poweradmin/poweradmin/releases/tag/v3.9.14),
   restore your `inc/config.inc.php`, merge any changes of your own into the shipped `.htaccess`,
   and delete `install/`. The configuration format does not change within 3.x, and options added
   in later 3.x releases have defaults in `inc/config-defaults.inc.php`; add one to your
   `inc/config.inc.php` only to change its default.
3. Run the update scripts from the 3.9.14 `sql/` directory for your starting version:

| You run | Scripts, in order |
|---------|-------------------|
| 3.0.x - 3.1.x | 3.2.0, 3.9.0, 3.9.7 |
| 3.2.0 - 3.8.x | 3.9.0, 3.9.7 |
| 3.9.0 - 3.9.6 | 3.9.7 |
| 3.9.7 - 3.9.13 | none |

### From 3.x to 4.4.3

4.1.0 and later no longer read `inc/config.inc.php` and do not ship the converter, so the
configuration is converted with a 4.0.x release on the way. You do not need to install 4.1, 4.2
or 4.3 in between.

1. Back up the database and the installation directory.
2. Run the 3.x scripts from the [table above](#within-3x-to-3914) for your starting version
   (take `3.9.7` from the 3.9.14 archive).
3. Unpack the [4.0.12 release](https://github.com/poweradmin/poweradmin/releases/tag/v4.0.12),
   copy your `inc/config.inc.php` into it and run `php config/migrate-config.php` there
   (see [v4.0.0](v4.0.0.md#configuration-migration)). Keep the resulting `config/settings.php`.
4. Run its `4.0.0`, `4.0.2` and `4.0.5` scripts.
5. Install the [4.4.3 release](https://github.com/poweradmin/poweradmin/releases/tag/v4.4.3) with
   the `config/settings.php` from step 3, delete `install/`, and make sure URL rewriting works.
6. Run its `4.1.0`, `4.2.0`, `4.3.0` and `4.4.0` scripts. On SQLite with the PowerDNS tables in
   the same file, also run `4.3.0-backfill` after `4.3.0` if you may later use API backend mode.

This route was tested in November 2026 on MySQL, PostgreSQL and SQLite with 3.3.0 and 3.9.7
databases and a converted 3.9.x configuration. A configuration from an older 3.x release may
use options the converter does not know; check `config/settings.php` afterwards.

Read [v4.1.0](v4.1.0.md) and [v4.2.0](v4.2.0.md) before step 6: 4.1.0 adds zone deletion
permissions to templates, and 4.2.0 renames the stock templates to Editor, Viewer and Guest.

### From 4.0 - 4.3 to 4.4.3

Install the [4.4.3 release](https://github.com/poweradmin/poweradmin/releases/tag/v4.4.3), keep
your `config/settings.php`, delete `install/`, and run the scripts for your starting version.
Take the scripts from the 4.4.3 `sql/` directory, not from the archive of each intermediate
release: on PostgreSQL the 4.1.0 and 4.2.0 scripts in the 4.1.0 and 4.2.0 archives fail with a
duplicate key error (see [v4.2.0](v4.2.0.md#postgresql-duplicate-key-in-the-420-script)).
The `4.0.5` script is only in the 4.0.x archives; take it from
[4.0.12](https://github.com/poweradmin/poweradmin/releases/tag/v4.0.12).

| You run | Scripts, in order |
|---------|-------------------|
| 4.0.0 - 4.0.1 | 4.0.2, 4.0.5, 4.1.0, 4.2.0, 4.3.0, 4.4.0 |
| 4.0.2 - 4.0.4 | 4.0.5, 4.1.0, 4.2.0, 4.3.0, 4.4.0 |
| 4.0.5 - 4.0.12 | 4.1.0, 4.2.0, 4.3.0, 4.4.0 |
| 4.1.x | 4.2.0, 4.3.0, 4.4.0 |
| 4.2.x | 4.3.0, 4.4.0 |
| 4.3.x | 4.4.0 |

Coming from 4.0.x or 4.1.x, PHP 8.2 is needed from 4.2.0 on, and 4.1.0 and later need URL
rewriting. On SQLite, run `4.3.0-backfill` after `4.3.0` if you may later use API backend mode.

## Unsupported Versions

Only the lines listed in [Version Support](../getting-started/lifecycle.md) get security fixes.
Poweradmin 2.x is the most exposed of the unsupported versions: its forms have no CSRF protection,
several pages print stored data without escaping, a logged-in user can change zones they do not
own, and a leftover `install/` directory can be used without logging in. Keep a 2.x installation
off the public internet and follow [Upgrading from 2.x](from-2x.md), which goes straight to 4.4.x.

## General Upgrade Instructions

When upgrading Poweradmin from any version to a newer one, follow these general steps:

1. **Backup your database** - This is critical before any upgrade
2. **Backup your existing files** - Make a complete backup of your current installation
3. **Check PHP** - 3.5.0 to 4.1.x need PHP 8.1 or later, 4.2.0 and later need PHP 8.2 or later
4. **Replace files** - Replace all files with the new version's files, merge your own changes into the shipped `.htaccess`, then delete the `install/` directory
5. **Restore configuration** - Depending on your version:
   - Staying on 3.x: restore `inc/config.inc.php` from your backup; nothing has to be converted
   - Moving from 3.x to 4.x: convert `inc/config.inc.php` with `php config/migrate-config.php`, which ships only in 4.0.x (see [From 3.x to 4.4.3](#from-3x-to-443))
   - Already on 4.x: restore `config/settings.php` from your backup
6. **Update database structure** - Run the update scripts the target version needs, in order (see the [Quick Path](#quick-path-to-a-supported-version))
7. **Test functionality** - Verify all features work correctly after upgrade

## Patch Version Upgrades (e.g., 4.4.x → 4.4.y)

For patch releases within the same minor version (e.g., 4.4.0 → 4.4.3, or 4.4.2 → 4.4.3), the upgrade process is straightforward:

1. **Backup your database and files** - Always a good practice
2. **Replace all application files** - Extract the new release over your existing installation
3. **Preserve your configuration** - Your `config/settings.php` (or `inc/config.inc.php` for older versions) remains unchanged
4. **Check release notes for SQL updates** - Only run database migration scripts if explicitly mentioned in the release notes for that version
5. **Clear PHP opcache** - If your environment uses opcache, restart PHP-FPM or your web server to clear cached bytecode:

    ```bash
    sudo systemctl restart php-fpm
    # or
    sudo systemctl restart apache2
    ```

6. **Verify functionality** - Test login and basic operations

**Key points for patch releases:**

- Patch releases maintain backward compatibility - no breaking changes
- Configuration format remains the same
- Database schema changes are rare in patch releases (but always check release notes)
- The same file replacement process applies as major upgrades

**Alternative: Symlink Strategy**

For easier rollbacks, consider using symlinks:

```bash
# Extract new version to versioned directory
tar -xzf v4.4.3.tar.gz -C /var/www/

# Update symlink to point to new version
ln -sfn /var/www/poweradmin-4.4.3 /var/www/poweradmin

# Keep config outside versioned directories
ln -s /etc/poweradmin/settings.php /var/www/poweradmin/config/settings.php
```

This allows quick rollback by simply changing the symlink back to the previous version.

## Upgrading a Docker or Docker Compose Deployment

The official image does not migrate an existing database. On startup the entrypoint loads the Poweradmin schema only into an empty database; a database created by an older version is left as it is. Upgrading a container therefore means: back up, switch the image tag, restart, and run the release's migration script yourself. The image ships the `sql/` directory together with the `psql`, `mysql` and `sqlite3` clients, and the `DB_*` variables are already in the container's environment, so the script can be run from inside the new container.

The examples below assume the Compose service names `poweradmin` and `postgres` (or `mysql`) and an upgrade from 4.3.x to 4.4.3. Adjust the names and the script version to your setup.

1. **Back up the database:**

    ```bash
    # PostgreSQL
    docker compose exec postgres pg_dump -U poweradmin poweradmin > poweradmin-before-4.4.sql

    # MySQL / MariaDB
    docker compose exec mysql mysqldump -u poweradmin -p poweradmin > poweradmin-before-4.4.sql
    ```

2. **Switch the image tag** in your Compose file (for example `poweradmin/poweradmin:4.4.3`), then pull and recreate only the application container:

    ```bash
    docker compose pull poweradmin
    docker compose up -d poweradmin
    ```

3. **Run the migration script from inside the new container:**

    ```bash
    # PostgreSQL
    docker compose exec poweradmin sh -c 'PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" ${DB_PORT:+-p "$DB_PORT"} -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 -f /app/sql/poweradmin-pgsql-update-to-4.4.0.sql'

    # MySQL / MariaDB
    docker compose exec poweradmin sh -c 'mysql -h "$DB_HOST" ${DB_PORT:+-P "$DB_PORT"} -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < /app/sql/poweradmin-mysql-update-to-4.4.0.sql'

    # SQLite (database file on the volume)
    docker compose exec poweradmin sh -c 'sqlite3 "${DB_FILE:-/db/pdns.db}" < /app/sql/poweradmin-sqlite-update-to-4.4.0.sql'
    ```

    If the password is supplied through a Docker secret (`DB_PASS__FILE`), `$DB_PASS` is not set in the `exec` shell; use `$(cat "$DB_PASS__FILE")` in its place.

    The image's MariaDB client requires TLS by default. If your database server does not offer TLS, the MySQL command stops with `TLS/SSL error: SSL is required, but the server does not support it`; add `--skip-ssl`.

4. **Check the application** - log in and open the zone templates and add zone pages.

Notes:

- Run one script per version, in order, and never skip a version. Coming from 4.2.x, run the 4.3.0 script before the 4.4.0 one. On SQLite with the PowerDNS tables in the same file, also run `sql/poweradmin-sqlite-update-to-4.3.0-backfill.sql` right after the 4.3.0 script if you may later switch the database to API backend mode; it fills in the zone names that mode reads.
- The `stable` and `latest` tags move between release lines at this release: `stable` now follows 4.4.x (it followed 4.3.x before) and `latest` follows 4.5.x. A Compose file on either tag jumps a minor version on the next pull and must run the update script for every minor version it crosses. Pin a version tag such as `4.4` or `4.4.3` to decide when you upgrade.
- Between the container restart and the migration, pages that read the new schema fail with "An error occurred while processing the request" (which pages depends on the release; for the 4.4.0 script, zone templates and add zone). The rest of the application keeps working, so the window is short but real; run the script right after the restart.
- Run each script once. The scripts are not idempotent: a second run stops with an error such as `column "is_default" of relation "zone_templ" already exists`, which is harmless but means the script was already applied.
- Patch releases (4.4.2 to 4.4.3) need no script unless their release notes say otherwise; switching the tag and restarting is enough.
- A volume-mounted `config/settings.php` is left untouched. Check the release notes for new settings or container variables you may want to set.

## Important Considerations

- Always read the release notes for the version you're upgrading to and any intermediate versions
- Neglecting to follow proper upgrade procedures may result in a non-functioning installation
- It's recommended to perform upgrades in a test environment first before applying to production
- After upgrading, check the system for any warnings or errors
- Verify that zones and records remain accessible and editable
- Coming from 3.x, zone owners carry over unchanged; groups are optional, see [User Groups](../user-guide/groups.md#coming-from-3x)
- Report any bugs or issues you encounter during the upgrade process

## Upgrade Path

The [Quick Path](#quick-path-to-a-supported-version) above covers 2.x, 3.x and 4.x installs in fewer steps. The list below shows every release with structural changes, for reference or for installs older than 2.1.7.

### Step-by-Step Path from 2.0.0

From 2.1.7 through 2.2.2, the shorter route in [Upgrading from 2.x](from-2x.md) installs 4.4.x
directly and runs the update scripts in order; it was tested from 2.1.7. For older versions
(e.g., 2.0.0), we recommend the following path:

1. 2.0.0 → 2.1.4 (Important database structure changes)
2. 2.1.4 → 2.2.2 (API integration changes)
3. 2.2.2 → 3.2.0 (DNSSEC implementation)
4. 3.2.0 → 3.9.14 (latest 3.x release; run the 3.9.0 and 3.9.7 update scripts)
5. 3.9.x → 4.0.12 (last 4.0.x release, complete architecture overhaul; run the 4.0.0, 4.0.2 and 4.0.5 update scripts and convert the configuration with `php config/migrate-config.php`, which ships only in 4.0.x - 4.1.0 and later no longer read `inc/config.inc.php`)
6. 4.0.12 → 4.1.0 (OIDC/SAML authentication, DNS wizards, permission improvements)
7. 4.1.0 → 4.2.0 (PHP 8.2 minimum, user groups, module system, BIND zone import/export)
8. 4.2.0 → 4.3.0 (PowerDNS API backend mode, zone metadata editor, separate API log table)
9. 4.3.0 → 4.4.x (Default zone template, PowerDNS capability detection, Views & Networks)
10. 4.4.x → 4.5.0 (Record change log, granular API keys, new permissions, API v1 removed)

Coming from 3.9.x (LTS until December 2027), upgrade to 4.4.x, the production line. Continue to 4.5.0 only if you want its features.

### Critical Versions with SQL Migrations

The following versions include important database structure changes:

- [v2.1.4](v2.1.4.md) - Added supermasters and domainmetadata tables
- [v3.0.0](v3.0.0.md) - Added cryptokeys table for DNSSEC
- [v3.2.0](v3.2.0.md) - Schema updates for PowerDNS API integration
- [v3.4.0](v3.4.0.md) - Added tsigkeys table
- [v3.9.7](v3.9.7.md) - Performance indexes on zones table
- [v4.0.0](v4.0.0.md) - Complete schema overhaul, including user management
- [v4.0.5](v4.0.5.md) - Primary key on records_zone_templ, PostgreSQL sequence fixes
- [v4.1.0](v4.1.0.md) - OIDC/SAML authentication, DNS wizards, zone deletion permissions, permission templates
- [v4.2.0](v4.2.0.md) - PHP 8.2 minimum, user groups, module system, BIND zone import/export
- [v4.3.0](v4.3.0.md) - PowerDNS API backend mode, zone metadata editor, separate API log table
- [v4.4.0](v4.4.0.md) - Default zone template (`zone_templ.is_default`), PowerDNS capability detection, Views & Networks for PowerDNS 5.0
- [v4.5.0](v4.5.0.md) - Serial policies (SOA-EDIT), record change log, granular API keys, log/metadata/ownership view permissions
- [v4.6.0](v4.6.0.md) (in development on the master branch) - Change approval workflow (`zone_change_requests` table, four permissions), template sharing with groups (`zone_templ_groups`), zone limits (`users.max_zones`, `user_groups.max_zones`), unique `users.username` index, UTC password reset expiry

### Recent Patch Releases

The following releases are bug fix updates. Unless marked otherwise, no special upgrade steps are required - simply replace files and preserve your configuration. Releases marked **requires SQL migration** need their `sql/` update script run first:

**v4.5.x Series:**

- **v4.5.1** (Oct 2026) - Zone and record access checked before reporting whether a zone or record exists, LDAP auto-provisioning reaches new users with a single login failure message, SAML responses refused unless they answer a sign-in started from the same browser, zone ids used for API zone addresses so classless reverse zones survive a decoding proxy, bulk add capped at 1000 lines and Add Record rows capped, DNSSEC records PowerDNS generates skipped on zone import, v2 dynamic DNS lowercases the hostname, non-numeric `DB_PORT` rejected in Docker, record change email addon shipped in the image. No database migration

**v4.4.x Series:**

- **v4.4.3** (Oct 2026) - Zone access checked before zones, records and catalog zones are reported as missing, SAML responses tied to the browser that started the sign-in, bulk add and Add Record caps, API zone addressing by PowerDNS zone id, a deleted user's zones kept when handed to a new owner in API backend mode, PostgreSQL permission sequences resynced in the 4.1.0 and 4.2.0 update scripts, non-numeric `DB_PORT` rejected in Docker. No database migration

- **v4.4.2** (Oct 2026) - Creating a zone inside a zone owned by another user is now refused by the new setting `dns.parent_zone_ownership_check`, on by default (see [Zone Overlap Protection](../configuration/dns-settings.md#zone-overlap-protection)). Also: new users only get a permission template within the creator's permissions, record comments sync to the related A or PTR record only in zones the user may edit, installer IP allow-list matches IPv6, dynamic DNS treats array query parameters as missing, username rename duplicate check fixed, MFA verified against the account that is signing in, exact email match for password reset, sendmail header line breaks refused, STARTTLS enforced when mail requires TLS, startup refused with the removed `md5` or `md5salt` password encryption, unknown record types and malformed RFC 3597 data refused, disabled accounts refused at OIDC and SAML login, opt-in strict session gates and single-use reset links, MFA setup and zone search paging fixes, Docker waits for the database before schema setup (`DB_WAIT_TIMEOUT`) and the `stable` tag now follows 4.4.x. API zone rename in SQL backend mode is refused. No database migration
- **v4.4.1** (Sep 2026) - Same fixes as v4.3.5 for the 4.4.x line, plus dynamic DNS routing each `myip` address to its own record family, bulk record paths matched before single-record lookup, the PowerDNS metrics URL derived from `pdns_api.url`, and container variables for the 4.4.0 settings. No database migration

**v4.3.x Series:**

- **v4.3.7** (Oct 2026) - A deleted user's zones kept when handed to a new owner in API backend mode, PostgreSQL permission sequences resynced in the 4.1.0 and 4.2.0 update scripts, dependency and base image updates. No database migration
- **v4.3.6** (Oct 2026) - Creating a zone inside a zone owned by another user is now refused by the new setting `dns.parent_zone_ownership_check`, on by default (see [Zone Overlap Protection](../configuration/dns-settings.md#zone-overlap-protection)). Also the v4.4.2 fixes that apply to 4.3.x, except the Docker database wait, plus fixes 4.4.x already had: global zone templates limited to superusers, `zone_content_edit_others` needed to assign a new zone to another user, the last owner of a zone can no longer be removed, IPv6 addresses matched in the login allow and deny lists, password reset declined for an email shared by several accounts, auth-critical fields kept out of user self-edit, API zone rename in SQL backend mode refused. The Docker `stable` tag no longer follows 4.3.x. No database migration
- **v4.3.5** (Sep 2026) - Same fixes as v4.2.6 for the 4.3.x line, plus LUA records restricted for client-level editors on every surface, one canonical zone id in API backend mode, and container config generation that escapes secrets and emits valid booleans. No database migration
- **v4.3.4** (Jul 2026) - User management and SSO account hardening, `max_input_vars` form fixes for large zones and groups, record/log/template binding fixes, MariaDB 11.6+ record search fix, per-zone logs button (**requires MySQL migration**: `sql/poweradmin-mysql-update-to-4.3.4.sql`, which the 4.4.0 and later scripts include; PostgreSQL/SQLite unaffected)
- **v4.3.3** (Jun 2026) - Permission and authorization hardening across API and DNSSEC, API-backend mode polish (record ordering, dashboard resilience), template sync correctness, Docker schema initialization
- **v4.3.2** (May 2026) - API-mode zone handling (reverse zone owner display, DNSSEC status on forward zones, record counts from PowerDNS, zone kind sync), template fixes (correct sync column, preserved spaces, API-mode safe), `X-Forwarded-For` header trust scoped to private peers, group-owned zone control visibility, DNSSEC sign events in activity feed
- **v4.3.1** (Apr 2026) - Patch release for 4.3.x line

**v4.2.x Series:**

- **v4.2.8** (Oct 2026) - PostgreSQL permission sequences resynced in the 4.1.0 and 4.2.0 update scripts, dependency and base image updates. No database migration
- **v4.2.7** (Oct 2026) - Creating a zone inside a zone owned by another user is now refused by the new setting `dns.parent_zone_ownership_check`, on by default (see [Zone Overlap Protection](../configuration/dns-settings.md#zone-overlap-protection)). Also the v4.3.6 fixes that apply to 4.2.x, plus LUA records restricted to editors above client level. No database migration
- **v4.2.6** (Sep 2026) - `interface.application_url` required for OIDC, SAML and password reset; Docker containers with SSO enabled refuse to start without a URL source; API user creation without `perm_templ` no longer yields an administrator; deactivating a user revokes their API keys; zone template records validated on save; five confirmation flows moved to POST (re-sync forked themes). No database migration
- **v4.2.5** (Jul 2026) - Same fixes as v4.3.4 for the 4.2.x line (**requires MySQL migration**: `sql/poweradmin-mysql-update-to-4.2.5.sql`; PostgreSQL/SQLite unaffected)
- **v4.2.4** (Jun 2026) - Same fixes as v4.3.3 for the 4.2.x line
- **v4.2.3** (May 2026) - `X-Forwarded-For` header trust scoped to private peers, group-owned zone control visibility, PostgreSQL `record_comment_links` strict-typing fix, bulk record CSV escaping, CNAME validator accepts numeric-string IDs, API record edits honor `zone_content_edit_own_as_client`, Users API `auth_method`/`use_ldap` sync, zone template column and content-listing fixes
- **v4.2.2** (Apr 2026) - Patch release for 4.2.x line
- **v4.2.1** (Apr 2026) - Patch release for 4.2.x line

**v4.1.x Series:**

- **v4.1.5** (Oct 2026) - Docker image only: FrankenPHP updated to 1.13.2 with PHP 8.4.27, exec-form health check. No database migration
- **v4.1.4** (May 2026) - Record search fix for an ambiguous `ORDER BY` column
- **v4.1.3** (Apr 2026) - Duplicate SOA serial increment on inline record add, comment search query referencing a non-existent table, plural-form headers and missing format specifiers in several locales
- **v4.1.2** (Mar 2026) - xmlseclibs updated to 3.1.5 (CVE-2026-32313), SSO fixes (default permission template applied to new users only, `auth_method` preserved on edit, OIDC groups read from the ID token), Docker entrypoint fixes for `PA_LOGGING_*` and volume-mounted config
- **v4.1.1** (Feb 2026) - DNSSEC fix for RFC 2317 reverse zones, login routing fix, IPv6 supermaster validation, LUA record handling, CSRF token fix, zone apex (`@`) symbol fix in multi-record form

**v4.0.x Series:**

- **v4.0.12** (Oct 2026) - Docker image only: FrankenPHP updated to 1.13.2 with PHP 8.4.27, exec-form health check. No database migration
- **v4.0.11** (May 2026) - Record search fix for an ambiguous `ORDER BY` column
- **v4.0.10** (Apr 2026) - Duplicate SOA serial increment on inline record add, format specifiers and plural headers across all locales
- **v4.0.9** (Mar 2026) - Zone creation API validates the template as a numeric ID, sign-zone button separated from the edit form to prevent accidental signing, Docker entrypoint fixes for volume-mounted config, light theme gradient fix
- **v4.0.7** (Feb 2026) - CSRF token fix for DNSSEC key deletion, MFA TOTP secret reuse fix, IPv6 supermaster validation, LUA record handling, zone apex (`@`) symbol fix
- **v4.0.6** (Jan 2026) - Zone deletion fixes, IPv6 PTR handling, MySQL SSL disabled by default for backwards compatibility
- **[v4.0.5](v4.0.5.md)** (Jan 2026) - Database compatibility (primary key fix), PostgreSQL sequence sync, PHP 8.4 fixes, new `show_forward_zone_associations` option (**requires SQL migration**)
- **v4.0.4** (Nov 2025) - LDAP+MFA fixes, automatic TXT record splitting, DNSSEC zone signing fixes
- **v4.0.3** (Oct 2025) - SOA serial updates on record operations, API pagination, dark mode fixes
- **v4.0.2** (Sep 2025) - MySQL strict mode compatibility, SPF validation, SMTP fixes
- **v4.0.1** (Aug 2025) - Docker MySQL config, v3.9.2→v4.0.0 migration fixes, LDAP form restoration

**v3.9.x Series (LTS):**

- **v3.9.14** (Oct 2026) - Dependency and base image updates only. No database migration
- **v3.9.13** (Oct 2026) - Creating a zone inside a zone owned by another user is now refused, on by default; turn it off with `$dns_parent_zone_ownership_check = false;` in `inc/config.inc.php` (see [Zone Overlap Protection](../configuration/dns-settings.md#zone-overlap-protection)). Also: new users only get a permission template within the creator's permissions, record comments sync to the related A or PTR record only in zones the user may edit, `zone_content_edit_others` needed to assign a new zone to another user, delegated managers can no longer edit superusers, LUA records limited to editors above client level, client-level editors can no longer delete NS records, control characters refused in records, SameSite set on the session cookie, installer IP allow-list matched by address family and prefix, dynamic DNS array parameter and username rename fixes, DNSSEC key management gated on the zone edit permission, template assignment needs `user_edit_templ_perm`, TLD data refreshed. `.htaccess` now ships in the archive, so merge your own before overwriting. No database migration
- **v3.9.12** (Sep 2026) - Permission checks on template, user and zone changes; template, supermaster and DNSSEC key changes require a confirmed POST; login timing equalised; session key warning distinguishes the shipped default; log and error output escaped; public suffix and TLD data refreshed. No database migration
- **v3.9.11** (Jul 2026) - Record edits and log entries bound to the record's real zone, duplicate email rejection, dependency updates
- **v3.9.10** (Mar 2026) - Translation updates for all locales
- **v3.9.9** (Jan 2026) - Allow HTML characters in TXT records, fix record name handling
- **v3.9.8** (Jan 2026) - CSRF protection, PostgreSQL fixes, API error handling improvements
- **v3.9.6** (Oct 2025) - CAA record validation support
- **v3.9.5** (Jul 2025) - MySQL ONLY_FULL_GROUP_BY compatibility fix
- **v3.9.4** (Jul 2025) - Configurable pagination rows per page

## Long-Term Support (LTS)

4.4.x and 3.9.x are LTS until December 2027. 4.2.x and 4.3.x reach end of life on
2027-01-31. See [Version Support](../getting-started/lifecycle.md) for every release line,
the support rules and the PHP range of each line.

## Troubleshooting

If you encounter issues during or after an upgrade:

1. Check the PHP and web server error logs
2. Verify database connectivity and permissions
3. Ensure file permissions are set correctly
4. Review the specific upgrade instructions for the version you're upgrading to

### Which update scripts have already run?

Poweradmin does not record the schema version in the database (the `migrations`
table that some scripts create is never written to), so on an inherited or
long-neglected installation you have to work it out from what each script adds.
Check the markers below from the top; the first one that is missing tells you
which script to run first. Then run every later script in order.

| Script | Marker that shows it has run |
|--------|------------------------------|
| 2.1.5 | column `zones.zone_templ_id` |
| 2.1.7 | table `records_zone_templ`, column `users.use_ldap` |
| 3.2.0 | tables `log_users`, `log_zones` |
| 3.9.0 | none (widens a column type only; safe to re-run) |
| 4.0.0 | tables `user_mfa`, `api_keys`, `login_attempts`, column `zone_templ.created_by` |
| 4.0.2 | none (changes a column type only; safe to re-run) |
| 4.1.0 | column `users.auth_method`, tables `oidc_user_links`, `saml_user_links` |
| 4.2.0 | tables `user_groups`, `zones_groups`, column `perm_templ.template_type` |
| 4.3.0 | columns `zones.zone_name`, `zones.zone_type`, `users.perm_templ_source`, table `log_api` |
| 4.4.0 | column `zone_templ.is_default` |
| 4.5.0 | columns `api_keys.is_readonly`, `login_attempts.attempt_type`, table `log_record_changes` |
| 4.6.0 | tables `zone_change_requests`, `zone_templ_groups` |

To check a column or table:

```sql
-- MySQL/MariaDB
SHOW COLUMNS FROM zones LIKE 'zone_name';
SHOW TABLES LIKE 'log_api';

-- PostgreSQL (psql)
\d zones
\dt log_api

-- SQLite
PRAGMA table_info(zones);
.tables log_api
```

Do not re-run a script whose marker is already present. Scripts up to 4.0.0
have no `IF NOT EXISTS` guards and stop at the first duplicate column or table,
which can leave the rest of that script unapplied. Take a dump before you start.
