# Project history

Poweradmin has been developed as an open source web interface for PowerDNS for more than two decades. This page gives a short overview of how the project got to where it is today.

## Origins

Poweradmin was started around 2002 by **Roeland Nieuwenhuis** and the PowerAdmin Team, with the project site at poweradmin.sjeemz.nl; the poweradmin.org domain was also registered in 2002. The 1.x releases were developed in CVS; the change log carried into today's repository runs from October 2002 to the 1.2.4 work in May 2003, and the code targeted PHP 4 and PowerDNS 2.x.

In April 2007 **Rejo Zenger** imported the 1.2.7 code into Subversion, which is where the history in today's repository begins. The 1.3 and 1.4 work followed that year and the 2.0.0 release in 2008. For many years the project website at poweradmin.org, the Trac issue tracker, the Subversion repository and the mailing lists were hosted by him.

## The 2.1.x releases (2008-2014)

The 2.1 series was developed over several years by a small group of volunteers, with **Scott Harvanek** acting as co-maintainer and release manager for part of that time.

- **2.1.5** was released in December 2010. It introduced linked zone templates, which required the template tables to use InnoDB so that changes could be applied in transactions.
- **2.1.6** followed in 2012. Its main changes were automatic PTR record creation for A and AAAA records, a PDO-based database layer replacing PEAR MDB2, bulk zone registration, salted password hashes, experimental SQLite and Oracle support, syslog logging of authentication events, new Chinese, Czech and Turkish translations, and XSS protection.
- **2.1.7** was released in 2014 and added a DNSSEC key management page.

No releases followed for more than seven years. Development did not stop: fixes and contributions kept arriving, most of them between 2015 and 2017, and were released in 2.1.8 in January 2022.

## Move to GitHub (2011)

In 2011 the project infrastructure was gradually moved away from a single server. Development moved from Subversion and Trac to Git and GitHub, the full Subversion history was imported, and the mailing list moved to Google Groups. Issues have been tracked on GitHub since then.

## Change of maintainer (2011)

In late 2011 **Edmondas Girkantas**, who had been committing since June 2010 and had become the most active developer, took over as project lead, with the agreement of the previous maintainers. He has maintained the project since.

## Later milestones

- **January 2022**: development picked up again with 2.1.8, followed by 2.1.9 and 2.2.0.
- **September 2022**: **3.0.0**, a restructured codebase with a new configuration format.
- **January 2025**: **3.9.0**, the last 3.x line, later made long-term support.
- **July 2025**: **4.0.0**, with the public REST API and multi-factor authentication.
- **February 2026**: **4.1.0**, with SAML and OpenID Connect single sign-on and API v2.
- **July 2026**: **4.4.0**, which adapts to the PowerDNS server behind it and is the 4.x long-term support line.
- **October 2026**: **4.5.0**, with a structured record change log and scoped API keys.

Activity grew with each step: about 370 commits a year in 2023 and 2024, more than 1,400 in 2025 and more than 4,000 in 2026.

See [What's New](../whats-new/index.md) for details of recent releases.

## Thanks

Many people have contributed code, testing, translations and infrastructure over the years. From the early years, thanks go in particular to Roeland Nieuwenhuis and the original PowerAdmin Team, [Rejo Zenger](https://github.com/rejozenger), [Scott Harvanek](https://github.com/mgob), [Peter Beernink](https://github.com/pbeernink), Okky Octaviano and [Fabian Dammekens](https://github.com/fdammeke).

The 2.x releases gained a lot from outside contributions: [Arsen Stasic](https://github.com/stasic) (DNSSEC and automatic PTR records), [Alex Fisher](https://github.com/alexjfisher) (LDAP authentication and logging), [Keenan Tims](https://github.com/ktims) (rectify-zone handling), [Josh Soref](https://github.com/jsoref) (record validation and spelling fixes), [Jeroen Boonstra](https://github.com/JeroenBo) (the Vagrant development VM), [Shin Sterneck](https://github.com/shinsterneck) (LUA records), [DecentM](https://github.com/DecentM) (the modern theme), [jAHu](https://github.com/j4Hu) (PHP 7.3 and OpenSSL support), [Max Base](https://github.com/BaseMax) (PHP 8 fixes), and [bynicolas](https://github.com/bynicolas) and [Lennie](https://github.com/Lennie) (DNSSEC fixes).

In the 3.x and 4.x series, thanks go to [b1tw0rker](https://github.com/b1tw0rker) (the basis of the spark dark theme), [benchea dan](https://github.com/bnchdan) (dashboard and navigation redesign), [Muckl](https://github.com/muckl) (German translation, mail and UI fixes), [Michiel Visser](https://github.com/michielvisser) (extensive testing and bug reports during the 4.x work) and [Patrick Omland](https://github.com/pomland-94) (DNSSEC key management and other API v2 work).

Thanks as well to the security researchers who reported vulnerabilities responsibly; they are credited in the [published security advisories](https://github.com/poweradmin/poweradmin/security/advisories).

Thanks also to everyone who reported bugs, sent patches, translated Poweradmin and helped other users on the mailing lists, GitHub issues and discussions.
