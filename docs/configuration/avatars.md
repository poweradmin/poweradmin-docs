# Avatar System

Poweradmin v4.1.0+ supports user avatars from OAuth providers and Gravatar.

## Overview

The avatar system displays user profile pictures in the interface. Avatars can be sourced from:

- **OIDC providers**: Profile pictures from OpenID Connect identity providers. SAML logins do not supply an avatar URL
- **Gravatar**: Global avatar service based on email address

## Configuration

| Setting                              | Default | Description                          |
|--------------------------------------|---------|--------------------------------------|
| `interface.avatar_oauth_enabled`     | `false` | Enable avatars from OAuth providers  |
| `interface.avatar_gravatar_enabled`  | `false` | Enable Gravatar integration          |
| `interface.avatar_priority`          | `oauth` | Priority: `oauth` or `gravatar`      |
| `interface.avatar_size`              | `40`    | Avatar size in pixels                |

## Configuration

```php
return [
    'interface' => [
        'avatar_oauth_enabled' => true,
        'avatar_gravatar_enabled' => true,
        'avatar_priority' => 'oauth',  // 'oauth' or 'gravatar'
        'avatar_size' => 40,
    ],
];
```

> **Note:** There are no `PA_AVATAR_*` environment variables. The Docker entrypoint writes no avatar keys, so configure avatars in `config/settings.php` (bind-mount the file into the container if needed).

## Avatar Priority

The `avatar_priority` setting determines which source is checked first:

- **oauth**: Check OAuth provider first, fall back to Gravatar
- **gravatar**: Check Gravatar first

The fallback only applies with `oauth`: if the login supplied no avatar URL, Gravatar is used instead. With `gravatar`, any user who has an email address gets a Gravatar URL (Gravatar serves a generated default image for unknown addresses), so the OAuth picture is never reached.

## OAuth Avatars

OAuth avatars are retrieved from identity providers during login:

- Azure AD, Google, Keycloak, etc. provide profile pictures
- The `picture` claim is mapped automatically
- The URL is kept in the session and the image is loaded by the browser straight from the provider

### OIDC Configuration

Ensure user mapping includes the avatar claim:

```php
'user_mapping' => [
    'avatar' => 'picture',
    // ... other mappings
],
```

## Gravatar Integration

Gravatar avatars are based on the user's email address:

1. Email is hashed using MD5
2. Avatar is fetched from `gravatar.com`
3. Default avatar shown if no Gravatar exists

Users can set their Gravatar at [gravatar.com](https://gravatar.com).

### Gravatar Defaults

If a user has no Gravatar, a default image is displayed. Gravatar provides several default styles:

- `mp` - Mystery person silhouette
- `identicon` - Geometric pattern
- `monsterid` - Monster avatar
- `wavatar` - Face avatar
- `retro` - 8-bit style

## Caching

Poweradmin does not cache avatar images server-side. It only builds the avatar URL (the provider's picture URL, or a Gravatar URL derived from the email) and hands it to the browser, which caches it under normal HTTP rules.

> **Note:** `interface.avatar_cache_ttl` exists in `settings.defaults.php` but is not read anywhere in the application. Setting it has no effect.

## Disabling Avatars

To disable avatars completely:

```php
'interface' => [
    'avatar_oauth_enabled' => false,
    'avatar_gravatar_enabled' => false,
],
```

## Privacy Considerations

1. **Gravatar**: Sends hashed email to external service
2. **OAuth**: Avatar URLs may be stored in session
3. **Browser requests**: Images are fetched by the user's browser directly from Gravatar or the identity provider

For privacy-conscious deployments, consider disabling Gravatar and relying only on OAuth avatars (which users explicitly provide to their identity provider).

## Related Documentation

- [OIDC Authentication](oidc.md)
- [SAML Authentication](saml.md)
- [UI Customization](ui/overview.md)
