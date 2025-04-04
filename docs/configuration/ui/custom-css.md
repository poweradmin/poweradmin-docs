# UI Styling

Poweradmin uses built-in themes for its user interface styling. Currently, the application does not support custom CSS files for styling customization.

## Available Themes

Poweradmin comes with the following themes, which can be selected in the configuration file:

- **ignite** (default): A clean, light theme with modern design elements
- **spark**: A dark theme optimized for reduced eye strain in low-light environments

## Theme Configuration

To change the theme, update the `theme` setting in the `config/settings.php` file under the `interface` section:

```php
return [
    'interface' => [
        'theme' => 'ignite',  // Options: 'ignite', 'spark'
    ],
];
```

## Screenshots

### Ignite Theme (Light)
![Ignite Theme](/screenshots/ignite_zone_list.png)

### Spark Theme (Dark)
![Spark Theme](/screenshots/spark_zone_list.png)

## Theme Features

Each theme provides consistent styling for:

- Navigation menus
- Form elements
- Buttons and controls
- Tables and data views
- Modals and dialogs
- Notifications and alerts

For more information about themes, see the [Themes documentation](./themes.md).

## Future Development

Custom CSS support may be implemented in future versions of Poweradmin. If you need UI customization beyond the available themes, consider:

1. Contributing to the Poweradmin project
2. Requesting the feature in the project's issue tracker