# Security Policies

Poweradmin offers various security features to protect your DNS management system. All security configurations are configured in the `config/settings.php` file under the `security` section.

## General Security Settings

- **session_key**: A unique key used for session security. Default: `change_this_key` (you should always change this)
- **password_encryption**: Password hashing algorithm. Options: 'bcrypt', 'argon2i', 'argon2id'. Default: `bcrypt`. Note: 'md5' and 'md5salt' were removed in 4.3.0
- **password_cost**: Cost factor for bcrypt algorithm. Default: `12`
- **login_token_validation**: Enable token validation for login form. Default: `true`
- **global_token_validation**: Enable token validation for all forms. Default: `true`
- **trusted_proxies**: Reverse proxy addresses allowed to set forwarded client-IP headers (`X-Forwarded-For`, `X-Real-IP`, `Client-IP`). Supports IPs, CIDRs (IPv4/IPv6), and IPv4 wildcards. Private and loopback peers are always trusted; add public proxy addresses here so their forwarded headers are honored. Default: `[]` (added in 4.5.0)

## Rotating the Session Key

`session_key` encrypts the credentials Poweradmin holds in the session. Its strength decides whether a leaked session store yields only password hashes or usable plaintext passwords, so it is worth treating as a secret in its own right.

Replace the current value if any of these apply:

- It is still `change_this_key`, or `p0w3r4dm1n` on the 3.x line. Both are published defaults and are in the public source tree.
- The configuration file has ever been committed to version control, copied between environments, or shared in a support thread.
- The key was written for you by the web installer before 4.5.0 (4.4.2, 4.3.6, 4.2.7 and 3.9.13 on the older lines). Those releases built it with `mt_rand()`, which is seeded from a 32-bit value, so the key is far weaker than its length suggests. Installations set up through Docker are unaffected: the entrypoint has always used `openssl rand`.

Generate a replacement from a real random source:

```bash
openssl rand -hex 32
```

Then set it in `config/settings.php`:

```php
return [
    'security' => [
        'session_key' => 'the-generated-value',
    ],
];
```

Rotating logs everyone out, because sessions encrypted under the old key can no longer be read. Nothing else is affected: stored password hashes, API keys, zone data and permissions do not depend on this value.

Poweradmin shows a warning in the page header, visible to superusers, when the configured key is missing, is one of the shipped defaults, or is shorter than 32 characters. The check can only judge length and known values, not the quality of the generator that produced the key, so an installer-generated key of adequate length will not raise a warning. If you do not know where your key came from, rotate it.

## Account Lockout

These settings help prevent brute force attacks by temporarily locking accounts after multiple failed login attempts:

- **enable_lockout**: Enable account lockout after failed login attempts. Default: `false`
- **lockout_attempts**: Number of failed attempts before account is locked. Default: `5`
- **lockout_duration**: Duration of the lockout in minutes. Default: `15`
- **track_ip_address**: Lock accounts based on IP address. Default: `true`
- **clear_attempts_on_success**: Clear failed attempts after successful login. Default: `true`

