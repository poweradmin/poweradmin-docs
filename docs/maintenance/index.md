# Maintenance Guide

This section provides guidance on maintaining your Poweradmin installation and ensuring its long-term performance and security.

## Regular Maintenance Tasks

### Database Maintenance

Regular database maintenance helps keep your Poweradmin installation running smoothly:

#### MySQL/MariaDB

```sql
-- Optimize tables to reclaim space and improve performance
OPTIMIZE TABLE users;
OPTIMIZE TABLE zones;
OPTIMIZE TABLE records;
OPTIMIZE TABLE domains;
OPTIMIZE TABLE supermasters;
OPTIMIZE TABLE domainmetadata;

-- Analyze tables to update statistics for the query optimizer
ANALYZE TABLE users;
ANALYZE TABLE zones;
ANALYZE TABLE records;
ANALYZE TABLE domains;
ANALYZE TABLE supermasters;
ANALYZE TABLE domainmetadata;
```

#### PostgreSQL

```sql
-- Update statistics
VACUUM ANALYZE users;
VACUUM ANALYZE zones;
VACUUM ANALYZE records;
VACUUM ANALYZE domains;
VACUUM ANALYZE supermasters;
VACUUM ANALYZE domainmetadata;
```

#### SQLite

```sql
-- Rebuild the database to optimize performance
VACUUM;
```

### Log Management

To prevent logs from consuming excessive disk space:

1. **Database Logs**: Implement a log rotation strategy for Poweradmin's database logs. Check
    your legal retention period first: the Swiss data protection ordinance (DSV Art. 4) asks for at
    least one year of logs of automated processing, and audit frameworks such as PCI DSS 10.5 also
    ask for one year. The example keeps 365 days:

    ```sql
    -- Example log cleanup (retain the last 365 days), MySQL/MariaDB syntax
    DELETE FROM log_users WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    DELETE FROM log_zones WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    DELETE FROM log_groups WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    DELETE FROM log_changesets WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    DELETE FROM log_record_changes WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    DELETE FROM log_api WHERE created_at < DATE_SUB(NOW(), INTERVAL 365 DAY);
    ```

    On PostgreSQL use `created_at < NOW() - INTERVAL '365 days'`; on SQLite use `created_at < datetime('now', '-365 days')`. Rows in `log_api` can also be pruned automatically with `logging.api_log_retention_days` (added in 4.5.0).

2. **A copy outside the database**: the log tables live in the same database that Poweradmin
    writes to, so anyone with its credentials can change or delete them. Enable syslog
    (`logging.syslog_enabled`) and forward it to a central or append-only collector (rsyslog,
    journald remote, a SIEM) so the audit trail survives. `log_changesets` and `log_record_changes`
    are not sent to syslog; back them up with the database.

3. **System Logs**: Configure log rotation for your web server and PHP logs:

    ```
    # Example logrotate configuration (/etc/logrotate.d/poweradmin)
    /var/log/apache2/poweradmin-*.log {
        rotate 14
        daily
        compress
        delaycompress
        missingok
        notifempty
        create 640 www-data adm
    }
    ```

### Backup Procedures

#### Database Backup

Regular database backups are essential:

```bash
# MySQL/MariaDB backup
mysqldump -u username -p --opt powerdns > powerdns_$(date +%Y%m%d).sql

# PostgreSQL backup
pg_dump -U username powerdns > powerdns_$(date +%Y%m%d).sql

# SQLite backup
sqlite3 poweradmin.sqlite .dump > poweradmin_$(date +%Y%m%d).sql
```

If PowerDNS uses a separate database (`database.pdns_db_name`), back it up too. With the PowerDNS
API backend, zones and DNSSEC keys live in PowerDNS, so back up PowerDNS itself as well.

#### Configuration Backup

Back up your Poweradmin configuration files. `config/settings.php` holds the session key and the
database, LDAP, OIDC and SMTP secrets in plain text, so encrypt the archive:

```bash
# Create an encrypted archive of the configuration files
tar -czf - /path/to/poweradmin/config/ | gpg --symmetric --cipher-algo AES256 -o poweradmin_config_$(date +%Y%m%d).tar.gz.gpg
```

#### Restoring and testing

A backup only counts once a restore has worked. Restore into a test instance regularly:

1. Load the database dump into an empty database (`mysql powerdns < powerdns_YYYYMMDD.sql`, `psql`, or `sqlite3 poweradmin.sqlite < poweradmin_YYYYMMDD.sql`).
2. Restore `config/settings.php` and point it at the test database.
3. Run the same Poweradmin version that made the backup, sign in, and check zones and logs.
4. Only then upgrade, if the restore is part of a move to a newer version.

Backups and syslog copies keep personal data (user names, email addresses, IP addresses) after it
is deleted in Poweradmin. Give them a retention period too (see [Personal Data and Privacy](../configuration/privacy.md)).

### Security Updates

1. **Poweradmin Updates**: Regularly check for and apply updates to Poweradmin
2. **Dependency Updates**: Keep PHP, web server, and other components updated
3. **Security Scans**: Periodically scan for vulnerabilities using tools like OWASP ZAP

## Monitoring

### Health Endpoints *(v4.5.0+)*

Poweradmin can expose an unauthenticated readiness endpoint at `/api/health` and a liveness
endpoint at `/ping`, so a monitoring system notices a dead database or an unreachable
PowerDNS API before a user does. Both are disabled by default. See
[Health Checks](../operations/health-checks.md).

### Performance Monitoring

Monitor system resource usage:

1. **Database Query Performance**: Enable slow query logging temporarily to identify performance bottlenecks
2. **Web Server Performance**: Monitor response times and resource utilization
3. **Disk Space**: Set up alerts for low disk space conditions

### Error Monitoring

Regularly check error logs for issues:

```bash
# Check Poweradmin-related PHP errors
grep -i "poweradmin" /var/log/php/error.log

# Check web server errors
grep -i "poweradmin" /var/log/apache2/error.log
```

## Routine Checks

Establish a routine maintenance schedule:

- **Daily**: Check for errors in logs
- **Weekly**: Monitor database size and performance
- **Monthly**: Run database optimization, prune old logs
- **Quarterly**: Test backups by performing a restore
- **Bi-annually**: Review user accounts and permissions

The built-in [Database Consistency Check](consistency-check.md) covers most of the structural
problems worth looking for - orphaned records, zones without owners or an SOA, and slave zones
with no master.

## Disaster Recovery

Prepare for potential system failures:

1. **Recovery Plan**: Document step-by-step recovery procedures
2. **Test Restores**: Regularly test your backup and restore procedures
3. **Alternate Access**: Ensure DNS records can be managed directly via PowerDNS if Poweradmin becomes unavailable

For more detailed guidance on specific maintenance tasks, refer to the other sections in this documentation.