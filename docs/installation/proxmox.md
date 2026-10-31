# Proxmox VE

The [Proxmox VE community scripts](https://community-scripts.github.io/ProxmoxVE/) project has a helper script that creates an LXC container with PowerDNS and Poweradmin already set up. The script is listed as **PowerDNS**, so searching the catalog for "poweradmin" finds nothing.

This script is maintained by the community-scripts project, not by the Poweradmin team. Report problems with the script itself to [community-scripts/ProxmoxVE](https://github.com/community-scripts/ProxmoxVE).

## What it installs

- A Debian 13 container (1 CPU, 1 GB RAM, 4 GB disk by default)
- PowerDNS Authoritative 5.0 from the PowerDNS repository, with the SQLite backend
- The latest Poweradmin release in `/opt/poweradmin`, served by Apache on port 80
- One SQLite database at `/var/lib/powerdns/powerdns.db`, shared by PowerDNS and Poweradmin
- An `admin` user with a random password

## Install

Run this in the Proxmox VE host shell:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/powerdns.sh)"
```

When it finishes, the script prints the container address. Open `http://<container-ip>` and log in as `admin`. The password is in `~/poweradmin.creds` inside the container:

```bash
cat ~/poweradmin.creds
```

## After installing

The script writes a minimal `/opt/poweradmin/config/settings.php`. Before you add real zones, change at least:

- `dns.hostmaster`, `dns.ns1` and `dns.ns2` - the script sets placeholder values (`localhost.lan`, `8.8.8.8`, `9.9.9.9`) that end up in the SOA and NS records of every new zone
- The admin email address and password, under **Users**

See [Basic Configuration](../configuration/basic.md) for the other settings. The site is plain HTTP, so put it behind a [reverse proxy](reverse-proxy.md) with TLS if anyone reaches it over an untrusted network.

## Update

Run the same command from the container's console (or type `update` there). It upgrades the PowerDNS packages and, when a new Poweradmin release is out, replaces `/opt/poweradmin` with it and keeps `config/settings.php`.

Containers created before 14 August 2026 kept the database at `/opt/poweradmin/powerdns.db`, inside the web root. The update moves it to `/var/lib/powerdns/powerdns.db` and fixes both config files, so run an update on any older container.
