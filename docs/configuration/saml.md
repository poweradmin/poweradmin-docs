# SAML Authentication

Poweradmin supports SAML 2.0 for single sign-on (SSO) authentication with enterprise identity providers like Azure AD, Okta, Auth0, and Keycloak.

## Overview

SAML (Security Assertion Markup Language) allows users to authenticate using their organization's identity provider. When enabled, users see additional "Sign in with..." buttons on the login page.

Key features:

- Automatic user provisioning from SAML assertions
- Link SAML accounts to existing users by email
- Sync user information from SAML attributes
- Map SAML groups/roles to Poweradmin permission templates
- Support for multiple providers simultaneously
- SP metadata generation for easy IdP configuration

## Global Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `saml.enabled` | false | Enable SAML authentication |
| `saml.auto_provision` | true | Auto-create users from SAML assertions |
| `saml.link_by_email` | true | Link SAML accounts to existing users by email |
| `saml.sync_user_info` | true | Sync user info on each login |
| `saml.default_permission_template` | "" | Default permission template for new users |

## Permission Template Mapping

Map SAML groups/roles to Poweradmin permission templates:

```php
'saml' => [
    'enabled' => true,
    'permission_template_mapping' => [
        'poweradmin-admins' => 'Administrator',
        'dns-operators' => 'DNS Operator',
        'dns-viewers' => 'Read Only',
    ],
],
```

## Service Provider (SP) Configuration

Poweradmin acts as a SAML Service Provider. Configure SP settings in the `sp` section:

| Setting | Default | Description |
|---------|---------|-------------|
| `sp.entity_id` | (auto) | SP Entity ID (defaults to `{base_url}/saml/metadata`) |
| `sp.assertion_consumer_service_url` | (auto) | ACS URL (defaults to `{base_url}/saml/acs`) |
| `sp.single_logout_service_url` | (auto) | SLO URL (defaults to `{base_url}/saml/sls`) |
| `sp.name_id_format` | emailAddress | NameID format |
| `sp.x509cert` | "" | SP certificate for signing (optional) |
| `sp.private_key` | "" | SP private key for signing (optional) |

```php
'saml' => [
    'enabled' => true,
    'sp' => [
        'entity_id' => 'https://poweradmin.example.com/saml/metadata',
        'name_id_format' => 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
    ],
],
```

## SP Metadata

Poweradmin can generate SP metadata for your identity provider. Access it at:

```
https://your-poweradmin.com/saml/metadata/{provider-id}
```

For example: `https://your-poweradmin.com/saml/metadata/azure`

## Provider Configuration

Each provider requires IdP-specific configuration:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal provider identifier |
| `display_name` | Yes | Text shown on login button |
| `entity_id` | Yes | IdP Entity ID |
| `sso_url` | Yes | IdP Single Sign-On URL |
| `slo_url` | No | IdP Single Logout URL |
| `x509cert` | Yes | IdP X.509 certificate (without headers) |
| `user_mapping` | Yes | Map SAML attributes to user fields |

### Azure AD (SAML)

