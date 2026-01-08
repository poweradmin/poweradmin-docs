# Docker Secrets

For production deployments, use Docker secrets to securely manage sensitive configuration values instead of plain environment variables.

## Overview

Any Poweradmin environment variable can be provided via a file by appending `__FILE` to the variable name. The container reads the file contents and uses them as the actual value.

```bash
# Instead of this:
-e DB_PASS=mySecretPassword

# Use this:
-e DB_PASS__FILE=/run/secrets/db_password
```

## Docker Compose Example

```yaml
version: '3.8'

services:
  poweradmin:
    image: poweradmin/poweradmin:stable
    ports:
      - "80:80"
    environment:
      DB_TYPE: mysql
      DB_HOST: mysql
      DB_USER: poweradmin
      DB_PASS__FILE: /run/secrets/db_password
      DB_NAME: poweradmin
      PA_PDNS_API_KEY__FILE: /run/secrets/pdns_api_key
      PA_SMTP_PASSWORD__FILE: /run/secrets/smtp_password
    secrets:
      - db_password
      - pdns_api_key
      - smtp_password

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/mysql_root_password
      MYSQL_DATABASE: poweradmin
      MYSQL_USER: poweradmin
      MYSQL_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - mysql_root_password
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  mysql_root_password:
    file: ./secrets/mysql_root_password.txt
  pdns_api_key:
    file: ./secrets/pdns_api_key.txt
  smtp_password:
    file: ./secrets/smtp_password.txt
```

## Docker Swarm Example

```yaml
version: '3.8'

services:
  poweradmin:
    image: poweradmin/poweradmin:stable
    ports:
      - "80:80"
    environment:
      DB_TYPE: mysql
      DB_HOST: mysql
      DB_USER: poweradmin
      DB_PASS__FILE: /run/secrets/db_password
      DB_NAME: poweradmin
    secrets:
      - db_password
    deploy:
      replicas: 2

secrets:
  db_password:
    external: true
```

Create external secrets:

```bash
echo "mySecretPassword" | docker secret create db_password -
echo "pdns_api_key_12345" | docker secret create pdns_api_key -
```

## Supported Secret Variables

### Database

| Variable | Description |
|----------|-------------|
| `DB_PASS__FILE` | Database password |
| `DB_USER__FILE` | Database username |

### PowerDNS API

| Variable | Description |
|----------|-------------|
| `PA_PDNS_API_KEY__FILE` | PowerDNS API key |

### Mail/SMTP

| Variable | Description |
|----------|-------------|
| `PA_SMTP_PASSWORD__FILE` | SMTP password |
| `PA_SMTP_USER__FILE` | SMTP username |

### Security

| Variable | Description |
|----------|-------------|
| `PA_SESSION_KEY__FILE` | Session encryption key |
| `PA_RECAPTCHA_SECRET_KEY__FILE` | reCAPTCHA secret key |
| `PA_RECAPTCHA_SITE_KEY__FILE` | reCAPTCHA site key |

### LDAP

| Variable | Description |
|----------|-------------|
| `PA_LDAP_BIND_PASSWORD__FILE` | LDAP bind password |
| `PA_LDAP_BIND_DN__FILE` | LDAP bind DN |

### OIDC

| Variable | Description |
|----------|-------------|
| `PA_OIDC_AZURE_CLIENT_SECRET__FILE` | Azure AD client secret |
| `PA_OIDC_GOOGLE_CLIENT_SECRET__FILE` | Google client secret |
| `PA_OIDC_KEYCLOAK_CLIENT_SECRET__FILE` | Keycloak client secret |
| `PA_OIDC_OKTA_CLIENT_SECRET__FILE` | Okta client secret |

### SAML

| Variable | Description |
|----------|-------------|
| `PA_SAML_SP_PRIVATE_KEY__FILE` | SAML SP private key |
| `PA_SAML_AZURE_X509_CERT__FILE` | Azure AD IdP certificate |
| `PA_SAML_OKTA_X509_CERT__FILE` | Okta IdP certificate |

### Admin User

| Variable | Description |
|----------|-------------|
| `PA_ADMIN_PASSWORD__FILE` | Initial admin password |

## Multi-line Secrets

For certificates and private keys, create files with the full content:

```bash
# Create certificate secret
cat > ./secrets/saml_cert.txt << 'EOF'
MIICnTCCAYUCBgF...
...certificate content...
EOF

# Create private key secret
cat > ./secrets/saml_key.txt << 'EOF'
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBg...
...key content...
-----END PRIVATE KEY-----
EOF
```

## Security Best Practices

1. **File permissions**: Set restrictive permissions on secret files

```bash
chmod 600 ./secrets/*
```

2. **Read-only mounts**: Mount secrets as read-only

```yaml
volumes:
  - ./secrets/db_password.txt:/run/secrets/db_password:ro
```

3. **Exclude from version control**: Add secrets to `.gitignore`

```
secrets/
*.key
*.pem
```

4. **Use external secrets in production**: For Swarm deployments, use external secrets managed outside of compose files

5. **Rotate secrets regularly**: Update secret files and restart containers

## Configuration Priority

Configuration is loaded in this order (later overrides earlier):

1. Default values
2. Configuration file (`config/settings.php`)
3. Environment variables
4. Docker secrets (`__FILE` variables)

## Error Handling

The container validates secrets at startup:

- **Mutual exclusivity**: Cannot set both `VAR` and `VAR__FILE` for the same variable
- **File existence**: Secret files must exist and be readable
- **Permission checks**: Files must be accessible by the container user

## Troubleshooting

### Check secret loading

```bash
docker logs poweradmin | grep -i secret
```

Look for messages like:
```
[2025-01-18 10:30:00] Getting secret DB_PASS from /run/secrets/db_password
```

### Enable debug mode

```yaml
environment:
  DEBUG: "true"
```

### Common issues

| Problem | Solution |
|---------|----------|
| File not found | Verify secret file path and mount |
| Permission denied | Check file permissions (readable by www-data) |
| Both variables set | Remove either `VAR` or `VAR__FILE`, not both |
| Empty value | Ensure secret file is not empty |

## Directory Structure

Recommended secrets directory layout:

```
project/
├── docker-compose.yml
└── secrets/
    ├── db_password.txt
    ├── pdns_api_key.txt
    ├── smtp_password.txt
    ├── oidc_client_secret.txt
    └── saml_sp_key.txt
```

## Related Documentation

- [Docker Installation](docker.md)
- [Basic Configuration](../configuration/basic.md)
- [OIDC Authentication](../configuration/oidc.md)
- [SAML Authentication](../configuration/saml.md)
