# DNS Templates

DNS templates in Poweradmin allow you to create standardized sets of DNS records that can be applied to multiple zones, streamlining zone management and ensuring consistency across domains.

## Template Management

Templates are managed through the Poweradmin interface and stored in the database. Each template can contain multiple DNS records of various types (A, CNAME, MX, etc.) that will be applied when the template is used.

Templates support placeholders that are automatically substituted:

- `[ZONE]` - replaced with the actual domain name
- `[SERIAL]` - replaced with current date + sequence (YYYYMMDD00)
- `[NS1]`, `[NS2]`, etc. - replaced with configured nameservers
- `[HOSTMASTER]` - replaced with configured hostmaster email

## Zone Template Application

### When Changing a Zone's Template

When you change a zone's template on the edit page:

- **Only template-generated records are overwritten** - the system specifically deletes records that were originally created from templates
- **Manual records are completely preserved** - any records you added manually remain untouched
- **Changes are immediate** - template application happens instantly when you save the change
- **SOA records are handled specially** - existing serial numbers are preserved and incremented appropriately

### How Poweradmin Tracks Template Records

Poweradmin maintains a database table (`records_zone_templ`) that tracks which DNS records were created from templates. This allows the system to:

- Identify which records can be safely replaced during template updates
- Preserve manually added records during template changes
- Maintain the relationship between zones and their source templates

## Template Synchronization

### Manual Updates Only

**Important**: Zones do NOT automatically update when templates are modified. This is by design to give administrators explicit control over when changes are applied.

### Methods to Apply Template Changes

**Individual Zone Update**:

1. Go to Edit Zone page
2. Change the template dropdown (even to the same template)
3. Save changes - this triggers a template refresh

**Bulk Zone Update**:

1. Go to Edit Template page
2. Click "Update Zones" button
3. This updates ALL zones currently using that template

### No Automatic Sync Indicators

Poweradmin does not currently provide interface indicators showing which zones are "out of sync" with their templates. Administrators must manually track when template changes need to be applied to existing zones.

## Permissions

### Zone Template Operations

Different template operations require different permissions:

- **Creating zone templates**: Requires `zone_templ_add` permission
- **Listing zone templates**: Requires `zone_master_add` OR `user_is_ueberuser` permission
- **Editing/deleting zone templates**: Requires `user_is_ueberuser` OR (`zone_templ_edit` AND template ownership)
- **Adding/editing/deleting template records**: Requires `user_is_ueberuser` OR (`zone_templ_edit` AND template ownership)

### Applying Templates to Zones

- **Creating zones with templates**: Requires `zone_master_add` OR `zone_slave_add` permission
- **Changing existing zone templates**: Requires zone editing permissions (`zone_content_edit_own` for owned zones or `zone_content_edit_others` for other zones)
- **Unlinking zones from templates**: Requires `user_is_ueberuser` OR zone editing permissions (`zone_content_edit_own`/`zone_content_edit_others` OR `zone_meta_edit_own`/`zone_meta_edit_others`)

### Permission Templates

Poweradmin also supports permission templates (different from zone templates):

- **Adding permission templates**: Requires `templ_perm_add` permission
- **Editing permission templates**: Requires `templ_perm_edit` permission
- **Deleting permission templates**: Requires `user_edit_templ_perm` permission

## Configuration

Template display in zone listings can be controlled via the `interface.zonelist_template` setting in your configuration file.

## See Also

* [Permissions](permissions.md) - For detailed permission requirements
* [Basic Configuration](../configuration/basic.md) - For template-related settings