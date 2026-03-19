# Multi-Factor Authentication (MFA)

Multi-factor authentication adds an extra layer of security to your Poweradmin account. With MFA enabled, you need both your password and a time-based one-time password (TOTP) from an authenticator app - or a code sent to your email - to log in.

Poweradmin supports two MFA methods:

- **Authenticator app** - uses a TOTP app such as Google Authenticator, Microsoft Authenticator, or Authy
- **Email verification** - sends a 6-digit code to your email address (requires [mail configuration](../configuration/mail.md))

> **Note:** MFA must be enabled globally by an administrator before users can set it up. See [Configuration](#configuration) below.

## Enabling MFA for Your Account

1. Log in to Poweradmin and navigate to **Account** in the top navigation bar
2. In the MFA section, select your preferred method (authenticator app or email)
3. If using an authenticator app:
    - A QR code is displayed on screen
    - Open your authenticator app and scan the QR code
    - Enter the 6-digit verification code shown in your app to confirm setup
4. If using email verification:
    - A verification code is sent to your registered email address
    - Enter the code to confirm setup
5. After successful verification, MFA is active on your account
6. Save your **recovery codes** in a safe place - you will need these if you lose access to your authenticator app or email

> **Warning:** Recovery codes can only be viewed once during setup. Store them securely before closing the page.

## Logging In with MFA

Once MFA is enabled, the login flow has an additional step:

1. Enter your username and password as usual
2. After successful password verification, you are prompted for your MFA code
3. Open your authenticator app and enter the current 6-digit code, or check your email for a verification code
4. If the code is valid, you are logged in

If your authenticator app code is not accepted, check that your device clock is accurate. TOTP codes are time-sensitive and allow a tolerance of approximately 30 seconds.

## MFA Enforcement

Administrators can require specific users to set up MFA. This is controlled through two mechanisms:

- **User access templates** - add the `user_enforce_mfa` permission to an access template assigned to users
- **Group access templates** - add the `user_enforce_mfa` permission to a group's access template, which enforces MFA for all group members

When MFA is enforced, users who have not yet set up MFA will be redirected to the MFA setup page after their next login. They cannot use Poweradmin until MFA is configured.

> **Note:** MFA enforcement requires both the global `mfa.enabled` and `mfa.enforced` settings to be set to `true` in your configuration. See [Configuration](#configuration) below.

## Disabling MFA

To disable MFA on your account:

1. Navigate to **Account** in the top navigation bar
2. In the MFA section, click **Disable MFA**
3. Confirm the action

After disabling, you will only need your password to log in.

> **Note:** If MFA is enforced for your account through a user or group template, you will be required to set it up again on your next login.

## Recovery

If you lose access to your authenticator app or email:

1. On the MFA verification screen, enter one of your **recovery codes** instead of a TOTP code
2. Each recovery code can only be used once - it is removed from your list after use
3. After logging in, go to **Account** and either:
    - Set up MFA again with a new authenticator app
    - Regenerate new recovery codes if your supply is running low

If you have no remaining recovery codes and cannot access your authenticator, contact your Poweradmin administrator. An admin can disable MFA on your account so you can set it up again.

## Configuration

MFA is configured in `config/settings.php` under the `security` section:

```php
'security' => [
    'mfa' => [
        'enabled' => true,
        'enforced' => true,
        'app_enabled' => true,
        'email_enabled' => true,
        'recovery_codes' => 8,
        'recovery_code_length' => 10,
    ],
],
```

- **enabled** - enable MFA functionality globally. Default: `false`
- **enforced** - enable MFA enforcement (works with `user_enforce_mfa` permission). Default: `false`
- **app_enabled** - allow authenticator app method. Default: `true`
- **email_enabled** - allow email verification method (requires [mail configuration](../configuration/mail.md)). Default: `true`
- **recovery_codes** - number of recovery codes to generate per user. Default: `8`
- **recovery_code_length** - character length of each recovery code. Default: `10`

For the full list of security settings, see [Security Policies](../configuration/security-policies.md).
