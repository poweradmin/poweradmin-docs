# Username Recovery

Poweradmin v4.1.0+ includes a username recovery feature that allows users to recover their forgotten username via email.

## Overview

When enabled, users can request their username by providing their registered email address. The system sends an email containing the username associated with that email address.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `security.username_recovery.enabled` | false | Enable username recovery feature |
| `security.username_recovery.rate_limit_attempts` | 5 | Maximum recovery attempts per time window |
| `security.username_recovery.rate_limit_window` | 3600 | Time window for rate limiting (seconds) |
| `security.username_recovery.min_time_between_requests` | 60 | Minimum time between requests (seconds) |

## Configuration

These keys live under the `security` section. A top-level `username_recovery` block is ignored.

```php
return [
    'security' => [
        'username_recovery' => [
            'enabled' => true,
            'rate_limit_attempts' => 5,
            'rate_limit_window' => 3600,      // 1 hour
            'min_time_between_requests' => 60, // 1 minute
        ],
    ],
];
```

## Docker Configuration

```yaml
environment:
  PA_USERNAME_RECOVERY_ENABLED: "true"
  PA_USERNAME_RECOVERY_RATE_LIMIT_ATTEMPTS: "5"
  PA_USERNAME_RECOVERY_RATE_LIMIT_WINDOW: "3600"
  PA_USERNAME_RECOVERY_MIN_TIME_BETWEEN: "60"
```

## Requirements

Username recovery requires:

1. **Email configured**: Mail settings must be properly configured
2. **User email addresses**: Users must have email addresses in their profiles
3. **`interface.application_url` (recommended)**: The login link in the email is built from this value alone. No request header and no web server variable is consulted, because the email goes to the account owner and a forged host would point a third party at an attacker's site. When it is empty the email is still sent, but the "Go to Login Page" link is omitted.

See [Mail Configuration](mail.md) for email setup.

## Rate Limiting

The rate limiting prevents abuse of the recovery feature:

- **Attempts per window**: Maximum 5 attempts (default) per hour
- **Minimum interval**: At least 60 seconds between requests
- **Per-IP tracking**: Rate limits are tracked per IP address

If a user exceeds the rate limit, they receive a generic message (to prevent email enumeration).

## Security Considerations

1. **Generic responses**: The system returns the same message whether or not the email exists, preventing email enumeration attacks

2. **Rate limiting**: Protects against brute-force attempts to discover valid email addresses

3. **Logging**: All recovery attempts are logged for security auditing

4. **Email verification**: Only sends to verified email addresses in the system

## User Flow

1. User clicks "Forgot username?" on login page
2. User enters their email address
3. System validates rate limits
4. If email exists, username is sent via email
5. User receives generic confirmation message (regardless of email existence)

## Related Documentation

- [Mail Configuration](mail.md)
- [Security Policies](security-policies.md)
