# Password Policies

Poweradmin allows you to enforce password policies to enhance the security of user accounts. All security
configurations, including account lockout and IP management policies, are now configured in the `config/settings.php`
file under the `security` section.

## Account Lockout

- **enable_lockout**: Enable or disable account lockout after multiple failed login attempts. Default: `false`.
- **lockout_attempts**: Number of failed login attempts before account is locked. Default: `5`.
- **lockout_duration**: Duration of the lockout in minutes. Default: `15`.
- **track_ip_address**: Enable tracking of IP addresses for failed login attempts. Default: `true`.
- **clear_attempts_on_success**: Clear failed attempt counter after successful login. Default: `true`.

## IP Address Management

- **whitelist_ip_addresses**: List of IP addresses that are always allowed to access the system. Supports IPs, CIDRs,
  and wildcards. Takes priority over blacklist. Default: `[]`.
- **blacklist_ip_addresses**: List of IP addresses that are blocked from accessing the system. Supports IPs, CIDRs, and
  wildcards. Default: `[]`.

These settings can be found in the `security.account_lockout` section of your `config/settings.php` file.

## Example Configuration

To enable account lockout and configure IP whitelisting, you can use the following configuration in your
`config/settings.php`:

```php
<?php

return [
    'security' => [
        'account_lockout' => [
            'enable_lockout' => true,
            'whitelist_ip_addresses' => ['192.168.1.0/24', '10.0.0.*'],
            'blacklist_ip_addresses' => ['1.2.3.4', '5.6.7.0/24'],
        ],
    ],
];
```

When `enable_lockout` is set to `true`, an account will be locked for 15 minutes after 5 failed login attempts. The
system tracks IP addresses by default and resets the failed attempts counter after a successful login. Whitelisted IPs
will never be locked out, while blacklisted IPs will always be blocked.
