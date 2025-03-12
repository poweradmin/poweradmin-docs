# Installation (Composer)

> **Note:** This is an alternative way to install and update Poweradmin using Composer.

## Installing Poweradmin

To install the latest stable version of Poweradmin, you can use the following Composer command:

```sh
composer create-project --no-dev poweradmin/poweradmin
```

This command will create a poweradmin folder in the current directory, download, and set up Poweradmin without
development dependencies. After running the Composer command, you need to create a simple configuration file at
`inc/config.inc.php` with basic database settings.

## Basic Configuration

Here is an example of what the `inc/config.inc.php` file should look like:

```php
<?php
// Database settings
$db_host = 'localhost';
$db_name = 'your_db_name';
$db_user = 'your_db_user';
$db_pass = 'your_db_password';
$db_type = 'mysql'; // or 'pgsql'
```

## SQLite Database Settings

If you are using SQLite, uncomment the following lines in the `inc/config.inc.php` file:

```php
// Database settings for SQLite
$db_type = 'sqlite';
$db_file = '/path/to/your/sqlite.db';
```

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