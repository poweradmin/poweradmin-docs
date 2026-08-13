# UI Customization Overview

Poweradmin provides several ways to customize the user interface to match your organization's needs. All UI configurations are set in the `settings.php` file under the `interface` section.

## Configuration Options

The following settings control the user interface appearance and behavior:

- **language**: Default language for the interface. Default: `en_EN`
- **enabled_languages**: Comma-separated list of available languages. Default: `ar_SA,bg_BG,bs_BA,cs_CZ,da_DK,de_DE,el_GR,en_EN,es_ES,et_EE,fa_IR,fi_FI,fr_FR,ga_IE,he_IL,hi_IN,hr_HR,hu_HU,id_ID,it_IT,ja_JP,ko_KR,lt_LT,lv_LV,ms_MY,nb_NO,nl_NL,pl_PL,pt_BR,pt_PT,ro_RO,ru_RU,sk_SK,sl_SI,sq_AL,sr_RS,sv_SE,th_TH,tr_TR,uk_UA,vi_VN,zh_CN,zh_TW`
- **theme**: UI theme name. Two themes ship with Poweradmin: `default` and `modern`. Any other directory under `theme_base_path` is accepted, so you can add your own. Default: `default`
- **style**: UI style. Options: `light`, `dark`. Default: `light`
- **theme_base_path**: Base path for theme templates. Default: `templates`
- **favicon_path**: Path or URL to a custom favicon. Empty uses the bundled `favicon.ico`. Default: `''` (added in 4.4.0)
- **logo_path**: Path or URL to a custom header logo image. Empty uses the bundled `assets/logo.png`. Default: `''` (added in 4.4.0)
- **title**: Application title displayed in browser tab and header logo. Useful for distinguishing multiple server instances. Default: `Poweradmin`
- **session_timeout**: Session timeout in seconds. Default: `1800` (30 minutes)
- **rows_per_page**: Number of items to display per page. Default: `10`

### UI Element Settings

- **show_record_id**: Show record ID column in edit mode. Default: `false`
- **position_record_form_top**: Position the "Add record" form at the top of the page. Default: `true`
- **position_save_button_top**: Position the "Save changes" button at the top of the page. Default: `false`
- **show_zone_comments**: Show or hide zone comments. Default: `true`
- **show_record_comments**: Show or hide record comments. Default: `false`
- **display_serial_in_zone_list**: Display serial number in zone list. Default: `false`
- **display_signed_serial_in_zone_list**: Display the serial served by PowerDNS with SOA-EDIT applied (the "signed" serial) in zone lists. Requires the API backend and PowerDNS 4.2+ (v4.5.0+). Default: `false`
- **display_template_in_zone_list**: Display template information in zone list. Default: `false`
- **display_owner_in_zone_list**: Display owner column in zone lists (v4.5.0+). Default: `true`
- **display_group_in_zone_list**: Display group column in zone lists (v4.5.0+). Default: `true`
- **show_zone_record_count**: Display record count column in zone lists. Each user can override this via their preferences. Default: `true`. In API backend mode this costs one PowerDNS request per zone shown on the page
- **display_fullname_in_zone_list**: Show user's full name instead of username in zone lists. Default: `false`
- **search_group_records**: Group records by name and content in search results. Default: `false`
- **reverse_zone_sort**: Reverse zone sorting algorithm. Options: 'natural' (default), 'hierarchical' (experimental). Default: `natural`
- **show_pdns_status**: Show PowerDNS server status page and dashboard card. Default: `false`
- **show_dashboard_stats**: Show zone, record, user, and group counts on the dashboard for admin users. Default: `true`
- **display_hostname_only**: Display only hostname part in zone edit form (strips zone suffix). Default: `false`
- **wide_layout**: Use the full browser width instead of a fixed-width page (v4.5.0+). Site-wide default; each user can override this in their account preferences. Default: `false`
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