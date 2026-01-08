# Username Recovery

Poweradmin v4.0.0+ includes a username recovery feature that allows users to recover their forgotten username via email.

## Overview

When enabled, users can request their username by providing their registered email address. The system sends an email containing the username associated with that email address.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `username_recovery.enabled` | false | Enable username recovery feature |
| `username_recovery.rate_limit_attempts` | 5 | Maximum recovery attempts per time window |
| `username_recovery.rate_limit_window` | 3600 | Time window for rate limiting (seconds) |
| `username_recovery.min_time_between_requests` | 60 | Minimum time between requests (seconds) |

## Modern Configuration

```php
return [
    'username_recovery' => [
        'enabled' => true,
        'rate_limit_attempts' => 5,
        'rate_limit_window' => 3600,      // 1 hour
        'min_time_between_requests' => 60, // 1 minute
    ],
];
```

## Docker Configuration

```yaml
environment:
  PA_USERNAME_RECOVERY_ENABLED: "true"
  PA_USERNAME_RECOVERY_RATE_LIMIT_ATTEMPTS: "5"
  PA_USERNAME_RECOVERY_RATE_LIMIT_WINDOW: "3600"
  PA_USERNAME_RECOVERY_MIN_TIME_BETWEEN_REQUESTS: "60"
```

## Requirements

Username recovery requires:

1. **Email configured**: Mail settings must be properly configured
2. **User email addresses**: Users must have email addresses in their profiles

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
