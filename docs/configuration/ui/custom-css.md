# UI Styling

Poweradmin uses built-in themes for its user interface styling. Currently, the application does not support custom CSS files for styling customization.

## Available Styles

Poweradmin comes with the following styles, which can be selected in the configuration file:

- **light** (default): A clean, bright interface style
- **dark**: A darker interface style that reduces eye strain in low-light environments

## Style Configuration

To change the style, update the `style` setting in the `settings.php` file under the `interface` section:

```php
return [
    'interface' => [
        'theme' => 'default',  // The theme to use (default, custom)
        'style' => 'dark',     // Options: 'light', 'dark'
    ],
];
```

## Theme and Style Relationship

In Poweradmin, the visual appearance is controlled by two settings:

1. **theme**: Controls the template structure
2. **style**: Controls the color scheme and visual appearance

This separation allows for maximum flexibility in customizing the interface.

## UI Customization Options

Without custom CSS, you can still customize the UI using:

1. **Custom themes**: Create custom templates in your theme directory
2. **Style selection**: Choose between light and dark styles
3. **Layout settings**: Configure which UI elements are shown and their positioning

For more information about UI customization, see:
- [Themes documentation](./themes.md)
- [Layout documentation](./layout.md) (includes custom header and footer setup)