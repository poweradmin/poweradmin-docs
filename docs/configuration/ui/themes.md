# Themes

Poweradmin includes built-in themes that can be selected through the configuration file to change the application's visual appearance.

## Available Themes

Poweradmin comes with the following themes:

- **ignite** (default): A clean, light theme with modern design elements
- **spark**: A dark theme optimized for reduced eye strain in low-light environments

## Theme Configuration

Configure your preferred theme in the `config/settings.php` file under the `interface` section:

```php
return [
    'interface' => [
        'theme' => 'ignite',  // Options: 'ignite', 'spark'
    ],
];
```

## Theme Screenshots

### Ignite Theme (Light)

The default light theme with a clean, professional interface.

![Ignite Theme](/screenshots/ignite_zone_list.png)

### Spark Theme (Dark)

A dark theme that reduces eye strain in low-light environments.

![Spark Theme](/screenshots/spark_zone_list.png)

## Theme Features

Each theme includes consistent styling for:

- Navigation menus
- Form elements
- Buttons and controls
- Tables and data views
- Modals and dialogs
- Notifications and alerts

## Theme Customization

While Poweradmin doesn't currently support custom theme creation, you can use [Custom CSS](./custom-css.md) to modify the appearance of the built-in themes.

For example, to change the primary color in the ignite theme:

```css
/* Custom color overrides for ignite theme */
.btn-primary {
    background-color: #3c8dbc;
    border-color: #367fa9;
}
```

For more advanced customization, see the [Custom CSS](./custom-css.md) documentation.