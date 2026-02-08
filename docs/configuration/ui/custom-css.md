# Custom CSS

Poweradmin supports custom CSS files that allow you to customize the interface styling while surviving application updates.

*Added in version 4.1.0*

## Overview

Each theme includes support for custom CSS extension files that are automatically loaded alongside the base theme styles. This allows you to:

- Customize colors, fonts, and spacing
- Add your organization's branding
- Override specific UI elements
- Keep customizations separate from core files

## Quick Start

1. Navigate to your theme's style directory:

    ```
    templates/default/style/
    ```

2. Copy the example files:

    ```bash
    cp custom_light.css.example custom_light.css
    cp custom_dark.css.example custom_dark.css
    ```

3. Edit the CSS files to match your preferences

4. Refresh your browser - custom styles are automatically loaded

## How It Works

| File | Description |
|------|-------------|
| `custom_light.css` | Loaded automatically when using Light style |
| `custom_dark.css` | Loaded automatically when using Dark style |

- Custom stylesheets override base theme styles using CSS cascade
- Files are only loaded if they exist (no errors if missing)
- Works with the existing light/dark theme switcher

## File Structure

```
templates/default/style/
├── light.css                    # Base light theme (don't modify)
├── dark.css                     # Base dark theme (don't modify)
├── custom_light.css.example     # Light theme customization examples
├── custom_dark.css.example      # Dark theme customization examples
├── custom_light.css             # Your light theme customizations (create this)
└── custom_dark.css              # Your dark theme customizations (create this)
```

## Example Customizations

### Custom Brand Colors

```css
/* custom_light.css */
:root {
    --bs-primary: #0066cc;
    --bs-primary-rgb: 0, 102, 204;
}

.navbar {
    background-color: #0066cc !important;
}
```

### Custom Logo Area

```css
/* custom_light.css */
.navbar-brand {
    font-weight: bold;
    color: #333 !important;
}
```

### Wider Content Area

```css
/* custom_light.css */
.container-fluid {
    max-width: 1600px;
}
```

## Tips

- Use `!important` when needed to ensure your styles override base theme styles
- Test with both light and dark themes if you use theme switching
- Remove example styles you don't need before deploying to production
- Keep customizations minimal for easier maintenance during upgrades

## Benefits

- **Update-safe**: Your customizations survive all Poweradmin updates
- **Automatic loading**: No configuration changes needed
- **Theme switching**: Works with existing light/dark theme switcher
- **CSS cascade**: Your styles naturally override base themes

## Available Styles

Poweradmin comes with the following base styles:

- **light** (default): A clean, bright interface style
- **dark**: A darker interface style that reduces eye strain in low-light environments

## Style Configuration

To change the default style, update the `style` setting in `config/settings.php`:

```php
return [
    'interface' => [
        'theme' => 'default',  // The theme to use (default, modern)
        'style' => 'dark',     // Options: 'light', 'dark'
    ],
];
```

## Theme and Style Relationship

In Poweradmin, the visual appearance is controlled by two settings:

1. **theme**: Controls the template structure (default, modern)
2. **style**: Controls the color scheme (light, dark)

This separation allows for maximum flexibility in customizing the interface.

## Related Documentation

- [Themes](./themes.md)
- [Layout](./layout.md) (includes custom header and footer setup)
