# Overview

Poweradmin is a web-based administration tool for the PowerDNS authoritative server. It manages
forward and reverse zones, records, DNSSEC, users and permissions, either against the PowerDNS
database directly or through the PowerDNS API.

![Poweradmin Dashboard](../screenshots/dashboard.png)

## What it does

- Zone and record management for forward and reverse zones, with templates, bulk operations and
  BIND zone file import and export
- DNSSEC key management, DS and DNSKEY display, and per-zone serial policy
- Users, groups and a permission template system, with LDAP, OIDC and SAML single sign-on
- A REST API with scoped API keys, so zones can be driven from scripts and automation
- Audit logging of zone, record, user and API activity

The [Features](features.md) page lists these in full, with the release each one arrived in.

## Quick evaluation

Two ways to try Poweradmin without committing to an installation:

- [Docker Demo](docker-demo.md) brings up a complete environment with FrankenPHP and SQLite in a
  single command. Start here if you want to click around the interface.
- [Headless / API-First Quickstart](headless-quickstart.md) sets up an instance driven entirely
  through the API. Start here if you plan to manage DNS from scripts or CI.

## Before you install

Poweradmin needs PHP 8.2 or newer, one of MySQL/MariaDB, PostgreSQL or SQLite, and PowerDNS
Authoritative Server 4.0.0 or newer. From version 4.1.0 the web server must also rewrite all
requests to `index.php`, because Poweradmin uses clean URLs.

[System Requirements](requirements.md) has the full list, including PHP extensions, the supported
distributions and their default PHP versions, the tested software combinations and PowerDNS version
notes.

## Installing

Once the requirements are met, the [Installation](../installation/index.md) section covers the
options: Docker, the distribution guides for Debian, Ubuntu and CentOS/RHEL, the web installer
wizard, manual installation and Composer.

Upgrading from an existing installation instead? See [Upgrading](../upgrading/index.md), and
[What's New](../whats-new/index.md) for what each 4.x release added.
