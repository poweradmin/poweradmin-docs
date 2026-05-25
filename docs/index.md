# Poweradmin Documentation

Welcome to the official documentation for Poweradmin, an administration tool for PowerDNS that can be driven through a web UI, a REST API, or both at the same time.

## Overview

Poweradmin manages PowerDNS zones and records with the same validation rules whether you go through the web interface or the REST API. Use the UI for day-to-day operations, the API for scripts, CI, and infrastructure-as-code, or run completely headless after the initial setup.

## Features

- **User Management**: Manage users and roles with different permissions
- **DNS Management**: Create, update, and delete DNS zones and records
- **Templates**: Use templates for bulk operations
- **Dynamic DNS**: Configure and manage dynamic DNS settings
- **Security**: Implement best practices for securing your DNS infrastructure
- **Logging and Monitoring**: Configure logging and monitor your DNS setup
- **API**: Access and manage your DNS data programmatically using the Poweradmin API

## Quick Start Guide

Pick the path that matches how you want to use Poweradmin:

- **Web UI**: [Docker Demo](getting-started/docker-demo.md) - one container, log in, manage zones in the browser
- **Headless / API-first**: [Headless Quickstart](getting-started/headless-quickstart.md) - bring the API up and drive PowerDNS from scripts in about five minutes
- **Production install**: [Installation Overview](installation/index.md) - Docker, Debian, Ubuntu, CentOS, or manual setups
- **Configuration**: [Basic Configuration](configuration/basic.md) - all settings explained
- **User Management**: [Users and Roles](user-guide/users-roles.md) - users, groups, permissions, MFA

## Documentation Sections

- **[Getting Started](getting-started/overview.md)**: System requirements and feature overview
- **[Installation](installation/index.md)**: Detailed installation guides for different environments
- **[Configuration](configuration/basic.md)**: All configuration options and settings
- **[User Guide](user-guide/users-roles.md)**: Practical usage instructions
- **[Advanced Topics](advanced/logging-config.md)**: Detailed technical information
- **[Upgrading](upgrading/index.md)**: Version-specific upgrade guides
- **[Troubleshooting](troubleshooting/debugging.md)**: Solutions for common issues
- **[Contributing](contributing/development.md)**: How to contribute to the project

## Get Involved

Poweradmin is an independently funded open-source project. Your support helps keep the project alive and growing.

- [GitHub Repository](https://github.com/poweradmin/poweradmin) - source code and releases
- [Issue Tracker](https://github.com/poweradmin/poweradmin/issues) - bug reports and feature requests
- [Discussions](https://github.com/poweradmin/poweradmin/discussions) - community support and ideas

### Support the Project

If you find Poweradmin valuable, consider supporting its development:

- [GitHub Sponsors](https://github.com/sponsors/edmondas)
- [Open Collective](https://opencollective.com/poweradmin)
- [PayPal](https://paypal.me/egirkantas)

Thanks to everyone who has contributed over the years!

## License and Disclaimer

Poweradmin is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).

This project is not associated with [PowerDNS.com](https://www.powerdns.com/index.html), [Open-Xchange](https://www.open-xchange.com), or any other external parties. It is independently funded and maintained.

Thank you for using Poweradmin!