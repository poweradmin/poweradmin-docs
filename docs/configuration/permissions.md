# Permissions Settings

Poweradmin supports two permission management approaches that can be used independently or together:

- **User access templates** - Assign permission templates directly to individual users. Permissions apply globally across the system.
- **Group access templates** - Assign permission templates to groups, then add users to groups. Permissions apply to zones owned by the group.

Both systems are enabled by default. You can hide either one from the UI by setting the corresponding toggle to `false` in your `settings.php` file.

## Configuration

Add a `permissions` section to your `settings.php`:

```php
'permissions' => [
    'show_user_access_templates' => true,
    'show_group_access_templates' => true,
],
```

### Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `show_user_access_templates` | `true` | Show per-user access template assignment in the UI |
| `show_group_access_templates` | `true` | Show group-based access template management in the UI |

## Usage Scenarios

### Group-only permissions (recommended for larger teams)

Set `show_user_access_templates` to `false` to hide user-level template assignment. All permission management happens through groups:

```php
'permissions' => [
    'show_user_access_templates' => false,
    'show_group_access_templates' => true,
],
```

When user templates are hidden:

- New users are automatically assigned the minimal (Guest) permission template
- The template dropdown is hidden from user creation and edit forms
- The Template column is hidden from the users list
- The permission template list shows only group templates
- The "Access" nav menu is renamed to "Templates"

### User-only permissions (simpler setups)

Set `show_group_access_templates` to `false` to hide group management entirely:

```php
'permissions' => [
    'show_user_access_templates' => true,
    'show_group_access_templates' => false,
],
```

When group templates are hidden:

- The Groups navigation menu is hidden
- Group membership sections are hidden from user forms
- The Groups column is hidden from the users list
- Group management pages return an error if accessed directly
- The permission template list shows only user templates

### Both enabled (default)

When both are enabled, the permission template list shows both user and group types with filter tabs, and all UI elements are visible.

## Important Notes

> **Warning:** These toggles hide the management UI but do **not** change backend permission resolution. Both user templates and group memberships are always evaluated regardless of toggle values. Existing assignments remain active when hidden from the UI. Review and clean up existing assignments before disabling either option.

- The admin user created during installation retains full access via their Administrator template.
- API endpoints are not affected by these toggles - both template types remain accessible via the API.

> **Note:** The `permissions` settings group was introduced in Poweradmin 4.3.0.
