# Reset Admin Password

If the administrator account is locked out and the "Forgot password" flow is not available (no mail configured, no second admin account, lost MFA device), the password can be reset directly in the database.

Poweradmin 4.3.0 and later store passwords as bcrypt, argon2i, or argon2id hashes. The `md5` and `md5salt` algorithms were removed. The active algorithm is set by `security.password_encryption` in `config/settings.php` (default: `bcrypt`).

## 1. Generate a New Password Hash

Run this on the same host as Poweradmin so the PHP version matches. Replace `NewPassword123` with the password you want.

**bcrypt (default):**

```bash
php -r 'echo password_hash("NewPassword123", PASSWORD_BCRYPT, ["cost" => 12]) . "\n";'
```

The `cost` value should match `security.password_cost` in your configuration (default: `12`).

**argon2i:**

```bash
php -r 'echo password_hash("NewPassword123", PASSWORD_ARGON2I) . "\n";'
```

**argon2id:**

```bash
php -r 'echo password_hash("NewPassword123", PASSWORD_ARGON2ID) . "\n";'
```

Copy the resulting hash (it begins with `$2y$`, `$argon2i$`, or `$argon2id$`).

### Legacy versions (Poweradmin 3.x, or 4.2 and older)

The 3.x LTS branch and pre-4.3 releases still accept `md5` and `md5salt` hashes. Use these only if `security.password_encryption` is set to one of those values; otherwise stick with the bcrypt/argon2 commands above.

**md5** (the default on Poweradmin 2.x; 3.x has defaulted to bcrypt since 3.0.0):

```bash
php -r 'echo md5("NewPassword123") . "\n";'
```

**md5salt** (`security.password_encryption = 'md5salt'`):

```bash
php -r '$a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; $salt = ""; for ($i = 0; $i < 5; $i++) { $salt .= $a[random_int(0, 61)]; } echo md5($salt . "NewPassword123") . ":" . $salt . "\n";'
```

The stored format is `md5(salt + password) + ":" + salt`, and the salt format is strict: **exactly 5 characters**, each drawn from `a-z`, `A-Z`, `0-9` or `@#$%^*()_-!`.

> **Warning:** Poweradmin identifies the algorithm by regex-matching the whole stored value against `^[a-f0-9]{32}:[a-zA-Z0-9@#$%^*()_\-!]{5}$` - it does not split on the `:`. A salt of any other length or character set makes the login fail with "Unable to determine hash algorithm", which leaves the account unusable.

## 2. Update the User Record

Open your database client and run the appropriate statement. The `users` table is the same on MySQL/MariaDB, PostgreSQL, and SQLite.

```sql
UPDATE users
SET password = '<paste-hash-here>',
    active = 1,
    use_ldap = 0,
    auth_method = 'sql'
WHERE username = 'admin';
```

Notes:

- Quote the hash with single quotes. Bcrypt and argon2 hashes contain `$` characters but no embedded single quotes, so they are safe inside `'...'`.
- `auth_method` was added in Poweradmin 4.1.0. If your install is older, that column may not exist - drop it from the `SET` clause. The legacy `use_ldap` column has been present since 2.1.7.
- Resetting both `use_ldap = 0` and `auth_method = 'sql'` forces the account back onto local password authentication. Otherwise Poweradmin will continue routing the login through LDAP/SAML/OIDC and ignore the new hash.
- Setting `active = 1` re-enables the account in case it was disabled.

## 3. Clear MFA (Only If You Lost the Device)

If multi-factor authentication is enabled for that user and the second factor is no longer available, disable it before logging in. MFA state lives in the separate `user_mfa` table:

```sql
DELETE FROM user_mfa WHERE user_id = (SELECT id FROM users WHERE username = 'admin');
```

Removing the row is the safest option - the next login will not prompt for a second factor, and you can re-enrol MFA from the user profile afterwards. If you prefer to keep the secret on file (for example to restore it later), update the row instead:

```sql
UPDATE user_mfa
SET enabled = 0
WHERE user_id = (SELECT id FROM users WHERE username = 'admin');
```

## 4. Log In and Change the Password

Log in with the temporary password, then change it through the web UI under your user profile. Poweradmin will re-hash the password using the currently configured algorithm and cost, which keeps the stored hash aligned with `security.password_encryption` and `security.password_cost`.

## Troubleshooting

- **"Invalid username or password" after the update.** Confirm you updated the row for the right account (`SELECT id, username, active, use_ldap FROM users WHERE username = 'admin';`) and that the hash was copied without trailing whitespace or line breaks.
- **PHP `password_hash` not available.** Make sure you are running a supported PHP version: 4.0.x and 4.1.x require PHP 8.1 or newer, and 4.2.0 onwards requires PHP 8.2 or newer.
- **Hash starts with `$1$` or is 32 hex characters.** That is a legacy md5/md5salt hash from an older Poweradmin version. Current releases still verify those hashes at login and re-hash them to the configured algorithm afterwards, so the account is not locked out - only hash generation was removed in 4.3.0. You can still replace it with a bcrypt/argon2 hash using the steps above.
