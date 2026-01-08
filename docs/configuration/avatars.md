# Avatar System

Poweradmin v4.0.0+ supports user avatars from OAuth providers and Gravatar.

## Overview

The avatar system displays user profile pictures in the interface. Avatars can be sourced from:

- **OAuth providers**: Profile pictures from OIDC/SAML identity providers
- **Gravatar**: Global avatar service based on email address

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `interface.avatar_oauth_enabled` | true | Enable avatars from OAuth providers |
| `interface.avatar_gravatar_enabled` | true | Enable Gravatar integration |
| `interface.avatar_priority` | oauth | Priority: oauth or gravatar |
| `interface.avatar_size` | 40 | Avatar size in pixels |
| `interface.avatar_cache_ttl` | 3600 | Cache TTL in seconds |

## Modern Configuration

```php
return [
    'interface' => [
        'avatar_oauth_enabled' => true,
        'avatar_gravatar_enabled' => true,
        'avatar_priority' => 'oauth',  // 'oauth' or 'gravatar'
        'avatar_size' => 40,
        'avatar_cache_ttl' => 3600,    // 1 hour
    ],
];
```

## Docker Configuration

```yaml
environment:
  PA_AVATAR_OAUTH_ENABLED: "true"
  PA_AVATAR_GRAVATAR_ENABLED: "true"
  PA_AVATAR_PRIORITY: "oauth"
  PA_AVATAR_SIZE: "40"
  PA_AVATAR_CACHE_TTL: "3600"
```

## Avatar Priority

The `avatar_priority` setting determines which source is checked first:

- **oauth**: Check OAuth provider first, fall back to Gravatar
- **gravatar**: Check Gravatar first, fall back to OAuth

If the primary source has no avatar, the secondary source is used.

## OAuth Avatars

OAuth avatars are retrieved from identity providers during login:

- Azure AD, Google, Keycloak, etc. provide profile pictures
- The `picture` claim is mapped automatically
- Avatars are cached locally to reduce provider requests

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

Avatars are cached to improve performance:

- **Cache TTL**: Default 1 hour (3600 seconds)
- **Cache key**: Based on user ID and source
- **Cache invalidation**: Automatic on logout

Adjust `avatar_cache_ttl` based on your needs:
- Lower values: More frequent updates, more requests
- Higher values: Better performance, stale avatars

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
3. **Caching**: Avatars may be cached on server

For privacy-conscious deployments, consider disabling Gravatar and relying only on OAuth avatars (which users explicitly provide to their identity provider).

## Related Documentation

- [OIDC Authentication](oidc.md)
- [SAML Authentication](saml.md)
- [UI Customization](ui/overview.md)
