# OpenID Connect (OIDC) Authentication

Poweradmin supports OpenID Connect (OIDC) for single sign-on (SSO) authentication with identity providers like Azure AD, Google, Keycloak, Okta, Authentik, and Auth0.

## Overview

OIDC allows users to authenticate using their existing identity provider credentials. When enabled, users see additional "Sign in with..." buttons on the login page.

Key features:

- Automatic user provisioning from OIDC provider
- Link OIDC accounts to existing users by email
- Sync user information (name, email) from provider
- Map OIDC groups to Poweradmin permission templates
- Support for multiple providers simultaneously
- PKCE (Proof Key for Code Exchange) for enhanced security

## Global Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `oidc.enabled` | false | Enable OIDC authentication |
| `oidc.auto_provision` | true | Auto-create users from OIDC provider |
| `oidc.link_by_email` | true | Link OIDC accounts to existing users by email |
| `oidc.sync_user_info` | true | Sync user info (name, email) on each login |
| `oidc.default_permission_template` | "" | Default permission template for new users |

## Permission Template Mapping

Map OIDC groups to Poweradmin permission templates for automatic role assignment:

```php
'oidc' => [
    'enabled' => true,
    'permission_template_mapping' => [
        'poweradmin-admins' => 'Administrator',
        'dns-operators' => 'DNS Operator',
        'dns-viewers' => 'Read Only',
    ],
],
```

When a user logs in, their OIDC groups are matched against this mapping. The first match determines their permission template.

## Provider Configuration

Each provider requires specific configuration. All providers share these common fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal provider identifier |
| `display_name` | Yes | Text shown on login button |
| `client_id` | Yes | OAuth client ID from provider |
| `client_secret` | Yes | OAuth client secret from provider |
| `auto_discovery` | No | Use OpenID Connect Discovery (default: true) |
| `metadata_url` | Conditional | OpenID Configuration endpoint (if auto_discovery) |
| `scopes` | No | OAuth scopes (default: openid profile email) |
| `logout_url` | No | Provider logout endpoint |
| `user_mapping` | No | Map OIDC claims to user fields |

### Azure AD (Microsoft)

