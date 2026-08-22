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

## Requirements

### `interface.application_url` must be set

SAML needs it to derive the SP URLs. The `entityID`, ACS and SLO URLs advertised to the identity provider are built from `interface.application_url` alone, and no request header is consulted. With it unset and no explicit `sp` URLs configured, SAML login and `/saml/metadata` fail with:

```
Error generating SAML metadata: interface.application_url must be configured before SAML
can be used: it defines the entityID and ACS URL advertised to the identity provider.
```

Set it to the full public URL of the install:

```php
'interface' => [
    'application_url' => 'https://dns.example.com/poweradmin',
],
```

Alternatively, set `sp.entity_id`, `sp.assertion_consumer_service_url` and `sp.single_logout_service_url` explicitly (see [Service Provider Configuration](#service-provider-sp-configuration)). Those are then used as given and nothing is derived, so `application_url` is not required for SAML.

Earlier versions derived the host from the web server's `SERVER_NAME` when this was empty. That fallback has been removed: under the official Docker image (FrankenPHP/Caddy) and under Apache's default `UseCanonicalName Off`, `SERVER_NAME` comes from the client's `Host` header, so a forged header could advertise an attacker's ACS URL to an IdP that consumes SP metadata dynamically.

## Global Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `saml.enabled` | false | Enable SAML authentication |
| `saml.auto_provision` | true | Auto-create users from SAML assertions |
| `saml.link_by_email` | true | Link SAML accounts to existing users by email |
| `saml.sync_user_info` | true | Sync user info on each login |
| `saml.default_permission_template` | "Guest" | Default permission template for new users |

### Superuser rights are never provisioned from an identity provider

`saml.allow_superuser_provisioning` (default `false`, added in 4.5.0) blocks two ways an
IdP claim could otherwise mint a global administrator:

- a `permission_template_mapping` entry pointing at a template that grants
  `user_is_ueberuser`, and
- a `group_mapping` entry pointing at a Poweradmin group whose template grants it - note
  the installer ships an `Administrators` group bound to exactly such a template.

With the default in place, both are refused and logged. If your deployment genuinely
relies on the IdP deciding who is an administrator, set the flag to `true`; otherwise
grant administrator rights in Poweradmin itself, where an existing administrator has to
act.

### Account linking and template resolution

`saml.default_permission_template` must name a template that exists. When a new
user matches no group mapping and the named template cannot be found, provisioning
is refused rather than falling back to an arbitrary template - the lowest template
id is normally the bundled Administrator template.

`saml.link_by_email` only links an incoming identity to an existing local account when:

- the assertion carries no `email_verified` claim, or carries one that is true. An
  address the provider has not vouched for is not treated as proof of identity.
- the matched local account does not hold `user_is_ueberuser`. A superuser account
  is never claimed by email; link it explicitly by subject instead.

Both checks are logged when they block a link, so a login that stops working after
an upgrade can be traced in the application log.

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

## Group Membership Mapping

Separate from permission templates, you can also map SAML groups to Poweradmin groups. This controls zone ownership and access through group membership.

Key differences from permission template mapping:

- `permission_template_mapping` assigns **one** permission template per user
- `group_mapping` assigns **multiple** Poweradmin groups per user

```php
'saml' => [
    'enabled' => true,
    'group_mapping' => [
        'external-admins' => 'Administrators',
        'dns-managers' => 'Zone Managers',
        'dns-editors' => 'Editors',
        'dns-viewers' => 'Viewers',
        'dns-guests' => 'Guests',
    ],
],
```

A single SAML group can also be mapped to multiple Poweradmin groups by giving an array as the value (added in 4.4.0). The user is added to every Poweradmin group listed:

```php
'group_mapping' => [
    'team1' => ['Editors', 'Viewers'],
    'team2' => ['Editors'],
    'platform-admins' => 'Administrators', // single-value form still works
],
```

Predefined Poweradmin groups:

- **Administrators** - Full administrative access to all system functions
- **Zone Managers** - Full zone management including creation, editing, and deletion
- **Editors** - Edit zone records but cannot modify SOA and NS records
- **Viewers** - Read-only access to zones with search capability
- **Guests** - Temporary group with no permissions (awaiting approval)

> **Note:** Both `permission_template_mapping` and `group_mapping` read from the same SAML attribute specified by `user_mapping.groups`. Group memberships are re-evaluated on every login - users are added to or removed from mapped groups based on their current SAML assertion.

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
https://your-poweradmin.com/saml/metadata?provider={provider-id}
```

For example: `https://your-poweradmin.com/saml/metadata?provider=azure`. With no `provider` parameter the first configured provider is used.

> **Note:** The SP entity ID is the bare `https://your-poweradmin.com/saml/metadata`, with no provider suffix. The query parameter only selects which IdP the generated document is tailored for.

## Provider Configuration

Each provider requires IdP-specific configuration:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Display label for the provider. The provider identifier is the array key, not this field |
| `display_name` | Yes | Text shown on login button |
| `entity_id` | Yes | IdP Entity ID |
| `sso_url` | Yes | IdP Single Sign-On URL |
| `slo_url` | No | IdP Single Logout URL |
| `x509cert` | Yes | IdP X.509 certificate (PEM string, with or without `-----BEGIN CERTIFICATE-----`/`-----END CERTIFICATE-----` headers and line breaks) |
| `user_mapping` | Yes | Map SAML attributes to user fields |

### Azure AD (SAML)

1. In Azure Portal, go to Enterprise Applications > New Application
2. Create a non-gallery application
3. Configure Single Sign-On > SAML
4. Set Entity ID: `https://your-poweradmin.com/saml/metadata` (no provider suffix - it must match the SP entity ID exactly, or the assertion is rejected on audience mismatch)
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
            'x509cert' => 'MIICnTCCAYUCBgF...', // Base64 cert body, or a full PEM string
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
4. Set Audience URI (SP Entity ID): `https://your-poweradmin.com/saml/metadata` (no provider suffix)
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
3. Set Client ID: `https://your-poweradmin.com/saml/metadata` (Keycloak uses the client ID as the SP entity ID, so it must carry no provider suffix)
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

Anything you set here overrides the derived defaults below.

| Setting | Default | Description |
|---------|---------|-------------|
| `wantAssertionsSigned` | true when the provider has an `x509cert`, otherwise false | Require signed assertions |
| `wantNameId` | true | Require NameID in assertions |
| `authnRequestsSigned` | true when `sp.private_key` is set, otherwise false | Sign authentication requests |
| `logoutRequestSigned` | true when `sp.private_key` is set, otherwise false | Sign logout requests |
| `logoutResponseSigned` | true when `sp.private_key` is set, otherwise false | Sign logout responses |
| `signMetadata` | true when `sp.private_key` is set, otherwise false | Sign the generated SP metadata |
| `signatureAlgorithm` | rsa-sha256 | Signature algorithm |

Signing therefore switches on by itself once you configure an SP key and certificate, and assertion signing is required as soon as the provider has an IdP certificate configured.

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

> **Note:** The `permission_template_mapping` and `group_mapping` settings can be configured via environment variables using the `=` delimiter and comma-separated entries:
>
> ```yaml
> PA_SAML_PERMISSION_TEMPLATE_MAPPING: "admins=Administrator,editors=Viewer"
> PA_SAML_GROUP_MAPPING: "admins=Administrators,editors=Editors"
> ```
>
> Group names containing colons (e.g., SAML URNs) are supported. Whitespace around commas and delimiters is trimmed automatically.
>
> For 1:n group mappings, separate the Poweradmin groups with a pipe (`|`) so one SAML group can grant access to several Poweradmin groups (added in 4.4.0):
>
> ```yaml
> PA_SAML_GROUP_MAPPING: "team1=Editors|Viewers,team2=Administrators"
> ```

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

- Paste the certificate exactly as your IdP exports it (Base64 download from
  Azure / Okta / Keycloak is fine). Both raw Base64 bodies and full PEM
  strings (`-----BEGIN CERTIFICATE-----` ... `-----END CERTIFICATE-----`) are
  accepted, with or without embedded line breaks.
- If the login page logs *"x509cert is not a valid X.509 certificate"* the
  pasted value cannot be parsed by `openssl_x509_read` - check for stray
  characters, truncation, or that you copied the certificate body rather than
  the metadata wrapper.

## Related Documentation

- [OIDC Authentication](oidc.md)
- [LDAP Integration](ldap.md)
- [Security Policies](security-policies.md)
