# Password Policies

Poweradmin allows you to enforce password policies to enhance the security of user accounts. All security
configurations, including password policies, are now configured in a single `config/settings.php` file under the
`security` section. This consolidates all security-related settings into one location for easier management.

## Password Rules

- **enable_password_rules**: Enable or disable password rules enforcement. Default: `true`.
- **min_length**: Minimum length of the password, counted in characters (from 4.6.0; earlier versions count bytes, so a non-ASCII letter counts as two or more). Default: `6`.
- **require_uppercase**: Require at least one uppercase letter. Default: `true`.
- **require_lowercase**: Require at least one lowercase letter. Default: `true`.
- **require_numbers**: Require at least one numeric digit. Default: `true`.
- **require_special**: Require at least one special character. Default: `false`.
- **special_characters**: List of allowed special characters. Default: `!@#$%^&*()+-=[]{}|;:,.<>?`.

## Password Security Settings

The following additional security settings are available in the `security` section:

- **password_encryption**: Choose the password hashing algorithm. Options: 'bcrypt', 'argon2i', 'argon2id'. Default: `bcrypt`. Note: 'md5' and 'md5salt' were removed in 4.3.0. Existing legacy hashes are still verified and automatically upgraded on login.

- **password_cost**: Cost factor for bcrypt algorithm. Default: `12`.

### bcrypt and long passwords

bcrypt only uses the first 72 bytes of a password and ignores the rest. A non-ASCII letter takes two or more bytes, so the limit is reached with fewer characters. From 4.6.0, while `password_encryption` is `bcrypt`, a new password longer than 72 bytes is refused when it is set, changed or reset. Login is not affected, so users who already have a longer password keep signing in with it. The installer applies the same limit to the administrator password. A password containing a NUL byte is refused with any algorithm.

argon2i and argon2id have no such limit. You can switch `password_encryption` to `argon2id` at any time: existing bcrypt hashes keep working and each one is rehashed with argon2id at the user's next successful login. Check that your PHP build includes Argon2 first (`php -r 'var_dump(defined("PASSWORD_ARGON2ID"));'` prints `bool(true)`); the official Docker image does.

## Recommended Settings

The defaults are kept for compatibility with existing installs. Current guidance from [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html#sec5) and [Microsoft](https://learn.microsoft.com/en-us/microsoft-365/admin/misc/password-policy-recommendations) favours length over character rules:

- **Length over complexity.** Set `min_length` to at least `8`, or `15` for accounts that sign in with a password alone. Turn off `require_uppercase`, `require_lowercase`, `require_numbers` and `require_special`: forced character mixes lead to predictable passwords such as `Password1!`.
- **No forced rotation.** Do not make users change passwords on a schedule. Ask for a change only when a password may have been exposed.
- **Limit failed logins.** Enable [account lockout](security-policies.md#account-lockout).
- **Add a second factor.** Enable [multi-factor authentication](security-policies.md#multi-factor-authentication-mfa); it does more than any password rule.
- **Use argon2id** for `password_encryption` (see above).

## Not implemented

Poweradmin has no password expiration and no password reuse prevention. There are no
configuration keys for either - nothing in `config/settings.defaults.php` corresponds to them, so
adding keys of your own has no effect.

Both are tracked and scheduled for 4.8.0:
[#651](https://github.com/poweradmin/poweradmin/issues/651) (expiration) and
[#652](https://github.com/poweradmin/poweradmin/issues/652) (reuse prevention).

Until then, if you need enforced rotation or reuse history, handle it in your identity provider
and authenticate through [LDAP](ldap.md), [OIDC](oidc.md) or [SAML](saml.md) rather than local
passwords.

## Example Configuration

The recommended settings above, in `config/settings.php`:

```php
<?php

return [
    'security' => [
        'password_encryption' => 'argon2id',
        'password_policy' => [
            'enable_password_rules' => true,
            'min_length' => 12,
            'require_uppercase' => false,
            'require_lowercase' => false,
            'require_numbers' => false,
            'require_special' => false,
        ],
        'account_lockout' => [
            'enable_lockout' => true,
        ],
    ],
];
```

Settings you leave out keep their defaults, so the four `require_*` keys must be set to `false` explicitly.