1. In Azure Portal, go to Enterprise Applications > New Application
2. Create a non-gallery application
3. Configure Single Sign-On > SAML
4. Set Entity ID: `https://your-poweradmin.com/saml/metadata/azure`
5. Set Reply URL (ACS): `https://your-poweradmin.com/saml/acs`
6. Download the Certificate (Base64)

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'azure' => [
            'name' => 'Microsoft Azure AD',
            'display_name' => 'Sign in with Microsoft',
            'entity_id' => 'https://sts.windows.net/{tenant-id}/',
            'sso_url' => 'https://login.microsoftonline.com/{tenant-id}/saml2',
            'slo_url' => 'https://login.microsoftonline.com/{tenant-id}/saml2',
            'x509cert' => 'MIICnTCCAYUCBgF...', // Certificate without BEGIN/END headers
            'user_mapping' => [
                'username' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
                'email' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
                'first_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
                'last_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
                'display_name' => 'http://schemas.microsoft.com/identity/claims/displayname',
                'groups' => 'http://schemas.microsoft.com/ws/2008/06/identity/claims/groups',
            ],
        ],
    ],
],
```

### Okta (SAML)

1. In Okta Admin Console, go to Applications > Create App Integration
2. Select SAML 2.0
3. Set Single Sign-On URL: `https://your-poweradmin.com/saml/acs`
4. Set Audience URI (SP Entity ID): `https://your-poweradmin.com/saml/metadata/okta`
5. Configure attribute statements
6. Download the IdP metadata or certificate

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'okta' => [
            'name' => 'Okta',
            'display_name' => 'Sign in with Okta',
            'entity_id' => 'http://www.okta.com/{app-id}',
            'sso_url' => 'https://{domain}.okta.com/app/{app-name}/{app-id}/sso/saml',
            'slo_url' => 'https://{domain}.okta.com/app/{app-name}/{app-id}/slo/saml',
            'x509cert' => 'MIIDpDCCAoygAwIBAgIGAX...', // Certificate
            'user_mapping' => [
                'username' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
                'email' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
                'first_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
                'last_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
                'groups' => 'http://schemas.xmlsoap.org/claims/Group',
            ],
        ],
    ],
],
```

### Auth0 (SAML)

1. In Auth0 Dashboard, go to Applications > Create Application
2. Enable SAML2 Web App addon
3. Configure SAML settings
4. Download IdP metadata

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'auth0' => [
            'name' => 'Auth0',
            'display_name' => 'Sign in with Auth0',
            'entity_id' => 'urn:auth0:{tenant}:{connection}',
            'sso_url' => 'https://{tenant}.auth0.com/samlp/{client-id}',
            'slo_url' => 'https://{tenant}.auth0.com/samlp/{client-id}/logout',
            'x509cert' => 'MIIDDTCCAfWgAwIBAgIJAP...', // Certificate
            'user_mapping' => [
                'username' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier',
                'email' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
                'first_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
                'last_name' => 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
                'groups' => 'http://schemas.auth0.com/roles',
            ],
        ],
    ],
],
```

### Keycloak (SAML)

1. In Keycloak Admin Console, create a new Client
2. Set Client Protocol to "saml"
3. Set Client ID: `https://your-poweradmin.com/saml/metadata/keycloak`
4. Configure endpoints and download certificate

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'keycloak' => [
            'name' => 'Keycloak',
            'display_name' => 'Sign in with Keycloak',
            'entity_id' => 'https://keycloak.example.com/realms/{realm}',
            'sso_url' => 'https://keycloak.example.com/realms/{realm}/protocol/saml',
            'slo_url' => 'https://keycloak.example.com/realms/{realm}/protocol/saml',
            'x509cert' => 'MIIClTCCAX0CBgF...', // Certificate
            'user_mapping' => [
                'username' => 'username',
                'email' => 'email',
                'first_name' => 'firstName',
                'last_name' => 'lastName',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

### Generic SAML Provider

For other SAML identity providers:

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'custom' => [
            'name' => 'Custom SAML IdP',
            'display_name' => 'Sign in with SSO',
            'entity_id' => 'https://idp.example.com/metadata',
            'sso_url' => 'https://idp.example.com/sso',
            'slo_url' => 'https://idp.example.com/slo',
            'x509cert' => 'MIIDpDCCAoygAwIBAgIGAX...',
            'user_mapping' => [
                'username' => 'uid',
                'email' => 'email',
                'first_name' => 'firstName',
                'last_name' => 'lastName',
                'display_name' => 'displayName',
                'groups' => 'groups',
            ],
            'security' => [
                'wantAssertionsSigned' => true,
                'wantNameId' => true,
            ],
        ],
    ],
],
```

## User Mapping

SAML attributes are mapped to Poweradmin user fields. Common attribute formats:

**XML URI Format** (Azure AD, Okta, Auth0):
```
http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname
http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname
```

**Simple Format** (Keycloak):
```
email
firstName
lastName
```

| Poweradmin Field | Description |
|------------------|-------------|
| `username` | User's login name |
| `email` | Email address |
| `first_name` | First name |
| `last_name` | Last name |
| `display_name` | Display name |
| `groups` | Group/role memberships |

## Security Settings

Configure security options per provider:

```php
'security' => [
    'nameIdEncrypted' => false,
    'authnRequestsSigned' => false,
    'logoutRequestSigned' => false,
    'logoutResponseSigned' => false,
    'signMetadata' => false,
    'wantAssertionsSigned' => true,
    'wantNameId' => true,
    'wantAssertionsEncrypted' => false,
    'signatureAlgorithm' => 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
    'digestAlgorithm' => 'http://www.w3.org/2001/04/xmlenc#sha256',
],
```

| Setting | Default | Description |
|---------|---------|-------------|
| `wantAssertionsSigned` | true | Require signed assertions |
| `wantNameId` | true | Require NameID in assertions |
| `authnRequestsSigned` | false | Sign authentication requests |
| `signatureAlgorithm` | rsa-sha256 | Signature algorithm |

## SP Signing (Optional)

For IdPs that require signed requests, generate a certificate and key:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout sp-private.key \
  -out sp-certificate.crt \
  -subj "/CN=poweradmin-sp"
```

