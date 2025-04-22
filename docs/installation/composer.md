# Installation (Composer)

> **Note:** This is an alternative way to install and update Poweradmin using Composer.

## Prerequisites

- PHP 8.1 or higher
- Composer installed on your system
- Required PHP extensions: pdo, pdo_mysql/pdo_pgsql/pdo_sqlite

See [System Requirements](../getting-started/requirements.md) for detailed requirements.

## Installing Poweradmin

To install the latest stable version of Poweradmin, you can use the following Composer command:

```sh
composer create-project --no-dev poweradmin/poweradmin
```

This command will create a poweradmin folder in the current directory, download, and set up Poweradmin without
development dependencies. After running the Composer command, you need to create or modify the configuration file at
`config/settings.php` with your database and application settings.

## Directory Structure

After installation, you should have the following structure:

```
poweradmin/
├── ...
├── config/
│ ├── settings.defaults.php
│ └── settings.php
├── lib/
├── ...
├── vendor/
├── composer.json
└── composer.lock
```

## Basic Configuration

Here is an example of what the `config/settings.php` file should look like:

```php
<?php

return [
    /**
     * Database Settings
     */
    'database' => [
        'host' => 'localhost',
        'name' => 'your_db_name',
        'user' => 'your_db_user',
        'password' => 'your_db_password',
        'type' => 'mysql', // or 'pgsql', 'sqlite'
    ],

    /**
     * Security Settings
     */
    'security' => [
        'session_key' => 'generate_a_strong_random_key_here',
    ],

    /**
     * DNS Settings
     */
    'dns' => [
        'hostmaster' => 'hostmaster.example.com',
        'ns1' => 'ns1.example.com',
        'ns2' => 'ns2.example.com',
    ],
];
```

See [Basic Configuration](../configuration/basic.md) for all available options.

## SQLite Database Settings

If you are using SQLite, modify the database section in the `config/settings.php` file:

```php
'database' => [
    'type' => 'sqlite',
    'file' => '/path/to/your/sqlite.db',
],
```

**Important:** Ensure proper file permissions and directory location for the SQLite database file.

## Updating Poweradmin

If you installed Poweradmin using `composer create-project --no-dev poweradmin/poweradmin`, here's how to update it
later:

1. Navigate to your project directory in the terminal:

```sh
cd /path/to/poweradmin
```

2. If you want to update to a newer version of the Poweradmin package itself, you'll need to modify the version
   constraint in your `composer.json` file, then run the update command. For specifically updating just the Poweradmin
   package:

```sh
composer update poweradmin/poweradmin --no-dev
```

If the project has specific update instructions, check the documentation or GitHub repository for any additional steps
that might be required (such as database migrations).

The `--no-dev` flag ensures that development dependencies aren't installed, keeping your production environment clean,
just like when you initially installed the project.

## Post-Installation Steps

1. Set up the database schema (see [MySQL/MariaDB](../database/mysql-configuration.md), [PostgreSQL](../database/postgresql-configuration.md),
   or [SQLite](../database/sqlite.md) setup)
2. Configure web server permissions
3. Set up initial admin user (see instructions below)
4. Configure PowerDNS connection

## Creating the Initial Admin User Manually

If you're not using the web installer or prefer to set up your admin user directly in the database, follow these steps:

### 1. Generate a password hash

You'll need to create a secure password hash. You can use PHP from the command line to generate one:

```sh
php -r 'echo password_hash("your_secure_password", PASSWORD_DEFAULT) . "\n";'
```

Copy the resulting hash which will look something like:
```
$2y$10$abcdefghijklmnopqrstuOzxLkPHAUXTCg9vRMf/Q4WrCQI3K.0jK
```

### 2. Insert the admin user into the database

#### For MySQL/MariaDB:

```sql
INSERT INTO users 
(username, password, fullname, email, description, perm_templ, active, use_ldap) 
VALUES 
('admin', 'THE_PASSWORD_HASH_YOU_GENERATED', 'Administrator', 'admin@example.com', 'System Administrator', 1, 1, 0);

-- Make the user a super-admin
INSERT INTO perm_items (user_id, perm_id) VALUES (1, 1);
```

#### For PostgreSQL:

```sql
INSERT INTO users 
(username, password, fullname, email, description, perm_templ, active, use_ldap) 
VALUES 
('admin', 'THE_PASSWORD_HASH_YOU_GENERATED', 'Administrator', 'admin@example.com', 'System Administrator', 1, 1, 0);

-- Make the user a super-admin
INSERT INTO perm_items (user_id, perm_id) VALUES (1, 1);
```

#### For SQLite:

```sql
INSERT INTO users 
(username, password, fullname, email, description, perm_templ, active, use_ldap) 
VALUES 
('admin', 'THE_PASSWORD_HASH_YOU_GENERATED', 'Administrator', 'admin@example.com', 'System Administrator', 1, 1, 0);

-- Make the user a super-admin
INSERT INTO perm_items (user_id, perm_id) VALUES (1, 1);
```

### 3. Verify user creation

You should now be able to log in to the PowerAdmin interface with the username 'admin' and the password you created.

## Troubleshooting

For common installation issues and solutions, see [Common Issues](../troubleshooting/common-issues.md).