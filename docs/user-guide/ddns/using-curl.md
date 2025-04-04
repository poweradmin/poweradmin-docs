# Using cURL for Dynamic DNS Updates

cURL is a versatile command-line tool that can be used to update DNS records in Poweradmin. Here are various examples of using cURL with the Dynamic DNS update system.

## Basic Update Examples

### Update IPv4 Address

```bash
curl -u username:password "https://dns.example.com/dynamic_update.php?hostname=host.example.com&myip=192.0.2.1"
```

### Automatic IP Detection

```bash
curl -u username:password "https://dns.example.com/dynamic_update.php?hostname=host.example.com&myip=whatismyip"
```

### Update IPv6 Address

```bash
curl -u username:password "https://dns.example.com/dynamic_update.php?hostname=host.example.com&myip6=2001:db8::1"
```

## Advanced Usage

### Combined Multiple IPv4 and IPv6 Update

```bash
# Update multiple A records and single AAAA record in one request
curl -u user:pass "https://yourhost/dynamic_update.php?hostname=host.example.com&myip=1.2.3.4,5.6.7.8&myip6=2001:db8::1&dualstack_update=1"
```

### Dual-Stack Update

```bash
curl -u username:password "https://dns.example.com/dynamic_update.php?hostname=host.example.com&myip=192.0.2.1&myip6=2001:db8::1&dualstack_update=1"
```

### Multiple IP Addresses

```bash
curl -u username:password "https://dns.example.com/dynamic_update.php?hostname=host.example.com&myip=192.0.2.1,192.0.2.2"
```

### Using URL Parameters Instead of Basic Auth

```bash
curl "https://dns.example.com/dynamic_update.php?username=user&password=pass&hostname=host.example.com&myip=192.0.2.1"
```

## Scripting Examples

### Basic Update Script

```bash
#!/bin/bash
USERNAME="your_username"
PASSWORD="your_password"
HOSTNAME="your.hostname.com"
SERVER="https://dns.example.com/dynamic_update.php"

curl -s -u "$USERNAME:$PASSWORD" "$SERVER?hostname=$HOSTNAME&myip=whatismyip"
```

### Periodic Update Script

```bash
#!/bin/bash
USERNAME="your_username"
PASSWORD="your_password"
HOSTNAME="your.hostname.com"
SERVER="https://dns.example.com/dynamic_update.php"
INTERVAL=300  # Update every 5 minutes

while true; do
    curl -s -u "$USERNAME:$PASSWORD" "$SERVER?hostname=$HOSTNAME&myip=whatismyip"
    sleep $INTERVAL
done
```

## Error Handling

The update script returns HTTP status codes and messages that can be captured:

```bash
response=$(curl -s -w "%{http_code}" -u "$USERNAME:$PASSWORD" "$SERVER?hostname=$HOSTNAME&myip=whatismyip")
if [ $response -eq 200 ]; then
    echo "Update successful"
else
    echo "Update failed with code: $response"
fi
```

## Security Considerations

- Always use HTTPS to protect credentials
- Consider using Basic Authentication instead of URL parameters
- Store credentials securely, not in plain text
- Use specific IP ranges if possible
- Monitor for unusual update patterns
