# Upgrading from 2.x

Poweradmin 2.x reached end of life long ago and has known security issues that will not be fixed.
Among them: forms have no CSRF protection, several pages print stored data without escaping, a
logged-in user can change zones they do not own, and a leftover `install/` directory can be used
without logging in. Upgrade to 4.4.x, the LTS line, and until then keep 2.x off the public
internet (VPN, IP allow-list or web server authentication).

This page describes a direct upgrade from 2.1.7 through 2.2.2 to 4.4.x. It was tested in November
2026 by upgrading a 2.1.7 database to 4.4.x on MariaDB and PostgreSQL. There is no need to install
every release in between: you install 4.4.x and run the update scripts it ships, in order.

## Before you start

- Back up the PowerDNS database and the Poweradmin tables (they usually share one database).
- 4.4.x needs PHP 8.2 or later. 2.1.7 and older need the mcrypt extension, so such a server most
  likely runs PHP 7.1 or older; plan a new PHP installation rather than an in-place upgrade.
- Upgrade PowerDNS and its database schema first, following the
  [PowerDNS upgrade notes](https://doc.powerdns.com/authoritative/upgrading.html). 2.1.7 and older
  were built for PowerDNS 3.x. Reference schemas for current PowerDNS releases ship in
  Poweradmin's `sql/pdns/` directory.
- On MySQL, keep the database's existing character set. Converting a PowerDNS 3.x-era schema to
  utf8 fails on `records.content VARCHAR(64000)`.
- On 2.1.4 through 2.1.6, first run only the SQL from the [v2.1.5](v2.1.5.md), [v2.1.6](v2.1.6.md)
  and [v2.1.7](v2.1.7.md) pages for each release after yours; skip their file and tarball steps.
  The 2.1.7 PHP migration that links existing records to their zone templates cannot run on this
  route, so those records stay unlinked. Older than 2.1.4: follow the incremental path in the
  [upgrade overview](index.md#upgrade-path).

## Upgrade steps

1. Install the 4.4.x release files in a new directory (see [Installation](../installation/index.md)).
   Do not copy the old files over.
2. Create a new `config/settings.php`. The 2.x `inc/config.inc.php` format is not read by 4.x,
   and the converter `config/migrate-config.php` only ships in 4.0.x. Copy the database
   connection details and DNS defaults over by hand.
3. Run the update scripts from the 4.4.x `sql/` directory, one at a time, in this order. Do not run
   `update-to-2.1.7`: a 2.1.7 or later database already contains its changes, and the script fails.

    | Database | Scripts, in order |
    | --- | --- |
    | MySQL / MariaDB | `2.2.1`, `3.2.0`, `3.9.0`, `4.0.0`, `4.0.2`, `4.1.0`, `4.2.0`, `4.3.0`, `4.4.0` |
    | PostgreSQL | `3.2.0`, `3.9.0`, `4.0.0`, `4.0.2`, `4.1.0`, `4.2.0`, `4.3.0`, `4.4.0` |
    | SQLite | `3.2.0`, `3.9.0`, `4.0.0`, `4.0.2`, `4.1.0`, `4.2.0`, `4.3.0`, `4.3.0-backfill`, `4.4.0` |

    For MySQL, each step looks like this:

    ```bash
    mysql -u root -p pdns < sql/poweradmin-mysql-update-to-2.2.1.sql
    ```

    Already on 2.2.1 or 2.2.2? Skip the MySQL `2.2.1` script and start with `3.2.0`.

4. Add the `zone_content_edit_own_as_client` permission if it is missing. Databases created by
   2.1.7 or older, or loaded from the SQL files instead of the installer (MySQL files before
   2.2.1, all 2.x PostgreSQL and SQLite files), do not have it, and no
   update script before 4.6.0 adds it. Without it, the Editor templates cannot edit records.
   Check first with `SELECT id FROM perm_items WHERE name = 'zone_content_edit_own_as_client';`
   and run the following only if that returns nothing:

    ```sql
    INSERT INTO perm_items (name, descr)
    VALUES ('zone_content_edit_own_as_client', 'User is allowed to edit record, but not SOA and NS.');

    INSERT INTO perm_templ_items (templ_id, perm_id)
    SELECT pt.id, pi.id
    FROM perm_templ pt
    JOIN perm_items pi ON pi.name = 'zone_content_edit_own_as_client'
    WHERE (pt.name = 'Editor' AND pt.template_type = 'user')
       OR (pt.name = 'Editors' AND pt.template_type = 'group');
    ```

5. PostgreSQL only, and only if `SELECT id FROM perm_items WHERE name = 'zone_content_edit_own';`
   returns something other than 44: the database was loaded from the 2.x PostgreSQL SQL file,
   which numbers the permissions 1-21 instead of 41-61. The 4.4.x copy of the 4.1.0 script grants
   the new delete permissions by those fixed numbers, so templates that could edit zones do not
   get the matching delete permission. Re-grant **zone_delete_own** and **zone_delete_others** to
   such templates under **Access > List templates**.
6. Delete the `install/` directory, then log in.

## After the upgrade

- Existing passwords keep working. 2.x stored unsalted MD5 hashes by default; 4.4.x accepts them
  and replaces each one with a bcrypt hash on the user's first login. Ask users who never log in
  to reset their password, or reset it for them.
- Review users, permission templates and zone owners. 2.x let any logged-in user change zone types,
  slave masters and owners, so check for changes you did not make.
- Some differences from a fresh 4.4.x schema remain. None affect how 4.4.x works:
    - MySQL tables keep their old character set, and a few columns keep older types.
    - An empty legacy `migrations` table stays.
    - `records_zone_templ` has no `id` primary key, which matters only for MySQL InnoDB Cluster
      or Group Replication.
    - On MySQL, `zones` has no `domain_id` index, and no `owner` index either on databases
      created from the 2.2.x SQL file; on PostgreSQL it keeps only the combined `domain_id, owner`
      index.
- From here, follow the normal [upgrade instructions](index.md) for later releases.
