# Poweradmin Development Guide

## Development Environment Setup

### Prerequisites
- PHP 8.1 or higher
- MySQL, PostgreSQL, or SQLite
- Composer
- Node.js and NPM (for frontend assets)
- PowerDNS server (for testing)

### Installation for Development

**1. Clone the repository:**

```
git clone https://github.com/poweradmin/poweradmin.git
cd poweradmin
```

**2. Install dependencies:**

```
composer install
npm install
```

**3. Configure the application:**

- Copy `config/settings.defaults.php` to a new file in the same directory
- Modify the settings according to your environment

## Project Structure

### Core Components
- **lib/**: Core library code
  - **Application/**: Controllers, services, and application logic
  - **Domain/**: Domain models and business logic
  - **Infrastructure/**: Database, API clients, and external services

### Frontend
- **assets/**: JavaScript and CSS files
- **style/**: CSS files (ignite.css, spark.css)
- **templates/**: HTML templates

### Testing
- **tests/**: Test files
  - **unit/**: Unit tests
  - **integration/**: Integration tests
  - **plans/**: Test plans

- **cypress/**: End-to-end tests

## Documentation

Some documentation can be generated from the source code using phpDocumentor.

To generate the documentation, run the following command:

```bash
phive install phpDocumentor
composer run docs
```

The documentation will be generated in the `docs` directory.

## Testing

Poweradmin has comprehensive testing support including unit tests, integration tests, and end-to-end tests. For detailed information on testing methodologies, frameworks, and running tests, please see the [Testing Guide](testing.md).

## Continuous Integration
- The project uses GitHub Actions for CI/CD
- Ensure all tests pass before submitting pull requests

## Coding Standards
Poweradmin follows PSR-12 with project-specific modifications. For detailed information on coding standards, tools for code quality, and how to enforce them, see the [Coding Standards Guide](coding-standards.md).

## Database Migrations

- Database migrations are managed with Phinx
- See `db/migrations/` for existing migrations
- Create new migrations with:

```
./vendor/bin/phinx create MyNewMigration
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure coding standards
5. Submit a pull request

### Contribution Guidelines

1. **Code Quality**: Ensure your code follows the project's style and standards
2. **Testing**: Test your changes thoroughly before submitting
3. **Documentation**: Include appropriate documentation for new features

### Attribution Policy

All meaningful contributions are credited in release notes. Please note:

- Sometimes similar ideas come from multiple contributors; implementation quality determines which is merged
- Contributions may be partially accepted or rewritten to maintain project consistency
- Even if your exact code isn't used, your ideas will still be credited if they influence the final implementation

If you notice your contribution hasn't been acknowledged in the release notes, please reach out - we want to ensure everyone receives proper recognition.

## Internationalization
- Translation files are in the `locale/` directory
- New strings should be wrapped in `_()` for translation

## Security Considerations
- Always validate user input
- Use prepared statements for database queries
- Follow secure coding practices
- Use CSRF tokens for forms
