#!/bin/sh

cd ../poweradmin.github.io/

mkdocs gh-deploy --verbose --config-file ../poweradmin-docs/mkdocs.yml --remote-branch master
