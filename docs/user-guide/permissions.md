# User Permissions

This document provides detailed explanations of all user permissions available in Poweradmin. For information about user roles and general permission concepts, see [Users and Roles](users-roles.md).

## Zone Permissions

### zone_master_add

- Allows the user to add a master zone
- User can create new authoritative DNS zones
- Required for creating zones from templates
- Also governs the **Producer** catalog kind on PowerDNS 4.7+, since a producer catalog is authored locally like any primary zone

### zone_slave_add

- Allows the user to add a slave zone
- User can create zones that pull data from a master server
- Requires specifying the IP address of the master server
- Also governs the **Consumer** catalog kind on PowerDNS 4.7+, because a consumer replicates from a remote primary, which is what this permission covers. Without it, Consumer is not offered on the add-zone form

### zone_content_view_own

- Allows the user to view the content of zones they own
- This includes viewing all records within the zone
- Basic permission needed for zone management

### zone_content_edit_own

- Allows the user to edit the content of zones they own
- This includes adding, modifying, and deleting records
- Essential for managing DNS records in owned zones

### zone_meta_edit_own

- Allows the user to add additional owners to their zone (if user_view_others is set to true)
- User can remove owners (including themselves)
- User cannot orphan a zone (at least one user must remain)
- User can change zone type (i.e. from native to slave)
- User can set IP of master server for slave zone
- User can change used zone template (requires `zone_content_edit_own` plus either `zone_master_add` or `zone_slave_add`)

### zone_content_view_others

- Allows the user to view the content of zones owned by other users
- This is a read-only permission for zones the user doesn't own
- Useful for administrators or team environments

### zone_content_edit_others

- Allows the user to edit the content of zones owned by other users
- User can modify records in zones they don't own
- Powerful permission that should be granted cautiously

### zone_meta_edit_others

- Allows the user to edit the metadata of zones owned by other users
- Can change owners, zone types, and master server IPs for others' zones
- High-level permission typically reserved for administrators

### zone_content_edit_own_as_client

- Allows the user to edit record content in zones they own, except SOA, NS and LUA records
- Limited permission for users who should only modify certain record types
- Provides restricted zone management capabilities
- Common use case: tenant or end-customer self-service, where users can manage their own A/AAAA/CNAME/MX/TXT records but must not touch the zone's authority (SOA), its delegation (NS), or [LUA records](https://doc.powerdns.com/authoritative/lua-records/index.html), which execute code on the DNS server
- Enforced uniformly in the web UI and across the record APIs (since 4.2.3); creating, editing, or deleting an SOA, NS or LUA record returns HTTP 403 for users limited to this permission
- LUA is held to a stricter standard inside zone templates: seeding one requires full `all` or `own` edit rights, because template records are written straight to the backend and land in every zone created from that template
- To additionally allow managing delegation NS records for subdomains, grant `zone_content_edit_ns_subzone`

### zone_content_edit_ns_subzone

- Allows users limited to `zone_content_edit_own_as_client` to add, edit, and delete NS records below the zone apex
- SOA and apex NS records remain restricted regardless of this permission
- Use case: end customers who delegate subdomains (e.g. `subdomain.example.com`) to another DNS provider while the zone's own NS set stays under the operator's control
- Not granted to any permission template by default; assign it explicitly in the permission template editor
- Has no effect on its own - it only extends `zone_content_edit_own_as_client`
- Applies to the web UI and the record APIs
- Added in v4.5.0

### zone_metadata_view_own / zone_metadata_view_others

