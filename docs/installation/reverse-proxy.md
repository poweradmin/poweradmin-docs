# Reverse Proxy Configuration

Poweradmin works behind reverse proxies with no special configuration required. The Docker image uses FrankenPHP (Caddy-based) which handles URL routing internally.

## Client IP Resolution

When running behind a reverse proxy, the container sees the proxy's IP address instead of the real client IP. This affects both access logs (`docker logs`) and application audit logs.

To fix this, set the `TRUSTED_PROXIES` environment variable so Caddy resolves the real client IP from proxy headers:

```yaml
services:
  poweradmin:
    image: poweradmin/poweradmin:stable
    environment:
      TRUSTED_PROXIES: private_ranges
```

The `private_ranges` value trusts all private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) and is recommended for most Docker deployments. For specific CIDRs, use a comma-separated list: `TRUSTED_PROXIES=172.17.0.0/16,10.0.0.0/8`.

Both `X-Forwarded-For` and `X-Real-IP` headers are supported. Your reverse proxy must forward at least one of these headers - see the examples below for proxy-specific configuration.

### Two trust layers (Docker)

`TRUSTED_PROXIES` configures two layers at once. The Docker image (4.5.0 and later) writes the same list to Poweradmin's `security.trusted_proxies` setting in addition to the Caddy server, so the application also honors forwarded headers from the listed proxies:

- **Caddy** resolves the real client IP for its own access logs.
- **The application** decides whether to trust forwarded headers for audit logs and per-IP rate limiting. By default it only trusts private/loopback peers, which is why a proxy on a **public** (non-RFC1918) address needs its IP listed here.

The `private_ranges` keyword applies to Caddy only; the application always trusts private/loopback peers. Set `PA_TRUSTED_PROXIES` if the application allowlist must differ from the Caddy list.

### Non-Docker installs

Outside Docker, set the application allowlist directly in `config/settings.php`. This is required when the proxy connects from a public address:

```php
'security' => [
    'trusted_proxies' => ['203.0.113.10', '2001:db8::/32'],
],
```

See [Security Policies](../configuration/security-policies.md) for details.

## Traefik

### Basic Setup (HTTP only)

```yaml
services:
  traefik:
    image: traefik:v3.3
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

  poweradmin:
    image: poweradmin/poweradmin:stable
    environment:
      PA_CREATE_ADMIN: "true"
      DB_TYPE: sqlite
    volumes:
      - poweradmin-db:/db
    labels:
      - traefik.enable=true
      - traefik.http.routers.poweradmin.entrypoints=web
      - traefik.http.routers.poweradmin.rule=Host(`poweradmin.example.com`)
      - traefik.http.services.poweradmin.loadbalancer.server.port=80

volumes:
  poweradmin-db:
```

### HTTPS with HTTP-to-HTTPS Redirect

When using HTTPS, you need two routers: one for the `websecure` entrypoint to serve traffic, and one for the `web` entrypoint to redirect HTTP to HTTPS.

```yaml
services:
  traefik:
    image: traefik:v3.3
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt

  poweradmin:
    image: poweradmin/poweradmin:stable
    environment:
      PA_CREATE_ADMIN: "true"
      DB_TYPE: sqlite
    volumes:
      - poweradmin-db:/db
    labels:
      - traefik.enable=true
      - traefik.http.middlewares.redirect-https.redirectScheme.scheme=https
      - traefik.http.middlewares.redirect-https.redirectScheme.permanent=true
      - traefik.http.routers.poweradmin_http.entrypoints=web
      - traefik.http.routers.poweradmin_http.rule=Host(`poweradmin.example.com`)
      - traefik.http.routers.poweradmin_http.middlewares=redirect-https
      - traefik.http.routers.poweradmin.entrypoints=websecure
      - traefik.http.routers.poweradmin.rule=Host(`poweradmin.example.com`)
      - traefik.http.routers.poweradmin.tls=true
      - traefik.http.routers.poweradmin.tls.certresolver=letsencrypt
      - traefik.http.services.poweradmin.loadbalancer.server.port=80

volumes:
  poweradmin-db:
  letsencrypt:
```

A common mistake is defining the `redirect-https` middleware without creating an HTTP router that uses it. Without the HTTP router (`poweradmin_http` above), requests on port 80 have no matching route and Traefik returns 404.

### Global HTTP-to-HTTPS Redirect

Instead of adding redirect labels to each service, you can configure a global redirect in Traefik's static configuration:

```yaml
services:
  traefik:
    command:
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
```

With this approach, you only need the `websecure` router on each service.

## Nginx

```nginx
server {
    listen 80;
    server_name poweradmin.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name poweradmin.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Caddy

```
poweradmin.example.com {
    reverse_proxy localhost:8080
}
```

Caddy automatically provisions TLS certificates via Let's Encrypt.

## Apache

```apache
<VirtualHost *:80>
    ServerName poweradmin.example.com
    Redirect permanent / https://poweradmin.example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName poweradmin.example.com

    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem

    ProxyPreserveHost On
    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/
</VirtualHost>
```

Requires `mod_proxy`, `mod_proxy_http`, and `mod_ssl` modules.
