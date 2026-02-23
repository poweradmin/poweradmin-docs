# Docker Installation

Poweradmin provides official Docker images for easy deployment with FrankenPHP.

## Docker Images

Official images are available at:

- **Docker Hub**: [`poweradmin/poweradmin`](https://hub.docker.com/r/poweradmin/poweradmin)
- **GitHub Container Registry**: [`ghcr.io/poweradmin/poweradmin`](https://github.com/poweradmin/poweradmin/pkgs/container/poweradmin)

### Image Tags

| Tag | Description |
|-----|-------------|
| `stable` | Stable release from `release/4.0.x` (recommended for production) |
| `next` | Upcoming release from `release/4.1.x` (stabilizing) |
| `latest` | Latest release from master branch |
| `lts` | Long-term support from `release/3.x` |
| `dev` | Development version (not for production) |
| `v*` | Specific version (e.g., `v4.0.0`, `v4.1.0`) |

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
| `PA_MFA_ENABLED` | false | Enable multi-factor authentication |
| `PA_RECAPTCHA_ENABLED` | false | Enable reCAPTCHA on login |

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

### Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LDAP_ENABLED` | false | Enable LDAP authentication |
| `PA_OIDC_ENABLED` | false | Enable OpenID Connect |
| `PA_SAML_ENABLED` | false | Enable SAML authentication |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LOGGING_TYPE` | null | Logger type: `null` or `native` |
| `PA_LOGGING_LEVEL` | info | Log level (debug, info, warning, error, etc.) |
| `PA_LOGGING_DATABASE_ENABLED` | false | Log zone/record changes to database |
| `PA_LOGGING_SYSLOG_ENABLED` | false | Log auth attempts to syslog |

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
