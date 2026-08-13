# Contributing Translations

Poweradmin uses the GNU gettext system for internationalization. Translation files are stored as `.po` (Portable Object) files in the `locale/` directory.

## Supported Languages

Poweradmin ships 43 locales as of v4.5.0.

| Locale  | Language               | Locale  | Language               |
|---------|------------------------|---------|------------------------|
| ar_SA   | Arabic                 | lt_LT   | Lithuanian             |
| bg_BG   | Bulgarian              | lv_LV   | Latvian                |
| bs_BA   | Bosnian                | ms_MY   | Malay                  |
| cs_CZ   | Czech                  | nb_NO   | Norwegian Bokmål       |
| da_DK   | Danish                 | nl_NL   | Dutch                  |
| de_DE   | German                 | pl_PL   | Polish                 |
| el_GR   | Greek                  | pt_BR   | Portuguese (Brazil)    |
| en_EN   | English                | pt_PT   | Portuguese             |
| es_ES   | Spanish                | ro_RO   | Romanian               |
| et_EE   | Estonian               | ru_RU   | Russian                |
| fa_IR   | Persian                | sk_SK   | Slovak                 |
| fi_FI   | Finnish                | sl_SI   | Slovenian              |
| fr_FR   | French                 | sq_AL   | Albanian               |
| ga_IE   | Irish                  | sr_RS   | Serbian                |
| he_IL   | Hebrew                 | sv_SE   | Swedish                |
| hi_IN   | Hindi                  | th_TH   | Thai                   |
| hr_HR   | Croatian               | tr_TR   | Turkish                |
| hu_HU   | Hungarian              | uk_UA   | Ukrainian              |
| id_ID   | Indonesian             | vi_VN   | Vietnamese             |
| it_IT   | Italian                | zh_CN   | Chinese (Simplified)   |
| ja_JP   | Japanese               | zh_TW   | Chinese (Traditional)  |
| ko_KR   | Korean                 |         |                        |

Arabic, Persian and Hebrew are right-to-left; the interface flips direction for them.

## File Structure

```
locale/
├── i18n-template-php.pot          # Master template (source of truth)
├── en_EN/
│   └── LC_MESSAGES/
│       ├── messages.po            # Translation source file
│       └── messages.mo            # Compiled binary (auto-generated)
├── de_DE/
│   └── LC_MESSAGES/
│       ├── messages.po
│       └── messages.mo
└── ...
```

- **`.pot`** (PO Template) - Master template extracted from source code containing all translatable strings.
- **`.po`** (Portable Object) - Human-editable translation file for each locale.
- **`.mo`** (Machine Object) - Compiled binary used at runtime, generated from `.po` files.

## How to Contribute

### Prerequisites

- A PO file editor such as [Poedit](https://poedit.net/), [Lokalize](https://apps.kde.org/lokalize/), or any text editor
- GNU gettext tools (`msgfmt`) for compiling
- Git for cloning and submitting changes

### Steps

1. **Fork and clone the repository:**

    ```bash
    git clone https://github.com/poweradmin/poweradmin.git
    cd poweradmin
    ```

2. **Open the PO file** for your language, for example German:

    ```
    locale/de_DE/LC_MESSAGES/messages.po
    ```

3. **Translate the strings.** Each entry looks like this:

    ```po
    #: lib/Application/Controller/ZoneController.php:45
    msgid "Zone has been added successfully."
    msgstr "Zone wurde erfolgreich hinzugefügt."
    ```

    - `#:` shows the source file and line where the string is used
    - `msgid` is the original English string (do not modify)
    - `msgstr` is your translation

4. **Handle format strings** carefully. Strings with `%s`, `%d`, or `%1$s` placeholders must keep those placeholders intact:

    ```po
    #, php-format
    msgid "There are %d zones in the database."
    msgstr "Es gibt %d Zonen in der Datenbank."
    ```

5. **Handle plural forms.** Some strings have plural variants:

    ```po
    msgid "One zone"
    msgid_plural "%d zones"
    msgstr[0] "Eine Zone"
    msgstr[1] "%d Zonen"
    ```

    The number of `msgstr[]` entries depends on the language's plural rules defined in the PO file header.

6. **Compile your changes:**

    ```bash
    msgfmt locale/de_DE/LC_MESSAGES/messages.po \
        -o locale/de_DE/LC_MESSAGES/messages.mo
    ```

7. **Submit a pull request** with both the `.po` and `.mo` files.

### Tips

- Preserve HTML tags (`<a>`, `<strong>`, etc.) in translations
- Keep placeholder variables (`%s`, `%d`) in the same order unless using positional syntax (`%1$s`)
- Untranslated strings fall back to English automatically
- Test your translations by switching the language on the login page
- Focus on commonly seen strings first (menu items, buttons, form labels)
- Entries marked `#, fuzzy` need review and are not used at runtime - remove the fuzzy flag after verifying

## Checking Translation Progress

To see how complete a translation is:

```bash
msgfmt --statistics locale/de_DE/LC_MESSAGES/messages.po
```

Output example:

```
2650 translated messages, 45 fuzzy translations, 25 untranslated messages.
```

## Tools

### Poedit

[Poedit](https://poedit.net/) is a cross-platform PO file editor with syntax highlighting, validation, and translation memory. It compiles `.mo` files automatically on save.

### Command-line

```bash
# Compile PO to MO
msgfmt messages.po -o messages.mo

# Check PO file for errors
msgfmt --check messages.po

# Show translation statistics
msgfmt --statistics messages.po
```
