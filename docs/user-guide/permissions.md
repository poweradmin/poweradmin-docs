# User Permissions

This document provides detailed explanations of all user permissions available in Poweradmin. Understanding these permissions is crucial for properly configuring user access within the system.

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

For more detailed information on implementing these permissions, please refer to the [Poweradmin documentation](https://www.poweradmin.org/documentation/).

When configuring user permissions, keep the principle of least privilege in mind - only grant the permissions necessary for a user to perform their required functions.