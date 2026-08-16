# Password Policies

Poweradmin allows you to enforce password policies to enhance the security of user accounts. All security
configurations, including password policies, are now configured in a single `config/settings.php` file under the
`security` section. This consolidates all security-related settings into one location for easier management.

## Password Rules

- **enable_password_rules**: Enable or disable password rules enforcement. Default: `true`.
- **min_length**: Minimum length of the password. Default: `6`.
- **require_uppercase**: Require at least one uppercase letter. Default: `true`.
- **require_lowercase**: Require at least one lowercase letter. Default: `true`.
- **require_numbers**: Require at least one numeric digit. Default: `true`.
- **require_special**: Require at least one special character. Default: `false`.
- **special_characters**: List of allowed special characters. Default: `!@#$%^&*()+-=[]{}|;:,.<>?`.

## Password Security Settings

The following additional security settings are available in the `security` section:

- **password_encryption**: Choose the password hashing algorithm. Options: 'bcrypt', 'argon2i', 'argon2id'. Default: `bcrypt`. Note: 'md5' and 'md5salt' were removed in 4.3.0. Existing legacy hashes are still verified and automatically upgraded on login.

- **password_cost**: Cost factor for bcrypt algorithm. Default: `12`.

## Not available

Poweradmin has no password expiration and no password reuse prevention. There are no
configuration keys for either - nothing in `config/settings.defaults.php` corresponds to them,
so adding keys of your own has no effect.

If you need enforced rotation or reuse history, handle it in your identity provider and
authenticate through [LDAP](ldap.md), [OIDC](oidc.md) or [SAML](saml.md) instead of local
passwords.

## Example Configuration

To enable password rules with custom settings, add the following configuration to your `config/settings.php`:

```php
<?php

return [
    'security' => [
        'password_encryption' => 'bcrypt',
        'password_cost' => 12,
        'password_policy' => [
            'enable_password_rules' => true,
            'min_length' => 8,
            'require_special' => true,
        ],
    ],
];
```

When `enable_password_rules` is set to `true`, passwords will be validated according to the configured rules. In this
example, passwords must be at least 8 characters long and include special characters, along with the default
requirements for uppercase letters, lowercase letters, and numbers.
