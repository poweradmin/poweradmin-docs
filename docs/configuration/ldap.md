# LDAP Integration

Poweradmin supports LDAP (Lightweight Directory Access Protocol) authentication, allowing you to integrate with your existing directory service such as Active Directory or OpenLDAP.

## Configuration Settings

The LDAP settings are configured in the `config/settings.php` file under the `ldap` section:

- **enabled**: Enable LDAP authentication. Default: `false`
- **debug**: Enable LDAP debug logging. Default: `false`
- **uri**: LDAP server URI. Default: `ldap://domaincontroller.example.com`
- **base_dn**: Base DN where users are stored. Default: `ou=users,dc=example,dc=com`
- **bind_dn**: Bind DN for LDAP authentication. Default: `cn=admin,dc=example,dc=com`
- **bind_password**: Bind password for LDAP authentication
- **user_attribute**: User attribute (uid for OpenLDAP, sAMAccountName for Active Directory). Default: `uid`
- **protocol_version**: LDAP protocol version. Default: `3`
- **search_filter**: Additional search filter. Default: empty

## Example Configuration

```php
return [
    'ldap' => [
        'enabled' => true,
        'debug' => false,
        'uri' => 'ldap://domaincontroller.example.com',
        'base_dn' => 'ou=users,dc=example,dc=com',
        'bind_dn' => 'cn=admin,dc=example,dc=com',
        'bind_password' => 'some_password',
        'user_attribute' => 'uid',
        'protocol_version' => 3,
        'search_filter' => '',
    ],
];
```

## Basic Setup

1. Enable LDAP authentication by setting `'enabled' => true` in the configuration array.
2. Configure your LDAP server URI and base DN.
3. Set binding credentials if required.
4. Adjust the `search_filter` to match your LDAP schema.

## Advanced Configuration

### SSL/TLS Connection

For secure LDAP (LDAPS), use the following configuration:

```php
'uri' => 'ldaps://domaincontroller.example.com',
```

### User Attribute Mapping

Configure how Poweradmin maps LDAP attributes to user properties:

- For OpenLDAP: `'user_attribute' => 'uid'`
- For Active Directory: `'user_attribute' => 'sAMAccountName'`

## Example Directory Configurations

### Active Directory

```php
return [
    'ldap' => [
        'enabled' => true,
        'uri' => 'ldap://ad.company.com',
        'base_dn' => 'DC=company,DC=com',
        'bind_dn' => 'CN=ServiceAccount,OU=Users,DC=company,DC=com',
        'bind_password' => 'password',
        'user_attribute' => 'sAMAccountName',
        'search_filter' => '(&(objectClass=user)(sAMAccountName=%s))',
    ],
];
```

### OpenLDAP

```php
return [
    'ldap' => [
        'enabled' => true,
        'uri' => 'ldap://ldap.company.com',
        'base_dn' => 'ou=users,dc=company,dc=com',
        'bind_dn' => 'cn=admin,dc=company,dc=com',
        'bind_password' => 'password',
        'user_attribute' => 'uid',
        'search_filter' => '(&(objectClass=posixAccount)(uid=%s))',
    ],
];
```

## Troubleshooting

Common LDAP issues and solutions:

- **Connection Failed**: Verify server URI and firewall settings
- **Binding Failed**: Check bind DN and password
- **User Not Found**: Verify search filter and user attribute
- **SSL Certificate Issues**: Ensure proper CA certificates are installed

## Security Considerations

- Always use LDAPS (LDAP over SSL/TLS) in production environments
- Implement least privilege access for binding
- Regularly rotate LDAP binding credentials
- Consider implementing connection timeout settings
- Monitor failed authentication attempts

## Adding Users to PowerAdmin

Add a user to Poweradmin:

![PowerAdmin LDAP User](../../screenshots/pwa_ldap.png)

The same user should exist in the LDAP schema:

![OpenLDAP User](../../screenshots/openldap.png)