1. Register an application in Azure Portal > App registrations
2. Add a redirect URI: `https://your-poweradmin.com/oidc/callback`
3. Create a client secret
4. Configure optional claims for groups if needed

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'azure' => [
            'name' => 'Microsoft Azure AD',
            'display_name' => 'Sign in with Microsoft',
            'client_id' => 'your-client-id',
            'client_secret' => 'your-client-secret',
            'tenant' => 'your-tenant-id',  // or 'common' for multi-tenant
            'auto_discovery' => true,
            'metadata_url' => 'https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration',
            'logout_url' => 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout',
            'scopes' => 'openid profile email',
            'user_mapping' => [
                'username' => 'email',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

**Note**: For group claims, configure "Group claims" in Azure AD App > Token configuration.

### Google

1. Go to Google Cloud Console > APIs & Services > Credentials
2. Create an OAuth 2.0 Client ID
3. Add authorized redirect URI: `https://your-poweradmin.com/oidc/callback`

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'google' => [
            'name' => 'Google',
            'display_name' => 'Sign in with Google',
            'client_id' => 'your-client-id.apps.googleusercontent.com',
            'client_secret' => 'your-client-secret',
            'auto_discovery' => true,
            'metadata_url' => 'https://accounts.google.com/.well-known/openid-configuration',
            'logout_url' => 'https://accounts.google.com/logout',
            'scopes' => 'openid profile email',
            'user_mapping' => [
                'username' => 'email',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
            ],
        ],
    ],
],
```

### Keycloak

1. Create a client in Keycloak Admin Console
2. Set Access Type to "confidential"
3. Add valid redirect URI: `https://your-poweradmin.com/oidc/callback`
4. Enable "groups" scope if using group mapping

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'keycloak' => [
            'name' => 'Keycloak',
            'display_name' => 'Sign in with Keycloak',
            'client_id' => 'poweradmin',
            'client_secret' => 'your-client-secret',
            'base_url' => 'https://keycloak.example.com',
            'realm' => 'master',
            'auto_discovery' => true,
            'metadata_url' => '{base_url}/realms/{realm}/.well-known/openid-configuration',
            'logout_url' => '{base_url}/realms/{realm}/protocol/openid-connect/logout',
            'scopes' => 'openid profile email groups',
            'user_mapping' => [
                'username' => 'preferred_username',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

### Okta

1. Create an OIDC application in Okta Admin Console
2. Set Sign-in redirect URI: `https://your-poweradmin.com/oidc/callback`
3. Note your Okta domain (e.g., your-org.okta.com)

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'okta' => [
            'name' => 'Okta',
            'display_name' => 'Sign in with Okta',
            'client_id' => 'your-client-id',
            'client_secret' => 'your-client-secret',
            'domain' => 'your-org.okta.com',
            'auto_discovery' => true,
            'metadata_url' => 'https://{domain}/.well-known/openid-configuration',
            'logout_url' => 'https://{domain}/oauth2/v1/logout',
            'scopes' => 'openid profile email groups',
            'user_mapping' => [
                'username' => 'preferred_username',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

### Authentik

1. Create an OAuth2/OpenID Provider in Authentik
2. Create an Application linked to the provider
3. Add redirect URI: `https://your-poweradmin.com/oidc/callback`

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'authentik' => [
            'name' => 'Authentik',
            'display_name' => 'Sign in with Authentik',
            'client_id' => 'your-client-id',
            'client_secret' => 'your-client-secret',
            'base_url' => 'https://authentik.example.com',
            'application_slug' => 'poweradmin',
            'auto_discovery' => true,
            'metadata_url' => '{base_url}/application/o/{application_slug}/.well-known/openid-configuration',
            'logout_url' => '{base_url}/application/o/{application_slug}/end-session/',
            'scopes' => 'openid profile email',
            'user_mapping' => [
                'username' => 'preferred_username',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

### Auth0

1. Create an application in Auth0 Dashboard
2. Set Application Type to "Regular Web Application"
3. Add callback URL: `https://your-poweradmin.com/oidc/callback`

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'auth0' => [
            'name' => 'Auth0',
            'display_name' => 'Sign in with Auth0',
            'client_id' => 'your-client-id',
            'client_secret' => 'your-client-secret',
            'domain' => 'your-tenant.auth0.com',
            'auto_discovery' => true,
            'metadata_url' => 'https://{domain}/.well-known/openid-configuration',
            'logout_url' => 'https://{domain}/v2/logout',
            'scopes' => 'openid profile email',
            'user_mapping' => [
                'username' => 'nickname',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

### Generic OIDC Provider

For providers not listed above, use manual endpoint configuration:

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'custom' => [
            'name' => 'Custom OIDC',
            'display_name' => 'Sign in with SSO',
            'client_id' => 'your-client-id',
            'client_secret' => 'your-client-secret',
            'auto_discovery' => false,
            'authorize_url' => 'https://provider.example.com/oauth/authorize',
            'token_url' => 'https://provider.example.com/oauth/token',
            'userinfo_url' => 'https://provider.example.com/oauth/userinfo',
            'logout_url' => 'https://provider.example.com/oauth/logout',
            'scopes' => 'openid profile email',
            'user_mapping' => [
                'username' => 'preferred_username',
                'email' => 'email',
                'first_name' => 'given_name',
                'last_name' => 'family_name',
                'display_name' => 'name',
                'groups' => 'groups',
            ],
        ],
    ],
],
```

## User Mapping

The `user_mapping` array maps OIDC claims to Poweradmin user fields:

| Poweradmin Field | Common OIDC Claims | Description |
|------------------|-------------------|-------------|
| `username` | preferred_username, email | User's login name |
| `email` | email | Email address |
| `first_name` | given_name | First name |
| `last_name` | family_name | Last name |
| `display_name` | name | Display name |
| `groups` | groups | Group memberships |
| `avatar` | picture | Profile picture URL |

## Docker Configuration

Use environment variables with the `PA_OIDC_` prefix:

```yaml
environment:
  PA_OIDC_ENABLED: "true"
  PA_OIDC_AUTO_PROVISION: "true"
  PA_OIDC_KEYCLOAK_CLIENT_ID: "poweradmin"
  PA_OIDC_KEYCLOAK_CLIENT_SECRET: "your-secret"
  PA_OIDC_KEYCLOAK_BASE_URL: "https://keycloak.example.com"
  PA_OIDC_KEYCLOAK_REALM: "master"
```

For secrets, use the `__FILE` suffix:

```yaml
secrets:
  oidc_client_secret:
    file: ./secrets/oidc_client_secret.txt

services:
  poweradmin:
    environment:
      PA_OIDC_KEYCLOAK_CLIENT_SECRET__FILE: /run/secrets/oidc_client_secret
    secrets:
      - oidc_client_secret
```

## Multiple Providers

You can configure multiple OIDC providers. Users will see all enabled providers on the login page:

```php
'oidc' => [
    'enabled' => true,
    'providers' => [
        'azure' => [
            // Azure AD configuration...
        ],
        'google' => [
            // Google configuration...
        ],
    ],
],
```

## Security Considerations

1. **Use HTTPS**: OIDC requires HTTPS for redirect URIs in production
2. **Protect client secrets**: Use Docker secrets or environment variables, never commit secrets to version control
3. **Validate redirect URIs**: Configure exact redirect URIs in your identity provider
4. **PKCE**: Poweradmin uses PKCE (Proof Key for Code Exchange) automatically for enhanced security
5. **State validation**: CSRF protection via state parameter is enabled by default

## Troubleshooting

### Login redirects fail

- Verify the redirect URI in your provider matches exactly: `https://your-poweradmin.com/oidc/callback`
- Check that your Poweradmin URL is accessible from the user's browser
- For reverse proxy setups, ensure `X-Forwarded-Proto` header is set

### User not created after login

- Check `auto_provision` is enabled
- Verify the user mapping includes required fields (username, email)
- Check application logs for provisioning errors

### Groups not mapped

- Ensure the `groups` scope is requested
- Verify your provider returns groups in the expected claim
- Check the `user_mapping.groups` matches your provider's claim name
- In Azure AD, configure Group claims in Token configuration

### "Invalid state" error

- Clear browser cookies and try again
- Check session configuration in Poweradmin
- Verify server time is synchronized (NTP)

## Related Documentation

- [SAML Authentication](saml.md)
- [LDAP Integration](ldap.md)
- [Security Policies](security-policies.md)
