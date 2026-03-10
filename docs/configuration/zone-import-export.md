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
