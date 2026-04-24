# Docker Installation

Poweradmin provides official Docker images for easy deployment with FrankenPHP.

## Docker Images

Official images are available at:

- **Docker Hub**: [`poweradmin/poweradmin`](https://hub.docker.com/r/poweradmin/poweradmin)
- **GitHub Container Registry**: [`ghcr.io/poweradmin/poweradmin`](https://github.com/poweradmin/poweradmin/pkgs/container/poweradmin)

### Image Tags

| Tag | Description |
|-----|-------------|
| `stable` | Stable release from `release/4.2.x` (recommended for production) |
| `latest` | Latest release from `master` branch |
| `dev` | Development version from `develop` branch (not for production) |
| `lts` | Long-term support from `release/3.x` |
| `v*` | Specific version (e.g., `v4.2.1`) |

> **Note:** The `next` tag has been removed. The `stable` tag now tracks `release/4.2.x` instead of the retired `release/4.0.x`.

## Quick Start

### SQLite (Default)

```bash
docker run -d --name poweradmin -p 80:80 \
  -e PA_CREATE_ADMIN=1 \
  -v poweradmin-db:/db \
  poweradmin/poweradmin:stable
```

Check logs for the generated admin password:

```bash
docker logs poweradmin | grep -i password
```

### MySQL

```bash
docker run -d --name poweradmin -p 80:80 \
  -e PA_CREATE_ADMIN=1 \
  -e DB_TYPE=mysql \
  -e DB_HOST=mysql-server \
  -e DB_USER=poweradmin \
  -e DB_PASS=your-password \
  -e DB_NAME=poweradmin \
  -e DNS_NS1=ns1.example.com \
  -e DNS_NS2=ns2.example.com \
  -e DNS_HOSTMASTER=hostmaster.example.com \
  poweradmin/poweradmin:stable
```

### PostgreSQL

```bash
docker run -d --name poweradmin -p 80:80 \
  -e PA_CREATE_ADMIN=1 \
  -e DB_TYPE=pgsql \
  -e DB_HOST=postgres-server \
  -e DB_USER=poweradmin \
  -e DB_PASS=your-password \
  -e DB_NAME=poweradmin \
  -e DNS_NS1=ns1.example.com \
  -e DNS_NS2=ns2.example.com \
  -e DNS_HOSTMASTER=hostmaster.example.com \
  poweradmin/poweradmin:stable
```

## Docker Compose

### Basic Setup with MySQL

```yaml
version: '3.8'

services:
  poweradmin:
    image: poweradmin/poweradmin:stable
    ports:
      - "80:80"
    environment:
      PA_CREATE_ADMIN: "true"
      PA_ADMIN_PASSWORD: "change-me"
      DB_TYPE: mysql
      DB_HOST: mysql
      DB_USER: poweradmin
      DB_PASS: poweradmin-password
      DB_NAME: poweradmin
      DNS_NS1: ns1.example.com
      DNS_NS2: ns2.example.com
      DNS_HOSTMASTER: hostmaster.example.com
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root-password
      MYSQL_DATABASE: poweradmin
      MYSQL_USER: poweradmin
      MYSQL_PASSWORD: poweradmin-password
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

### With PowerDNS

```yaml
version: '3.8'

services:
  poweradmin:
    image: poweradmin/poweradmin:stable
    ports:
      - "8080:80"
    environment:
      PA_CREATE_ADMIN: "true"
      DB_TYPE: mysql
      DB_HOST: mysql
      DB_USER: poweradmin
      DB_PASS: poweradmin-password
      DB_NAME: poweradmin
      PA_PDNS_DB_NAME: pdns
      DNS_NS1: ns1.example.com
      DNS_NS2: ns2.example.com
      DNS_HOSTMASTER: hostmaster.example.com
      PA_PDNS_API_URL: http://powerdns:8081
      PA_PDNS_API_KEY: your-api-key
    depends_on:
      - mysql
      - powerdns

  powerdns:
    image: powerdns/pdns-auth-49
    ports:
      - "53:53/udp"
      - "53:53/tcp"
    environment:
      PDNS_gmysql_host: mysql
      PDNS_gmysql_user: pdns
      PDNS_gmysql_password: pdns-password
      PDNS_gmysql_dbname: pdns
      PDNS_api: "yes"
      PDNS_api_key: your-api-key
      PDNS_webserver: "yes"
      PDNS_webserver_address: "0.0.0.0"
      PDNS_webserver_allow_from: "0.0.0.0/0"
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root-password
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  mysql-data:
```

## Admin User Creation

The container can automatically create an admin user on first startup:

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_CREATE_ADMIN` | false | Enable admin creation (true/1/yes) |
| `PA_ADMIN_USERNAME` | admin | Admin username |
| `PA_ADMIN_PASSWORD` | (auto) | Admin password (auto-generated if not set) |
| `PA_ADMIN_EMAIL` | admin@example.com | Admin email |
| `PA_ADMIN_FULLNAME` | Administrator | Admin display name |

If `PA_ADMIN_PASSWORD` is not set, a secure password is generated and logged:

```bash
docker logs poweradmin | grep -i password
```

**Note**: The admin user is only created if it doesn't already exist.

## Key Environment Variables

### Database

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_TYPE` | sqlite | Database type: sqlite, mysql, pgsql |
| `DB_HOST` | - | Database hostname |
| `DB_PORT` | - | Database port (3306 for MySQL, 5432 for PostgreSQL) |
| `DB_USER` | - | Database username |
| `DB_PASS` | - | Database password |
| `DB_NAME` | - | Database name |
| `PA_PDNS_DB_NAME` | - | Separate PowerDNS database (MySQL only) |

### DNS

| Variable | Default | Description |
|----------|---------|-------------|
| `DNS_NS1` | ns1.example.com | Primary nameserver |
| `DNS_NS2` | ns2.example.com | Secondary nameserver |
| `DNS_HOSTMASTER` | hostmaster.example.com | Hostmaster email |

### Security

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_SESSION_KEY` | (auto) | Session encryption key |
| `PA_PASSWORD_ENCRYPTION` | bcrypt | Password hashing: `bcrypt`, `argon2i`, `argon2id` |
| `PA_LOGIN_TOKEN_VALIDATION` | true | Enable CSRF token validation for login |
| `PA_GLOBAL_TOKEN_VALIDATION` | true | Enable CSRF token validation for all forms |
| `PA_MFA_ENABLED` | false | Enable multi-factor authentication |
| `PA_MFA_ENFORCED` | false | Enforce MFA for users with enforce permission |
| `PA_RECAPTCHA_ENABLED` | false | Enable reCAPTCHA on login |
| `PA_RECAPTCHA_VERSION` | v3 | reCAPTCHA version: `v2` or `v3` |
| `PA_LOCKOUT_ENABLED` | false | Enable account lockout after failed logins |
| `PA_LOCKOUT_ATTEMPTS` | 5 | Failed attempts before lockout |
| `PA_LOCKOUT_DURATION` | 15 | Lockout duration in minutes |
| `PA_PASSWORD_RESET_ENABLED` | false | Enable password reset functionality |
| `PA_USERNAME_RECOVERY_ENABLED` | false | Enable username recovery functionality |

### Interface

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_APP_TITLE` | Poweradmin | Application title |
| `PA_DEFAULT_LANGUAGE` | en_EN | Default language |
| `PA_SESSION_TIMEOUT` | 1800 | Session timeout (seconds) |
| `PA_STYLE` | light | UI style: light or dark |

### PowerDNS API

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_PDNS_API_URL` | - | PowerDNS API URL |
| `PA_PDNS_API_KEY` | - | PowerDNS API key |

### Modules

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_MODULE_CSV_EXPORT_ENABLED` | true | Enable CSV export module |
| `PA_MODULE_ZONE_IMPORT_EXPORT_ENABLED` | false | Enable zone import/export module |
| `PA_MODULE_ZONE_IMPORT_EXPORT_AUTO_TTL` | 300 | Default TTL for imported records (seconds) |
| `PA_MODULE_ZONE_IMPORT_EXPORT_MAX_FILE_SIZE` | 1048576 | Max upload file size in bytes |
| `PA_MODULE_WHOIS_ENABLED` | false | Enable WHOIS lookup module |
| `PA_MODULE_WHOIS_RESTRICT_TO_ADMIN` | true | Restrict WHOIS to administrators |
| `PA_MODULE_RDAP_ENABLED` | false | Enable RDAP lookup module |
| `PA_MODULE_RDAP_RESTRICT_TO_ADMIN` | true | Restrict RDAP to administrators |
| `PA_MODULE_EMAIL_PREVIEWS_RESTRICT_TO_ADMIN` | true | Restrict email previews to administrators |
| `PA_MODULE_DNS_WIZARDS_TYPES` | DMARC,SPF,DKIM,CAA,TLSA,SRV | Comma-separated list of DNS wizard types |

For detailed module configuration, see the [Configuration](../configuration/zone-import-export.md) section.

### Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LDAP_ENABLED` | false | Enable LDAP authentication |
| `PA_LDAP_USER_ATTRIBUTE` | uid | User attribute (`uid` for OpenLDAP, `sAMAccountName` for AD) |
| `PA_OIDC_ENABLED` | false | Enable OpenID Connect |
| `PA_SAML_ENABLED` | false | Enable SAML authentication |

### Custom CA Certificate

| Variable | Default | Description |
|----------|---------|-------------|
| `TRUSTED_CA_FILE` | - | Path to a custom CA certificate file inside the container |

Use this when connecting to services (OIDC, SAML, LDAP, PowerDNS API) that use self-signed or internal CA certificates:

```bash
docker run -d --name poweradmin -p 80:80 \
  -e TRUSTED_CA_FILE=/certs/my-ca.crt \
  -v /path/to/my-ca.crt:/certs/my-ca.crt:ro \
  poweradmin/poweradmin
```

### Miscellaneous

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_TIMEZONE` | UTC | Default timezone |
| `PA_EDIT_CONFLICT_RESOLUTION` | last_writer_wins | Edit conflict resolution strategy |
| `PA_DNS_CUSTOM_TLDS` | - | Comma-separated custom TLDs (e.g., `dn42,home`) |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LOGGING_TYPE` | null | Logger type: `null` or `native` |
| `PA_LOGGING_LEVEL` | info | Log level (debug, info, warning, error, etc.) |
| `PA_LOGGING_DATABASE_ENABLED` | false | Log zone/record changes to database |
| `PA_LOGGING_SYSLOG_ENABLED` | false | Log auth attempts to syslog |
| `PA_LOGGING_SYSLOG_IDENTITY` | poweradmin | Syslog program identity |
| `PA_LOGGING_SYSLOG_FACILITY` | LOG_USER | Syslog facility (`LOG_USER`, `LOG_LOCAL0`-`LOG_LOCAL7`) |

For complete environment variable reference, see the [DOCKER.md](https://github.com/poweradmin/poweradmin/blob/master/DOCKER.md) in the source repository.

## Volumes

| Path | Description |
|------|-------------|
| `/db` | SQLite database directory |
| `/app/config` | Configuration files (optional) |

## Secrets

For production, use Docker secrets instead of environment variables for sensitive data. See [Docker Secrets](docker-secrets.md) for details.

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  poweradmin:
    environment:
      DB_PASS__FILE: /run/secrets/db_password
    secrets:
      - db_password
```

## Non-Root / Rootless Deployment

The Poweradmin image supports running as a non-root user for restricted Kubernetes clusters and OpenShift. No separate image variant is needed - the entrypoint adapts automatically.

### Behavior

| Start mode | Port | Privileges | Use case |
|------------|------|------------|----------|
| Root (default) | 80 | Drops to www-data after setup | Standard Docker, unrestricted K8s |
| Non-root | 8080 (auto) | No chown/chmod/CA install | Restricted K8s, OpenShift |

### Docker (Non-Root)

```bash
docker run --rm --user 82:82 -p 8080:8080 \
  -e DB_TYPE=sqlite \
  poweradmin/poweradmin:stable
```

### Kubernetes (Restricted)

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 82
    runAsGroup: 82
    fsGroup: 82
  containers:
    - name: poweradmin
      image: poweradmin/poweradmin:stable
      ports:
        - containerPort: 8080
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
      env:
        - name: DB_TYPE
          value: sqlite
```

`fsGroup: 82` ensures volumes are group-writable for `www-data` (GID 82).

### Custom Port

Override the auto-detected port with `SERVER_PORT`:

```bash
docker run --rm -e SERVER_PORT=9090 -p 9090:9090 poweradmin/poweradmin
```

### Limitations (Non-Root)

- `TRUSTED_CA_FILE` requires root - a warning is logged if set in non-root mode
- Volumes must be pre-configured as writable (use `fsGroup` or host permissions)

## Troubleshooting

### Check container logs

```bash
docker logs poweradmin
```

### Access container shell

```bash
docker exec -it poweradmin /bin/sh
```

### Database connection issues

1. Verify database is accessible from container
2. Check credentials are correct
3. Ensure database exists and user has permissions

### Permission issues with volumes

```bash
docker run --user root ...
# or fix permissions on host
sudo chown -R 1000:1000 /path/to/volume
```

## Related Documentation

- [Docker Secrets](docker-secrets.md)
- [Manual Installation](manual.md)
- [Basic Configuration](../configuration/basic.md)
