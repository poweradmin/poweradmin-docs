# Password Policies

Poweradmin allows you to enforce password policies to enhance the security of user accounts. These policies are
configured in the `config/security_policy.php` file. Below are the available options:

## Account Lockout

- **enable_lockout**: Enable or disable account lockout after multiple failed login attempts. Default: `false`.
- **lockout_attempts**: Number of failed login attempts before account is locked. Default: `5`.
- **lockout_duration**: Duration of the lockout in minutes. Default: `15`.
- **track_ip_address**: Enable tracking of IP addresses for failed login attempts. Default: `true`.
- **clear_attempts_on_success**: Clear failed attempt counter after successful login. Default: `true`.

## IP Address Management

**Note:** The following settings are not implemented yet.

- **whitelist_ip_addresses**: List of IP addresses that are always allowed to access the system. Default: `[]`.
- **blacklist_ip_addresses**: List of IP addresses that are blocked from accessing the system. Default: `[]`.

These settings can be customized by modifying the `config/security_policy.php` file. The default values are provided by
the [SecurityPolicyDefaults](https://github.com/poweradmin/poweradmin/blob/master/lib/Domain/Config/SecurityPolicyDefaults.php)
class.

## Example Configuration

To enable the currently defined security policies, you can update the `config/security_policy.php` file with the
following content:

```php
<?php

return [
    'enable_lockout' => true,
];
```

When `enable_lockout` is set to `true`, an account will be locked for 15 minutes after 5 failed login attempts. The
system tracks IP addresses by default and resets the failed attempts counter after a successful login. Setting this to
`false` disables the entire account lockout mechanism, regardless of other lockout-related settings.
