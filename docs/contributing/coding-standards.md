# PowerAdmin Coding Standards

PowerAdmin follows a set of coding standards based on PSR-12 with some project-specific modifications. This document outlines these standards and how to enforce them.

## Standards Overview

1. **Base Standard**: PSR-12
2. **Modifications**:
   - Excludes PSR12.Classes.OpeningBraceSpace rule
   - Line length set to 250 characters (instead of PSR-12 default)
3. **Autoloading**: PSR-4 (as specified in composer.json)

## Code Quality Tools

PowerAdmin uses several tools to maintain code quality:

### PHP_CodeSniffer (PHPCS/PHPCBF)
- Checks for coding standard violations
- Can automatically fix many issues with PHPCBF

### PHP-CS-Fixer
- Additional code style fixing
- Complements PHPCS for more comprehensive style enforcement

### PHPStan
- Static analysis tool
- Detects potential errors and type inconsistencies

### Psalm
- Type checker
- Configured with level 2 error reporting

### PHPMD (PHP Mess Detector)
- Detects code smells and potential problems
- Helps maintain cleaner, more maintainable code

## Using the Tools

### Running Code Style Checks

```bash
# Check code style for lib directory
composer check:lib

# Check code style for all PHP files
composer check:all
```

### Auto-Fixing Code Style Issues

```bash
# Fix code style in lib directory
composer format:lib

# Fix code style in all PHP files
composer format:all
```

### Running PHP-CS-Fixer

```bash
# Check style with PHP-CS-Fixer
composer style:check

# Fix style with PHP-CS-Fixer
composer style:fix
```

### Static Analysis

```bash
# Run PHPStan static analysis
composer analyse:all

# Run Psalm type checking
composer check:psalm
```

### PHP Mess Detection

```bash
# Run PHPMD
composer check:phpmd:lib
```

## Setting Up Your Development Environment

For a consistent development experience, configure your IDE to use these coding standards:

### PhpStorm

1. Install the PHP_CodeSniffer plugin
2. Configure it to use the project's phpcs.xml file
3. Enable "Reformat Code" to use PSR-12 with project modifications

### VSCode

1. Install the PHP Intelephense or PHP CodeSniffer extensions
2. Configure them to use the project's phpcs.xml file

## Pre-Commit Hooks

Consider setting up Git pre-commit hooks to automatically check/fix code style before commits:

1. Install [husky](https://github.com/typicode/husky) and [lint-staged](https://github.com/okonet/lint-staged)
2. Configure lint-staged to run PHP_CodeSniffer or PHP-CS-Fixer on staged PHP files

## Additional Resources

- [PSR-12 Documentation](https://www.php-fig.org/psr/psr-12/)
- [PHP_CodeSniffer Documentation](https://github.com/squizlabs/PHP_CodeSniffer/wiki)
- [PHP-CS-Fixer Documentation](https://github.com/FriendsOfPHP/PHP-CS-Fixer)
- [PHPStan Documentation](https://phpstan.org/user-guide/getting-started)
- [Psalm Documentation](https://psalm.dev/docs/)