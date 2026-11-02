#!/usr/bin/env python3
"""Fail when a page under docs/ is not listed in the mkdocs.yml nav, or the nav lists a missing page.

MkDocs enforces the first through validation.nav under --strict; Zensical does not, so this
keeps the rule independent of the build engine.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


class Loader(yaml.SafeLoader):
    """SafeLoader that tolerates the !!python/name tags used by markdown extension options."""


Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def nav_pages(node):
    if isinstance(node, str):
        if node.endswith(".md") and "://" not in node:
            yield node
    elif isinstance(node, list):
        for item in node:
            yield from nav_pages(item)
    elif isinstance(node, dict):
        for value in node.values():
            yield from nav_pages(value)


def main():
    config = yaml.load((ROOT / "mkdocs.yml").read_text(), Loader=Loader)
    docs = ROOT / config.get("docs_dir", "docs")
    listed = set(nav_pages(config.get("nav", [])))
    present = {
        p.relative_to(docs).as_posix()
        for p in docs.rglob("*.md")
        if not any(part.startswith(".") for part in p.relative_to(docs).parts)
    }

    status = 0
    for page in sorted(present - listed):
        print(f"::error file=docs/{page}::not in the mkdocs.yml nav")
        status = 1
    for page in sorted(listed - present):
        print(f"::error file=mkdocs.yml::nav lists docs/{page}, which does not exist")
        status = 1
    if not status:
        print(f"nav OK: {len(present)} pages, all listed")
    return status


if __name__ == "__main__":
    sys.exit(main())
