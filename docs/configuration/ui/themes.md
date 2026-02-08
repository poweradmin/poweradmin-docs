# Themes

Poweradmin includes built-in themes that can be selected through the configuration file to change the application's visual appearance.

## Available Themes

Poweradmin comes with the following themes:

- **default**: The standard theme
- **custom**: For custom theme templates

## Theme Configuration

Configure your preferred theme in the `settings.php` file under the `interface` section:

```php
return [
    'interface' => [
        'theme' => 'default',  // Options: 'default', 'custom', etc.
        'style' => 'light',    // Options: 'light', 'dark'
        'theme_base_path' => 'templates', // Base path for theme templates
    ],
];
```

## Theme Screenshots

### Light Style
![Light Theme](/screenshots/modern.png)

### Dark Style
![Dark Theme](/screenshots/punk.png)

## Theme Components

Each theme includes consistent styling for:

- Navigation menus
- Form elements
- Buttons and controls
- Tables and data views
- Modals and dialogs
- Notifications and alerts

## Creating Custom Themes

Poweradmin supports custom themes through the theme templates system. To create a custom theme:

1. Set the theme to `custom` in your settings
2. Create a directory structure in your theme base path:

```
templates/
└── custom/
    ├── header.html
    ├── footer.html
    └── other template files...
```

3. Customize the template files to match your organization's branding

## Theme Customization

For more information on customizing themes, see:
- [Custom UI Layout](./layout.md) (includes custom header and footer setup)
- [Custom CSS](./custom-css.md) (for additional style customization)