- Allow the user to see a zone's PowerDNS metadata, for zones they own and for zones they do not
- Split out of `zone_content_view_own` / `zone_content_view_others` so metadata visibility can be withheld from users who may still read records
- The 4.5.0 migration auto-grants each of these to every permission template that already held the matching `zone_content_view_*`, so nothing a user could see before the upgrade disappears
- Viewing only. Editing metadata still requires `zone_meta_edit_own` or `zone_meta_edit_others`
- See [Zone Metadata](zones.md#zone-metadata)
- Added in v4.5.0

### zone_ownership_view_own / zone_ownership_view_others

- Allow the user to see who owns a zone, for zones they own and for zones they do not
- Split out of `zone_content_view_*` on the same terms as the metadata permissions above, and auto-granted the same way on upgrade
- Useful for hiding the customer list in multi-tenant installations while leaving record access intact
- Added in v4.5.0

### zone_dnssec_manage_own

- Allows the user to manage DNSSEC keys for zones they own: add, edit, activate, deactivate, delete, and import or export keys
- Previously key management was superuser-only, so delegating DNSSEC meant handing out full superuser rights
- Independent of record editing. A user can be allowed to manage keys without being allowed to edit records, and the reverse
- Zones marked `PRESIGNED` are excluded - Poweradmin does not manage keys for zones signed elsewhere
- See [DNSSEC](../configuration/dnssec.md)
- Added in v4.5.0

### zone_delete_own

- Allows the user to delete zones they own
- Separates deletion from edit permissions for finer access control
- Added in v4.1.0

### zone_delete_others

- Allows the user to delete zones owned by other users
- Administrative permission for managing all zones
- Added in v4.1.0

## Search Permissions

### search

- Allows the user to perform searches across the system
- User can search for zones, records, and other elements
- Basic functionality for finding resources in larger deployments

## User Permissions

### user_view_others

- Allows the user to view information about other users
- Can see usernames and access levels of others
- Required for assigning zone ownership to other users

### user_edit_own

- Allows the user to edit their own user information
- User can change their password and other personal details
- Basic self-service permission

### user_edit_others

- Allows the user to edit information for other users
- Can modify other users' details and access rights
- High-level administrative permission

### user_add_new

- Allows the user to add new users to the system
- Can create accounts for others to access Poweradmin
- Administrative permission for expanding system access

### user_passwd_edit_others

- Allows the user to change passwords for other users
- Can reset passwords when users are locked out
- Administrative security management permission

### user_edit_templ_perm

- Allows the user to change the permission template assigned to users
- Can modify user access by applying different templates
- Streamlines permission management for administrators

The permission delegates template management, not the granting of administrator rights.
Two limits apply to holders who are not themselves administrators:

- A template that grants `user_is_ueberuser` cannot be assigned to anyone, on either the
  user editor or the user create form. Assigning one requires `user_is_ueberuser`.
- The holder's own template can only be changed if they also hold `user_edit_others`.
  Without it, the template stored on their account is kept and the submitted value is
  ignored, so they cannot promote themselves.

Both limits apply equally to the REST API user endpoints, so automation is held to the
same rule as the web interface. Assigning any ordinary template is unaffected.

### user_enforce_mfa

- Requires the holder to complete multi-factor authentication at login
- Applies when the permission comes from the user's own template or from a group they belong to
- Only takes effect when `security.mfa.enabled` is on; `security.mfa.skip_for_external_auth` can exempt logins that came through an external identity provider

### user_is_ueberuser

- Grants superuser status with full access to all functions
- User has unlimited privileges throughout Poweradmin
- Bypasses normal permission checks
- Should be granted very selectively

## Template Permissions

### templ_perm_add

- Allows the user to add new permission templates
- Templates define sets of permissions that can be assigned to users
- Streamlines user permission management

### templ_perm_edit

- Allows the user to edit existing permission templates
- Can modify permission sets used for multiple users
- Useful for maintaining consistent permission groups

> **Neither permission can hand out administrator rights.** A template's permission
> list is itself a grant of authority, so a holder of `templ_perm_add`/`templ_perm_edit`
> who is not already an administrator cannot put `user_is_ueberuser` into a template,
> and cannot edit a template that already carries it. The latter also prevents stripping
> permissions off the Administrator template. Administrators are unaffected.

## Zone Template Permissions

These cover zone templates (reusable sets of DNS records), not the permission
templates above.

### zone_templ_add

- Allows the user to create new zone templates
- Also required to save an existing zone's records as a new template
- Together with `zone_templ_edit`, gates access to the zone template list

### zone_templ_edit

- Allows the user to edit and delete existing zone templates
- Covers adding, editing and deleting the records inside a template, and pushing template changes out to the zones that use it

## API Permissions

### api_manage_keys

- Allows the user to create, view, edit and revoke their own REST API keys
- Gates the API Keys page and the equivalent service operations
- Administrators hold this implicitly
- The API itself must be enabled with `api.enabled`; see [API Configuration](../configuration/api.md)

## Supermaster Permissions

### supermaster_view

- Allows the user to view supermaster servers
- Can see the list of authoritative name servers
- Read-only access to supermaster configurations

### supermaster_add

- Allows the user to add new supermaster servers
- Can configure authoritative name servers for PowerDNS
- Advanced configuration permission

### supermaster_edit

- Allows the user to edit existing supermaster servers
- Can modify authoritative name server configurations
- Advanced permission for managing DNS infrastructure

## Log Permissions

These permissions grant access to the activity logs without granting full
superuser rights. They require database logging to be enabled. In the access
template editor each permission appears under the group shown below (the editor
groups permissions by name prefix).

### zone_logs_view_own

- Allows the user to view the zone activity log for zones they own (directly or through a group)
- Scopes the Zone Logs view and the per-zone Logs button to owned zones only
- Appears under "Zone Permissions" in the permission template editor
- Added in v4.5.0

### zone_logs_view_others

- Allows the user to view the zone activity log for all zones, including those they do not own
- Intended for delegated auditors who need cross-zone visibility without superuser rights
- Appears under "Zone Permissions" in the permission template editor
- Added in v4.5.0

### user_logs_view

- Allows the user to view the user activity log (logins, user management, and related events)
- Global, read-only auditor permission; does not grant any user management rights
- Appears under "User Permissions" in the permission template editor
- Added in v4.5.0

### group_logs_view

- Allows the user to view the group activity log
- Global, read-only auditor permission; does not grant any group management rights
- Appears under "Other Permissions" in the permission template editor
- Added in v4.5.0