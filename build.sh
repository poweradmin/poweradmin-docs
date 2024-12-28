#!/bin/sh

cd ../poweradmin.github.io/
cp -R ../poweradmin-docs/screenshots screenshots

mkdocs gh-deploy --config-file ../poweradmin-docs/mkdocs.yml --remote-branch master
