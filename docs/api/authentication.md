# API Authentication

Poweradmin supports two authentication methods for API requests: API keys
(recommended) and HTTP Basic Authentication. Both must be enabled in
`config/settings.php` before they can be used; see
[API Configuration](../configuration/api.md) for the settings.

## API key authentication

API keys are the recommended method for scripts, CI, and any
long-lived integration. They can be revoked individually without disrupting
other clients and they do not expose user passwords.

### Issuing a key

API keys are created through the web UI:

1. Log in to Poweradmin.
2. Go to **Settings -> API Keys** (`/settings/api-keys`).
3. Click **Add API Key**, give it a recognizable name, and copy the value.
   The full key is shown only once.

A regular user can hold up to `api.max_keys_per_user` keys (default 5). Admin
users have no limit.

### Using a key

Send the key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key-here" \
     -H "Content-Type: application/json" \
     https://poweradmin.example.com/api/v2/zones
```

The key inherits the permissions of the user it belongs to. If that user can
edit zone X in the web UI, the key can edit zone X over the API; if they
cannot, the key cannot either.

### Restricting what a key can do

*Available since v4.5.0.*

By default a key can do everything its owner can. The add and edit forms let you
narrow that down, which is what you want for a key handed to a monitoring agent, a
CI job, or a single application.

![Add API Key](../screenshots/api-key-add.png)

Three independent restrictions are available:

| Restriction | Effect |
|---|---|
| **Read-only** | Only `GET` and `HEAD` requests are accepted. Everything else gets `403`. |
| **Allowed operations** | Tick any of `view`, `create`, `update`, `delete`. A request whose operation is not ticked gets `403`. Leave all unticked to allow every operation. |
| **Zone access** | Select specific zones. Requests targeting any other zone get `403`. Leave empty to allow every zone the owner can reach. |

Operations map onto HTTP methods: `POST` is create, `PUT` and `PATCH` are update,
`DELETE` is delete, and everything else is view. Endpoints that do more than one
thing in a single request, such as a dynamic DNS upsert or a bulk record change,
must satisfy every operation they perform.

Restrictions only narrow access - they never widen it. A read-only key belonging to
a user with no zone permissions still cannot read anything.

Existing keys are unrestricted after an upgrade, so nothing changes until you
edit a key and apply restrictions.

> **Note:** These restrictions are enforced on API v2 only. API v1 was removed in
> 4.5.0 and answers `410 Gone`.

### Rotating and revoking keys

From **Settings -> API Keys** you can:

- **Regenerate** a key (invalidates the old value, issues a new one)
- **Disable** a key temporarily without deleting it
- **Delete** a key permanently

Rotate keys on a schedule that matches your security policy, and revoke
immediately if a key may have leaked.

## HTTP Basic Authentication

When `api.basic_auth_enabled` is `true`, the API also accepts standard HTTP
Basic Auth with a Poweradmin username and password:

```bash
curl -u alice:s3cret \
     -H "Content-Type: application/json" \
     https://poweradmin.example.com/api/v2/zones
```

This is convenient for ad-hoc requests but it has trade-offs:

- The password travels with every request - HTTPS is mandatory
- Revoking access means changing the user's password (which affects the UI too)
- MFA-enabled accounts are not supported over Basic Auth

For anything beyond exploration, prefer API keys.

## Required request headers

| Header | When | Notes |
|--------|------|-------|
| `X-API-Key` | API key auth | The full key value |
| `Authorization: Basic ...` | Basic auth | Base64-encoded `user:pass` |
| `Content-Type: application/json` | All `POST`, `PUT` requests | Required for body parsing |
| `Accept: application/json` | Optional | Responses are always JSON |

Some reverse-proxy setups strip the `Authorization` header by default. If
Basic Auth or API keys appear to be ignored, check that your web server is
forwarding the header to PHP - see the nginx example in
[API Configuration](../configuration/api.md#web-server-requirements).

## Common authentication errors

| Status | Meaning | What to check |
|--------|---------|---------------|
| `401 Unauthorized` | No credentials, or bad credentials | Header name, key value, account is active |
| `403 Forbidden` | Authenticated but lacks permission | The owning user's permission template |
| `404 Not Found` | Often a resource that the user cannot see | Permissions can mask resources as missing |

## Next steps

- [Endpoints](endpoints.md) - what you can call once authenticated
- [API Configuration](../configuration/api.md) - server-side settings
- [Headless Quickstart](../getting-started/headless-quickstart.md) - end-to-end
  walkthrough including issuing a key and making your first request
