# Personal Data and Privacy

This page lists the personal data Poweradmin stores, how long it keeps it, what it sends to other services, and how to answer access, correction and deletion requests. It is meant as input for your own privacy notice and records of processing under the GDPR or a similar law (UK GDPR, Swiss FADP, CCPA/CPRA, LGPD and others).

Poweradmin is self-hosted: all data stays in your own database and servers, and nothing is sent to the Poweradmin project. Whether an installation complies with a privacy law depends on how you run it. Poweradmin cannot make that decision for you.

This page describes Poweradmin 4.6.0.

## What Poweradmin stores

### Accounts

| Table | Personal data | Kept until |
|---|---|---|
| `users` | Username, full name, email, description, permission template, sign-in method | The account is deleted |
| `user_preferences` | Interface preferences (language, theme, page sizes) | The account is deleted |
| `user_mfa` | MFA type, TOTP secret, recovery codes, last use | MFA is turned off or the account is deleted |
| `user_group_members` | Group memberships | The account is deleted |
| `api_keys` | Key name, creator, creation and last-use time (the key itself is stored as a hash) | The key or its creator is deleted |
| `oidc_user_links`, `saml_user_links` | Identity provider subject, username and email from the provider | The account is deleted |
| `user_agreements` | Accepted agreement version, time, IP address, browser user agent | The account is deleted |
| `zones` | Which user owns which zone | The zone or the user is deleted |

For accounts that sign in with OIDC or SAML, the full name and email are copied from the identity provider and updated at every sign-in while `sync_user_info` is on (the default).

### Sign-in, password reset and recovery

| Table | Personal data | Kept until |
|---|---|---|
| `login_attempts` | User, IP address, time, success | Removed automatically once the lockout window has passed (`security.account_lockout.lockout_duration`, 15 minutes by default) |
| `password_reset_tokens` | Email, IP address, token hash | Expired tokens, and used tokens older than 7 days, are removed the next time someone requests or uses a reset. Deleting the account removes them at once |
| `username_recovery_requests` | Email, IP address, time | Rows older than 30 days are removed the next time someone requests a username reminder. Deleting the account removes them at once |

On a quiet installation, rows in the last two tables can stay longer than these periods, because the cleanup only runs when someone uses the feature.

### Audit logs

These are written only when `logging.database_enabled` is on (it is off by default):

| Table | Personal data |
|---|---|
| `log_users`, `log_zones`, `log_groups` | Text lines with the client IP address, username and the action, for example `client_ip:192.0.2.10 user:alice operation:login_success`. Adding a user also records their email, and password reset and username recovery requests record the email that was entered |
| `log_changesets`, `log_record_changes` | User ID, username, client IP address, and the full record before and after each change |
| `log_api` | API requests (with `logging.api_request_logging` on) and failed authentication or permission errors, with client IP address and user |

Only `log_api` has a built-in retention setting (`logging.api_log_retention_days`, 0 = keep forever). The other log tables grow until you delete old rows, see [Maintenance](../maintenance/index.md) for example queries.

With `logging.syslog_enabled` on, the same audit lines also go to syslog, where your syslog setup decides how long they are kept.

### Data in PowerDNS

- **Record comments**: PowerDNS stores the username of whoever wrote a record comment in `comments.account`.
- **DNS records**: records such as SOA (the RNAME contact address), RP, TXT and SMIMEA can contain names and email addresses, and they are published in public DNS. Poweradmin warns when you add RP, EUI-48, EUI-64 and SMIMEA records.

### Sessions

Poweradmin uses standard PHP sessions, stored on the server. A session holds the user ID, username and, for local and LDAP accounts, the password encrypted with `security.session_key`. Sessions end when the user signs out or after `interface.session_timeout` seconds of inactivity.

## Cookies and browser storage

All cookies and stored values are needed for the application to work or are set by the user's own choice, so no cookie consent banner is needed for Poweradmin itself.

| Name | Type | Purpose | Lifetime |
|---|---|---|---|
| PHP session cookie (`PHPSESSID` unless changed) | Cookie | Keeps the user signed in | Until the browser closes |
| `oidc_flow` | Cookie | Links an OIDC sign-in to the browser that started it | Minutes, during sign-in |
| `__Host-saml_flow` | Cookie | Links a SAML sign-in to the browser that started it | Minutes, during sign-in |
| `style` | localStorage | Light or dark theme chosen by the user | Until cleared |
| `poweradmin_language` | localStorage | Language chosen by the user | Until cleared |

The session cookie is `HttpOnly`, `SameSite=Lax`, and `Secure` when the site is served over HTTPS.

## External services

By default Poweradmin sends no data to third parties. Each of the following only runs when you turn it on:

| Service | Setting | What is sent |
|---|---|---|
| Google reCAPTCHA | `security.recaptcha.enabled` | The visitor's browser loads Google's script on the login, forgot password and forgot username pages, which gives Google the visitor's IP address and sets Google cookies. The server also sends the reCAPTCHA response to Google |
| Gravatar | `interface.avatar_gravatar_enabled` | The browser requests an image from gravatar.com using a hash of the user's email, which gives Gravatar the email hash and the viewer's IP address |
| OIDC avatars | `interface.avatar_oauth_enabled` | The browser loads the picture URL from the identity provider |
| WHOIS and RDAP lookups | `whois.enabled`, `rdap.enabled` | The zone name is sent to the registry's WHOIS or RDAP server |
| OIDC, SAML, LDAP | Per provider | Sign-in data is exchanged with the identity provider or directory you configure |
| Mail | `mail.*` | Password reset, username reminders and notifications go through the mail server you configure |
| PowerDNS API | `pdns_api.*` | Zone data goes to your own PowerDNS server |

The API documentation page (`/api/docs`) loads Swagger UI from Poweradmin's own files, not from a CDN.

## Handling requests from users

### Access and portability

There is no built-in export yet. Collect a user's data from the tables above with SQL, using their user ID, username and email.

### Correction

Users with the `user_edit_own` permission can change their own full name, email and description. Others need an administrator. For OIDC and SAML accounts, change the data at the identity provider: Poweradmin copies it again at the next sign-in.

### Restriction

Deactivating an account (unchecking **Active** on the user's edit page) stops all use of it straight away, including open sessions, while keeping the data.

### Deletion

Deleting a user removes their account, preferences, MFA settings, group memberships, API keys, identity provider links, agreement acceptances, login attempts, zone ownership and their pending password reset and username recovery requests. Zone templates that the user shared with groups can be handed to another user.

These stay after deletion and must be removed by hand if needed:

- audit log entries (`log_users`, `log_zones`, `log_groups`, `log_api`, `log_changesets`, `log_record_changes`);
- the username in PowerDNS `comments.account`;
- copies in backups and syslog.

## Recommended settings

- Turn on audit logging (`logging.database_enabled`) if you need to show who changed what, and plan how long to keep it.
- Set `logging.api_log_retention_days` when API request logging is on.
- Delete old rows from the other log tables on a schedule (see [Maintenance](../maintenance/index.md)).
- Leave Gravatar off unless you need it, and tell users when it is on.
- If you use reCAPTCHA, mention Google in your privacy notice.
- Keep OIDC and SAML client secrets and the LDAP bind password out of `settings.php` with environment variables or Docker secrets (see `DOCKER-SECRETS.md` in the repository).
- Point users to your own privacy notice, for example from the [user agreement](user-agreements.md) text.

## Related Documentation

- [Database Logging](database-logging.md)
- [Security Policies](security-policies.md)
- [User Agreements](user-agreements.md)
- [Avatar System](avatars.md)
- [Maintenance](../maintenance/index.md)
