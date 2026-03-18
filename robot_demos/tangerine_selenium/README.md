# Tangerine Selenium Robot Tests

This suite mirrors the Tangerine UI checks from `pytest_demo/tests/ui/tangerine_selenium` using Robot Framework and Selenium WebDriver.

## Architecture

This test suite uses a custom Python library `selenium_keywords.py` that provides Robot Framework keywords for Selenium operations. This approach:

- **Supports CI/CD**: Automatically uses Selenium Grid when `SELENIUM_REMOTE_URL` is set
- **Supports local testing**: Falls back to local Chrome WebDriver
- **Provides proper resource management**: Each test suite gets its own browser instance
- **Mirrors Playwright approach**: Uses the same pattern as `tangerine_playwright/` tests

See `IMPLEMENTATION_NOTES.md` for detailed architecture information.

## Test Coverage

- Homepage title verification
- Sign-in page navigation and title verification
- Sign-up page navigation and title verification
- Cookie banner handling (automatic in `Test Setup`)

Each test file includes:
- **Suite Setup**: `Open Browser Session` - Creates a fresh browser instance
- **Test Setup**: `Open Tangerine Homepage` - Navigates to homepage before each test
- **Suite Teardown**: `Close Browser Session` - Cleans up and captures screenshot

## Running Locally

```bash
# Headless (default)
robot robot_demos/tangerine_selenium

# With GUI
SELENIUM_HEADLESS=0 robot robot_demos/tangerine_selenium
```

## Running in CI

The GitHub Actions workflow automatically sets `SELENIUM_REMOTE_URL` to use Selenium Grid:

```bash
SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub robot robot_demos/tangerine_selenium
```

## Outputs

Robot output files are generated in the current directory:
- `output.xml`
- `log.html`
- `report.html`

When running with `-d temps` flag:
```bash
robot -d temps robot_demos/tangerine_selenium
```

Files are saved to `temps/`:
- `temps/output.xml`
- `temps/log.html`
- `temps/report.html`

## Dependencies

- Robot Framework 7.0+
- Selenium 4.0+
- Python 3.10+
