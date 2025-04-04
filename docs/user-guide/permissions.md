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

### zone_comment_edit_own
- Allows the user to add or edit comments for zones they own
- Comments provide documentation and context for zones
- Helps with zone organization and management

### zone_comment_edit_others
- Allows the user to add or edit comments for zones owned by other users
- Users can annotate zones they don't own
- Useful for team environments where documentation is shared

## Record Permissions

### record_comment_edit_own
- Allows the user to add or edit comments for records in zones they own
- Comments can provide context for specific DNS records
- Helps with documentation and change tracking

### record_comment_edit_others
- Allows the user to add or edit comments for records in zones they don't own
- Users can annotate records in other users' zones
- Useful for collaborative environments

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

### user_add
- Allows the user to add new users to the system
- Can create accounts for others to access Poweradmin
- Administrative permission for expanding system access

### user_is_ueberadmin
- Grants superuser (ueberadmin) status
- User has full access to all functions in Poweradmin
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

## Zone Template Permissions

### zone_templ_add
- Allows the user to add new zone templates
- Templates provide pre-defined sets of records for new zones
- Helps standardize zone creation

### zone_templ_edit
- Allows the user to edit existing zone templates
- Can modify the record sets used for new zone creation
- Useful for maintaining standardized zone configurations

### zone_templ_view
- Allows the user to view available zone templates
- Read-only access to template configurations
- Basic permission needed to use templates

## Log Permissions

### log_view
- Allows the user to view system logs
- Can see login attempts and changes to zones/records
- Useful for auditing and troubleshooting

## Supermaster Permissions

### supermaster_view
- Allows the user to view supermaster servers
- Can see the list of authoritative name servers
- Read-only access to supermaster configurations

### supermaster_add
- Allows the user to add new supermaster servers
- Can configure authoritative name servers for PowerDNS
- Advanced configuration permission

## Additional Information

For more detailed information on implementing these permissions, please refer to the [Poweradmin documentation](https://www.poweradmin.org/documentation/).

When configuring user permissions, keep the principle of least privilege in mind - only grant the permissions necessary for a user to perform their required functions.