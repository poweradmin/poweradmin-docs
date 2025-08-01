# Poweradmin System Requirements

## Overview

Poweradmin requires PHP 8.1 or higher to run. This document outlines the supported Linux and BSD distributions as well
as those that are not supported due to PHP version constraints. For the best experience, ensure your system meets or
exceeds the recommended requirements.

---

## Minimum Requirements

- **PHP**: 8.1 or higher (including 8.2, 8.3, 8.4, etc.)
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
- **PowerDNS**: PowerDNS authoritative server 4.0.0+
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
| 4.0.x      | 8.1.31         | 4.7.4    | 10.11.10 | 9.1.0  | 16.3       | 3.45.3 |
| 3.9.x      | 8.1.31         | 4.7.4    | 10.11.10 | 9.1.0  | 16.3       | 3.45.3 |
| 3.8.x      | 8.1.28         | 4.5.5    | 10.11.8  | -      | 16.3       | 3.45.3 |
| 3.7.x      | 8.1.2          | 4.5.3    | 11.1.2   | 8.2.0  | 16.0       | 3.40.1 |
| 3.6.x      | 8.1.2          | 4.5.3    | 11.1.2   | 8.1.0  | 16.0       | 3.40.1 |
| 3.5.x      | 8.1.17         | 4.5.3    | 10.11.2  | 8.0.32 | 15.2       | 3.34.1 |
| 3.4.x      | 7.4.3 / 8.1.12 | 4.2.1    | 10.10.2  | 8.0.31 | 15.1       | 3.34.1 |
