# Brute-Force Protection with fail2ban

Poweradmin logs every authentication and MFA event in a single structured
format that [fail2ban](https://www.fail2ban.org/) can consume. This page
documents the log format, shows the filter and jail you need, and explains
the trade-offs between the different event types.

This complements the built-in [account lockout](../configuration/security-policies.md)
(which throttles attempts against a single account) by letting fail2ban
escalate to **IP-level bans** at the firewall.

## Prerequisites

1. Enable syslog output in `config/settings.php`:

    ```php
    'logging' => [
        'syslog_enabled' => true,
        'syslog_identity' => 'poweradmin',
        'syslog_facility' => LOG_USER,
    ],
    ```

2. Make sure your syslog daemon writes Poweradmin's events to a file you
   can point fail2ban at - for example `/var/log/poweradmin.log` via
   rsyslog:

    ```
    :programname, isequal, "poweradmin"   /var/log/poweradmin.log
    & stop
    ```

## Event Types

Every Poweradmin authentication event uses the same field order:

```
client_ip:<ip> user:<username> operation:<op> auth_method:<sql|ldap|oidc|saml> [reason:<code>] [mfa_type:<app|email>]
```

The `operation:` token is what fail2ban filters on.

| `operation:` | Severity | When it fires | Should fail2ban ban? |
| --- | --- | --- | --- |
| `login_success` | NOTICE | Successful credential check (or SAML/OIDC handshake completed) | No |
| `login_failed` | WARNING | Credential check rejected: unknown user, wrong password, or disabled account | **Yes** |
| `login_locked` | WARNING | Attempt arrived against an account already locked by `LoginAttemptService` | Optional - useful for escalation |
| `login_error` | WARNING | Infrastructure failure: LDAP server unreachable, OIDC `?error=` callback, SAML assertion validation exception | **No** - the user was never credential-checked |
| `mfa_verify` | INFO | MFA code accepted, user fully authenticated | No |
| `mfa_failed` | WARNING | MFA code rejected after password was already correct | **Yes** - high-confidence brute force |

### Why `login_error` is separate

If you put `operation:login_error` into the same filter as
`login_failed`, an LDAP outage or a misconfigured IdP would cause every
legitimate user's login attempt to be counted against the client IP and
trigger bans. Keep them separate.

`login_error` lines still go to your audit log (and to the admin UI under
the **Login error** event filter), so operators can investigate, but
fail2ban skips them.

## fail2ban Filter

Create `/etc/fail2ban/filter.d/poweradmin.conf`:

```ini
[Definition]
# Match credential failures and MFA brute force.
# Deliberately excludes operation:login_error (backend/IdP outages) and
# operation:login_locked (already throttled at the application layer).
failregex = ^.*\bpoweradmin\b.*client_ip:<HOST> .*operation:(login_failed|mfa_failed)\b

ignoreregex =

# fail2ban journal hint: the same regex works whether logs come from
# rsyslog or systemd-journal, as long as syslog_identity is "poweradmin".
```

The `<HOST>` token tells fail2ban which capture group is the client IP.
The regex anchors on:

- `\bpoweradmin\b` - the syslog identity, so unrelated lines on the same
  file don't match.
- `operation:(login_failed|mfa_failed)` - the credential-side events
  only.

## fail2ban Jail

Add to `/etc/fail2ban/jail.local`:

```ini
[poweradmin]
enabled  = true
filter   = poweradmin
logpath  = /var/log/poweradmin.log
maxretry = 5
findtime = 10m
bantime  = 1h
# Optional: ban for longer on repeat offenders
# bantime.increment = true
```

Tune `maxretry`/`findtime` to match your application-level
`account_lockout.lockout_attempts` if you want fail2ban to fire at the
same time the account-level lockout does, or set it higher to use
fail2ban only as a secondary line.

Reload fail2ban:

```sh
fail2ban-client reload
```

## Verifying It Works

1. Tail your Poweradmin log file:

    ```sh
    tail -f /var/log/poweradmin.log
    ```

2. From a test machine, hit the login form with a wrong password a few
   times. You should see:

    ```
    May 21 22:00:01 host poweradmin[1234]: client_ip:203.0.113.42 user:admin operation:login_failed auth_method:sql reason:wrong_password
    ```

3. After `maxretry` attempts, fail2ban should ban the IP:

    ```sh
    fail2ban-client status poweradmin
    ```

## Combining with the Built-In Lockout

The application-level [account lockout](../configuration/security-policies.md)
and fail2ban are complementary:

- **Application lockout** stops attempts against a single account, even
  if they come from different IPs. It surfaces as `operation:login_locked`.
- **fail2ban** stops attempts from a single IP, even if they target
  different usernames. It runs at the firewall and doesn't burn database
  rows.

A common setup: keep the application lockout aggressive on a per-account
basis (e.g. 5 attempts), and run fail2ban with a higher threshold over a
longer window (e.g. 20 attempts in an hour) so it only catches sustained
distributed scans.

## Admin UI

The same events are searchable in **Audit Log** under these filter
entries:

- `login_failed`, `login_locked`, `login_error`
- `mfa_failed`, `mfa_verify`
- `oidc_login_error`, `saml_login_error` (per-backend variants of
  `login_error`)
- Legacy `oidc_login_failed`, `saml_login_failed` (kept for historical
  rows logged before 4.4.0)
