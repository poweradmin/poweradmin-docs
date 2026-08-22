#!/bin/sh
# Local mirror of the CI build. Deploys happen automatically on push to main
# (.github/workflows/deploy.yml); use that workflow's "Run workflow" button
# for a manual redeploy rather than pushing the site from a workstation.
#
#   ./build.sh          build with --strict, exactly as CI does
#   ./build.sh serve    build, then serve on http://127.0.0.1:8000
#
# Install the pinned toolchain first: pip install -r requirements.txt

set -e

mkdocs build --strict

if [ "$1" = "serve" ]; then
    mkdocs serve
fi
