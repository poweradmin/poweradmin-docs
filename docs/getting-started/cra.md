# EU Cyber Resilience Act

The EU Cyber Resilience Act (Regulation (EU) 2024/2847, "CRA") sets security requirements for
products with digital elements sold in the EU. This page is for companies that ship Poweradmin as
part of a product or service, and for DNS operators under NIS2 who need to assess the software they
run. It is not legal advice.

## Who the obligations fall on

Poweradmin is free software under the GPL, developed by volunteers and not sold. Free and open
source software that is not supplied in the course of a commercial activity is outside the CRA's
manufacturer obligations (Recitals 18 and 19). If you integrate Poweradmin into a product you place
on the market, the manufacturer obligations are yours, and Article 13(5) asks you to exercise due
diligence on the components you use. The information below is meant to help with that.

## What the project provides

| CRA requirement (Annex I) | Status |
|---|---|
| Coordinated vulnerability disclosure and a security contact (Part II (5), (6)) | [SECURITY.md](https://github.com/poweradmin/poweradmin/blob/master/SECURITY.md): private reporting through GitHub, an email fallback, a reply within 7 days |
| Security updates for a defined support period, free of charge (Part II (2), (8)) | Fixes go to every supported branch. Support periods and end dates are on [Version Support](lifecycle.md) |
| Published advisories (Part II (4)) | [GitHub security advisories](https://github.com/poweradmin/poweradmin/security/advisories), with CVE ids |
| Software bill of materials (Part II (1)) | An SPDX SBOM of the Docker image, `vendor/` included, is attached to each tagged release |
| Known vulnerabilities in dependencies (Part I (2)(a)) | Dependabot updates, a weekly `composer audit` of the maintained branches, and a daily Trivy scan of the published images |
| Secure development | Static analysis (PHPStan, Phan, Psalm taint analysis, Semgrep), GitHub Actions pinned to commit hashes, Dockerfile linting |
| Secure by default (Part I (2)(b)) | The API, metrics, DNSSEC, password reset and LDAP/OIDC/SAML are off until enabled. The Docker image generates a random admin password and session key |
| Protection of stored and transmitted data (Part I (2)(e)) | Passwords are hashed (bcrypt or Argon2); API keys and reset tokens are stored as hashes; outbound HTTPS verifies certificates; SMTP can require TLS; LDAP over `ldaps://` (see [LDAP](../configuration/ldap.md)) |
| Logging of security events (Part I (2)(l)) | Sign-ins, failures, lockouts, MFA and administrative changes are written to the database and syslog when logging is enabled (see [Compliance Settings](../configuration/compliance.md)) |

## Planned

These are tracked as GitHub issues:

- Database audit logging on by default for new installs ([#1880](https://github.com/poweradmin/poweradmin/issues/1880))
- An admin notice for insecure settings ([#1872](https://github.com/poweradmin/poweradmin/issues/1872)) and an optional check for new releases ([#1692](https://github.com/poweradmin/poweradmin/issues/1692))
- Encryption of stored second-factor secrets ([#1883](https://github.com/poweradmin/poweradmin/issues/1883))

To report a vulnerability, follow [SECURITY.md](https://github.com/poweradmin/poweradmin/blob/master/SECURITY.md).
