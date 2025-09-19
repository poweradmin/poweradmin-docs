# UI Customization Overview

Poweradmin provides several ways to customize the user interface to match your organization's needs. All UI configurations are set in the `settings.php` file under the `interface` section.

## Configuration Options

The following settings control the user interface appearance and behavior:

- **language**: Default language for the interface. Default: `en_EN`
- **enabled_languages**: Comma-separated list of available languages. Default: `cs_CZ,de_DE,en_EN,es_ES,fr_FR,it_IT,ja_JP,lt_LT,nb_NO,nl_NL,pl_PL,pt_PT,ru_RU,tr_TR,zh_CN`
- **theme**: UI theme name. Options: `default`, `custom`. Default: `default`
- **style**: UI style. Options: `light`, `dark`. Default: `light`
- **theme_base_path**: Base path for theme templates. Default: `templates`
- **title**: Title displayed in the browser. Default: `Poweradmin`
- **session_timeout**: Session timeout in seconds. Default: `1800` (30 minutes)
- **rows_per_page**: Number of items to display per page. Default: `10`
- **index_display**: Display mode for the index page. Options: `cards`, `list`. Default: `cards`

### UI Element Settings

- **show_record_id**: Show record ID column in edit mode. Default: `true`
- **position_record_form_top**: Position the "Add record" form at the top of the page. Default: `false`
- **position_save_button_top**: Position the "Save changes" button at the top of the page. Default: `false`
- **show_zone_comments**: Show or hide zone comments. Default: `true`
- **show_record_comments**: Show or hide record comments. Default: `false`
- **display_serial_in_zone_list**: Display serial number in zone list. Default: `false`
- **display_template_in_zone_list**: Display template information in zone list. Default: `false`
- **display_fullname_in_zone_list**: Show user's full name instead of username in zone lists. Default: `false`
- **search_group_records**: Group records by name and content in search results. Default: `false`
- **reverse_zone_sort**: Reverse zone sorting algorithm. Options: 'natural' (default), 'hierarchical' (experimental). Default: `natural`
- **show_pdns_status**: Show PowerDNS server status page and dashboard card. Default: `false`
- **display_hostname_only**: Display only hostname part in zone edit form (strips zone suffix). Default: `false`
- **enable_consistency_checks**: Enable database consistency checks page. Default: `false`

### Zone Editing Features

- **add_reverse_record**: Enable checkbox to add PTR record from regular zone view. Default: `true`
- **add_domain_record**: Enable checkbox to add A/AAAA record from reverse zone view. Default: `true`

## Example Configuration

```php
return [
    'interface' => [
        'language' => 'en_EN',
        'theme' => 'custom',
        'style' => 'dark',
        'theme_base_path' => 'templates',
        'title' => 'DNS Management Console',
        'rows_per_page' => 20,
        'index_display' => 'list',
        'show_record_comments' => true,
        'position_save_button_top' => true,
    ],
];
```

## Customization Options

Poweradmin offers several ways to customize the user interface:

1. **Themes and Styles**: Choose between different themes and light/dark styles
2. **Custom Templates**: Create custom header and footer templates
3. **Layout Configuration**: Control which UI elements are displayed and their positioning

See the specific documentation pages for more detailed information on each customization option:

- [Themes](./themes.md)
- [Layout](./layout.md) (includes custom header and footer setup)
- [UI Styling](./custom-css.md)