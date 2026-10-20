# Zone Import/Export Configuration

## Overview

Poweradmin includes zone import/export functionality that allows users to import zones from BIND zone files and export zones as zone files. This is useful for migrating zones between DNS servers or for backup purposes.

## Configuration Options

Zone import/export settings can be configured in the `config/settings.php` file under the `modules` > `zone_import_export` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable zone import/export functionality |
| `auto_ttl_value` | `300` | Default TTL in seconds for records when importing zone files |
| `max_file_size` | `1048576` | Maximum allowed file upload size in bytes (default: 1 MB) |

## Configuration Example

### PHP Configuration

```php
return [
    'modules' => [
        'zone_import_export' => [
            'enabled' => true,
            'auto_ttl_value' => 300,
            'max_file_size' => 1048576,
        ],
    ],
];
```

### Docker Environment Variables

```bash
docker run -d --name poweradmin -p 80:80 \
  -e PA_MODULE_ZONE_IMPORT_EXPORT_ENABLED=true \
  -e PA_MODULE_ZONE_IMPORT_EXPORT_AUTO_TTL=300 \
  -e PA_MODULE_ZONE_IMPORT_EXPORT_MAX_FILE_SIZE=1048576 \
  poweradmin/poweradmin
```

| Variable | Description | Default |
|----------|-------------|---------|
| `PA_MODULE_ZONE_IMPORT_EXPORT_ENABLED` | Enable zone import/export module | `false` |
| `PA_MODULE_ZONE_IMPORT_EXPORT_AUTO_TTL` | Default TTL for imported records (seconds) | `300` |
| `PA_MODULE_ZONE_IMPORT_EXPORT_MAX_FILE_SIZE` | Max upload file size in bytes | `1048576` |

## Usage

When enabled, zone import/export features are available from:

1. **Zone Export** - Export any zone as a BIND zone file from the zone management page
2. **Zone Import** - Import zones from BIND zone files via the Tools menu

### Zone Export

1. Navigate to any zone in Poweradmin
2. Click the **Export** button or icon
3. Select **Zone File** format
4. The zone file will be downloaded in BIND format

### Zone Import

1. Navigate to **Tools** > **Zone Import** in the navigation menu
2. Upload a BIND-format zone file
3. Review the parsed records
4. Confirm the import

### Record Comments *(v4.6.0+)*

Zone files can carry Poweradmin record comments, so a zone keeps them when it is exported
and imported again. Both directions need `interface.show_record_comments` enabled.

**Export.** Tick **Include comments** in the zone page's **Export** menu before choosing
**Zone File**. Each comment is written on the line above its record, one marker line per
line of the comment:

```
; poweradmin-comment: web server
; poweradmin-comment: replaced in March
www.example.com. 3600 IN A 192.0.2.1
```

The marker starts with `;`, so BIND, `pdnsutil load-zone` and other tools read it as an
ordinary comment. With the box unticked the export is unchanged. A file with comments is
built by Poweradmin from the zone's records rather than taken from the PowerDNS zone
export.

**Import.** Zone Import reads `; poweradmin-comment:` lines back into the comment of the
record that follows them; the preview shows how many comments will be imported and lists
them next to their records. Other `;` comments are ignored as before. A marker that is not
directly followed by a record is skipped with a warning. When record comments are
disabled, the comments in the file are skipped and the preview says so.

Disabled records are not exported, with or without comments, because a zone file cannot
mark a record as disabled. The copy kept when a change request deletes a zone is the
exception: it writes them as `; poweradmin-disabled:` lines, and Zone Import restores those
as disabled records.

### Supported Features

- BIND zone file format
- DNSSEC record types
- IDN (Internationalized Domain Names) support
- Record comment synchronization
- Automatic TTL assignment for records without explicit TTL values

## Security Considerations

- Zone import requires appropriate user permissions
- File uploads are limited by the `max_file_size` setting
- Imported records are validated before being added to the database
