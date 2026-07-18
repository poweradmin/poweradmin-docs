# User Permissions

This document provides detailed explanations of all user permissions available in Poweradmin. For information about user roles and general permission concepts, see [Users and Roles](users-roles.md).

## Zone Permissions

### zone_master_add

- Allows the user to add a master zone
- User can create new authoritative DNS zones
- Required for creating zones from templates

### zone_slave_add

- Allows the user to add a slave zone
- User can create zones that pull data from a master server
- Requires specifying the IP address of the master server

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
- User can change used zone template (requires zone_master_add and zone_content_edit_own permissions)

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

- Allows the user to edit record content in zones they own, except SOA and NS records
- Limited permission for users who should only modify certain record types
- Provides restricted zone management capabilities
- Common use case: tenant or end-customer self-service, where users can manage their own A/AAAA/CNAME/MX/TXT records but must not touch the zone's authority (SOA) or delegation (NS) records
- Enforced uniformly in the web UI and across the v1/v2 record APIs (since 4.2.3); creating, editing, or deleting an SOA or NS record returns HTTP 403 for users limited to this permission
- To additionally allow managing delegation NS records for subdomains, grant `zone_content_edit_ns_subzone`

### zone_content_edit_ns_subzone

- Allows users limited to `zone_content_edit_own_as_client` to add, edit, and delete NS records below the zone apex
- SOA and apex NS records remain restricted regardless of this permission
- Use case: end customers who delegate subdomains (e.g. `subdomain.example.com`) to another DNS provider while the zone's own NS set stays under the operator's control
- Not granted to any permission template by default; assign it explicitly in the permission template editor
- Has no effect on its own - it only extends `zone_content_edit_own_as_client`
- Applies to the web UI and the v1/v2 record APIs
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
- Advanced permission for managing DNS infrastructure