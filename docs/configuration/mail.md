# Mail Configuration

This document describes how to configure email settings in Poweradmin.

## Overview

Poweradmin supports sending emails for various purposes:
- User registration confirmations
- Password reset requests
- DNS zone changes notifications
- System alerts

## Configuration Options

The mail settings are configured in the `config/settings.php` file under the `mail` section:

- **enabled**: Enable email functionality. Default: `false`
- **from**: Default "from" email address. Default: `poweradmin@example.com`
- **from_name**: Default "from" name. Default: empty
- **transport**: Transport method. Options: 'smtp', 'sendmail', 'php'. Default: `smtp`

### SMTP Settings

- **host**: SMTP server hostname. Default: `smtp.example.com`
- **port**: SMTP server port. Default: `587`
- **username**: SMTP authentication username. Default: empty
- **password**: SMTP authentication password. Default: empty
- **encryption**: Encryption method. Options: 'tls', 'ssl', empty. Default: `tls`
- **auth**: Whether SMTP requires authentication. Default: `false`

### Sendmail Settings

- **sendmail_path**: Path to sendmail binary. Default: `/usr/sbin/sendmail -bs`

### Email Templates

- **password_email_subject**: Subject for password reset emails. Default: `Your new account information`
- **email_signature**: Signature added to emails. Default: `DNS Admin`
- **email_title**: Title used in email templates. Default: `Your DNS Account Information`

## Example Configuration

```php
return [
    'mail' => [
        'enabled' => true,
        'from' => 'dns@company.com',
        'from_name' => 'DNS Administrator',
        'transport' => 'smtp',
        'host' => 'smtp.company.com',
        'port' => 587,
        'username' => 'smtp_user',
        'password' => 'smtp_password',
        'encryption' => 'tls',
        'auth' => true,
    ],
];
```

## Testing Mail Configuration

After configuring the mail settings, you can test your configuration by:

1. Going to Administration → System Settings
2. Clicking "Test Mail Configuration"
3. Entering a test email address
4. Clicking "Send Test Email"

## Troubleshooting

Common email issues and solutions:

- **Emails not sending**: Verify SMTP credentials and server settings
- **SSL/TLS errors**: Check encryption settings and port numbers
- **Authentication failures**: Verify username and password
- **Delayed delivery**: Review mail server queue and spam settings

## Security Considerations

- Use TLS encryption when possible
- Use dedicated email accounts for the application
- Regularly rotate SMTP credentials
- Be cautious with email content to avoid potential phishing concerns