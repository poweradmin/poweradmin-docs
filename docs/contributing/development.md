# Poweradmin Development Guide

> **Note:** The repository's own [CONTRIBUTING.md](https://github.com/poweradmin/poweradmin/blob/master/CONTRIBUTING.md)
> is the canonical source for branch targeting, commit conventions and the pull request process.
> This page covers the development environment and project layout.

## Development Environment Setup

### Prerequisites

- PHP 8.2 or higher
- MySQL/MariaDB, PostgreSQL, or SQLite
- Composer
- A PowerDNS server for testing
- Node.js and npm, only if you intend to run the Playwright end-to-end tests

### Option 1: Devcontainer (recommended)

The repository ships a devcontainer providing MariaDB, PostgreSQL, SQLite and Adminer, with
instances of Poweradmin already configured against each. Open the repository in VS Code with the
Dev Containers extension and reopen in the container.

Load the test users with:

```bash
.devcontainer/scripts/import-test-data.sh
```

### Option 2: Manual setup

**1. Clone the repository:**

```bash
git clone https://github.com/poweradmin/poweradmin.git
cd poweradmin
```

**2. Install dependencies:**

```bash
composer install
```

**3. Configure the application:**

```bash
cp config/settings.defaults.php config/settings.php
# Edit config/settings.php with your database and PowerDNS settings
```

Never edit `config/settings.defaults.php` itself. It is the reference for every available setting
and is overwritten on upgrade.

## Project Structure

### Core components

