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
- **debug**: Enable debug logging for email operations. Default: `false` *(Added in v4.0.3)*

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
        'smtp' => [
            'host' => 'smtp.example.com',
            'port' => 587,
            'username' => 'smtp_user',
            'password' => 'smtp_password',
            'encryption' => 'tls',  // 'tls', 'ssl', or null
            'auth' => true,
        ],
        'debug' => false,  // Set to true for detailed logging (v4.0.3+)
    ],
];
```

## Troubleshooting

### Email Debug Logging *(v4.0.3+)*

Enable detailed debug logging to troubleshoot email delivery issues:

```php
'mail' => [
    'debug' => true,  // Enable comprehensive debug logging
],
```

When enabled, Poweradmin logs:
- SMTP connection attempts and responses
- Authentication process
- Email composition and sending operations
- Detailed error messages

Check your web server error log or PHP error log for debug output.

### TLS/STARTTLS Issues *(Fixed in v4.1.0)*

**Problem:** Email sending fails with TLS/STARTTLS errors in versions prior to v4.1.0.

**Solution:** Upgrade to v4.1.0 or later, which includes proper TLS/STARTTLS connection handling.

If you're experiencing issues with TLS encryption:

1. **Verify encryption setting:**
   ```php
   'encryption' => 'tls',  // For STARTTLS on port 587
   // or
   'encryption' => 'ssl',  // For SMTPS on port 465
   // or
   'encryption' => null,   // For unencrypted connections (not recommended)
   ```

2. **Common port and encryption combinations:**
   - **Port 587** with `'encryption' => 'tls'` (STARTTLS) - Most common
   - **Port 465** with `'encryption' => 'ssl'` (SMTPS) - Older systems
   - **Port 25** with `'encryption' => null` - Not recommended

### Email Rejection Due to Long Lines *(Fixed in v4.0.3)*

**Problem:** Some SMTP servers reject emails with lines longer than 998 characters (RFC 5322 limit).

**Solution:** Upgrade to v4.0.3 or later, which implements proper line wrapping for email content.

This particularly affects:
- Long DKIM signatures
- Extensive HTML email templates
- Large text blocks in password reset emails

### Common SMTP Authentication Issues

**Problem:** SMTP authentication fails even with correct credentials.

**Troubleshooting steps:**

1. **Verify credentials:** Double-check username and password
2. **Test SMTP connectivity:**
   ```bash
   telnet smtp.example.com 587
   ```
3. **Check firewall rules:** Ensure outbound SMTP ports are open
4. **Review server logs:** Enable `'debug' => true` for detailed logging
5. **Try alternative ports:** Test port 465 (SSL) or 25 if 587 fails

### Email Not Being Delivered

**Common causes:**

1. **Incorrect "from" address:** Some SMTP servers require matching authentication username
2. **SPF/DKIM issues:** Ensure your server's IP is authorized to send from the domain
3. **Blacklisted IP:** Check if your server's IP is on spam blacklists
4. **Rate limiting:** SMTP server may be throttling connections

**Debugging steps:**

1. Enable debug logging: `'debug' => true`
2. Check mail server logs
3. Verify email appears in sent items (if using external SMTP)
4. Test with a simple mail client using same credentials

## Version History

### v4.1.0
- **Fixed:** TLS/STARTTLS connection handling (issue #861)
  - Properly handles different encryption modes
  - Resolves connection failures with certain SMTP servers

### v4.0.3
- **Added:** Comprehensive debug and operational logging
  - Detailed SMTP transaction logging
  - Authentication process visibility
  - Error message improvements
- **Fixed:** Email rejection due to long lines (issue #798)
  - Implements RFC 5322 compliant line wrapping
  - Prevents SMTP server rejections

### v4.0.2
- **Fixed:** Invalid SMTP headers causing server rejections (issue #774)
  - Removed non-standard headers
  - Improved RFC compliance
- **Fixed:** SMTP authentication and response parsing issues
  - Better error handling
  - More reliable authentication

### v4.0.0
- New Twig-based email template system
- Support for custom email templates
- Dark mode email templates
- Plain text body support
- Template preview functionality
- Multiple transport options (SMTP, sendmail, PHP mail)

## Related Documentation

- [Password Reset Configuration](password-reset.md) - Password reset email settings
- [Security Policies](security-policies.md) - MFA email verification
- [User Agreements](user-agreements.md) - Agreement acceptance notifications

