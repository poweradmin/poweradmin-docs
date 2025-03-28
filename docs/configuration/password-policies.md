# Password Policies

Poweradmin allows you to enforce password policies to enhance the security of user accounts. These policies are
configured in the `config/password_policy.php` file. Below are the available options:

## Password Rules

- **enable_password_rules**: Enable or disable password rules enforcement. Default: `false`.
- **min_length**: Minimum length of the password. Default: `6`.
- **require_uppercase**: Require at least one uppercase letter. Default: `true`.
- **require_lowercase**: Require at least one lowercase letter. Default: `true`.
- **require_numbers**: Require at least one numeric digit. Default: `true`.
- **require_special**: Require at least one special character. Default: `false`.
- **special_characters**: List of allowed special characters. Default: `!@#$%^&*()+-=[]{}|;:,.<>?`.

## Password Expiration

**Note:** The following settings are not implemented yet.

- **enable_expiration**: Enable or disable password expiration. Default: `false`.
- **max_age_days**: Maximum age of the password in days before it expires. Default: `90`.

## Password Reuse Prevention

**Note:** The following settings are not implemented yet.

- **enable_reuse_prevention**: Enable or disable prevention of password reuse. Default: `false`.
- **prevent_reuse**: Number of previous passwords to check against for reuse. Default: `5`.

These settings can be customized by modifying the `config/password_policy.php` file. The default values are provided by
the [PasswordPolicyDefaults](https://github.com/poweradmin/poweradmin/blob/master/lib/Domain/Config/PasswordPolicyDefaults.php)
class.

## Example Configuration

To enable the currently defined password policies, you can update the `config/password_policy.php` file with the
following content:

```php
<?php

return [
    'enable_password_rules' => true,
];
```

When `enable_password_rules` is set to `true`, passwords will be required to be at least 6 characters long and contain
at least one uppercase letter, one lowercase letter, and one number. Special characters are not required by default, but
when used, they must be from the allowed set: `!@#$%^&*()+-=[]{}|;:,.<>?`
