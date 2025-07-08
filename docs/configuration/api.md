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

## Configuration Example

```php
return [
    'api' => [
        'enabled' => true,
        'basic_auth_enabled' => true,
        'basic_auth_realm' => 'DNS Management API',
        'log_requests' => true,
        'docs_enabled' => true,
    ],
];
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