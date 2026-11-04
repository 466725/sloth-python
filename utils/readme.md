# Utilities

The `utils` package contains shared configuration, database, browser-test,
self-healing locator, logging, integration, and AI-assisted test-generation
helpers. Most modules support the repository's test suites and developer tooling;
they are not a separate application.

## Contents

- [Package map](#package-map)
- [Configuration](#configuration)
- [Database helpers](#database-helpers)
- [Browser and UI test helpers](#browser-and-ui-test-helpers)
- [Self-healing locators](#self-healing-locators)
- [AI-generated UI tests](#ai-generated-ui-tests)
- [Logging](#logging)
- [External integrations](#external-integrations)
- [Tests](#tests)

## Package map

| Package | Responsibility |
| --- | --- |
| [`config/`](config/) | Shared environment-backed settings |
| [`data_base/`](data_base/) | MySQL and DB-API connection/query helpers |
| [`browser/`](browser/) | Playwright and MCP bridge |
| [`self_healing/`](self_healing/) | Fallback locators, DOM similarity, locator persistence, and browser lifecycle |
| [`ai_gen/`](ai_gen/) | AI-assisted pytest/Playwright generation |
| [`observability/`](observability/) | Logging configuration and handlers |
| [`integrations/`](integrations/) | Google Analytics request capture |
| [`qtest_utilities/`](qtest_utilities/) | Optional qTest reporting client |

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

### Playwright and MCP bridge

`utils.browser.MCPPlaywrightHelper` adapts a Playwright page and an async MCP client. It can pass page HTML to `analyze_dom` and `suggest_locator` tools, and can call `validate_event` for analytics payloads. The MCP client is provided by the caller; this package does not start an MCP server.

### Google Analytics capture

`utils.integrations.GoogleAnalyticsTracker` listens to Playwright page requests and stores matching GA4 collect requests. Use `get_events()`, `find_event(name)`, and the assertion helpers to inspect captured event names and parameters. `clear_events()` resets captured data between checks.

## Self-healing locators

[`utils.self_healing`](self_healing/__init__.py) exports synchronous
`find_element(page, key, locator, auto_update=True)` and
`click(page, key, locator, auto_update=True)` helpers for Playwright pages.
They are shared by the Tangerine pytest and Robot suites; there is no separate
root-level `self_healing` package.

### Modules and recovery flow

| Module | Responsibility |
| --- | --- |
| [`element_finder.py`](self_healing/element_finder.py) | Try the primary locator, then fallbacks in order; support `id`, `css`, `xpath`, and `text` strategies |
| [`dom_similarity.py`](self_healing/dom_similarity.py) | Score DOM candidates using text, ID, class, name, ARIA label, and tag; suggest a replacement |
| [`self_healing.py`](self_healing/self_healing.py) | Coordinate recovery and optional persistence; retry failed clicks with Escape and a forced click |
| [`locator_store.py`](self_healing/locator_store.py) | Load keyed JSON definitions and update stored primary locators |
| [`driver_manager.py`](self_healing/driver_manager.py) | Provide the `get_page()` Chromium context manager with browser/context cleanup |

1. Try the primary locator and each fallback; return the first matching locator.
2. If all fail, scan `page.content()` with BeautifulSoup and lxml.
3. Use the locator's `expected` metadata to score candidates. If no candidate
   reaches **0.45**, log the failure and re-raise the original lookup error.
4. Build a locator from the best candidate. With `auto_update=True`, persist it
   as the stored primary locator before returning it.

Self-healing is heuristic, not proof that the intended control was found.
Assert the expected action/result in tests. A healed candidate is not separately
checked for uniqueness or visibility before return, and `click()` may force its
retry past normal actionability checks.

### Use an existing locator

Use an existing synchronous Playwright `page` fixture:

```python
from utils.self_healing import click, find_element
from utils.self_healing.locator_store import get_locator


def test_login_link(page):
    page.goto("https://www.tangerine.ca/en/personal")
    key = "tangerine.login"
    definition = get_locator(key)
    link = find_element(page, key, definition, auto_update=False)
    assert link.is_visible()
    click(page, key, definition, auto_update=False)
```

The live site and browser binaries are required for this example.
`auto_update=False` keeps locator JSON unchanged; the default is **True**, so
review any test-produced locator changes before committing.

### Locator storage

Definitions live in the repository-relative
[locator directory](../tests/pytest_tests/ui_suites/locators/), independent of
the process's working directory:

| Built-in key | File |
| --- | --- |
| `tangerine.login` | [`signinpage.json`](../tests/pytest_tests/ui_suites/locators/signinpage.json) |
| `tangerine.signup` | [`signuppage.json`](../tests/pytest_tests/ui_suites/locators/signuppage.json) |

Each definition has a `primary` strategy, optional ordered `fallbacks`, and
optional `expected` metadata. `load_locators()` merges the default files and
rejects duplicate keys. `get_locator(key, file_path=...)` can read a custom file;
`update_primary_locator(..., file_path=...)` can write one explicitly.
The high-level healing helpers do **not** accept that custom file path: disable
automatic updates when using a definition outside the default store.

The [root self-healing guide](../readme.md#self-healing-framework-playwright)
describes the broader workflow and Robot integration. The
[import/path regression tests](../tests/unit/others/test_self_healing_imports.py)
check public exports, working-directory independence, and Robot library imports
without starting a browser.

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
