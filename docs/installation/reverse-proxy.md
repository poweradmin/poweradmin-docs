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

### Two or more proxies *(v4.5.0+)*

Each proxy appends the address it received the request from to `X-Forwarded-For`, so behind two
proxies the header reads `client, proxy1`. Poweradmin reads the header from the right and skips only
the addresses listed in `security.trusted_proxies`; the first address it does not know is logged as
the client. `X-Forwarded-For` is read before `X-Real-IP`, so a correct `X-Real-IP` from the outer
proxy does not change the result. The proxy that connects to Poweradmin is trusted automatically when its address is
private, but the proxies further out appear only inside the header and must be listed.

For example, with `client 10.10.10.10 -> proxy1 10.20.20.20 -> proxy2 -> Poweradmin`, set
`TRUSTED_PROXIES=private_ranges,10.20.20.20` in Docker (keep `private_ranges` so Caddy still
resolves the address for its own access log), or `'trusted_proxies' => ['10.20.20.20']` under
`security` in `config/settings.php`. Without it the logs show 10.20.20.20. `private_ranges` does
not help here, because it applies to Caddy only.

Reading from the right is deliberate: the leftmost address can be set by the client, so trusting it
would let anyone choose the address shown in audit logs and counted for login rate limits.

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

## Framing and Response Headers *(v4.6.0+)*

Every response from Poweradmin carries these headers:

| Header | Value |
|---|---|
| `X-Frame-Options` | `DENY` |
| `Content-Security-Policy` | `frame-ancestors 'none'; object-src 'none'; base-uri 'self'` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `same-origin` |

Poweradmin cannot be shown inside a frame by default. To embed it in a portal or dashboard, list
the origins that may do so in `config/settings.php`:

```php
'interface' => [
    'frame_ancestors' => ['https://portal.example.com', 'https://*.example.net'],
],
```

`object-src 'none'` blocks plugin content, which Poweradmin does not use, and `base-uri 'self'` stops an
injected `<base>` tag from redirecting relative script and form URLs.

With origins set, the policy becomes `frame-ancestors 'self' https://portal.example.com ...; object-src 'none'; base-uri 'self'` and
`X-Frame-Options` is no longer sent, because it cannot name several origins. The default is an empty list,
which denies all framing. Entries must be an `http://` or `https://` origin with no path;
`https://*.example.com` allows every subdomain. Origins are lowercased, and an invalid entry is
dropped and logged as a warning.

The headers come from the application, so a proxy that passes requests through needs nothing extra. Files
that the web server serves itself, such as CSS and images, bypass the application. The
`nginx.conf.example` and `caddy.conf.example` shipped with Poweradmin add the same four headers
to those files:

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    add_header X-Frame-Options "DENY" always;
    add_header Content-Security-Policy "frame-ancestors 'none'" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "same-origin" always;
}
```

If you allow framing, change or drop the two framing headers in that block to match.

> **Note:** The application already sets these headers on dynamic pages. A header added again at the
> proxy for the same pages can contradict `interface.frame_ancestors`, so leave them to the application.

### HSTS

Poweradmin does not send `Strict-Transport-Security`, because only the server that terminates TLS knows
that every request arrives over HTTPS. Set it there once HTTPS works for all users, starting with a short
`max-age` and raising it when nothing breaks.

```nginx
add_header Strict-Transport-Security "max-age=31536000" always;
```

```caddy
header Strict-Transport-Security "max-age=31536000"
```

```apache
Header always set Strict-Transport-Security "max-age=31536000"
```

Add `includeSubDomains` only when every subdomain of the host is served over HTTPS.

## Health endpoints *(v4.5.0+)*

If you enable the health endpoints, restrict them at the proxy. They answer without a
session and without an API key, so anyone who can reach the path can call them.

```nginx
location ~ ^/(ping|api/health)$ {
    allow 10.0.0.0/8;
    deny all;
    try_files $uri /index.php$is_args$args;
}
```

```apache
<LocationMatch "^/(ping|api/health)$">
    Require ip 10.0.0.0/8
</LocationMatch>
```

See [Health Checks](../operations/health-checks.md).
