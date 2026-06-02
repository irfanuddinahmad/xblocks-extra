# xblocks-extra

A collection of XBlocks for the Open edX platform.

## Purpose

This repository serves as the consolidated home for several previously standalone XBlock packages, brought together to streamline maintenance and simplify dependency management. These XBlocks are not installed by default in the Open edX platform but can be added as needed. Each XBlock **preserves its original package path** to serve as a drop-in replacement when migrating from the standalone packages.

The following XBlocks have been migrated here from their respective repositories:

- [AudioXBlock](src/audio/README.md) migrated [from](https://github.com/openedx-unsupported/AudioXBlock)
- [FeedbackXBlock](src/feedback/README.rst) migrated [from](https://github.com/openedx/FeedbackXBlock)
- [Free Text Response XBlock](src/freetextresponse/README.rst) migrated [from](https://github.com/openedx/xblock-free-text-response)
- [xblock-image-modal](src/imagemodal/README.rst) migrated [from](https://github.com/openedx-unsupported/xblock-image-modal)
- [xblock-qualtrics-survey](src/qualtricssurvey/README.rst) migrated [from](https://github.com/openedx-unsupported/xblock-qualtrics-survey)
- [xblock-sql-grader](src/sql_grader/README.rst) migrated [from](https://github.com/openedx/xblock-sql-grader)
- [xblock-submit-and-compare](src/submit_and_compare/README.md) migrated [from](https://github.com/openedx-unsupported/xblock-submit-and-compare)

## Migrating from Standalone Packages

If you currently have any of the standalone packages listed above
installed, you should migrate to `xblocks-extra`. 
See the [Migration Guide](docs/how-tos/migrating-process-operator-guidelines.rst) for the instructions.


## Installation

```bash
pip install xblocks-extra
```

## Development

### Prerequisites

- Python 3.12+
- Django 4.2 or 5.2

### Setup

```bash
# Clone the repository
git clone https://github.com/openedx/xblocks-extra.git
cd xblocks-extra

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
make test
```

### Linting

```bash
make lint
make format  # Auto-fix formatting issues
```

## Translating

Internationalization (i18n) is when a program is made aware of multiple languages.
Localization (l10n) is adapting a program to local language and cultural habits.

This project follows [OEP-58](https://docs.openedx.org/en/latest/developers/concepts/oep58.html) for centralized
translation management via the [openedx-translations](https://github.com/openedx/openedx-translations) repository.
The daily extraction workflow in openedx-translations clones this repo, runs `make extract_translations`, and pushes
the combined source `.po` file to Transifex for the translation community to translate.

### Prerequisites

- `edx-i18n-tools` (included in `[dev]` dependencies)
- `gettext` system package (`brew install gettext` on macOS, `sudo apt install gettext` on Ubuntu)

### Translation Workflow

1. **Mark translatable strings** in Python and JavaScript using `gettext` / `ugettext`.
2. **Extract** source strings: `make extract_translations`
3. **Compile** translations: `make compile_translations`

### Make Targets

| Target | Description |
|--------|-------------|
| `extract_translations` | Extract translatable strings from all XBlocks into per-xblock `text.po` files, then merge into a combined `conf/locale/en/LC_MESSAGES/django.po` for OEP-58 |
| `compile_translations` | Compile `.po` files into `.mo` message files for each XBlock |
| `dummy_translations` | Generate dummy (Esperanto) `.po` files for testing |
| `build_dummy_translations` | Extract, generate dummy, and compile translations |
| `validate_translations` | Build dummy translations and detect changed source files |
| `detect_changed_source_translations` | Check if source `.po` files are up-to-date |
| `pull_translations` | Pull translations from Transifex |
| `push_translations` | Extract and push source translations to Transifex |
| `install_transifex_client` | Install the Transifex CLI client |

### How It Works

Each XBlock in `src/` has its own `conf/locale/` directory with a `config.yaml` and `.tx/config`.
During extraction:

1. `i18n_tool extract` runs in each XBlock directory, producing `django.po` (and optionally `djangojs.po`).
2. If `djangojs.po` exists, it is merged into `django.po` using `msgcat`.
3. The merged file is renamed to `text.po`.
4. All per-xblock `text.po` files are combined via `msgcat --use-first` into a single
   `conf/locale/en/LC_MESSAGES/django.po` at the repository root for the openedx-translations pipeline.

### Verifying Translations

```bash
# Dry-run extraction
make extract_translations

# Check the combined output
cat conf/locale/en/LC_MESSAGES/django.po

# Build and test with dummy translations
make build_dummy_translations

# Verify Transifex config (requires tx CLI)
cd src/<xblock_name> && tx status
```

> **Note:** The `.gitignore` ignores `*.po` and `*.mo` files. This is expected — translation source
> files are managed in the [openedx-translations](https://github.com/openedx/openedx-translations)
> repository, not committed here.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](https://openedx.org/contributor-guidelines) before submitting a pull request.

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
