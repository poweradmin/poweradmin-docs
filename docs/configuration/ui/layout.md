# Layout Customization

Poweradmin allows you to customize various layout aspects to better fit your workflow. These settings are configured in the `config/settings.php` file under the `interface` section.

## Custom Header and Footer

In addition to the layout settings below, Poweradmin also supports custom header and footer templates. See [Custom Header and Footer](#custom-header-and-footer) section at the end of this document for details.

## UI Element Positioning

### Form Element Positioning

Control the positioning of key UI elements:

- **position_record_form_top**: Place the "Add record" form at the top of the page. Default: `false`
- **position_save_button_top**: Place the "Save changes" button at the top of the page. Default: `true`

```php
return [
    'interface' => [
        'position_record_form_top' => true,
        'position_save_button_top' => true,
    ],
];
```

### Content Display Options

Configure which information is displayed in the user interface:

- **show_record_id**: Show record ID column in edit mode. Default: `true`
- **show_zone_comments**: Show zone comments. Default: `true`
- **show_record_comments**: Show record comments. Default: `false`
- **display_serial_in_zone_list**: Show serial number in zone list. Default: `false`
- **display_template_in_zone_list**: Show template information in zone list. Default: `false`

```php
return [
    'interface' => [
        'show_record_id' => true,
        'show_zone_comments' => true,
        'show_record_comments' => true,
        'display_serial_in_zone_list' => true,
    ],
];
```

## Display Mode

Configure how the main index page displays information:

- **index_display**: Choose between card view or list view. Options: `cards`, `list`. Default: `cards`

```php
return [
    'interface' => [
        'index_display' => 'list',
    ],
];
```

## Pagination

Control how many items appear per page:

- **rows_per_page**: Number of items displayed per page. Default: `10`

```php
return [
    'interface' => [
        'rows_per_page' => 20,
    ],
];
```

## Zone Editing Features

Enable or disable special editing features:

- **add_reverse_record**: Add the checkbox option to create PTR records from A/AAAA record view. Default: `true`
- **add_domain_record**: Add the checkbox option to create A/AAAA records from PTR record view. Default: `true`

```php
return [
    'interface' => [
        'add_reverse_record' => true,
        'add_domain_record' => true,
    ],
];
```

## Example Full Configuration

```php
return [
    'interface' => [
        'position_record_form_top' => false,
        'position_save_button_top' => true,
        'show_record_id' => true,
        'show_zone_comments' => true,
        'show_record_comments' => true,
        'display_serial_in_zone_list' => true,
        'display_template_in_zone_list' => true,
        'index_display' => 'list',
        'rows_per_page' => 15,
        'add_reverse_record' => true,
        'add_domain_record' => true,
    ],
];
```

## Custom Header and Footer

Poweradmin allows you to personalize the header (logo and title) and footer sections by creating custom template files. This is useful for branding your installation or adding custom navigation elements.

### Configuration

First, you need to enable custom header/footer in the settings file. Create or edit the file `config/settings.php` with the following configuration:

```php
<?php
return [
    // Other existing settings...
    
    /**
     * Interface Settings
     */
    'interface' => [
        // Other interface settings...
        
        // Custom header and footer settings
        'custom_header' => true,  // Enable custom header
        'custom_footer' => true,  // Enable custom footer
        
        // Other interface settings...
    ],
    
    // Other existing settings...
];
```

### Creating Custom Templates

1. Create a directory named `custom` inside your `templates` folder:

```
mkdir -p templates/custom
```

2. Create the following files:

#### Custom Header (templates/custom/header.html)

```html
<!-- Your custom header content goes here -->
<img src="assets/your-logo.png" height="32">
<span class="fs-4">Your Custom Title</span>
```

#### Custom Footer (templates/custom/footer.html)

```html
<!-- Your custom footer content goes here -->
<p>© 2025 Your Organization - Powered by <strong>Poweradmin</strong></p>
```

Here are examples of custom templates in action:

#### Custom Header File Structure
![Custom Header Structure](../../screenshots/custom_header.png)

#### Custom Footer Example
![Custom Footer Example](../../screenshots/custom_footer.png)

### Template Variables

The following template variables are available in your custom templates:

#### Header Template Variables

- `{{ iface_title }}` - Title from configuration settings
- `{{ iface_style }}` - Current theme style (ignite or spark)
- `{{ file_version }}` - File version timestamp for cache busting

#### Footer Template Variables

- `{{ version }}` - Poweradmin version
- `{{ iface_style }}` - Current theme style
- `{{ file_version }}` - File version timestamp for cache busting

### Examples

#### Corporate Branding Header

```html
<img src="assets/corporate-logo.png" height="40">
<span class="fs-4 ms-2">Corporate DNS Management Portal</span>
```

#### Extended Footer with Links

```html
<div class="d-flex flex-column">
  <p class="mb-1">© 2025 Your Organization - DNS Management</p>
  <p class="mb-0 small">
    <a href="https://support.example.com" class="text-decoration-none">Support</a> |
    <a href="https://docs.example.com" class="text-decoration-none">Documentation</a> |
    <a href="mailto:dns-admin@example.com" class="text-decoration-none">Contact</a>
  </p>
</div>
```

### Notes

- The custom templates use Twig templating engine
- Bootstrap 5 classes are available for styling
- Changes may be overwritten during updates - keep backups of your custom files
- You can include custom JavaScript in your header/footer templates if needed