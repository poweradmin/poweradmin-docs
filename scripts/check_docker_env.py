#!/usr/bin/env python3
"""Report PA_* environment variables the Docker entrypoint uses but DOCKER.md omits.

Both files live in the poweradmin repo; this only checks them, because that is
where the fix belongs.
"""
import argparse
import re
import sys
from pathlib import Path

VAR_RE = re.compile(r"\bPA_[A-Z0-9_]+\b")
# Secrets are supplied either as PA_FOO or PA_FOO__FILE; documenting one covers both.
FILE_SUFFIX = "__FILE"


def names(path):
    return {canonical(v) for v in VAR_RE.findall(path.read_text())}


def canonical(var):
    return var[:-len(FILE_SUFFIX)] if var.endswith(FILE_SUFFIX) else var


def used_names(path):
    """Variables the entrypoint actually consumes.

    Two kinds of match are not real variables:
      - a truncated prefix from a glob in a log message (PA_SAML_*_ENABLED)
      - a name the entrypoint tests only so it can warn that it is NOT
        recognised (PA_PDNS_BACKEND exists purely to redirect to PA_DNS_BACKEND)
    """
    lines = path.read_text().split("\n")
    seen = {}
    for line in lines:
        for var in VAR_RE.findall(line):
            seen.setdefault(canonical(var), []).append(line)
    return {
        var for var, refs in seen.items()
        if not var.endswith("_")
        and not any(f"{var} is not a recognized variable" in ref for ref in refs)
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrypoint", required=True, type=Path)
    ap.add_argument("--docs", required=True, type=Path)
    args = ap.parse_args()

    used, documented = used_names(args.entrypoint), names(args.docs)
    undocumented = sorted(used - documented)
    unused = sorted(documented - used)

    print(f"{len(used)} variables used, {len(documented)} documented")
    if unused:
        print(f"\nDocumented but not referenced by the entrypoint ({len(unused)}):")
        for v in unused:
            print(f"  {v}")
    if undocumented:
        print(f"\nUsed by the entrypoint but missing from DOCKER.md ({len(undocumented)}):")
        for v in undocumented:
            print(f"  {v}")
        sys.exit(1)
    print("\nEvery variable the entrypoint uses is documented.")


if __name__ == "__main__":
    main()