- **lib/**: core library code in three layers; a lower layer never imports a higher one
  (`composer analyse:all` enforces this)
    - **Domain/**: business rules with no framework or storage dependency
        - `Model/`, `ValueObject/`, `Enum/`: entities, value objects and constant tables
        - `Port/`: the interfaces the application and infrastructure layers implement
          (backend providers, DNSSEC, audit logging, record change writer, password hashing)
        - `Repository/`: repository interfaces, split into narrow roles such as
          `UserLookupInterface` and `RecordListingInterface`
        - `Service/Auth/`, `Service/Zone/`, `Service/Template/`, `Service/Dns/`,
          `Service/User/`, `Service/Consistency/`, `Service/Validation/`: the use cases,
          grouped by the concern that changes them. They write through the repository
          interfaces, take the acting user as `Port\ActorInterface`, and report failures
          as result objects carrying a `Refusal`, never an HTTP status
        - `Service/DnsValidation/`: one validator per record type, sharing one
          `HostnameValidator` built from a `HostnamePolicy`
        - `Database/`: SQL dialect helpers (`DbCompat`, `TableNameService`, `CanonicalZoneSql`)
        - `Module/`: the `ModuleInterface` bundled modules implement
    - **Application/**: everything that faces a request
        - `Controller/`: web controllers grouped by route (`Zone/`, `Record/`, `Dnssec/`,
          `Auth/`, `User/`, `Template/`, `Log/`, `System/`) plus `Api/` (with the v2
          resource shapers under `Api/V2/Resource/`) and the shared `BaseController`
        - `Service/`: application services grouped like the domain ones (`Auth/`, `User/`,
          `Zone/`, `Record/`, `Backend/`, `Mail/`, `Web/`), and the composition root
          (`ControllerServiceFactory` with the concern factories under `Service/Factory/`)
        - `Boot/`: the `Kernel` every entry point boots through, `Http/` (request, refusal
          to status mapping), `Routing/`, `Web/` (page rendering), `Presenter/` (view
          models), `Module/` (module manifest, registry and the `ModuleServices` contract),
          `Console/` (the `bin/poweradmin` commands)
    - **Infrastructure/**: adapters for the outside world: `Repository/` (PDO and the
      PowerDNS API repositories, incl. search), `Api/` (the PowerDNS API client), `Service/`
      (backend providers), `Database/` (schema, credentials, seed data), `Logger/`,
      `Session/`, `Configuration/`, `Utility/`. Infrastructure imports nothing from the
      layers above it
    - **Module/**: the bundled modules (DNS wizards, zone import/export, WHOIS, RDAP,
      secondary zone import, CSV export, email previews), registered in
      `Application/Module/ModuleManifest.php`

Entry points are `index.php`, `dynamic_update.php`, `install/index.php` and
`bin/poweradmin`; all four boot through `Application\Boot\Kernel`.

Modules extend `Application\Controller\BaseController`, implement
`Domain\Module\ModuleInterface`, obtain core services through
`$this->moduleServices()` (`Application\Module\ModuleServices`), and otherwise depend on
the `Domain\Port`, `Domain\Repository` and `Domain\Service` namespaces plus the SDK value
types (`RecordAddResult`, `RecordAddAccess`, `ZoneCreateRequest`, `ZoneCreateFormMessages`,
`ChangeRequestMessages`). `composer analyse:all` rejects other imports of application
services from a module. Treat that as the module surface; the rest of `lib/` may move
between releases without notice.

### Frontend

- **assets/**: JavaScript and images
- **templates/**: Twig templates, with a `default` and a `modern` theme

The two themes must stay in sync except for the files listed in
`templates/theme-specific-templates.txt`. `composer lint:themes` enforces this.

### Testing

- **tests/**: PHPUnit suites (`unit`, `integration`, `functional`, `api`, `sql`, `docker`)
- **playwright/**: end-to-end browser tests

See the [Testing Guide](testing.md).

## Documentation

The public API is described by `docs/api/openapi.json` in the docs repository, generated
from the controller attributes. Regenerate it from a poweradmin checkout after changing
the API (the docs repository's drift check fails when it is stale):

```bash
composer docs:api -- --output ../poweradmin-docs/docs/api/openapi.json
```

A running instance also serves the same specification live at `/api/docs/v2/json` when
`api.docs_enabled` is on.

A browsable class reference for `lib/` is published from the `develop` branch at
[docs.poweradmin.org/reference](https://docs.poweradmin.org/reference/). The docs deploy builds it
with Doctum on every run, so it is never committed. To build it locally (the script downloads the
phar on first use and writes static HTML to `docs/reference/`, also ignored):

```bash
composer docs:reference
open docs/reference/index.html
```

`composer lint:docblocks` runs the same parser without building and fails on any `@param`
tag that does not match the method signature. It is part of `composer lint:all` and CI.

## Testing

Poweradmin has unit, integration, functional, API and end-to-end tests. See the
[Testing Guide](testing.md) for the layout and the commands.

## Continuous Integration

- The project uses GitHub Actions for CI
- Ensure the tests and the static analysis gate pass before submitting pull requests

## Coding Standards

Poweradmin follows PSR-12 with project-specific modifications. See the
[Coding Standards Guide](coding-standards.md).

## Database Schema Changes

Schema changes ship as SQL scripts in `sql/`, named for the release that introduces them, for
example `poweradmin-mysql-update-to-4.5.0.sql`. A change needs one script per supported database:
MySQL, PostgreSQL and SQLite.

Write them so they can be applied more than once, using `INSERT IGNORE` or
`ON CONFLICT DO NOTHING` and name-based lookups rather than hardcoded IDs.

> **Warning:** Poweradmin must never alter PowerDNS-owned tables such as `domains` and `records`.
> Anything Poweradmin needs to persist belongs in its own tables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests and the quality checks
5. Submit a pull request against the branch named in
   [CONTRIBUTING.md](https://github.com/poweradmin/poweradmin/blob/master/CONTRIBUTING.md)

### Contribution guidelines

1. **Code Quality**: follow the project's style and standards
2. **Testing**: add tests for new functionality and make sure the existing ones pass
3. **Documentation**: user-visible changes deserve a pull request against the
   [poweradmin-docs](https://github.com/poweradmin/poweradmin-docs) repository

### Attribution policy

All meaningful contributions are credited in release notes. Please note:

- Sometimes similar ideas come from multiple contributors; implementation quality determines which is merged
- Contributions may be partially accepted or rewritten to maintain project consistency
- Even if your exact code isn't used, your ideas will still be credited if they influence the final implementation

If you notice your contribution hasn't been acknowledged in the release notes, please reach out. We
want to ensure everyone receives proper recognition.

## Internationalization

- Translation files live in `locale/`
- New user-visible strings must be wrapped in `_()` so they can be translated
- See the [Translations Guide](translations.md)

## Security Considerations

- Always validate user input
- Use prepared statements for database queries, binding `PDO::PARAM_INT` for LIMIT, OFFSET and ID values
- Access request data through the `Request` class rather than `$_GET`, `$_POST` or `$_REQUEST`
- Read session state through `UserContextService` rather than `$_SESSION` directly
- Every POST route is CSRF validated; forms render the token with the `csrf_field()` macro
- Zone ownership is both direct and group-based, so permission checks must cover both
