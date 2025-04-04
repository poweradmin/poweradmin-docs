# Layout Customization

Poweradmin allows you to customize various layout aspects to better fit your workflow. These settings are configured in the `config/settings.php` file under the `interface` section.

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