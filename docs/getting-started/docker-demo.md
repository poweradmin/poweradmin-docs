# Docker Demo

The easiest way to evaluate Poweradmin is to use the Docker image, which provides a complete environment with FrankenPHP and SQLite database.

## Quick Demo

### 1. Get the Docker Image
```bash
docker pull poweradmin/poweradmin:latest
```

### 2. Run the Container
```bash
docker run -d --name poweradmin -p 80:80 poweradmin/poweradmin:latest
```

### 3. Access Poweradmin
- Open your browser and go to [http://localhost](http://localhost)
- Username: `admin`
- Password: `testadmin`

> **Note**: This demo uses SQLite with pre-configured test data.

## Architecture

The Docker image is based on [FrankenPHP](https://frankenphp.dev/), providing:

- **High Performance**: Persistent worker mode for better performance
- **Modern HTTP**: Native HTTP/2 and HTTP/3 support
- **Built-in Features**: Automatic HTTPS, real-time capabilities
- **Caddy Integration**: Built on Caddy web server

## Demo with External Database

### MySQL Demo
```bash
docker run -d --name poweradmin -p 80:80 \
  -e DB_TYPE=mysql \
  -e DB_HOST=your-mysql-host \
  -e DB_USER=poweradmin \
  -e DB_PASS=password \
  -e DB_NAME=poweradmin \
  -e DNS_NS1=ns1.yourdomain.com \
  -e DNS_NS2=ns2.yourdomain.com \
  -e DNS_HOSTMASTER=hostmaster.yourdomain.com \
  poweradmin/poweradmin:latest
```

### PostgreSQL Demo
```bash
docker run -d --name poweradmin -p 80:80 \
  -e DB_TYPE=pgsql \
  -e DB_HOST=your-postgres-host \
  -e DB_USER=poweradmin \
  -e DB_PASS=password \
  -e DB_NAME=poweradmin \
  -e DNS_NS1=ns1.yourdomain.com \
  -e DNS_NS2=ns2.yourdomain.com \
  -e DNS_HOSTMASTER=hostmaster.yourdomain.com \
  poweradmin/poweradmin:latest
```

## Demo with Docker Compose

### Basic Demo
```yaml
version: '3.8'
services:
  poweradmin:
    image: poweradmin/poweradmin:latest
    ports:
      - "80:80"
```

### Complete Demo with MySQL
```yaml
version: '3.8'
services:
  poweradmin:
    image: poweradmin/poweradmin:latest
    ports:
      - "80:80"
    environment:
      - DB_TYPE=mysql
      - DB_HOST=mysql
      - DB_USER=poweradmin
      - DB_PASS=password
      - DB_NAME=poweradmin
      - DNS_NS1=ns1.yourdomain.com
      - DNS_NS2=ns2.yourdomain.com
      - DNS_HOSTMASTER=hostmaster.yourdomain.com
      - PA_API_ENABLED=true
      - PA_API_DOCS_ENABLED=true
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=poweradmin
      - MYSQL_USER=poweradmin
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## Building from Source

If you want to build the Docker image from source:

```bash
# Clone the repository
git clone https://github.com/poweradmin/poweradmin.git
cd poweradmin

# Build the image
docker build --no-cache -t poweradmin .

# Run the container
docker run -d --name poweradmin -p 80:80 poweradmin
```

## Environment Variables (Demo Examples)

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_TYPE` | Database type | `sqlite`, `mysql`, `pgsql` |
| `PA_API_ENABLED` | Enable API | `true` |
| `PA_API_DOCS_ENABLED` | Enable API docs | `true` |
| `PA_APP_TITLE` | Application title | `My DNS Demo` |
| `PA_MAIL_ENABLED` | Enable email | `false` |

## API Demo

Enable the API to test RESTful endpoints:

```bash
docker run -d --name poweradmin -p 80:80 \
  -e PA_API_ENABLED=true \
  -e PA_API_DOCS_ENABLED=true \
  poweradmin/poweradmin:latest
```

Visit [http://localhost/api/docs](http://localhost/api/docs) to explore the API documentation.

## Next Steps

After evaluating the demo:

1. **Production Deployment**: See [Docker Deployment Guide](../deployment/docker.md) for production configurations
2. **Manual Installation**: Follow [Manual Installation](../installation/manual.md) for traditional setups
3. **Configuration**: Learn about [Configuration Options](../configuration/basic.md)

## Troubleshooting

- **Port conflicts**: Use `-p 8080:80` if port 80 is in use
- **View logs**: `docker logs poweradmin`
- **Container access**: `docker exec -it poweradmin /bin/sh`