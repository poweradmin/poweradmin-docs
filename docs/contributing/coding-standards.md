# Poweradmin Coding Standards

Poweradmin follows a set of coding standards based on PSR-12 with some project-specific modifications. This document outlines these standards and how to enforce them.

## Standards Overview

1. **Base Standard**: PSR-12
2. **Modifications**:
   - Excludes the `PSR12.Classes.OpeningBraceSpace` rule
   - Line length set to 250 characters (instead of the PSR-12 default)
3. **Autoloading**: PSR-4 (as specified in `composer.json`)
4. **Type hints and return types**: required on all methods

The rules live in `phpcs.xml` at the repository root.

## Code Quality Tools

### PHP_CodeSniffer (PHPCS/PHPCBF)

Checks for coding standard violations. PHPCBF fixes most of them automatically.

### PHPStan

Static analysis at level 4, with a baseline in `phpstan-baseline.neon`. This is the gate that runs
on pull requests.

### PHP-CS-Fixer

Additional style fixing, complementing PHPCS. Configured in `.php-cs-fixer.php`.

### Psalm

Used for taint analysis rather than as a second type checker, so it is a periodic check rather
than a pull request gate.

### Phan

Checks compatibility with each supported PHP version. Phan catches things PHPStan and Psalm pass
over, in particular docblocks that contradict the signature they document.

## Using the Tools

### Code style

```bash
# Check code style
composer check:all

# Auto-fix what can be fixed
composer format:all

# Run PHP-CS-Fixer
composer style:all
```

### Static analysis

```bash
# PHPStan at level 4 (the pull request gate)
composer analyse:phpstan

# Cognitive complexity, advisory only
composer analyse:complexity

# Psalm taint analysis
composer analyse:taint
```

### PHP version compatibility

```bash
# Check against one target version
composer compat:8.2

# Or all supported versions: 8.2, 8.3, 8.4, 8.5
composer compat:all
```

### Project-specific linters

```bash
# CSRF fields must use the csrf_field() macro, never a raw _token input
composer lint:twig

# templates/default and templates/modern must not drift apart
composer lint:themes

# Playwright assertions must not hide behind existence guards
composer lint:e2e-assertions
```

### Everything at once

```bash
composer analyse:all
```

This runs `check:all`, `analyse:phpstan`, `lint:twig` and `lint:themes`. Run it plus
`composer compat:8.2` before opening a pull request.

## Setting Up Your Development Environment

For a consistent development experience, configure your IDE to use these coding standards:

### PhpStorm

1. Install the PHP_CodeSniffer plugin
2. Configure it to use the project's `phpcs.xml` file
3. Enable "Reformat Code" to use PSR-12 with the project modifications

### VSCode

1. Install the PHP Intelephense or PHP CodeSniffer extensions
2. Configure them to use the project's `phpcs.xml` file

## Pre-Commit Hooks

Consider setting up Git pre-commit hooks to automatically check or fix code style before commits:

1. Install [husky](https://github.com/typicode/husky) and [lint-staged](https://github.com/okonet/lint-staged)
2. Configure lint-staged to run PHP_CodeSniffer or PHP-CS-Fixer on staged PHP files

## Additional Resources

- [PSR-12 Documentation](https://www.php-fig.org/psr/psr-12/)
- [PHP_CodeSniffer Documentation](https://github.com/squizlabs/PHP_CodeSniffer/wiki)
- [PHP-CS-Fixer Documentation](https://github.com/FriendsOfPHP/PHP-CS-Fixer)
- [PHPStan Documentation](https://phpstan.org/user-guide/getting-started)
- [Psalm Documentation](https://psalm.dev/docs/)
- [Phan Documentation](https://github.com/phan/phan/wiki)