These settings govern the password stage only. The second factor is throttled separately - see [Second-factor attempt limit](#second-factor-attempt-limit) below.

## Second-Factor Attempt Limit

A six-digit second factor is small enough to guess, so MFA verification is rate limited on its own, independently of the account lockout above. This limit is always active when MFA is enabled: it does not require `enable_lockout`, which ships disabled (added in 4.5.0).

- **mfa.max_verify_attempts**: Wrong MFA codes tolerated before verification is refused. Default: `5`
- **mfa.verify_lockout_duration**: Minutes to keep refusing attempts once the limit is reached. Default: `15`

Three behaviours differ from the password lockout, all deliberate:

- MFA failures are counted per account across every source address. `track_ip_address` does not apply, because an attacker rotating addresses would otherwise reset the counter on each request.
- `whitelist_ip_addresses` does not exempt the second factor. The whitelist exists so a bot cannot lock staff out of password login; the second factor is the only barrier left once a password is known, so it is never waived. The blacklist still applies.
- Reaching the limit invalidates any pending emailed code, and no replacement is sent until the lockout expires.

MFA failures are tracked separately from password failures, so a wrong code never blocks a later password login, and a fresh password login does not reset the MFA counter. Setting either value to `0` is treated as `1` rather than as "unlimited"; to remove the limit entirely, disable MFA.

## IP Address Management

Control which IP addresses can access the system:

- **whitelist_ip_addresses**: IP addresses that are always allowed to access the system. Takes priority over blacklist. Supports IPs, CIDRs, and wildcards. Default: `[]`
- **blacklist_ip_addresses**: IP addresses that are blocked from accessing the system. Supports IPs, CIDRs, and wildcards. Default: `[]`

## Example Configuration

```php
return [
    'security' => [
        'session_key' => 'random_secure_string_here',
        'password_encryption' => 'bcrypt',
        'password_cost' => 12,
        'login_token_validation' => true,
        'global_token_validation' => true,
        'trusted_proxies' => ['203.0.113.10', '2001:db8::/32'],
        'account_lockout' => [
            'enable_lockout' => true,
            'lockout_attempts' => 3,
            'lockout_duration' => 30,
            'track_ip_address' => true,
            'clear_attempts_on_success' => true,
            'whitelist_ip_addresses' => ['192.168.1.0/24', '10.0.0.*'],
            'blacklist_ip_addresses' => ['1.2.3.4', '5.6.7.0/24'],
        ],
        'mfa' => [
            'enabled' => true,
            'app_enabled' => true,
            'email_enabled' => true,
            'recovery_codes' => 8,
            'recovery_code_length' => 10,
            'max_verify_attempts' => 5,
            'verify_lockout_duration' => 15,
        ],
        'password_reset' => [
            'enabled' => true,
            'token_lifetime' => 3600,
            'rate_limit_attempts' => 5,
            'rate_limit_window' => 3600,
            'min_time_between_requests' => 60,
        ],
        'recaptcha' => [
            'enabled' => true,
            'site_key' => 'your_site_key_here',
            'secret_key' => 'your_secret_key_here',
            'version' => 'v3',
            'v3_threshold' => 0.5,
        ],
    ],
];
```

## Security Best Practices

1. **Always change the default session key** to a unique, random string
2. Use a strong password hashing algorithm (bcrypt or argon2id)
3. Enable account lockout in production environments
4. Implement IP whitelisting for admin access in sensitive environments
5. Enable both login and global token validation to prevent CSRF attacks
6. Use HTTPS for all production deployments
7. Regularly update Poweradmin to get the latest security fixes

## Multi-Factor Authentication (MFA)

Poweradmin supports multi-factor authentication to add an extra layer of security:

- **enabled**: Enable MFA functionality. Default: `false`
- **app_enabled**: Enable authenticator app option (TOTP). Default: `true`
- **email_enabled**: Enable email verification option. Default: `true`
- **recovery_codes**: Number of recovery codes to generate. Default: `8`
- **recovery_code_length**: Length of recovery codes. Default: `10`

## Password Reset

Secure password reset functionality with rate limiting:

- **enabled**: Enable/disable password reset functionality. Default: `false`
- **token_lifetime**: Token validity in seconds. Default: `3600` (1 hour)
- **rate_limit_attempts**: Maximum reset attempts per time window. Default: `5`
- **rate_limit_window**: Rate limit window in seconds. Default: `3600` (1 hour)
- **min_time_between_requests**: Minimum seconds between requests. Default: `60` (1 minute)

### `interface.application_url` is required

When password reset is enabled, `interface.application_url` must be set to the full public URL of the Poweradmin install, e.g. `https://dns.example.com/poweradmin`. The reset link in the email is built from this value only - request headers such as `Host` are never used. If `application_url` is empty, the password-reset endpoint accepts requests but does not send mail and logs an error: `Password reset email NOT sent: interface.application_url must be configured to build a trustworthy reset link`.

```php
return [
    'interface' => [
        'application_url' => 'https://dns.example.com/poweradmin',
    ],
];
```

The same setting is required for [OIDC](oidc.md#interfaceapplication_url-must-be-set) and [SAML](saml.md#interfaceapplication_url-must-be-set), which refuse to build the provider-bound redirect and metadata URLs without it. Poweradmin never derives these from the request: the web server takes `SERVER_NAME` from the client `Host` header under the official Docker image and under Apache's default `UseCanonicalName Off`.

## Google reCAPTCHA

Protect login forms from automated attacks using Google reCAPTCHA:

- **enabled**: Enable reCAPTCHA on login form. Default: `false`
- **site_key**: Your reCAPTCHA site key (public key). Default: `''`
- **secret_key**: Your reCAPTCHA secret key (private key). Default: `''`
- **version**: reCAPTCHA version: 'v2' or 'v3'. Default: `'v3'`
- **v3_threshold**: Score threshold for v3 (0.0 - 1.0). Default: `0.5`

### Setting up Google reCAPTCHA

1. Visit [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Create a new site and get your site key and secret key
3. Configure the keys in your settings:

```php
'security' => [
    'recaptcha' => [
        'enabled' => true,
        'site_key' => 'your_site_key_here',
        'secret_key' => 'your_secret_key_here',
        'version' => 'v3',
        'v3_threshold' => 0.5,
    ],
],
```

For more information about password policies, see the [Password Policies documentation](./password-policies.md).