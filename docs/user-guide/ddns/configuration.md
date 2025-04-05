# Dynamic DNS Configuration

This guide will walk you through the process of setting up Dynamic DNS (DDNS) in Poweradmin.

## Setting Up User Permissions

You'll need to create a user with specific permissions for DDNS updates:

1. Create a permission template:
    - Navigate to `Users > Add permission template`
    - Provide a meaningful name (e.g., "dynamic") and description
    - Select required permissions:
        - `zone_master_add`
        - `zone_content_view_own`
        - `zone_content_edit_own` or `zone_content_edit_own_as_client` or `zone_content_edit_others`

![Permission Template Setup](../../screenshots/dynamic_update_01.png)

2. Create a new user:
    - Navigate to `Users > Add user`
    - Fill in user details
    - Apply the previously created template

![User Creation](../../screenshots/dynamic_update_02.png)

## Configuring DNS Zone

After creating a user with appropriate permissions:

1. Log in as the new user
2. Select "Add master zone"
3. Enter your domain name
4. Navigate to the created zone
5. Add a record for dynamic updates

![Zone Creation](../../screenshots/dynamic_update_03.png)
![Record Configuration](../../screenshots/dynamic_update_04.png)

## Server-Side Configuration

The Dynamic DNS functionality in Poweradmin is provided by the `dynamic_update.php` script, which handles DNS record updates when IP addresses change.

### Configuration Options

The main configuration is controlled through Poweradmin's settings:

```php
return [
    'dynamicdns' => [
        'enabled' => true,             // Enable or disable DDNS functionality
        'ttl' => 60,                   // Default TTL for dynamic records (in seconds)
        'allow_auto_detect' => true,   // Allow automatic IP detection
        'allow_ipv4' => true,          // Allow IPv4 updates
        'allow_ipv6' => true,          // Allow IPv6 updates
        'require_authentication' => true, // Require user authentication
    ],
];
```

### Security Considerations

1. **Use HTTPS**: Always use HTTPS for DDNS updates to prevent credentials and updates from being intercepted.
2. **Create dedicated users**: Create specific users for DDNS updates with minimal permissions.
3. **IP restrictions**: Consider implementing IP restrictions for DDNS user accounts if your update sources have static IP addresses.
4. **Regular auditing**: Periodically review DDNS activity in logs to detect unusual patterns.

## Testing Your Configuration

After setup, you can test your configuration using:

```bash
curl -u username:password "https://yourserver.com/dynamic_update.php?hostname=host.yourdomain.com&myip=auto"
```

A successful response will look like:
```
good 192.168.1.100
```

## Troubleshooting

If you encounter issues with your DDNS setup:

1. **Check permissions**: Ensure the user has proper permissions for zone editing
2. **Verify zone ownership**: The user must own or have access to the zone being updated
3. **Check authentication**: Verify credentials are correctly configured
4. **Review logs**: Check Poweradmin logs for detailed error messages
5. **Test manually**: Try manual updates with cURL to isolate client vs. server issues

For client setup instructions, see [Client Setup](client-setup.md).