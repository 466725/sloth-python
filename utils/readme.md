# Utilities

The `utils` package contains shared configuration, database, browser-test, logging, integration, and AI-assisted test-generation helpers. Most modules support the repository's test suites and developer tooling; they are not a separate application.

## Contents

- [Configuration](#configuration)
- [Database helpers](#database-helpers)
- [Browser and UI test helpers](#browser-and-ui-test-helpers)
- [AI-generated UI tests](#ai-generated-ui-tests)
- [Logging](#logging)
- [External integrations](#external-integrations)
- [Tests](#tests)

## Configuration

`utils.config.config` loads a shared, immutable settings object from environment variables and the repository-root `.env` file. Modules can import `settings` or call `print_configured_settings()` to inspect non-secret settings:

```powershell
python -m utils.config.config
```

Common settings include:

| Area | Variables | Defaults |
| --- | --- | --- |
| UI target | `TANGERINE_URL`, `UI_LOCALE`, `SLEEP_TIME`, `COOKIE_BANNER_TIMEOUT_SECONDS` | Tangerine personal page, `en-US`, `1`, `5` |
| Playwright | `PW_HEADLESS`, `PW_SLOW_MO` | `false`, `0` |
| Logging | `LOG_LEVEL`, `LOG_FILE`, `LOG_FORMAT`, `LOG_DIRECTORY`, `LOG_MAX_BYTES` | `INFO`, unset, standard timestamp format, `temps/logs`, 500 MiB |
| AI test generation | `AI_GEN_MODEL`, `AI_GEN_BASE_URL`, `AI_GEN_MAX_DOM_CHARS`, `AI_GEN_OUTPUT_DIR` | `gpt-4.1`, OpenAI-compatible endpoint, `12000`, `temps/ai/ai_gen` |
| MySQL | `SLOTH_MYSQL_HOST`, `SLOTH_MYSQL_PORT`, `SLOTH_MYSQL_DB`, `SLOTH_MYSQL_USER`, `SLOTH_MYSQL_PASSWORD` | `localhost`, `3306`, `slothdb`, `slothuser`, empty password |

Boolean settings accept `1/true/yes/on` and `0/false/no/off`; invalid values raise a `ValueError`. The OpenAI base URL is normalized to include `/v1` for `api.openai.com`.

## Database helpers

`utils.data_base` provides reusable helpers for MySQL and DB-API connections, transactions, cursors, and parameterized queries:

- `DatabaseConfig.from_env()` loads MySQL connection settings.
- `connect_mysql()` opens a MySQL connection.
- `connection_scope()` safely opens, commits, rolls back, and closes connections.
- `cursor_scope()` gives direct cursor access for custom SQL handling.
- `execute_sql()`, `fetch_one()`, `fetch_all()`, and `fetch_value()` cover common SQL operations.
- `with_connection()` and `transactional()` wrap functions with managed connections.

The implementation is split between [`db_wrapper.py`](data_base/db_wrapper.py), which contains the connection and query helpers, and [`sql_queries.py`](data_base/sql_queries.py), which contains named SQL statements.

Configure MySQL access with these environment variables (also listed in [Configuration](#configuration)):

```env
SLOTH_MYSQL_HOST=localhost
SLOTH_MYSQL_PORT=3306
SLOTH_MYSQL_DB=slothdb
SLOTH_MYSQL_USER=slothuser
SLOTH_MYSQL_PASSWORD=replace-with-local-password
```

Install `mysql-connector-python` to open MySQL connections. Keep credentials in a local environment file or environment variables, not source control.

### Parameterized SQL

```python
from utils.data_base import connect_mysql, execute_sql, fetch_all

connection = connect_mysql()
try:
    execute_sql(
        connection,
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("Ada Lovelace", "ada@example.com"),
        commit=True,
    )
    rows = fetch_all(
        connection,
        "SELECT id, name FROM users WHERE email = %s",
        ("ada@example.com",),
    )
finally:
    connection.close()
```

### Cursor usage

```python
from utils.data_base import connect_mysql, cursor_scope

connection = connect_mysql()
try:
    with cursor_scope(connection, dictionary=True) as cursor:
        cursor.execute("SELECT id, name FROM users")
        for row in cursor:
            print(row["name"])
finally:
    connection.close()
```

### Transaction wrapper

```python
from utils.data_base import connect_mysql, execute_sql, transactional


@transactional(connect_mysql)
def create_user(name: str, email: str, *, connection):
    execute_sql(
        connection,
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email),
    )
```

## Browser and UI test helpers

### Self-healing locators

`utils.self_healing` exports `find_element` and `click` for Playwright-compatible pages. It tries the configured primary locator and fallbacks first. If those fail, it searches the page DOM for a sufficiently similar candidate, builds a replacement locator, and optionally updates the stored primary locator (`auto_update=True` by default).

Locator definitions live under `tests/pytest_tests/ui_suites/locators/`. The current built-in keys include `tangerine.login` and `tangerine.signup`. Review locator changes produced by a test run before committing them. The root [README's self-healing guide](../readme.md#self-healing-framework-playwright) describes the recovery flow and Robot Framework usage.

### Playwright and MCP bridge

`utils.browser.MCPPlaywrightHelper` adapts a Playwright page and an async MCP client. It can pass page HTML to `analyze_dom` and `suggest_locator` tools, and can call `validate_event` for analytics payloads. The MCP client is provided by the caller; this package does not start an MCP server.

### Google Analytics capture

`utils.integrations.GoogleAnalyticsTracker` listens to Playwright page requests and stores matching GA4 collect requests. Use `get_events()`, `find_event(name)`, and the assertion helpers to inspect captured event names and parameters. `clear_events()` resets captured data between checks.

## AI-generated UI tests

The `utils.ai_gen` CLI captures live browser context and uses an OpenAI-compatible model to draft a pytest + Playwright script. It collects DOM, screenshot, and network context, builds a prompt, normalizes the generated code, and writes the result to disk. Generated tests are starting points; review them before running or committing.

From the repository root, run:

```powershell
python -m utils.ai_gen.cli `
  --url "https://example.com" `
  --goal "Verify the page title and main navigation are visible" `
  --test-name "test_example_navigation" `
  --output "temps/ai/generated_playwright/test_example_navigation.py"
```

CLI options include `--url` and `--goal` (required), `--test-name`, `--output`, `--model`, `--base-url`, and `--headless true|false`. Relative output paths resolve from the repository root. Defaults come from `AI_GEN_*` settings. The CLI requires `OPENAI_API_KEY` or `ANSPIRE_API_KEYS`; credentials must be provided through the environment and kept out of source control. Playwright must be installed in the active Python environment, including its browser binaries.

The `utils.ai_gen.check_ai_gen` package contains small completion/check scripts and its [evaluation prompt](ai_gen/check_ai_gen/check_ai_gen.md).

## Logging

`utils.observability` exports `configure_logging()` and `get_logger()`. By default, logging writes a weekday-named file under `temps/logs`; configure a specific file with `LOG_FILE`, or adjust the directory and size limit with `LOG_DIRECTORY` and `LOG_MAX_BYTES`. The size-limited handler truncates the file when the next message would exceed the configured limit.

## External integrations

- `utils.qtest_utilities.QTestClient` creates qTest test runs and submits test logs. The pytest reporting fixture uses `QTEST_BASE_URL`, `QTEST_PROJECT_ID`, and `QTEST_API_TOKEN`; without those values, the optional qTest path is skipped.

## Tests

Utility-focused unit tests are under `tests/unit/`, including configuration, logging, analytics capture, MCP browser helpers, and AI test generation. Run the repository's Python test instructions from the [testing guide](../tests/testing_guide.md).

