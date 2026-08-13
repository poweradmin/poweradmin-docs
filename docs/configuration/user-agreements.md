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

1. **Login** - User logs in with an existing account
2. **Agreement Prompt** - The login pipeline redirects the user to `/user-agreement`
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

The agreement page always renders the `user_agreement.html` template of the active theme. There is no per-version template: to customize the text, create a single Twig fragment in the theme's `custom` directory.

```
templates/
├── default/
│   └── custom/
│       └── user_agreement_content.html
```

If that file exists it is included in place of the shipped default content. Changing `current_version` does not change which file is used, so update the fragment and the version together.

### Agreement Content Example

```twig
{# templates/default/custom/user_agreement_content.html #}
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
```

> **Note:** The file is a Twig template, not plain HTML. Literal `{{` and `{%` sequences are interpreted by Twig and must be escaped.

## Database Schema

The user agreement system uses the following database structure:

```sql
CREATE TABLE `user_agreements` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `agreement_version` varchar(50) NOT NULL,
    `accepted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ip_address` varchar(45) DEFAULT NULL,
    `user_agent` text DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_user_agreement` (`user_id`, `agreement_version`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_agreement_version` (`agreement_version`),
    CONSTRAINT `fk_user_agreements_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);
```

The `(user_id, agreement_version)` pair is unique, so a user has at most one row per version.

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

### New Users

Poweradmin has no self-registration: accounts are created by an administrator. The agreement does not gate account creation or activation, it gates access.

1. Administrator creates the account
2. User logs in and is redirected to the agreement page
3. Access to the rest of the interface is blocked until the agreement is accepted

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

Poweradmin has no built-in agreement reports or administrative screens: there is no acceptance overview, no per-user reset and no bulk operation. The audit data lives in the `user_agreements` table, so query it directly for compliance status, past versions or an individual user's history. To force everyone to re-accept, raise `current_version`.
