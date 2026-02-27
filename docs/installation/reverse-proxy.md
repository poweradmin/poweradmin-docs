# Reverse Proxy Configuration

Poweradmin works behind reverse proxies with no special configuration required. The Docker image uses FrankenPHP (Caddy-based) which handles URL routing internally.

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
