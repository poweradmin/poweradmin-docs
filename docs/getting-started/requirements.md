# Poweradmin System Requirements

## Overview

Poweradmin requires PHP 8.2 or higher to run. This document outlines the supported Linux and BSD distributions as well
as those that are not supported due to PHP version constraints. For the best experience, ensure your system meets or
exceeds the recommended requirements.

---

## Minimum Requirements

- **PHP**: 8.2 or higher (including 8.3, 8.4, 8.5)
- **PHP Extensions**:
    - `intl`
    - `gettext`
    - `openssl`
    - `filter`
    - `tokenizer`
    - `xml`
    - `pdo`
    - One of:
        - `pdo-mysql`
        - `pdo-pgsql`
        - `pdo-sqlite`
    - `ldap` (optional)
- **Database**: MariaDB 10.6+, MySQL 8.x, PostgreSQL, or SQLite
- **PowerDNS**: PowerDNS Authoritative Server 4.x or 5.x, tested from 4.5
- **Web Server**: Apache or NGINX
- **Operating System**: Linux or BSD

> **Note**: Other web server software, such as Caddy, might also be supported. However, these are usually not tested by
> the maintainer and may only work with help from the community.

### Web Server URL Rewriting

Starting with Poweradmin 4.1.0, URL rewriting is **required** for all web servers. Poweradmin uses clean URLs (e.g., `/login` instead of `index.php?page=login`), which require the web server to route all requests through `index.php`.

| Web Server | Requirement | How to Enable |
|------------|-------------|---------------|
| **Apache** | `mod_rewrite` enabled + `AllowOverride All` | `a2enmod rewrite` and set `AllowOverride All` in VirtualHost |
| **Nginx** | `try_files` directive | Use the provided [nginx.conf.example](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example) |
| **Caddy** | `try_files` directive | Use the provided [caddy.conf.example](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) |

The included `.htaccess` file handles routing automatically for Apache. For Nginx and Caddy, use the example configuration files from the repository.

> **Warning:** If you see 404 errors when accessing pages like `/login` or `/zones`, your web server is not routing requests to `index.php`. For Apache, ensure `mod_rewrite` is enabled and `AllowOverride All` is set. For Nginx/Caddy, verify your configuration matches the provided examples.

> **Note:** Poweradmin 4.0.x and earlier do not require URL rewriting for basic functionality, only for API support.

---

## Supported Platforms

PHP versions, PowerDNS versions and the Linux distributions Poweradmin runs on, with their support
dates and how to get a newer PHP or PowerDNS, are listed on [Version Support](lifecycle.md).

---

## BSD Operating Systems

Poweradmin is compatible with BSD operating systems that meet the PHP 8.2+ requirement. While not extensively tested, it
should work as long as the environment is properly configured.

FreeBSD 14.4 and the 15.x series carry PHP 8.3, 8.4 and 8.5 in the ports tree, with 8.4 as the
current default. `lang/php82` is deprecated and scheduled for removal on 2026-12-31, so install
`php84` rather than PHP 8.2 on a new system. See the [FreeBSD installation guide](../installation/freebsd.md)
for the package names, paths and service commands, which differ from the Linux guides.

---

## Tested Environments

Poweradmin has been tested with the following software combinations:

