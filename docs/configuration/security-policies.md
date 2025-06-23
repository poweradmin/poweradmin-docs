# Security Policies

Poweradmin offers various security features to protect your DNS management system. All security configurations are configured in the `config/settings.php` file under the `security` section.

## General Security Settings

- **session_key**: A unique key used for session security. Default: `change_this_key` (you should always change this)
- **password_encryption**: Password hashing algorithm. Options: 'md5', 'md5salt', 'bcrypt', 'argon2i', 'argon2id'. Default: `bcrypt`
- **password_cost**: Cost factor for bcrypt algorithm. Default: `12`
- **login_token_validation**: Enable token validation for login form. Default: `true`
- **global_token_validation**: Enable token validation for all forms. Default: `true`

## Account Lockout

These settings help prevent brute force attacks by temporarily locking accounts after multiple failed login attempts:

- **enable_lockout**: Enable account lockout after failed login attempts. Default: `false`
- **lockout_attempts**: Number of failed attempts before account is locked. Default: `5`
- **lockout_duration**: Duration of the lockout in minutes. Default: `15`
- **track_ip_address**: Lock accounts based on IP address. Default: `true`
- **clear_attempts_on_success**: Clear failed attempts after successful login. Default: `true`

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