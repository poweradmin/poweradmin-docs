# Poweradmin Testing Guide

## Overview
This document outlines the testing strategy and implementation details for the Poweradmin project.

## Test Frameworks & Tools

- **PHPUnit**: Primary testing framework for PHP code
- **Cypress**: End-to-end testing framework for UI testing

In addition to these testing frameworks, Poweradmin uses various code quality tools that are described in detail in the [Coding Standards Guide](coding-standards.md), including PHPStan, PHP_CodeSniffer, Psalm, PHPMD, and PHP-CS-Fixer.

## Test Directory Structure

```
/tests
├── integration - Integration tests
├── plans       - Test plans documentation
└── unit        - Unit tests

/cypress
├── e2e         - End-to-end test specs by feature
├── fixtures    - Test data files
└── support     - Cypress support and custom commands
```

## Types of Tests

### Unit Tests
Located in `/tests/unit`, these tests verify individual components in isolation, focusing on:
- Configuration management
- DNS record handling and formatting
- Router functionality
- IP address validation and handling
- User authentication and password encryption
- Various utility and helper functions

### Integration Tests
Located in `/tests/integration`, testing interactions between components, particularly database operations.

### End-to-End Tests
Located in `/cypress/e2e`, organized by feature:

#### Main Feature Tests
- **Authentication** - Login and form validation
- **User Management** - Creating, editing, and deleting users
- **Zone Management** - Adding master/slave zones and records
- **Record Management** - Adding, editing, and deleting different record types
- **Zone Templates** - Template creation and application
- **Search** - Zone and record searching

#### Corner Case Tests
- **Input Validation** - Testing edge cases in form validation
- **Error Handling** - Session management, security, and UI edge cases

The Cypress tests are located in the `cypress/e2e` directory organized by feature.

A complete test plan for UI testing is available in `tests/plans/cypress-ui-test-plan.md`.

### Manual Test Plans
Documentation in `/tests/plans` outlining test procedures for:
- UI testing (`tests/plans/cypress-ui-test-plan.md`)
- Installer testing (`tests/plans/installer-test-plan.md`) - Covers both regular installation flows and corner cases for properly testing the Poweradmin installation process

## Running Tests

### PHP Tests
```bash
# Run unit tests
composer tests

# Run integration tests
composer tests:integration
```

### Cypress Tests
```bash
# Open Cypress Test Runner
npm run cypress:open
# or
yarn cypress:open

# Run Cypress tests headlessly
npm run cypress:run
# or
yarn cypress:run
```

### Code Quality Checks
For running code quality checks, please refer to the [Coding Standards Guide](coding-standards.md) for detailed command usage.

## CI/CD Integration

The test suite is integrated with CI/CD pipelines to ensure code quality and prevent regressions.

## Test Coverage

Current test coverage focuses on:
- Core DNS management functionality
- User authentication and management
- Configuration validation
- UI workflows through Cypress tests

## Contributing Tests

When adding new features or fixing bugs:
1. Add appropriate unit tests for new classes and methods
2. Update or add Cypress tests for UI changes
3. Run the full test suite before submitting PRs
4. Ensure all code quality checks pass