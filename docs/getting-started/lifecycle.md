# Version Support

This page shows how long each Poweradmin release line gets fixes, and when PHP, PowerDNS and the
common Linux distributions stop getting updates. Use it to plan upgrades. Platform dates come from
[php.net](https://www.php.net/supported-versions.php), the
[PowerDNS EOL page](https://doc.powerdns.com/authoritative/appendices/EOL.html) and
[endoflife.date](https://endoflife.date/). They were checked in October 2026 and move as projects
publish new plans.

## Which version should I use?

- **Production**: 4.4.x. It is the 4.x LTS line and gets fixes until December 2027. In Docker, pin
  a version tag such as `4.4`.
- **Newest features**: the latest release. It gets fixes until three months after the next minor
  release.
- **Still on 3.x**: 3.9.x is LTS until December 2027. Plan the move to 4.4.x before then.

## Poweradmin Release Lines

The rules:

- The newest release line gets bug and security fixes.
- When a new minor release ships, the previous line gets three more months of fixes, then reaches
  end of life.
- One 4.x line at a time is Long-Term Support (LTS). LTS lines get bug and security fixes first,
  and security fixes only later in the period.
- 3.9.x is the last 3.x line and is LTS until December 2027.

```mermaid
%%{init: {'themeCSS': 'text { font-family: var(--md-mermaid-font-family); } .tick text { font-size: 16px; }', 'gantt': {'fontSize': 18, 'sectionFontSize': 18, 'barHeight': 32, 'barGap': 8, 'leftPadding': 80}, 'themeVariables': {'critBkgColor': '#e07a7a', 'critBorderColor': '#c95f5f'}}}%%
gantt
    dateFormat YYYY-MM-DD
    axisFormat %b %Y
    tickInterval 6month
    todayMarker on

    section 3.x
    3.9.x LTS              :crit, 2025-01-14, 2027-12-31

    section 4.x
    4.0.x                  :done, 2025-07-31, 2026-07-23
    4.1.x                  :done, 2026-02-08, 2026-07-23
    4.2.x (end estimated)  :2026-03-19, 2027-01-31
    4.3.x (end estimated)  :2026-04-23, 2027-01-31
    4.4.x LTS              :crit, 2026-07-23, 2027-12-31
```

| Line          | Status                                         | Fixes until                     | PHP       |
|---------------|------------------------------------------------|---------------------------------|-----------|
| 4.5.x         | Next release (4.5.0)                           | three months after 4.6.0        | 8.2 - 8.5 |
| 4.4.x         | **LTS**, recommended for production            | December 2027                   | 8.2 - 8.5 |
| 4.3.x         | Last fixes only                                | three months after 4.5.0        | 8.2 - 8.5 |
| 4.2.x         | Last fixes only                                | three months after 4.5.0        | 8.2 - 8.5 |
| 4.1.x, 4.0.x  | End of life                                    | -                               | 8.1 - 8.5 |
| 3.9.x         | **LTS**                                        | December 2027                   | 8.1 - 8.5 |
| 3.8.x and older | End of life                                  | -                               | -         |

4.4.x is the last line with API v1, which 4.5.0 removes. For how to move between versions, see
[Upgrading](../upgrading/index.md).

## Platform Timeline

```mermaid
%%{init: {'themeCSS': 'text { font-family: var(--md-mermaid-font-family); } .tick text { font-size: 16px; }', 'gantt': {'fontSize': 18, 'sectionFontSize': 18, 'barHeight': 32, 'barGap': 8, 'leftPadding': 150}}}%%
gantt
    dateFormat YYYY-MM-DD
    axisFormat %Y
    todayMarker on

    section PHP
    8.2                  :2022-12-08, 2026-12-31
    8.3                  :2023-11-23, 2027-12-31
    8.4                  :2024-11-21, 2028-12-31
    8.5                  :2025-11-20, 2029-12-31

    section PowerDNS
    4.9 critical fixes   :2024-03-15, 2026-09-30
    5.0 critical fixes   :2025-08-22, 2027-03-31
    5.1                  :2026-06-03, 2028-01-31

    section Distributions
    Ubuntu 22.04 (PDNS 4.5)  :2022-04-21, 2027-06-01
    Debian 12 (PDNS 4.7)     :2023-06-10, 2028-06-30
    EL 8 (PDNS 4.8)          :2019-05-07, 2029-05-31
    Ubuntu 24.04 (PDNS 4.8)  :2024-04-25, 2029-05-31
    Debian 13 (PDNS 4.9)     :2025-08-09, 2030-06-30
    Ubuntu 26.04 (PDNS 5.0)  :2026-04-23, 2031-05-29
    EL 9 (PDNS 5.0)          :2022-05-18, 2032-05-31
    EL 10 (PDNS 5.0)         :2025-05-20, 2035-05-31
```

## PHP

Poweradmin follows the PHP release calendar. PHP versions that get security fixes are supported.
When a PHP version reaches end of life, the next Poweradmin minor release drops it. New PHP
versions are added to compatibility testing soon after their release.

| PHP | Security fixes until | Poweradmin                              |
|-----|----------------------|-----------------------------------------|
| 8.5 | 31 December 2029     | Supported                               |
| 8.4 | 31 December 2028     | Supported                               |
| 8.3 | 31 December 2027     | Supported                               |
| 8.2 | 31 December 2026     | Supported up to 4.6.x, dropped in 4.7.0 |
| 8.1 | 31 December 2025     | 3.9.x only                              |

## PowerDNS

| PowerDNS | Upstream status     | Updates until                            |
|----------|---------------------|------------------------------------------|
| 5.1      | Supported           | about January 2028                       |
| 5.0      | Critical fixes only | until 5.3 is released (about March 2027) |
| 4.9      | Critical fixes only | until 5.2 is released                    |
| 4.8      | End of life         | June 2026                                |
| 4.7      | End of life         | August 2025                              |

Poweradmin supports PowerDNS 4.x and 5.x and is tested from 4.5 onward. Many supported
distributions still ship 4.x, so Poweradmin keeps 4.x support while they do. Features that need a
newer PowerDNS are listed in
[System Requirements](requirements.md#features-that-need-a-newer-powerdns).

## Distributions

Versions are from each distribution's default repositories. "Supported until" is the end of the
normal or LTS security support, without paid extended support.

| Distribution              | Supported until | PHP                      | PowerDNS   |
|---------------------------|-----------------|--------------------------|------------|
| Debian 13 (Trixie)        | June 2030 (LTS) | 8.4                      | 4.9        |
| Debian 12 (Bookworm)      | June 2028 (LTS) | 8.2                      | 4.7        |
| Ubuntu 26.04 LTS          | May 2031        | 8.5                      | 5.0        |
| Ubuntu 24.04 LTS          | May 2029        | 8.3                      | 4.8        |
| Ubuntu 22.04 LTS          | June 2027       | 8.1                      | 4.5        |
| RHEL/Rocky/AlmaLinux 10   | May 2035        | 8.3                      | 5.0 (EPEL) |
| RHEL/Rocky/AlmaLinux 9    | May 2032        | 8.0 (8.2/8.3 as modules) | 5.0 (EPEL) |
| RHEL/Rocky/AlmaLinux 8    | May 2029        | 7.2 (8.2 as module)      | 4.8 (EPEL) |
| Fedora 44                 | June 2027       | 8.5                      | 5.0        |
| FreeBSD 15                | December 2029   | 8.4                      | 5.1        |

No longer supported by their vendors: Debian 11 (August 2026), Ubuntu 20.04 (May 2025) and
openSUSE Leap 15.6 (April 2026).

On Ubuntu, PowerDNS is in the `universe` component, which gets security fixes from the community
or through Ubuntu Pro rather than standard Canonical support.

If your distribution ships an older PHP or PowerDNS than you need:

- **PHP on Debian and Ubuntu**: [sury.org](https://deb.sury.org/) for Debian, the
  [ondrej/php PPA](https://launchpad.net/~ondrej/+archive/ubuntu/php) for Ubuntu.
- **PHP on RHEL-based systems**: enable a newer module stream with
  `dnf module reset php && dnf module enable php:8.2` (or `php:8.3` on EL 9), or use
  [Remi](https://rpms.remirepo.net/).
- **PowerDNS**: the official [PowerDNS repositories](https://repo.powerdns.com/) provide 5.1 for
  Debian 11-13, Ubuntu 22.04-26.04 and EL 8-10.
- **Docker**: the Poweradmin image ships its own PHP, and PowerDNS publishes official images.

## What to Plan For

- **About three months after 4.5.0**: 4.2.x and 4.3.x reach end of life. Move to 4.4.x or newer.
- **End of 2026**: PHP 8.2 reaches end of life. Poweradmin 4.7.0 needs PHP 8.3. This affects
  Debian 12 and RHEL 8 users on PHP 8.2.
- **June 2027**: Ubuntu 22.04 standard support ends. It is the last supported distribution that
  ships PowerDNS older than 4.7.
- **December 2027**: 4.4.x and 3.9.x LTS end, and PHP 8.3 reaches end of life.
- **June 2028**: Debian 12 LTS ends. After that, every supported major distribution ships
  PowerDNS 4.8 or newer.
