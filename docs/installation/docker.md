# Docker Installation

Poweradmin provides official Docker images for easy deployment with FrankenPHP.

## Docker Images

Official images are available at:

- **Docker Hub**: [`poweradmin/poweradmin`](https://hub.docker.com/r/poweradmin/poweradmin)
- **GitHub Container Registry**: [`ghcr.io/poweradmin/poweradmin`](https://github.com/poweradmin/poweradmin/pkgs/container/poweradmin)

### Image Tags

The image tags published for production and development use are:

| Tag      | Source branch        | Description |
|----------|----------------------|-------------|
| `stable` | `release/4.3.x`      | Tracks the latest tagged release on the stable line - **recommended for production**. |
| `4.3.x`  | `release/4.3.x`      | Stable line; updates on every commit to the branch (more frequent than `stable`). |
| `4.4`    | Version tags on `master` | Newest release line (4.4.0) - fresh, still hardening; no dedicated branch yet. |
| `4.2.x`  | `release/4.2.x`      | Maintenance line, winding down - security fixes only. |
| `latest` | `master`             | Tracks `master`, which carries the newest release line between patch releases. |
| `dev`    | `develop`            | Development tip - not for production. |
| `lts`    | `release/3.x`        | Long-term support for the 3.x series. |
| `v*`     | Tagged release       | Pin to a specific version (e.g. `v4.3.4`). |

> **Note:** The `next` tag was removed when the release branch structure changed. The `stable` and per-version (`v*`) tags are the safest choices for production; the branch tags (`4.2.x`, `4.3.x`) update on every push and may include unreleased fixes.

## Quick Start

### SQLite

```bash
docker run -d --name poweradmin -p 80:80 \
  -e DB_TYPE=sqlite \
  -e PA_CREATE_ADMIN=1 \
  -v poweradmin-db:/db \
  poweradmin/poweradmin:stable
```

> **Warning:** `DB_TYPE` is required. There is no default. A container started
> without it logs `ERROR: DB_TYPE environment variable is required` and exits
> immediately.

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

> **Note:** The `DB_NAME` database and the `DB_USER` (with privileges on it) must already exist - the container does not create them. With the official `mysql`/`postgres` images, set `MYSQL_DATABASE`/`MYSQL_USER`/`MYSQL_PASSWORD` (or `POSTGRES_DB`/`POSTGRES_USER`/`POSTGRES_PASSWORD`) so they are provisioned on first start. Setting only the root password leaves the server with no Poweradmin database or user and fails with `ERROR 1045 Access denied`.

On startup the container loads the Poweradmin schema into an empty `DB_NAME` database automatically; an already-populated database is left untouched. PowerDNS stores its own zones and records in a separate database that PowerDNS (not Poweradmin) creates and initializes. If you instead keep both in one shared database, set `PA_INIT_PDNS_SCHEMA=true` to have the container load the PowerDNS schema into an empty `DB_NAME` as well; it is off by default and skipped when `PA_PDNS_DB_NAME` is set.

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
    volumes:
      - ./pdns.conf:/etc/powerdns/pdns.conf:ro
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

The official `powerdns/pdns-auth-*` images do not read `PDNS_*` environment
variables — that convention belongs to third-party images, and the official
image silently ignores them (see
[PowerDNS/pdns#14951](https://github.com/PowerDNS/pdns/issues/14951)). The only
configuration variable it honors is `PDNS_AUTH_API_KEY`; everything else has to
come from a config file or command-line arguments. The example above mounts a
`pdns.conf` next to the compose file:

```ini
launch=gmysql
gmysql-host=mysql
gmysql-user=pdns
gmysql-password=pdns-password
gmysql-dbname=pdns

api=yes
api-key=your-api-key
webserver=yes
webserver-address=0.0.0.0
webserver-allow-from=0.0.0.0/0
```

The example also relies on `./init.sql` to prepare MySQL on first startup: it
must create both databases and users, and load the PowerDNS schema into the
`pdns` database. Start with:

```sql
CREATE DATABASE poweradmin;
CREATE USER 'poweradmin'@'%' IDENTIFIED BY 'poweradmin-password';
GRANT ALL PRIVILEGES ON poweradmin.* TO 'poweradmin'@'%';

CREATE DATABASE pdns;
CREATE USER 'pdns'@'%' IDENTIFIED BY 'pdns-password';
GRANT ALL PRIVILEGES ON pdns.* TO 'pdns'@'%';

-- Poweradmin manages zones in the PowerDNS database (PA_PDNS_DB_NAME)
GRANT ALL PRIVILEGES ON pdns.* TO 'poweradmin'@'%';

USE pdns;
```

then append the [official PowerDNS MySQL schema](https://doc.powerdns.com/authoritative/backends/generic-mysql.html#default-schema)
matching your PowerDNS version:

```bash
curl https://raw.githubusercontent.com/PowerDNS/pdns/rel/auth-5.1.x/modules/gmysqlbackend/schema.mysql.sql >> init.sql
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

This page covers the variables you need to stand a deployment up and secure it. It
is deliberately a subset: the container accepts roughly 330 variables, and the
complete reference, versioned alongside the code, is
[DOCKER.md](https://github.com/poweradmin/poweradmin/blob/master/DOCKER.md) in the
source repository. Check there for anything not listed below, especially the
interface, mail, DNS validation and per-provider OIDC and SAML settings.

Every variable here can also be supplied from a file by appending `__FILE` to its
name; see [Docker Secrets](docker-secrets.md).

> **Note:** These variables only take effect when the container generates its own
> configuration. If `config/settings.php` (or `PA_CONFIG_PATH`) exists and is not
> empty, that file is used and the variables below are ignored. See
> [Configuration Priority](docker-secrets.md#configuration-priority).

### Database

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_TYPE` | *(required)* | Database type: sqlite, mysql, pgsql. The container exits at startup if this is unset |
| `DB_HOST` | - | Database hostname |
| `DB_PORT` | - | Database port (3306 for MySQL, 5432 for PostgreSQL) |
| `DB_USER` | - | Database username |
| `DB_PASS` | - | Database password |
| `DB_NAME` | - | Database name |
| `PA_PDNS_DB_NAME` | - | Separate PowerDNS database (MySQL only) |
| `PA_INIT_PDNS_SCHEMA` | false | Load PowerDNS schema into an empty `DB_NAME` on startup (MySQL/PostgreSQL; skipped when `PA_PDNS_DB_NAME` is set) |

### DNS

| Variable | Default | Description |
|----------|---------|-------------|
| `DNS_NS1` | ns1.example.com | Primary nameserver |
| `DNS_NS2` | ns2.example.com | Secondary nameserver |
| `DNS_HOSTMASTER` | hostmaster.example.com | Hostmaster email |
| `PA_DNS_BACKEND` | sql | DNS data backend: `sql` (direct database) or `api` (PowerDNS REST API, v4.3.0+). See [PowerDNS API](../configuration/powerdns-api.md) |

### Security

#### Session and password hashing

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_SESSION_KEY` | (auto) | Session encryption key. Set this explicitly in production so sessions survive a container restart |
| `PA_PASSWORD_ENCRYPTION` | bcrypt | Password hashing: `bcrypt`, `argon2i`, `argon2id`. The legacy `md5` and `md5salt` options were removed in 4.3.0 |
| `PA_PASSWORD_COST` | 12 | Cost factor for bcrypt hashing |
| `PA_LOGIN_TOKEN_VALIDATION` | true | Enable CSRF token validation for login |
| `PA_GLOBAL_TOKEN_VALIDATION` | true | Enable CSRF token validation for all forms |

#### Password policy

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_PASSWORD_RULES_ENABLED` | true | Enable password policy enforcement |
| `PA_PASSWORD_MIN_LENGTH` | 6 | Minimum password length |
| `PA_PASSWORD_REQUIRE_UPPERCASE` | true | Require at least one uppercase letter |
| `PA_PASSWORD_REQUIRE_LOWERCASE` | true | Require at least one lowercase letter |
| `PA_PASSWORD_REQUIRE_NUMBERS` | true | Require at least one number |
| `PA_PASSWORD_REQUIRE_SPECIAL` | false | Require at least one special character |

See [Password Policies](../configuration/password-policies.md) for the full policy, including the allowed special-character set, which has no environment variable and must be set in `settings.php`.

#### Account lockout

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LOCKOUT_ENABLED` | false | Enable account lockout after failed logins |
| `PA_LOCKOUT_ATTEMPTS` | 5 | Failed attempts before lockout |
| `PA_LOCKOUT_DURATION` | 15 | Lockout duration in minutes |
| `PA_LOCKOUT_TRACK_IP` | true | Lock accounts based on IP address |
| `PA_LOCKOUT_CLEAR_ON_SUCCESS` | true | Clear failed attempts after a successful login |

The IP whitelist and blacklist have no environment variables; set them in `settings.php`. See [Security Policies](../configuration/security-policies.md).

#### Multi-factor authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_MFA_ENABLED` | false | Enable multi-factor authentication |
| `PA_MFA_ENFORCED` | false | Enforce MFA for users holding `user_enforce_mfa` |
| `PA_MFA_APP_ENABLED` | true | Offer the authenticator app method. Ignored while email verification is unusable, so the last remaining method stays available |
| `PA_MFA_EMAIL_ENABLED` | true | Offer the email verification method |
| `PA_MFA_RECOVERY_CODES` | 8 | Number of recovery codes generated |
| `PA_MFA_RECOVERY_CODE_LENGTH` | 10 | Length of each recovery code |
| `PA_MFA_SKIP_FOR_EXTERNAL_AUTH` | false | Skip enforcement for LDAP, OIDC and SAML logins, trusting the identity provider (v4.5.0+) |
| `PA_MFA_MAX_VERIFY_ATTEMPTS` | 5 | Failed second-factor guesses before the code is refused (v4.5.0+) |
| `PA_MFA_VERIFY_LOCKOUT_DURATION` | 15 | Minutes to refuse further attempts once the limit is hit (v4.5.0+) |

Email-based MFA needs a working mail configuration; see [Mail](../configuration/mail.md).

#### Password reset

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_PASSWORD_RESET_ENABLED` | false | Enable password reset functionality |
| `PA_PASSWORD_RESET_TOKEN_LIFETIME` | 3600 | Token validity in seconds |
| `PA_PASSWORD_RESET_RATE_LIMIT_ATTEMPTS` | 5 | Maximum reset attempts per time window |
| `PA_PASSWORD_RESET_RATE_LIMIT_WINDOW` | 3600 | Rate limit window in seconds |
| `PA_PASSWORD_RESET_MIN_TIME_BETWEEN` | 60 | Minimum seconds between requests |

#### Username recovery

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_USERNAME_RECOVERY_ENABLED` | false | Enable username recovery functionality |
| `PA_USERNAME_RECOVERY_RATE_LIMIT_ATTEMPTS` | 5 | Maximum recovery attempts per time window |
| `PA_USERNAME_RECOVERY_RATE_LIMIT_WINDOW` | 3600 | Rate limit window in seconds |
| `PA_USERNAME_RECOVERY_MIN_TIME_BETWEEN` | 60 | Minimum seconds between requests |

#### reCAPTCHA

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_RECAPTCHA_ENABLED` | false | Enable reCAPTCHA on login |
| `PA_RECAPTCHA_SITE_KEY` | *(empty)* | Site key (public) |
| `PA_RECAPTCHA_SECRET_KEY` | *(empty)* | Secret key (private) |
| `PA_RECAPTCHA_VERSION` | v3 | reCAPTCHA version: `v2` or `v3` |
| `PA_RECAPTCHA_V3_THRESHOLD` | 0.5 | Score threshold for v3, from 0.0 to 1.0 |

#### Proxies

| Variable | Default | Description |
|----------|---------|-------------|
| `TRUSTED_PROXIES` | - | Comma-separated proxy CIDRs, or `private_ranges`, allowed to set forwarded-IP headers. See [Reverse Proxy](reverse-proxy.md) |

Account lockout (with `PA_LOCKOUT_TRACK_IP`) and the reset and recovery rate limits all throttle by client IP as well as by account. Behind a proxy they need `TRUSTED_PROXIES` set, or every request appears to come from the proxy's address.

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
| `PA_MODULE_WHOIS_DEFAULT_SERVER` | *(empty)* | Default WHOIS server |
| `PA_MODULE_WHOIS_CUSTOM_SERVERS` | *(empty)* | Custom TLD-to-server mapping, e.g. `za=whois.registry.net.za` |
| `PA_MODULE_WHOIS_SOCKET_TIMEOUT` | 10 | WHOIS socket timeout in seconds |
| `PA_MODULE_RDAP_ENABLED` | false | Enable RDAP lookup module |
| `PA_MODULE_RDAP_RESTRICT_TO_ADMIN` | true | Restrict RDAP to administrators |
| `PA_MODULE_RDAP_DEFAULT_SERVER` | *(empty)* | Default RDAP server |
| `PA_MODULE_RDAP_CUSTOM_SERVERS` | *(empty)* | Custom TLD-to-server mapping, e.g. `za=https://rdap.example.com/` |
| `PA_MODULE_RDAP_REQUEST_TIMEOUT` | 10 | RDAP request timeout in seconds |
| `PA_MODULE_EMAIL_PREVIEWS_ENABLED` | false | Enable the email template previews module |
| `PA_MODULE_EMAIL_PREVIEWS_RESTRICT_TO_ADMIN` | true | Restrict email previews to administrators |
| `PA_MODULE_DNS_WIZARDS_ENABLED` | false | Enable the DNS record wizards module |
| `PA_MODULE_DNS_WIZARDS_TYPES` | DMARC,SPF,DKIM,CAA,TLSA,SRV | Comma-separated list of DNS wizard types |

This table covers every module variable the container accepts. Two module settings have no
environment variable and must be set in `settings.php`: `modules.secondary_zone_import.enabled`
and the `modules.dns_wizards.caa_providers` list.

For detailed module configuration, see the [Configuration](../configuration/zone-import-export.md) section.

### Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LDAP_ENABLED` | false | Enable LDAP authentication |
| `PA_LDAP_URI` | *(empty)* | LDAP server URI, e.g. `ldaps://ldap.example.com:636` |
| `PA_LDAP_BASE_DN` | *(empty)* | Base DN where users are stored |
| `PA_LDAP_BIND_DN` | *(empty)* | Bind DN used to search the directory |
| `PA_LDAP_BIND_PASSWORD` | *(empty)* | Password for the bind DN |
| `PA_LDAP_SEARCH_FILTER` | *(empty)* | Additional LDAP search filter |
| `PA_LDAP_PROTOCOL_VERSION` | 3 | LDAP protocol version |
| `PA_LDAP_USER_ATTRIBUTE` | uid | User attribute (`uid` for OpenLDAP, `sAMAccountName` for AD) |
| `PA_LDAP_SYNC_USER_INFO` | false | Sync fullname/email from LDAP on login (v4.5.0+) |
| `PA_LDAP_AUTO_PROVISION` | false | Create missing users on first LDAP login (v4.5.0+) |
| `PA_LDAP_PERMISSION_TEMPLATE_MAPPING` | - | LDAP group to permission template mapping, `group:Template` comma-separated (v4.5.0+) |
| `PA_LDAP_GROUP_MAPPING` | - | LDAP group to Poweradmin group mapping, `group:PAGroup` comma-separated (v4.5.0+) |
| `PA_OIDC_ENABLED` | false | Enable OpenID Connect |
| `PA_SAML_ENABLED` | false | Enable SAML authentication |

The LDAP rows above are enough for a working LDAP setup. OIDC and SAML are not - each provider
needs its own block of variables (`PA_OIDC_AZURE_*`, `PA_SAML_OKTA_*` and so on), and there are
137 authentication variables in total across LDAP, OIDC and SAML. They are listed in
[DOCKER.md](https://github.com/poweradmin/poweradmin/blob/master/DOCKER.md); the settings behind
them are explained in [OIDC](../configuration/oidc.md) and [SAML](../configuration/saml.md).

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

### Interface and miscellaneous

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_CONFIG_PATH` | /app/config/settings.php | Path to the configuration file. When this file exists and is not empty it replaces the generated one, and the other `PA_*` variables are ignored |
| `PA_APP_TITLE` | Poweradmin | Application title |
| `PA_DEFAULT_LANGUAGE` | en_EN | Default language |
| `PA_STYLE` | light | UI style: light or dark |
| `PA_SESSION_TIMEOUT` | 1800 | Session timeout in seconds |
| `PA_TIMEZONE` | UTC | Default timezone |
| `PA_EDIT_CONFLICT_RESOLUTION` | last_writer_wins | Edit conflict resolution strategy |
| `PA_DNS_CUSTOM_TLDS` | - | Comma-separated custom TLDs (e.g., `dn42,home`) |

The interface has many more settings than the four above; see
[UI Overview](../configuration/ui/overview.md) for what is available and
`DOCKER.md` for their variables.

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `PA_LOGGING_TYPE` | null | Logger type: `null` or `native` |
| `PA_LOGGING_LEVEL` | info | Log level: `debug`, `info`, `notice`, `warning`, `error`, `critical`, `alert`, `emergency` |
| `PA_LOGGING_DATABASE_ENABLED` | false | Log zone/record changes to database |
| `PA_LOGGING_SYSLOG_ENABLED` | false | Log auth attempts to syslog |
| `PA_LOGGING_SYSLOG_IDENTITY` | poweradmin | Syslog program identity |
| `PA_LOGGING_SYSLOG_FACILITY` | LOG_USER | Syslog facility (`LOG_USER`, `LOG_LOCAL0`-`LOG_LOCAL7`) |

Anything not listed on this page is in
[DOCKER.md](https://github.com/poweradmin/poweradmin/blob/master/DOCKER.md), which
tracks the code and is tagged with each release.

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
