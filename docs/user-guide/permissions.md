# User Permissions

This document provides detailed explanations of all user permissions available in Poweradmin. Understanding these
permissions is crucial for properly configuring user access within the system.

## Basics of User Management

Poweradmin implements a permission-based user management system with two primary user levels:

1. **Uberusers** - Users that can do anything within the interface (administrators)
2. **Limited users** - Users with restricted permissions based on assigned templates

### Permission Templates

Permission templates were introduced in version 2.0.0 and are built from a set of individual permissions. Each
permission allows users to perform specific actions, such as viewing zone contents, editing zones, or creating
supermasters. By adding or removing permissions to a template and assigning that template to users, you can control user
access rights.

### Understanding Uberuser Status

The `user_is_ueberuser` permission overrules any other permission the user may or may not have been assigned. It grants
full access to all features that would otherwise require specific permissions. This is typically reserved for
administrators.

### Zone Ownership

Ownership is a designation that marks users as "owners" for specific zones. However, ownership alone doesn't grant any
privileges for these zones. The actual abilities are determined by the permissions in the user's assigned template. For
example, if a user owns zones but lacks the `zone_content_view_own` permission, they won't be able to see those zones.

### Edit Access and Zone Integrity

Poweradmin assumes that users with edit permissions for a zone can be trusted with full access to that zone. This is
because even partial edit access would allow a user to potentially break the zone's functionality. Therefore, if a user
can edit a zone, they're also granted delete permissions.

### Security Pitfalls

Be aware that granting any of these permissions can indirectly give users extensive rights:

- `user_edit_templ_perm`
- `templ_perm_edit`
- `user_add_new`

Users with these permissions can potentially create or modify templates to grant themselves `user_is_ueberuser` rights.
Additionally, anyone with root shell access to the server running Poweradmin or the PowerDNS database server effectively
has uberuser rights.

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
- Advanced permission for managing DNS infrastructure

## Additional Information

When configuring user permissions, keep the principle of least privilege in mind - only grant the permissions necessary
for a user to perform their required functions.