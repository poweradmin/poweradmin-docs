# Upgrading Poweradmin

## General Upgrade Instructions

When upgrading Poweradmin from any version to a newer one, follow these general steps:

1. **Backup your database** - This is critical before any upgrade
2. **Backup your existing files** - Make a complete backup of your current installation
3. **Replace files** - Replace all files with the new version's files
4. **Restore configuration** - Depending on your version:
   - For versions < 4.x: Restore `inc/config.inc.php` from your backup
   - For versions ≥ 4.x: Restore `config/settings.php` from your backup
5. **Update database structure** - If required by the specific version upgrade
6. **Test functionality** - Verify all features work correctly after upgrade

## Patch Version Upgrades (e.g., 4.0.x → 4.0.y)

For patch releases within the same minor version (e.g., 4.0.0 → 4.0.3, or 4.0.3 → 4.0.4), the upgrade process is straightforward:

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
tar -xzf poweradmin-4.0.4.tar.gz -C /var/www/

# Update symlink to point to new version
ln -sfn /var/www/poweradmin-4.0.4 /var/www/poweradmin

# Keep config outside versioned directories
ln -s /etc/poweradmin/settings.php /var/www/poweradmin/config/settings.php
```

This allows quick rollback by simply changing the symlink back to the previous version.

## Important Considerations

- Always read the release notes for the version you're upgrading to and any intermediate versions
- Neglecting to follow proper upgrade procedures may result in a non-functioning installation
- It's recommended to perform upgrades in a test environment first before applying to production
- After upgrading, check the system for any warnings or errors
- Verify that zones and records remain accessible and editable
- Report any bugs or issues you encounter during the upgrade process

## Upgrade Path

If you're upgrading across multiple major versions, it's often safest to upgrade incrementally through each major version rather than jumping directly to the latest version.

### Recommended Path from 2.0.0 to 4.1.0

If you're upgrading from a very old version (e.g., 2.0.0) to the latest 4.1.0, we recommend the following path:

1. 2.0.0 → 2.1.4 (Important database structure changes)
2. 2.1.4 → 2.2.2 (API integration changes)
3. 2.2.2 → 3.2.0 (DNSSEC implementation)
4. 3.2.0 → 3.9.3 (Security improvements)
5. 3.9.3 → 4.0.0 (Complete architecture overhaul)
6. 4.0.0 → 4.1.0 (Migration system removal and modernization)

### Critical Versions with SQL Migrations

The following versions include important database structure changes:

- [v2.1.4](v2.1.4.md) - Added supermasters and domainmetadata tables
- [v3.0.0](v3.0.0.md) - Added cryptokeys table for DNSSEC
- [v3.2.0](v3.2.0.md) - Schema updates for PowerDNS API integration
- [v3.4.0](v3.4.0.md) - Added tsigkeys table
- [v3.9.7](v3.9.7.md) - Performance indexes on zones table
- [v4.0.0](v4.0.0.md) - Complete schema overhaul, including user management
- [v4.0.5](v4.0.5.md) - Primary key on records_zone_templ, PostgreSQL sequence fixes
- [v4.1.0](v4.1.0.md) - Migration system removal and cleanup

### Recent Patch Releases

The following releases are bug fix updates with no special upgrade steps required. Simply replace files and preserve your configuration:

**v4.0.x Series:**

- **[v4.0.5](v4.0.5.md)** (Jan 2025) - Database compatibility (primary key fix), PostgreSQL sequence sync, PHP 8.4 fixes, new `show_forward_zone_associations` option (**requires SQL migration**)
- **v4.0.4** (Nov 2024) - LDAP+MFA fixes, automatic TXT record splitting, DNSSEC zone signing fixes
- **v4.0.3** (Oct 2024) - SOA serial updates on record operations, API pagination, dark mode fixes
- **v4.0.2** (Oct 2024) - MySQL strict mode compatibility, SPF validation, SMTP fixes
- **v4.0.1** (Aug 2024) - Docker MySQL config, v3.9.2→v4.0.0 migration fixes, LDAP form restoration

**v3.9.x Series (LTS):**

- **v3.9.8** (Jan 2025) - CSRF protection, PostgreSQL fixes, API error handling improvements
- **v3.9.6** (Oct 2024) - CAA record validation support
- **v3.9.5** (Jul 2024) - MySQL ONLY_FULL_GROUP_BY compatibility fix
- **v3.9.4** (Jul 2024) - Configurable pagination rows per page

## Troubleshooting

If you encounter issues during or after an upgrade:

1. Check the PHP and web server error logs
2. Verify database connectivity and permissions
3. Ensure file permissions are set correctly
4. Review the specific upgrade instructions for the version you're upgrading to
