# NAPTR Records

NAPTR records are used for things like SIP service discovery and ENUM (mapping phone numbers to URIs). They are easy to get wrong because the content field has six positional parts and three of them must be quoted.

## Content Format

The content field has this layout:

```
<order> <preference> "<flags>" "<service>" "<regexp>" <replacement>
```

| Part        | Notes                                                                                  |
|-------------|----------------------------------------------------------------------------------------|
| order       | Number 0-65535. Lower order is processed first.                                        |
| preference  | Number 0-65535. Tie-breaker when two records share the same order.                     |
| flags       | Quoted. Usually `"S"`, `"A"`, `"U"`, `"P"`, or `""`.                                   |
| service     | Quoted. For example `"SIP+D2U"` or `"E2U+sip"`.                                        |
| regexp      | Quoted substitution like `"!^.*$!sip:user@example.com!"`, or `""` if not used.         |
| replacement | A domain name, or `.` when the regexp is used.                                         |

You either fill in the regexp and use `.` as the replacement, or leave the regexp empty (`""`) and put a domain name in the replacement. Doing both at once is not valid.

## Examples

A terminal NAPTR that rewrites the input to a SIP URI:

```
100 10 "U" "E2U+sip" "!^.*$!sip:info@example.com!" .
```

A non-terminal NAPTR that points to an SRV lookup (common for SIP service discovery):

```
100 10 "S" "SIP+D2U" "" _sip._udp.sip.example.com.
```

## Priority Field

The Priority column in the add/edit form is not used by NAPTR - the order and preference are already inside the content. Leave Priority at `0`. A non-zero value is rejected by the validator.

## Common Mistakes

- Forgetting one of the two numbers at the start. The content needs both `order` and `preference`.
- Leaving off the quotes around flags, service, or regexp. All three must be quoted, even when empty (`""`).
- Setting a Priority other than `0`. NAPTR carries its own order/preference, so the row's Priority must stay at `0`.
- Mixing a non-empty regexp with a domain replacement. Use `.` as the replacement when the regexp is filled in.

## ENUM Records

For ENUM (E.164 to URI mapping, RFC 6116), the zone name lives under `e164.arpa`, the service starts with `E2U`, and the flag is normally `"U"`. Poweradmin will warn you if a NAPTR looks like an ENUM record but the fields do not line up.
