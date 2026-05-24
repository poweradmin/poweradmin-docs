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
- **Database**: MySQL 5.7.x/8.x, MariaDB, PostgreSQL, or SQLite
- **PowerDNS**: PowerDNS authoritative server 4.0.0+ (including 4.x and 5.x series)
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

## PHP Version Policy

Poweradmin tracks the [official PHP release lifecycle](https://www.php.net/supported-versions.php). Rather than maintain
a static list of supported versions, the policy is simple:

- **Actively supported** PHP versions (active or security-only) are supported by the current Poweradmin release.
- **End-of-life** PHP versions are dropped from the next Poweradmin minor release after they reach EOL.
- New PHP minor releases are added to compatibility testing (`composer compat:*`) shortly after their stable release.

This means the supported range moves forward over time. Always consult [php.net/supported-versions.php](https://www.php.net/supported-versions.php)
for the authoritative EOL calendar before planning a long-running deployment.

---

## Supported Distributions

Default PHP versions are taken from each distribution's official package repository as of May 2026.

| Distribution                 | Default PHP | Notes                                                                                                                                                                                  |
|------------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Debian 13 (Trixie)           | 8.4         | Current stable; meets the minimum out of the box.                                                                                                                                      |
| Debian 12 (Bookworm)         | 8.2         | Oldstable; meets the minimum out of the box.                                                                                                                                           |
| Ubuntu 26.04 LTS             | 8.5         | Released April 2026; meets the minimum out of the box.                                                                                                                                 |
| Ubuntu 24.04 LTS             | 8.3         | Meets the minimum out of the box.                                                                                                                                                      |
| Ubuntu 22.04 LTS             | 8.1         | Below the 8.2 minimum - install PHP 8.2 or newer from the [ondrej/php PPA](https://launchpad.net/~ondrej/+archive/ubuntu/php). Standard support ends April 2027.                       |
| Fedora 44                    | 8.5         | Apache included by default.                                                                                                                                                            |
| Fedora 43                    | 8.4         | Apache included by default.                                                                                                                                                            |
| Rocky Linux 10 / AlmaLinux 10 | 8.3        | RHEL 10 dropped modularity; PHP 8.3 ships directly from AppStream. Use the [Remi repository](https://rpms.remirepo.net/) for newer releases.                                           |
| Rocky Linux 9 / AlmaLinux 9  | 8.0         | Below the 8.2 minimum - run `dnf module reset php && dnf module enable php:8.2` (or `php:8.3`) to enable a newer module stream, or install from Remi.                                  |
| OpenSUSE Leap 15.6           | 8.2         | Meets the minimum out of the box.                                                                                                                                                      |

---

## BSD Operating Systems

Poweradmin is compatible with BSD operating systems that meet the PHP 8.2+ requirement. While not extensively tested, it
should work as long as the environment is properly configured.

---

## Unsupported Distributions

The following distributions are EOL or otherwise out of support and ship a PHP version below Poweradmin's 8.2 minimum. Distributions listed in "Supported" with a note about a third-party PPA or module stream are not repeated here.

| Distribution        | Default PHP | Reason                                                         |
|---------------------|-------------|----------------------------------------------------------------|
| Debian 11 (Bullseye) | 7.4         | LTS support ended June 2026.                                  |
| Ubuntu 20.04 LTS     | 7.4         | Standard support ended April 2025.                            |
| Rocky/AlmaLinux 8.x  | 7.2         | PHP below minimum; consider upgrading to 9.x or 10.x.         |

---

## Notes

- Distributions listed as unsupported can potentially be configured manually with a custom PHP build, but this is not
  officially supported.

- Upgrade paths are recommended for unsupported distributions to maintain security and compatibility.

## Tested Environments

Poweradmin has been tested with the following software combinations:

| Poweradmin | PHP            | PowerDNS | MariaDB  | MySQL  | PostgreSQL | SQLite |
|------------|----------------|----------|----------|--------|------------|--------|
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

For production environments, prefer a branch that is still receiving upstream fixes. PowerDNS publishes its own [End of Life (EOL) schedule](https://doc.powerdns.com/authoritative/appendices/EOL.html), which is the authoritative source - the dates below were correct at the time of writing but move forward with each release.

- **PowerDNS 4.8.x / 4.9.x**: EOL as of 2025. Plan an upgrade.
- **PowerDNS 5.0.x and newer**: Current stable branch with active support.