| Poweradmin | PHP            | PowerDNS | MariaDB  | MySQL  | PostgreSQL | SQLite |
|------------|----------------|----------|----------|--------|------------|--------|
| 4.5.x      | 8.2            | 5.1.4    | 10.11    | -      | 16.11      | -      |
| 4.4.x      | 8.2            | 4.9.12   | 10.11    | -      | 16.11      | -      |
| 4.3.x      | 8.2            | 4.9.12   | 10.11    | -      | 16.11      | -      |
| 4.2.x      | 8.2            | 4.9.12   | 10.11    | -      | 16.11      | -      |
| 4.1.x      | 8.2            | 4.9.12   | 10.11    | -      | 16.11      | -      |
| 4.0.x      | 8.2.29         | 4.9.5    | 10.11.15 | -      | 16.3       | 3.51.1 |
| 3.9.x      | 8.1.31         | 4.7.4    | 10.11.10 | 9.1.0  | 16.3       | 3.45.3 |
| 3.8.x      | 8.1.28         | 4.5.5    | 10.11.8  | -      | 16.3       | 3.45.3 |
| 3.7.x      | 8.1.2          | 4.5.3    | 11.1.2   | 8.2.0  | 16.0       | 3.40.1 |
| 3.6.x      | 8.1.2          | 4.5.3    | 11.1.2   | 8.1.0  | 16.0       | 3.40.1 |
| 3.5.x      | 8.1.17         | 4.5.3    | 10.11.2  | 8.0.32 | 15.2       | 3.34.1 |
| 3.4.x      | 7.4.3 / 8.1.12 | 4.2.1    | 10.10.2  | 8.0.31 | 15.1       | 3.34.1 |

---

## PowerDNS Compatibility

### Supported PowerDNS Versions

Poweradmin manages the PowerDNS Authoritative Server only; the PowerDNS Recursor is not managed.

Poweradmin supports **PowerDNS Authoritative Server 4.x and 5.x**. It is tested from 4.5 onward.
Versions 4.0-4.4 are expected to work but are not tested, and all of them are end of life upstream.
See [Version Support](lifecycle.md) for PowerDNS and distribution support dates.

### Tested PowerDNS Versions

The development environment of 4.5.x and newer runs PowerDNS 5.1 by default and can switch to
4.5, 4.6, 4.7, 4.8, 4.9 or 5.0. Versions older than 4.5 are not tested. See
[Tested Environments](#tested-environments) for each release line.

### Features That Need a Newer PowerDNS

Poweradmin reads the PowerDNS version through the API and hides features the server does not
support. Everything else works on any supported version.

| PowerDNS | Features                                                                                           |
|----------|----------------------------------------------------------------------------------------------------|
| 4.4      | SVCB, HTTPS and APL records                                                                        |
| 4.5      | CSYNC, NID, L32, L64 and LP records; ED448 DNSSEC keys                                              |
| 4.6      | Autoprimary management in API backend mode                                                         |
| 4.7      | Catalog zones (Producer and Consumer)                                                              |
| 4.8      | ZONEMD records                                                                                     |
| 5.0      | [Views and networks](../user-guide/views-networks.md) (LMDB backend only); RFC 9615 DNSSEC bootstrapping |
| 5.1      | RESINFO, WALLET, HHIT and BRID records; `dohpath`, `ohttp` and `tls-supported-groups` SVCB parameters |

### API Backend Mode

API backend mode (`dns.backend = api`) works on any supported version, but it is
noticeably faster from **PowerDNS 5.0** onward:

- **5.0+**: record edits and comment reads fetch only the RRset they need, and zone lists with the record count column hidden fetch only the SOA record. Older servers leave disabled records out of these narrowed reads, so Poweradmin fetches the whole zone instead.
- **4.3+**: zone lists skip the per-zone DNSSEC lookup when no column needs it.

Nothing breaks on older versions, so this is a performance recommendation, not a requirement.

### Why Poweradmin Has Broad PowerDNS Compatibility

Poweradmin maintains compatibility across PowerDNS versions due to its architectural design:

- **Database-level operations**: Most Poweradmin operations work directly with the PowerDNS database schema, which remains relatively stable across versions
- **PowerDNS API integration**: The PowerDNS API is used specifically for DNSSEC operations, providing modern functionality while maintaining backward compatibility
- **Minimal version-specific dependencies**: The core DNS management features don't rely on version-specific PowerDNS features

### PowerDNS Version Recommendations

For production, prefer a PowerDNS version that still gets upstream fixes. See
[Version Support](lifecycle.md#powerdns) for the current status of each PowerDNS release.
