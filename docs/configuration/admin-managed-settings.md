# Admin-Managed Settings (4.5.0)

Poweradmin 4.5.0 introduces an internal layered settings model so individual configuration values can move from `config/settings.php` into the database and become editable through the admin UI without rebuilding the file. **No setting is migrated automatically** - this page describes the plumbing that future features will use.

## Layered resolution

When code reads a setting through `AppSettingsService`, the value is resolved in this order:

1. **`app_settings` table** - a row keyed by the dotted setting name (e.g. `interface.theme`)
2. **`config/settings.php`** - the matching `ConfigurationManager` entry, split on the first `.` (so `interface.theme` falls back to `get('interface', 'theme')`)
3. **Caller-supplied default**

The first non-null value wins. Reads are memoized within a single request.

## When to use what

| Storage | Use for |
|---|---|
| `config/settings.php` | Bootstrap configuration the app needs before the DB is reachable: database credentials, encryption keys, install paths, file logging targets. |
| `app_settings` (DB) | Generic admin-managed knobs - UI toggles, defaults, thresholds. Reach for this when you want an admin to flip a value without editing files on disk. |
| Dedicated table (e.g. [`record_type_defaults`](../user-guide/reverse-dns.md#per-record-type-default-ttls)) | Settings that have structure - per-type, per-zone, per-user overrides - or that need indexed lookups beyond a single key. |

## Schema

The `app_settings` table is created by the 4.5.0 schema update (`sql/poweradmin-{mysql,pgsql,sqlite}-update-to-4.5.0.sql`):

```sql
CREATE TABLE app_settings (
    setting_key   varchar(128) NOT NULL PRIMARY KEY,
    setting_value text         NOT NULL,
    value_type    varchar(16)  NOT NULL DEFAULT 'string',
    created_at    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

`value_type` is a hint (`string`, `int`, `bool`, `json`) that `AppSettingsService` uses to cast `setting_value` on read.

## For developers

`AppSettingsService` exposes typed getters and setters:

```php
$service = new AppSettingsService($config, $repository);

$theme  = $service->getString('interface.theme', 'light');
$ttl    = $service->getInt('dns.ttl', 86400);
$debug  = $service->getBool('app.debug', false);
$types  = $service->getArray('dns.top_record_types', ['A', 'AAAA']);

$service->setString('interface.theme', 'dark');
$service->clear('dns.ttl'); // falls back to ConfigurationManager
```

When the schema update hasn't been applied yet, `DbAppSettingRepository::isReady()` returns false and reads degrade silently to the `ConfigurationManager` path - no user-visible breakage.

## What's not in 4.5.0

- No setting has been moved from `config/settings.php` yet. The new table exists but is empty.
- There is no admin UI for editing `app_settings` rows. Future features will add focused UIs (similar to [TTL defaults by record type](../user-guide/reverse-dns.md#per-record-type-default-ttls)) that read/write specific keys.
- Per-user overrides remain in [`user_preferences`](../user-guide/index.md) - `app_settings` is system-wide.
