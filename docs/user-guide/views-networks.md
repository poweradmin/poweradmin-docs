# Views and Networks

*Available since v4.4.0. Requires PowerDNS 5.0 or newer and the PowerDNS API backend.*

PowerDNS 5.0 can answer the same query differently depending on which network the client
came from - the feature usually called split-horizon DNS. Poweradmin exposes two pages for
it: **Views**, which assigns zone variants to a view, and **Networks**, which maps client
networks to views.

> **Note:** Both pages are superuser-only, need `dns.backend` set to `api`, and refuse to
> load on PowerDNS older than 5.0. On an older server the page reports "Views require
> PowerDNS 5.0 or newer" instead of rendering. See
> [PowerDNS API](../configuration/powerdns-api.md) for the backend setup.

## How the two pieces fit together

1. You create a zone variant in PowerDNS, named `zone..variant`, for example
   `example.com..trusted`. The variant is a separate zone with its own records.
2. On the **Views** page you assign that variant to a view name, for example `trusted`.
3. On the **Networks** page you map a CIDR block, for example `10.0.0.0/8`, to the same
   view.

A resolver querying from `10.1.2.3` then gets the records from `example.com..trusted`, while
everyone else gets the plain `example.com`.

## Views

The Views page is at `/views`. It lists each view with the zone variants assigned to it, and
a form to add another.

Two things to know:

- **The variant zone must already exist in PowerDNS.** Poweradmin assigns an existing zone
  to a view; it does not create the variant for you.
- **View names accept letters, digits, dots, underscores and hyphens.** Anything else is
  rejected.

To assign a zone, enter the view name (`trusted`) and the full variant zone name
(`example.com..trusted`). Removing an assignment takes the zone back out of the view; it does
not delete the zone.

## Networks

The Networks page is at `/networks`. Each network maps to exactly one view, and every
resolver in that network sees only the zone variants belonging to it.

PowerDNS evaluates networks **longest-prefix first**. A more specific subnet wins over a
broader one, so `10.0.1.0/24` mapped to `office` overrides `10.0.0.0/8` mapped to `internal`
for a client at `10.0.1.5`.

To add a mapping, enter the CIDR (`192.168.0.0/16`) and the view name (`trusted`).

## Related pages

- [PowerDNS API](../configuration/powerdns-api.md) - enabling the API backend
- [Zone Management](zones.md) - creating the variant zones themselves
