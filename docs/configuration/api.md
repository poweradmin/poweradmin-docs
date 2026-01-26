# API Configuration

## Overview

Poweradmin includes a RESTful API that allows external applications to interact with DNS records and zones programmatically. The API supports both API key authentication and HTTP Basic Authentication.

## Configuration Options

API settings can be configured in the `config/settings.php` file under the `api` section.

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Enable API functionality (including API keys) |
| `basic_auth_enabled` | `false` | Enable HTTP Basic Authentication for public API endpoints |
| `basic_auth_realm` | `Poweradmin API` | Realm name for HTTP Basic Authentication |
| `log_requests` | `false` | Log all API requests |
| `docs_enabled` | `false` | Enable API documentation at /api/docs endpoint |
| `max_keys_per_user` | `5` | Maximum API keys per user (admin users unlimited) |

## Configuration Example

```php
return [
    'api' => [
        'enabled' => true,
        'basic_auth_enabled' => true,
        'basic_auth_realm' => 'DNS Management API',
        'log_requests' => true,
        'docs_enabled' => true,
        'max_keys_per_user' => 5,  // Admin users have no limit
    ],
];
```

## Web Server Requirements

The API requires proper web server configuration to function correctly. The PHP router handles API path parsing from `REQUEST_URI`, so explicit per-endpoint rewrite rules are not needed—just route all `/api/*` requests to `index.php`.

### Key Requirements

| Requirement | Description |
|-------------|-------------|
| **CORS Headers** | Required for cross-origin API requests from browsers |
| **Authorization Header** | Must be forwarded to PHP for API key authentication |
| **Clean URL Routing** | Route non-file requests to `index.php` |

### Configuration Examples

Use the web server configuration examples from the Poweradmin repository:

**Apache:**

