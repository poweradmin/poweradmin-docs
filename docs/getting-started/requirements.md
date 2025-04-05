# PowerAdmin System Requirements

## Overview

PowerAdmin requires PHP 8.1 or higher to run. This document outlines the supported Linux and BSD distributions as well
as those that are not supported due to PHP version constraints. For the best experience, ensure your system meets or
exceeds the recommended requirements.

---

## Minimum Requirements

- **PHP**: 8.1 or higher
- **PHP Extensions**:
  - intl
  - gettext
  - openssl
  - pdo
  - pdo-mysql, pdo-pgsql or pdo-sqlite
  - session
  - filter
  - tokenizer
  - ldap (optional)
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

PowerAdmin is compatible with BSD operating systems that meet the PHP 8.1+ requirement. While not extensively tested, it
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
