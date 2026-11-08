# Compliance Settings

Poweradmin's defaults are kept for compatibility with existing installs, so they do not meet most
audit frameworks out of the box. This page lists the settings that get you there for the common
requirements in PCI DSS v4.0 (requirement 8), CIS Controls v8 (safeguards 5 and 6) and NIST
SP 800-63B. It covers Poweradmin itself; the web server, database and operating system need their
own hardening.

Docker installs set the same values through the `PA_*` environment variables shown in brackets.
`settings.php` is generated on the first start only, so changing a variable later has no effect
until the file is regenerated (see [Docker](../installation/docker.md)).

## Requirements reachable by configuration

| Requirement | Setting |
|---|---|
| PCI DSS 8.3.4: lock after at most 10 failed attempts, for at least 30 minutes | `security.account_lockout.enable_lockout = true`, `lockout_attempts = 10` or lower, `lockout_duration = 30` (`PA_LOCKOUT_ENABLED`, `PA_LOCKOUT_ATTEMPTS`, `PA_LOCKOUT_DURATION`). PCI counts per user ID: either set `track_ip_address = false`, or keep it on and set `username_attempts = 10` (`PA_LOCKOUT_TRACK_IP`, `PA_LOCKOUT_USERNAME_ATTEMPTS`; 4.6.0 and later). |
| PCI DSS 8.2.8: sign out after 15 minutes idle | `interface.session_timeout = 900` (`PA_SESSION_TIMEOUT`, in seconds) |
| NIST SP 800-63B AAL2: re-authenticate at least every 12 hours | `interface.session_max_lifetime = 43200` (`PA_SESSION_MAX_LIFETIME`; 4.6.0 and later) |
| PCI DSS 8.3.6: at least 12 characters | `security.password_policy.enable_password_rules = true`, `min_length = 12` (`PA_PASSWORD_MIN_LENGTH`). NIST and Microsoft advise against character-class rules; see [Password Policies](password-policies.md#recommended-settings). |
| PCI DSS 8.4, CIS 6.3/6.5: MFA for administrative access | `security.mfa.enabled = true`, `enforced = true`, `email_enabled = false`, `skip_for_external_auth = false` (`PA_MFA_ENABLED`, `PA_MFA_ENFORCED`, `PA_MFA_EMAIL_ENABLED`, `PA_MFA_SKIP_FOR_EXTERNAL_AUTH`). Then give the Administrator permission template the **`user_enforce_mfa`** permission: enforcement applies only to users who hold it, and super admin rights do not imply it. Keep `api.basic_auth_enabled = false` (`PA_API_BASIC_AUTH_ENABLED`), since HTTP Basic auth on the API does not ask for a second factor. |
| CIS 6.7: centralised authentication | `ldap.enabled`, `oidc.enabled` or `saml.enabled` (see [LDAP](ldap.md), [OIDC](oidc.md), [SAML](saml.md)) |
| PCI DSS 10, CIS 8: audit logging | `logging.database_enabled = true` and `logging.syslog_enabled = true` (`PA_LOGGING_DATABASE_ENABLED`, `PA_LOGGING_SYSLOG_ENABLED`), and `logging.api_request_logging = true` (`PA_LOGGING_API_REQUEST_LOGGING`) to record successful API calls as well. Forward syslog to a central collector so the records are kept outside the database the application can write to. |
| Password storage | `security.password_encryption = 'argon2id'`; existing hashes are upgraded at the next sign-in (see [Password Policies](password-policies.md#bcrypt-and-long-passwords)) |
| Secrets | Keep `session_key`, the admin password and the PowerDNS API key out of the environment listing with Docker secrets (`PA_SESSION_KEY__FILE`, `PA_ADMIN_PASSWORD__FILE`, `PA_PDNS_API_KEY__FILE`; see [Docker Secrets](../installation/docker-secrets.md)) |

## Not covered yet

These requirements cannot be met with a setting today:

- **Disabling dormant accounts** (PCI DSS 8.2.6, CIS 5.3). Poweradmin does not track the last sign-in. Until it does, review accounts by hand.
- **Changing a temporary password at first sign-in** (PCI DSS 8.3.5). There is no "must change password" flag yet.
- **Password expiry** (PCI DSS 8.3.9). Not implemented ([#651](https://github.com/poweradmin/poweradmin/issues/651)). PCI accepts MFA as the alternative.
- **Maximum API key lifetime** (PCI DSS 8.6). Set an expiry date on each key by hand.

## Logging and debugging

`mail.transport = 'logger'` writes every outgoing email, password reset links included, to the
PHP error log. Use it only for debugging, never on a production system.
