# User Agreement Configuration

## Overview

Poweradmin supports a user agreement system that requires users to accept terms and conditions before using the system. This is useful for organizations that need to enforce usage policies or compliance requirements.

## Configuration Options

User agreement settings can be configured in the `config/settings.php` file under the `user_agreement` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable user agreement system |
| `current_version` | `1.0` | Current agreement version |
| `require_on_version_change` | `true` | Require re-acceptance when version changes |

## Configuration Example

```php
return [
    'user_agreement' => [
        'enabled' => true,
        'current_version' => '2.1',
        'require_on_version_change' => true,
    ],
];
```

## How It Works

### First-Time Users

1. **Registration/Login** - User creates account or logs in
2. **Agreement Prompt** - System displays user agreement
3. **Acceptance Required** - User must accept to continue
4. **Access Granted** - User can access the system

### Version Updates

When `require_on_version_change` is enabled:

1. **Version Check** - System compares user's accepted version with current
2. **Re-acceptance Required** - Users with older versions must re-accept
3. **Updated Record** - System records new acceptance date and version

### Agreement Storage

The system tracks:
- **User ID** - Which user accepted
- **Version** - Which version was accepted
- **Timestamp** - When agreement was accepted
- **IP Address** - From where agreement was accepted (for audit)

## Agreement Content Management

### Creating Agreement Content

Create agreement templates in your theme directory:

```
templates/
├── user_agreement/
│   ├── agreement_v1.0.html
│   ├── agreement_v2.0.html
│   └── agreement_v2.1.html
```

### Agreement Template Example

```html
<!-- templates/user_agreement/agreement_v2.1.html -->
<div class="user-agreement">
    <h2>DNS Management System - Terms of Use</h2>
    
    <h3>1. Acceptable Use</h3>
    <p>You agree to use this DNS management system only for legitimate business purposes...</p>
    
    <h3>2. Data Protection</h3>
    <p>All DNS data is confidential and must not be shared with unauthorized parties...</p>
    
    <h3>3. Security Requirements</h3>
    <ul>
        <li>Use strong passwords and change them regularly</li>
        <li>Do not share your account credentials</li>
        <li>Report security incidents immediately</li>
    </ul>
    
    <h3>4. Compliance</h3>
    <p>Users must comply with all applicable laws and regulations...</p>
    
    <div class="agreement-footer">
        <p><strong>Version:</strong> 2.1</p>
        <p><strong>Effective Date:</strong> January 1, 2024</p>
    </div>
</div>
```

## Database Schema

The user agreement system uses the following database structure:

```sql
CREATE TABLE user_agreements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    version VARCHAR(20) NOT NULL,
    accepted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_version (user_id, version)
);
```

## Administrative Functions

### Viewing Agreement Status

Administrators can view:
- **User acceptance status** - Which users have accepted current version
- **Acceptance history** - Historical acceptance records
- **Compliance reports** - Generate reports for audit purposes

### Forcing Re-acceptance

Administrators can:
- **Update version** - Change current version to force re-acceptance
- **Reset user status** - Require specific users to re-accept
- **Bulk operations** - Handle multiple users at once

## Use Cases

### Corporate Environment

```php
'user_agreement' => [
    'enabled' => true,
    'current_version' => 'CORP-2024.1',
    'require_on_version_change' => true,
],
```

**Benefits:**
- Legal compliance
- Policy enforcement
- Audit trail
- User accountability

### Service Provider

```php
'user_agreement' => [
    'enabled' => true,
    'current_version' => 'SLA-v3.2',
    'require_on_version_change' => true,
],
```

**Benefits:**
- Service level agreements
- Terms of service
- Liability protection
- Customer acknowledgment

## Integration with User Management

### New User Registration

When creating new users:
1. User completes registration
2. Agreement prompt appears
3. Acceptance is required before activation
4. User account is fully activated

### Existing User Management

For existing deployments:
1. Enable agreement system
2. Set current version
3. Users prompted on next login
4. Gradual rollout possible

## Compliance and Auditing

### Audit Trail

The system maintains:
- **Acceptance records** - Who accepted what and when
- **IP addresses** - Location of acceptance
- **User agents** - Browser/client information
- **Version history** - Track version changes

### Reporting

Generate reports for:
- **Compliance status** - Current acceptance rates
- **Historical data** - Past agreement versions
- **User activity** - Individual user agreement history

## Troubleshooting

### Common Issues

1. **Agreement not displaying**: Check template files exist
2. **Version not updating**: Verify configuration syntax
3. **Database errors**: Check table structure and permissions
4. **Users bypassing agreement**: Verify middleware configuration

### Best Practices

1. **Version naming**: Use clear, descriptive version numbers
2. **Regular updates**: Review and update agreements periodically
3. **Clear language**: Make agreements understandable
4. **Backup data**: Maintain acceptance records for compliance