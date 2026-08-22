# Poweradmin Documentation

Source for the Poweradmin documentation published at **[docs.poweradmin.org](https://docs.poweradmin.org)**.

Poweradmin itself lives in the [main repository](https://github.com/poweradmin/poweradmin).

## Building locally

```bash
pip install -r requirements.txt   # pinned toolchain, same versions CI uses
./build.sh                        # build with --strict, exactly as CI does
./build.sh serve                  # build, then serve on http://127.0.0.1:8000
```

## Contributing

Edit the Markdown under `docs/` and open a pull request. Every page has an edit link in the top
right on the site, which takes you straight to the right file.

A change has to pass three checks, all of which run on pull requests and again before anything
deploys:

- `mkdocs build --strict` - broken links, dead anchors, and pages missing from the navigation
- `markdownlint-cli2` - the house style: dash bullets, four-space nested indentation, blank lines
  around lists and code fences
- a check that no code fence sits unindented after a numbered list item, which would detach it from
  the step it belongs to

Run all three locally with `./build.sh` and `npx markdownlint-cli2`.

### Generated pages

Two pages are generated from the Poweradmin source and must not be edited by hand:

| Page | Generated from |
|---|---|
| `docs/configuration/settings-reference.md` | `config/settings.defaults.php` via `scripts/gen_settings_reference.py` |
| `docs/api/openapi.json` (rendered by `docs/api/reference.md`) | the API controller annotations, via `composer docs:api:json` |

A weekly workflow re-derives both from the Poweradmin repository and fails if they have drifted. It
also checks that every `PA_*` variable the Docker entrypoint reads is documented in `DOCKER.md`.

## Deployment

Pushing to `main` builds the site and publishes it to
[poweradmin.github.io](https://github.com/poweradmin/poweradmin.github.io). There is no manual
deploy step - use the "Run workflow" button on the *Deploy Documentation* workflow if you need to
republish without a commit.

## License

See [LICENSE](LICENSE).
