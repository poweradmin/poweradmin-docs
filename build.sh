#!/bin/sh

cd ../poweradmin.github.io/
mkdocs gh-deploy --config-file ../poweradmin-docs/mkdocs.yml --remote-branch master
