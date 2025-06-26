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

- **enabled**: Enable email functionality. Default: `true`
- **from**: Default "from" email address. Default: `poweradmin@example.com`
- **from_name**: Default "from" name. Default: empty
- **return_path**: Default "Return-Path" address for bounce handling. Default: `poweradmin@example.com`
- **transport**: Transport method. Options: 'smtp', 'sendmail', 'php'. Default: `php`

### SMTP Settings

- **host**: SMTP server hostname. Default: `smtp.example.com`
- **port**: SMTP server port. Default: `587`
- **username**: SMTP authentication username. Default: empty
- **password**: SMTP authentication password. Default: empty
- **encryption**: Encryption method. Options: 'tls', 'ssl', empty. Default: `tls`
- **auth**: Whether SMTP requires authentication. Default: `false`

### Sendmail Settings

- **sendmail_path**: Path to sendmail binary. Default: `/usr/sbin/sendmail -bs`


## Example Configuration

```php
return [
    'mail' => [
        'enabled' => true,
        'from' => 'dns@example.com',
        'from_name' => 'DNS Administrator',
        'return_path' => 'dns@example.com',
        'transport' => 'smtp',
        'host' => 'smtp.example.com',
        'port' => 587,
        'username' => 'smtp_user',
        'password' => 'smtp_password',
        'encryption' => 'tls',
        'auth' => true,
    ],
];
```

