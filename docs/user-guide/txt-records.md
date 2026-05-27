# TXT Records

TXT records hold free-form text. The common reasons to add one are email authentication (SPF, DKIM, DMARC), or a verification string that a third-party service asks you to publish at a specific hostname to prove control of the domain.

This page covers the typical cases someone working with a third-party service will run into. For configuration that controls record-type availability and auto-quoting, see [DNS Settings](../configuration/dns-settings.md).

> **Tip:** If your administrator has enabled DNS Wizards, the SPF, DKIM, and DMARC wizards build the record content for you from a short form - skip ahead to [Wizards](#wizards-admin-enabled). The manual steps below are for installations without wizards or for record shapes the wizards do not cover.

## Adding a TXT Record

1. Open the zone from the zone list.
2. In the input row at the top of the record table:
    - **Name**: the hostname part only (e.g. `@` for the zone apex, `_dmarc` for DMARC, `selector1._domainkey` for DKIM).
    - **Type**: select `TXT`.
    - **Content**: the value, wrapped in double quotes (e.g. `"v=spf1 include:_spf.example.com -all"`).
    - **TTL**: leave at the zone default unless the third-party service requires a specific value.
    - **Priority**: must be `0`. TXT records do not use priority.
3. Click **Add Record**.

> **Tip:** If the third-party instructions show the record as `host TXT "value"`, only the `value` (with surrounding quotes) goes into the **Content** field.

## Quoting

The content must be wrapped in double quotes. The validator rejects unquoted content unless `dns.txt_auto_quote` is enabled by the administrator. If the value itself contains a quote character, escape it with a backslash (`\"`).

A site-wide auto-quote setting exists for installations where users routinely paste unquoted strings:

```php
'dns' => [
    'txt_auto_quote' => true,
],
```

When this is on, Poweradmin wraps the supplied content in quotes automatically. It is off by default to keep the stored content identical to what was typed.

## Email Authentication Records

### SPF (Sender Policy Framework)

Published at the zone apex. Tells receivers which servers may send mail on behalf of the domain.

- **Name**: `@` (or leave blank for the zone apex)
- **Type**: `TXT`
- **Content**: `"v=spf1 include:_spf.example.com -all"`

Replace `_spf.example.com` with the include host your email or marketing provider gave you. A domain should have exactly one SPF record. If the third party gives you a second `v=spf1` string, merge it into your existing record's `include:` chain instead of adding a second TXT.

### DKIM (DomainKeys Identified Mail)

Published at a selector-specific hostname provided by the email service. The public key is long and almost always exceeds 255 bytes.

- **Name**: `selector1._domainkey` (the third party supplies the selector name)
- **Type**: `TXT`
- **Content**: `"v=DKIM1; k=rsa; p=MIGfMA0GCSq..." "...continuation of the public key..."`

A single TXT string on the wire is capped at 255 bytes. For longer values (DKIM keys, long DMARC reporting URIs), split the content into multiple quoted strings separated by a space. Poweradmin accepts the multi-string form and PowerDNS serves the strings concatenated. Do not insert line breaks or strip the quotes when splitting.

### DMARC (Domain-based Message Authentication, Reporting & Conformance)

Published at `_dmarc` under the zone apex.

- **Name**: `_dmarc`
- **Type**: `TXT`
- **Content**: `"v=DMARC1; p=none; rua=mailto:dmarc-reports@example.com"`

Start with `p=none` to collect reports without affecting delivery, then tighten to `p=quarantine` or `p=reject` once the reports look clean.

## Verification Records

Third-party services (Google Workspace, Microsoft 365, certificate authorities, survey or transactional-email platforms) commonly ask for a TXT record that proves you control the domain. The pattern is almost always the same:

- They give you a **host** and a **value**.
- You paste them as **Name** and **Content** on the zone.
- After saving, you wait for propagation (TTL seconds, default 86400 unless you lowered it) and click the verify button on the third party's side.

Typical examples:

| Service              | Name                       | Content shape                       |
|----------------------|----------------------------|-------------------------------------|
| Google Workspace     | `@`                        | `"google-site-verification=..."`    |
| Microsoft 365        | `@`                        | `"MS=ms..."`                        |
| Let's Encrypt (DNS-01) | `_acme-challenge`        | `"<random token>"`                  |
| Generic SaaS         | `<provided host>`          | `"<provided token>"`                |

For ACME / Let's Encrypt DNS challenges, the record is short-lived. Set a low TTL (e.g. 60-300) so revisions propagate quickly, and delete the record after the certificate is issued.

## Wizards (Admin-Enabled)

Administrators can enable record wizards that walk users through SPF, DKIM, DMARC, and CAA fields and produce a correctly formatted TXT record. They are off by default. See [DNS Wizards](../configuration/dns-wizards.md) for the configuration. When enabled, the wizards appear as buttons above the record table in the zone editor.

## Common Mistakes

- **Forgetting the quotes**. Content must be in double quotes unless the admin has enabled `dns.txt_auto_quote`.
- **Setting a non-zero Priority**. TXT records do not use priority; the validator rejects anything other than `0`.
- **Adding a second SPF record**. Only one `v=spf1` TXT is allowed at the apex. Merge entries into the existing record's `include:` chain.
- **Splitting DKIM with line breaks**. Split into multiple quoted strings on the same line (`"part1" "part2"`), not newline-separated.
- **Putting the full hostname in the Name field**. Use only the host part (`_dmarc`, `selector1._domainkey`), not the full FQDN.
- **Verifying immediately**. Wait at least the record's TTL before asking the third party to re-check. Long default TTLs (24h) are the usual cause of "record not found" errors during verification.
