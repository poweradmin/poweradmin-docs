# What's New

This section covers what each 4.x release added, so you can see what you gain by upgrading
and find the feature you half-remember reading about. For the mechanics of upgrading -
migration scripts, breaking changes, step-by-step instructions - see
[Upgrading](../upgrading/index.md).

> **Note:** Screenshots throughout this section come from the current release. A feature
> introduced in an earlier version is shown as it looks today, not as it looked when it
> shipped.

## The 4.x releases at a glance

| Release | Date | Theme | Headline features |
|---------|------|-------|-------------------|
| [v4.5.0](v4.5.0.md) | unreleased | Change tracking and finer-grained access | Record change log, granular API keys, serial policies, ten new permissions, API v1 removed |
| [v4.4.0](v4.4.0.md) | July 2026 | The interface adapts to your server | PowerDNS version awareness, views and networks, DNSSEC key import/export, zone ownership modes |
| [v4.3.0](v4.3.0.md) | April 2026 | API backend, metadata, audit | PowerDNS API backend mode, zone metadata editor, audit logging overhaul |
| [v4.2.0](v4.2.0.md) | March 2026 | Groups and modules | User groups, group-based zone ownership, the module system, BIND zone import/export |
| [v4.1.0](v4.1.0.md) | February 2026 | Identity and URLs | SAML and OIDC single sign-on, clean URLs, DNS record wizards, API v2 |
| [v4.0.0](v4.0.0.md) | July 2025 | The rewrite | New configuration system, REST API, MFA, bulk operations, WHOIS and RDAP |

## Coming from 3.x

Version 4.0.0 was a rewrite rather than an increment. The configuration file moved from
`inc/config.inc.php` to `config/settings.php`, the codebase was restructured, and a large
amount of functionality arrived that 3.x never had: an API, multi-factor authentication,
bulk record operations, themes, and a guided installer.

[What's New in 4.0.0](v4.0.0.md) covers the feature side. The
[4.0.0 upgrade guide](../upgrading/v4.0.0.md) covers the migration itself, which needs
attention - do not treat it as a drop-in replacement.

The 3.x line is still maintained for security and bug fixes. It receives no new features.

## Reading the release pages

Each page has the same shape:

- **Highlights** - the handful of features that define the release, with links to the full
  documentation for each.
- **Also in this release** - everything else worth knowing about, in a table.
- **Patch releases** - what the follow-up releases in that line added.

Features are documented in the main sections of this site, not here. The release pages tell
you when something arrived and point you at the page that explains it.