- The included `.htaccess` file handles everything automatically
- Ensure `AllowOverride All` and `mod_rewrite` are enabled
- Version links: [4.0.x .htaccess](https://github.com/poweradmin/poweradmin/blob/release/4.x/.htaccess) | [4.1.x+ .htaccess](https://github.com/poweradmin/poweradmin/blob/master/.htaccess)

**Nginx:**

- [nginx.conf.example (4.0.x)](https://github.com/poweradmin/poweradmin/blob/release/4.x/nginx.conf.example)
- [nginx.conf.example (4.1.x+)](https://github.com/poweradmin/poweradmin/blob/master/nginx.conf.example) — includes subfolder deployment support

**Caddy:**

- [Caddyfile.example (4.0.x)](https://github.com/poweradmin/poweradmin/blob/release/4.x/Caddyfile.example)
- [caddy.conf.example (4.1.x+)](https://github.com/poweradmin/poweradmin/blob/master/caddy.conf.example) — includes subfolder deployment support

### Minimal Nginx Example

If you need a minimal configuration, ensure these key elements are present:

```nginx
# CORS and API routing
location ~ ^/api {
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-API-Key" always;

    if ($request_method = 'OPTIONS') {
        return 204;
    }

    try_files $uri $uri/ /index.php$is_args$args;
}

# PHP handling - ensure Authorization header is forwarded
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param HTTP_AUTHORIZATION $http_authorization;
    include fastcgi_params;
}
```

## Authentication Methods

### API Key Authentication

API keys provide secure, token-based authentication:

1. **Generate API keys** - Create keys for each application
2. **Permissions** - Restrict access to specific operations
3. **Revocation** - Easily revoke compromised keys

#### Using API Keys

```bash
curl -H "X-API-Key: your-api-key-here" \
     -H "Content-Type: application/json" \
     https://your-domain.com/api/v1/zones
```

### HTTP Basic Authentication

Traditional username/password authentication:

```bash
curl -u username:password \
     -H "Content-Type: application/json" \
     https://your-domain.com/api/v1/zones
```

## API Endpoints

### Zone Management

- `GET /api/v1/zones` - List all zones
- `GET /api/v1/zones/{id}` - Get zone details
- `POST /api/v1/zones` - Create new zone
- `PUT /api/v1/zones/{id}` - Update zone
- `DELETE /api/v1/zones/{id}` - Delete zone

### Record Management

- `GET /api/v1/zones/{id}/records` - List zone records
- `GET /api/v1/records/{id}` - Get record details
- `POST /api/v1/zones/{id}/records` - Create record
- `PUT /api/v1/records/{id}` - Update record
- `DELETE /api/v1/records/{id}` - Delete record

### User Management

- `GET /api/v1/users` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user details
- `POST /api/v1/users` - Create user (admin only)
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Permission Management

- `GET /api/v1/permissions` - List available permissions
- `GET /api/v1/permissions/{id}` - Get permission details

### Permission Templates

- `GET /api/v1/permission-templates` - List permission templates
- `GET /api/v1/permission-templates/{id}` - Get permission template details
- `POST /api/v1/permission-templates` - Create permission template
- `PUT /api/v1/permission-templates/{id}` - Update permission template
- `DELETE /api/v1/permission-templates/{id}` - Delete permission template

### Internal API Endpoints

The following endpoints are available for internal use (session-based authentication):

- `GET /api/internal/zones/{id}/validate` - Validate zone configuration
- `GET /api/internal/users/{id}/preferences` - Get user preferences
- `PUT /api/internal/users/{id}/preferences` - Update user preferences
- `POST /api/internal/validation` - Validate various data types

## API Documentation

When `docs_enabled` is true, interactive API documentation is available at `/api/docs`. This provides:

- **Interactive testing** - Test API endpoints directly
- **Request/response examples** - See data formats
- **Authentication guide** - Learn how to authenticate
- **Error codes** - Understand error responses

## Security Considerations

### Production Setup

```php
'api' => [
    'enabled' => true,
    'basic_auth_enabled' => false, // Use API keys only
    'log_requests' => true,        // Enable audit logging
    'docs_enabled' => false,       // Disable docs in production
],
```

### Security Best Practices

1. **Use HTTPS only** - Never expose API over HTTP
2. **API key rotation** - Regularly rotate API keys
3. **Access control** - Restrict API access by IP if possible
4. **Audit logging** - Log all API requests and responses

## Request/Response Format

### Request Format

```json
{
    "name": "example.com",
    "type": "A",
    "content": "192.168.1.100",
    "ttl": 3600
}
```

### Response Format

```json
{
    "success": true,
    "data": {
        "id": 123,
        "name": "example.com",
        "type": "A",
        "content": "192.168.1.100",
        "ttl": 3600,
        "created_at": "2023-01-01T12:00:00Z",
        "updated_at": "2023-01-01T12:00:00Z"
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid record type",
        "details": {
            "field": "type",
            "value": "INVALID"
        }
    }
}
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Invalid API key or credentials
2. **403 Forbidden**: Insufficient permissions
3. **500 Internal Server Error**: Server configuration issue

### Debugging

Enable request logging for troubleshooting:

```php
'api' => [
    'log_requests' => true,
],
```

Check logs in your configured logging destination for detailed request/response information.

## PowerDNS Metrics API *(v4.0.3+)*

Poweradmin can integrate with PowerDNS metrics endpoints for monitoring and status information.

### Configuration

```php
'pdns' => [
    'api_url' => 'http://localhost:8081/api/v1',
    'api_key' => 'your-powerdns-api-key',
    'server_id' => 'localhost',
    'metrics' => [
        'enabled' => true,
        'basic_auth' => [
            'username' => 'admin',
            'password' => 'your-password',
        ],
    ],
],
```

### Basic Authentication for Metrics *(v4.0.3+)*

Starting with v4.0.3, Poweradmin supports Basic Authentication for accessing PowerDNS metrics endpoints (issue #800). This is useful when your PowerDNS API is protected with Basic Auth in addition to API keys.

**Example configuration:**

```php
'pdns' => [
    'metrics' => [
        'enabled' => true,
        'basic_auth' => [
            'username' => 'metrics_user',
            'password' => 'secure_password',
        ],
    ],
],
```

## Pagination *(v4.0.1+)*

### Optional Pagination Parameters

Starting with v4.0.1, pagination is optional for zones and users endpoints (issue #803). You can now request all records without pagination limits.

**Without pagination (returns all results):**
```bash
GET /api/v1/zones
GET /api/v1/users
```

**With pagination:**
```bash
GET /api/v1/zones?page=1&limit=50
GET /api/v1/users?page=2&limit=25
```

### Pagination Response

```json
{
    "success": true,
    "data": [...],
    "pagination": {
        "total": 150,
        "page": 1,
        "limit": 50,
        "pages": 3
    }
}
```

## Version History

### v4.1.0
- Improved API stability and error handling

### v4.0.4
- **Fixed:** Basic Auth TypeError when LDAP authentication is enabled (issue #799)
  - Resolves compatibility issues between Basic Auth and LDAP
  - Properly handles authentication context

### v4.0.3
- **Added:** Basic Auth support for PowerDNS metrics endpoint (issue #800)
  - Enables authentication for metrics API calls
  - Supports username/password in addition to API keys

### v4.0.2
- **Fixed:** Routing and method validation issues (issue #767)
- **Fixed:** Graceful handling of missing optional fields (issue #818)

### v4.0.1
- **Added:** Optional pagination for zones and users endpoints (issue #803)
  - Can now request all records without pagination
  - Backward compatible with paginated requests
- **Fixed:** SOA serial updates on all record operations (issue #804)
  - Ensures zone serial increments properly
  - Maintains DNS propagation consistency

### v4.0.0
- Initial API implementation
- API key management system
- RESTful endpoints for zones, records, users
- Permission template management
- Interactive API documentation
- Request logging and audit trails

## Related Documentation

- [Security Policies](security-policies.md) - API authentication and authorization
- [PowerDNS API](powerdns-api.md) - PowerDNS API configuration
- [Logging Configuration](logging.md) - API request logging setup