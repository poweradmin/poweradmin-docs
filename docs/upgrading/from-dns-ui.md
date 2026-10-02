# Migrating from Opera DNS UI

[Opera DNS UI](https://github.com/operasoftware/dns-ui) (dns-ui) is a PHP interface for PowerDNS with LDAP
login, per-zone access levels and a change review workflow. It talks to PowerDNS only over the HTTP API and keeps
users, access and history in its own PostgreSQL database. See [Migrating from Other Tools](from-other-tools.md)
for the general approach.

There is no import tool. This page describes a manual migration. Try it on a test copy first.

> **Note:** Several steps rely on features added in Poweradmin 4.5.0 and 4.6.0, marked where they appear. See
> [What's New](../whats-new/v4.6.0.md) for which versions are released.

## What Carries Over

Records live in PowerDNS. Point Poweradmin at the same PowerDNS and the zones are there. So are the RRset comments
dns-ui writes, because it stores them in PowerDNS. Poweradmin hides record comments by default; set
`interface.show_record_comments` to `true` to show them.

| Stays in PowerDNS | Must be recreated in Poweradmin |
|---|---|
| Zones and records | Users (or created on first LDAP login) |
| RRset comments | Global admin flag |
| DNSSEC keys and zone metadata | Per-zone access (administrator, operator) |
| The zone "classification", in the `account` field | Pending change requests |
| | SOA and NS templates |
| | Settings in `config/config.ini` |

The change log and its change comments are not migrated. dns-ui stores each change as a serialized PHP object,
which no other tool can read. Keep the dns-ui database if you need the history.

## Before You Start

Export the worklist from the dns-ui database (PostgreSQL):

```sql
-- users, with the global admin and active flags
SELECT uid, name, email, auth_realm, admin, active
FROM "user"
ORDER BY uid;

-- per-zone access; global admins see every zone without a row here
SELECT rtrim(z.name, '.') AS zone, u.uid, za.level::text AS level
FROM zone_access za
JOIN zone z ON z.id = za.zone_id
JOIN "user" u ON u.id = za.user_id
WHERE z.active
ORDER BY z.name, u.uid;

-- change requests still waiting for review
SELECT rtrim(z.name, '.') AS zone, u.uid AS requested_by, p.request_date
FROM pending_update p
JOIN zone z ON z.id = p.zone_id
LEFT JOIN "user" u ON u.id = p.author_id
ORDER BY p.request_date;
```

Review or reject the pending requests in dns-ui before you switch. They cannot be moved.

Also write down the `[ldap]` section of `config/config.ini`, and which scripts call the dns-ui API. Back up the
PowerDNS database and the dns-ui database.

## Steps

### 1. Install Poweradmin

Pick a method from the [Installation](../installation/index.md) section. Poweradmin creates its own tables for
users, groups and permissions. Do not point it at the dns-ui database.

### 2. Connect It to the Same PowerDNS

dns-ui uses only the PowerDNS API, with `[powerdns] api_url` and `api_key`. Poweradmin can do the same in API
backend mode: set `dns.backend` to `api`, plus `pdns_api.url` and `pdns_api.key`. `pdns_api.url` is the server
address alone, for example `http://localhost:8081`, not the full `/api/v1/servers/localhost` path dns-ui uses.
Some features are limited in this mode, see
[API Backend Mode](../configuration/powerdns-api.md#api-backend-mode-v430).

If Poweradmin can reach the PowerDNS database, SQL mode (the default) has the full feature set. See
[PowerDNS API](../configuration/powerdns-api.md) for both modes.

Sign in as the administrator and open the zone list. You should see the existing zones.

### 3. Set Up Login

dns-ui never checks a password itself. The web server authenticates the user, usually against LDAP, and dns-ui
reads the username from `REMOTE_USER`. Poweradmin does not accept a login from the web server. It authenticates
against LDAP itself, see [LDAP Integration](../configuration/ldap.md).

Take the values from dns-ui's `[ldap]` section:

| dns-ui `[ldap]` | Poweradmin `ldap` |
|---|---|
| `host` | `uri`. There is no StartTLS setting; use an `ldaps://` URI |
| `bind_dn`, `bind_password` | `bind_dn`, `bind_password` |
| `dn_user` | `base_dn` |
| `user_id` | `user_attribute` |
| `user_name`, `user_email` | `fullname_attribute`, `email_attribute` with `sync_user_info` |
| `dn_group`, `group_member` | `groups_attribute`, usually `memberOf`; Poweradmin reads the groups from the user entry |
| `admin_group_cn` | An entry in `permission_template_mapping`, plus `allow_superuser_provisioning` |

dns-ui creates a user on first login. Poweradmin does the same with `auto_provision` on (since 4.5.0, like the group
mappings below). Use `search_filter` to
limit login to the people who used dns-ui, see
[Granting access to an Active Directory group](../configuration/ldap.md#granting-access-to-an-active-directory-group-without-pre-creating-users).

dns-ui finds the admin group by its CN. Poweradmin's `permission_template_mapping` and `group_mapping` match the
value of `groups_attribute` exactly, which for `memberOf` is the full DN of the group, not its CN. On OpenLDAP,
`memberOf` needs the overlay enabled. A mapping that grants `user_is_ueberuser` takes effect only with
`ldap.allow_superuser_provisioning` set to `true`.

dns-ui's `user_active` attribute has no equivalent. Disable departed users in Poweradmin, or exclude them with
`search_filter`.

Two-factor login is off by default, set `security.mfa.enabled` to offer it, see [MFA](../user-guide/mfa.md).

### 4. Recreate Access Levels

dns-ui has a global admin flag and two levels per zone:

- **administrator**: edits the zone directly and reviews change requests for it.
- **operator**: requests changes, which a zone administrator approves.

Poweradmin has the same review step since 4.6.0, see [Change Requests](../user-guide/change-requests.md). Turn it
on with `approval.enabled`. dns-ui's `[web] force_change_review` corresponds to `approval.require_review_for_all`, and
`force_change_comment` to `logging.require_change_comment`.

Poweradmin permissions come from [permission templates](../user-guide/users-roles.md), on the user and on each
[group](../user-guide/groups.md) the user belongs to. A user's rights are the combination of all of them, and an
"own" right covers every zone the user owns, directly or through any group. Levels per zone therefore work through
groups as long as each user holds one level:

1. Create two group templates:
    - "Zone administrator": `zone_content_view_own`, `zone_content_edit_own`, `zone_meta_edit_own` and
      `zone_change_approve_own`.
    - "Zone operator": `zone_content_view_own` and `zone_change_request_own`.
2. For each team, create one group with each template, for example "web-admins" and "web-operators".
3. Add the users to the groups, and give each group the zones from your `zone_access` export. On a group's zones
   page you can move several zones at once.

A user who is an administrator of some zones and an operator of others gets both templates, so they edit all of
their zones directly. Review such users in the `zone_access` export before you start. Turning on
`approval.require_review_for_all` sends everyone's changes through review instead.

Global admins map to users with the `user_is_ueberuser` permission, through `permission_template_mapping` and
`allow_superuser_provisioning` in the LDAP settings. Give everyone else a personal template with few rights, since
their zone rights come from groups. If your LDAP groups match the teams, `group_mapping` keeps group membership in
step with the directory.

Only global admins may change SOA and NS records in dns-ui. In Poweradmin, editing the SOA record needs
`zone_content_edit_others`, so the "Zone administrator" template above cannot change it. NS records can be edited
by anyone who may edit the zone, unless their template uses `zone_content_edit_own_as_client`.

For a large number of zones, script the assignment with `/api/v2/groups/{id}/zones`, see the
[API Reference](../api/reference.md).

### 5. Recreate Templates

dns-ui's SOA and NS templates fill in the zone creation form. In Poweradmin the defaults for new zones are the
`dns.hostmaster`, `dns.ns1` to `dns.ns4` and `dns.soa_*` settings, see
[DNS Settings](../configuration/dns-settings.md). For more than one set, create
[DNS templates](../user-guide/dns-templates.md).

### 6. Optional Features

- **Notifications.** dns-ui mails the SOA contact and the zone administrators when a change is requested.
  Poweradmin mails every user who may review the request, and the SOA contact with
  `notifications.change_request_soa_contact`. Mail is off by default, see
  [Notifications](../user-guide/change-requests.md#notifications).
- **Zone deletion.** dns-ui needs a second admin to confirm a deletion. In Poweradmin a deletion goes through review
  only for users who request changes instead of editing directly, or for everyone with
  `approval.require_review_for_all`. A reviewer may approve their own request.
- **Reverse records.** dns-ui adds a PTR for each new A or AAAA record. Poweradmin offers the same as a checkbox
  when `interface.add_reverse_record` is on (the default).
- **Classification.** dns-ui shows the PowerDNS `account` field as a free-text "classification". Poweradmin does
  not show it. Two settings use it, both off by default; leave them off to keep the classifications:
  `dns.adopt_zone_owner_from_account` gives a zone whose classification matches a username to that user, and
  `dns.sync_zone_owner_to_account` overwrites the field with the zone owner's username.
- **DNSSEC.** dns-ui only turns signing on and off. Poweradmin also manages keys; it is off by default, set
  `dnssec.enabled`. Existing keys stay in PowerDNS. See [DNSSEC](../user-guide/dnssec.md).
- **Import and export.** Both tools import and export BIND zone files, see
  [Zone Import/Export](../configuration/zone-import-export.md).

### 7. Replace Scripts

dns-ui's API also lives under `/api/v2`, but it is a different API. It authenticates through the web server and
takes a list of actions in one `PATCH`. Poweradmin's API authenticates with an API key in the `X-API-Key` header
and has separate endpoints for zones and records. Rewrite scripts against [API Overview](../api/overview.md) and
[API Authentication](../api/authentication.md). Enable the API with `api.enabled`.

### 8. Switch Over

1. Ask a few users from each team to sign in and check that they see their zones and can do what their level
   allowed before.
2. Stop making changes in dns-ui. Both tools write to PowerDNS, so a record changed in one shows up in the other.
   dns-ui logs nothing for changes made elsewhere, and Poweradmin logs nothing for changes made in dns-ui.
3. Turn off dns-ui's `scripts/ldap_update.php` cron job and the git-tracked export, if you used them.
4. Keep the dns-ui database for its change history, then shut dns-ui down.

## Concept Mapping

| Opera DNS UI | Poweradmin |
|---|---|
| Web server login (`REMOTE_USER`) | [LDAP](../configuration/ldap.md), [OIDC](../configuration/oidc.md) or [SAML](../configuration/saml.md) login in Poweradmin |
| User created on first login | LDAP `auto_provision` (4.5.0+) |
| `admin_group_cn` | `permission_template_mapping` to a template with `user_is_ueberuser` |
| Zone access: administrator | Group with an edit and approve template, owning the zone |
| Zone access: operator | Group with a request-only template, owning the zone |
| Pending change request | [Change request](../user-guide/change-requests.md), `approval.enabled` (4.6.0+) |
| `force_change_review` | `approval.require_review_for_all` |
| `force_change_comment` | `logging.require_change_comment` |
| RRset comment | Record comment, `interface.show_record_comments` |
| Change log | [Record change log](../user-guide/record-change-log.md), not migrated |
| SOA and NS templates | `dns.*` defaults and [DNS templates](../user-guide/dns-templates.md) |
| Classification (`account`) | Kept in PowerDNS, not used by Poweradmin |
| Git-tracked export | No equivalent |
| `/api/v2` with web server login | [REST API](../api/overview.md) `/api/v2` with API keys |
