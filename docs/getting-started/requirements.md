# Poweradmin System Requirements

## Overview

Poweradmin requires PHP 8.1 or higher to run. This document outlines the supported Linux and BSD distributions as well
as those that are not supported due to PHP version constraints. For the best experience, ensure your system meets or
exceeds the recommended requirements.

---

## Minimum Requirements

- **PHP**: 8.1 or higher (including 8.2, 8.3, 8.4, etc.)

> **PHP 8.1 Deprecation Notice:** Poweradmin **4.1.x will be the last version to support PHP 8.1**. Starting with version 4.2.x, the minimum required PHP version will be **8.2**. Users on PHP 8.1 should plan their PHP upgrade accordingly.
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
- **Database**: MySQL 5.7.x/8.x, MariaDB, PostgreSQL, or SQLite
- **PowerDNS**: PowerDNS authoritative server 4.0.0+ (including 4.x and 5.x series)
- **Web Server**: Apache or NGINX
- **Operating System**: Linux or BSD

> **Note**: Other web server software, such as Caddy, might also be supported. However, these are usually not tested by
> the maintainer and may only work with help from the community.

---

## Supported Distributions

| Distribution  | PHP Version | Notes                      |
|---------------|-------------|----------------------------|
| Debian 12.7   | 8.2         |                            |
| Ubuntu 22.04  | 8.1         |                            |
| Ubuntu 24.04  | 8.3         |                            |
| Fedora 40     | 8.3         | Apache included by default |
| Fedora 41     | 8.3         | Apache included by default |
| OpenSuse 15.6 | 8.2         |                            |

---

## BSD Operating Systems

Poweradmin is compatible with BSD operating systems that meet the PHP 8.1+ requirement. While not extensively tested, it
should work as long as the environment is properly configured.

---

## Unsupported Distributions

| Distribution            | PHP Version | Reason for Lack of Support |
|-------------------------|-------------|----------------------------|
| Debian 11               | 7.4         | PHP below minimum version  |
| Ubuntu 20.04            | 7.4         | PHP below minimum version  |
| CentOS Stream release 9 | 8.0         | PHP below minimum version  |
| Rocky 8.10              | 7.2         | PHP below minimum version  |
| Rocky 9.4               | 8.0         | PHP below minimum version  |
| Alma 8.10               | 7.2         | PHP below minimum version  |
| Alma 9.4                | 8.0         | PHP below minimum version  |

---

## Notes

- Distributions listed as unsupported can potentially be configured manually with a custom PHP build, but this is not
  officially supported.

- Upgrade paths are recommended for unsupported distributions to maintain security and compatibility.

## Tested Environments

Poweradmin has been tested with the following software combinations:

| Poweradmin | PHP            | PowerDNS | MariaDB  | MySQL  | PostgreSQL | SQLite |
|------------|----------------|----------|----------|--------|------------|--------|
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

Poweradmin officially supports **PowerDNS Authoritative Server 4.0.0 and newer**, including:

- **PowerDNS 4.x series** (4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9)
- **PowerDNS 5.x series** (5.0 and newer)

### Community-Reported Compatibility

While official testing is conducted with PowerDNS 4.7.4, community users have successfully reported using Poweradmin with:

- PowerDNS 4.8.x
- PowerDNS 4.9.x
- PowerDNS 5.0.x and newer

### Why Poweradmin Has Broad PowerDNS Compatibility

Poweradmin maintains compatibility across PowerDNS versions due to its architectural design:

- **Database-level operations**: Most Poweradmin operations work directly with the PowerDNS database schema, which remains relatively stable across versions
- **PowerDNS API integration**: The PowerDNS API is used specifically for DNSSEC operations, providing modern functionality while maintaining backward compatibility
- **Minimal version-specific dependencies**: The core DNS management features don't rely on version-specific PowerDNS features

### PowerDNS Version Recommendations

For production environments, consider:

- **PowerDNS 4.8.x**: Supported until March 2025 (critical fixes only)
- **PowerDNS 4.9.x**: Supported until September 2025 (critical fixes only)
- **PowerDNS 5.0.x and newer**: Current stable branch with active support

Refer to the [PowerDNS End of Life (EOL) schedule](https://doc.powerdns.com/authoritative/appendices/EOL.html) for the latest support information.
