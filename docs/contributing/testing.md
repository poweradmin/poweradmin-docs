# Poweradmin Testing Guide

## Overview

This document outlines the testing strategy and implementation details for the Poweradmin project.

## Test Frameworks and Tools

- **PHPUnit**: unit, integration and functional tests
- **Playwright**: end-to-end browser tests

Poweradmin also uses several code quality tools, described in the
[Coding Standards Guide](coding-standards.md): PHPCS, PHPStan, PHP-CS-Fixer, Psalm and Phan.

## Test Directory Structure

```
/tests
├── unit        - Unit tests
├── integration - Integration tests (need a database)
├── functional  - Functional tests
├── api         - Public API v2 test scripts, driven by run-tests.sh
├── sql         - Schema and migration checks
├── docker      - Docker image tests
└── helpers     - Shared test helpers

/playwright
├── tests       - End-to-end specs, one directory per feature
├── fixtures    - Test data
├── helpers     - Login and other shared steps
└── tools       - Maintenance scripts, not part of the suite
```

## Types of Tests

### Unit Tests

Located in `tests/unit`, these verify individual components in isolation: DNS record validation and
formatting, IP address handling, routing, configuration, password hashing, permission logic, and
the various services and value objects.

### Integration Tests

Located in `tests/integration`, testing interactions between components, particularly database
operations. These need a running database, which the devcontainer provides.

### Functional Tests

Located in `tests/functional`, exercising whole request flows rather than single classes.

### End-to-End Tests

Located in `playwright/tests`, organised by feature, covering areas including authentication, user
and group management, zones and records, zone templates, DNSSEC, API keys, bulk operations, search,
the installer, and error and corner cases.

### API Tests

`tests/api` holds shell-driven tests for the public API v2, run against a live instance through
`tests/api/run-tests.sh`.

## Running Tests

### PHP tests

```bash
# Unit tests
composer tests

# Integration tests (requires a database, e.g. the devcontainer)
composer tests:integration

# Functional tests
composer tests:functional

# Every PHPUnit suite
composer tests:all
```

### End-to-end tests

The Playwright suite runs against a live instance, so start the devcontainer first. `BASE_URL`
selects which instance to hit.

```bash
# Install the browsers once
npx playwright install

# Run against the default instance
npm run test:e2e

# Or target a specific backend
npm run test:e2e:mysql      # http://localhost:8080
npm run test:e2e:pgsql      # http://localhost:8081
npm run test:e2e:sqlite     # http://localhost:8082

# Interactive runner, headed browser, and the last HTML report
npm run test:e2e:ui
npm run test:e2e:headed
npm run test:e2e:report
```

> **Note:** The suite shares one database per instance, so run it with `--workers=1` unless you are
> targeting separate instances. Parallel workers on a single instance interfere with each other.

### API tests

```bash
npm run test:api            # against MySQL
npm run test:api:pgsql
npm run test:api:sqlite
```

### Code quality checks

See the [Coding Standards Guide](coding-standards.md) for the full command list.

## CI/CD Integration

GitHub Actions runs the PHPUnit suites and the static analysis gate on pull requests. Make sure
both pass locally before submitting.

## Contributing Tests

When adding new features or fixing bugs:

1. Add unit tests for new classes and methods
2. Add or update Playwright specs for UI changes
3. Run the full test suite before submitting a pull request
4. Ensure the code quality checks pass

> **Note:** An assertion placed inside an existence guard can never fail, so it tests nothing.
> `composer lint:e2e-assertions` rejects that pattern in Playwright specs.