Configure in settings:

```php
'saml' => [
    'sp' => [
        'x509cert' => file_get_contents('/path/to/sp-certificate.crt'),
        'private_key' => file_get_contents('/path/to/sp-private.key'),
    ],
],
```

## Docker Configuration

Use environment variables with the `PA_SAML_` prefix:

```yaml
environment:
  PA_SAML_ENABLED: "true"
  PA_SAML_AUTO_PROVISION: "true"
  PA_SAML_AZURE_ENTITY_ID: "https://sts.windows.net/tenant-id/"
  PA_SAML_AZURE_SSO_URL: "https://login.microsoftonline.com/tenant-id/saml2"
```

For certificates and keys, use Docker secrets:

```yaml
secrets:
  saml_idp_cert:
    file: ./secrets/idp-certificate.crt
  saml_sp_key:
    file: ./secrets/sp-private.key

services:
  poweradmin:
    environment:
      PA_SAML_AZURE_X509_CERT__FILE: /run/secrets/saml_idp_cert
      PA_SAML_SP_PRIVATE_KEY__FILE: /run/secrets/saml_sp_key
    secrets:
      - saml_idp_cert
      - saml_sp_key
```

## Multiple Providers

Configure multiple SAML providers:

```php
'saml' => [
    'enabled' => true,
    'providers' => [
        'azure' => [
            // Azure AD configuration...
        ],
        'okta' => [
            // Okta configuration...
        ],
    ],
],
```

## Troubleshooting

### "Invalid signature" error

- Verify the IdP certificate is correct and not expired
- Ensure the certificate is without BEGIN/END headers
- Check if your IdP rotated certificates

### User not created after login

- Check `auto_provision` is enabled
- Verify user mapping includes required fields
- Check that required attributes are released by IdP

### NameID missing error

- Configure NameID format in IdP to match SP expectations
- Ensure IdP is configured to send NameID

### Groups not mapped

- Verify IdP is configured to release group claims
- Check the attribute name matches `user_mapping.groups`
- For Azure AD, configure Group claims in Token configuration

### Redirect loop

- Clear browser cookies
- Verify ACS URL matches exactly in IdP configuration
- Check for mixed HTTP/HTTPS issues

### Certificate errors

- Certificates should be PEM format without headers
- Remove `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`
- Ensure no extra whitespace or line breaks

## Related Documentation

- [OIDC Authentication](oidc.md)
- [LDAP Integration](ldap.md)
- [Security Policies](security-policies.md)
