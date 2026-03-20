# Tangerine Selenium Robot Tests

This suite mirrors the Tangerine UI checks from `pytest_demo/tests/ui/tangerine_selenium` using Robot Framework and Selenium WebDriver.

## Coverage

- Homepage title verification
- Sign-in navigation and title verification
- Sign-up navigation and title verification
- Cookie banner handling in `Test Setup` (`Open Tangerine Homepage`)

## Runtime Behavior

- `Suite Setup`: `Open Browser Session`
- `Test Setup`: `Open Tangerine Homepage`
- `Test Teardown`: `Capture Failure Artifacts`
- `Suite Teardown`: `Close Browser Session`

On failure, screenshot links are logged into Robot `log.html`/`report.html`.

## Running Locally

```powershell
# Headless (default)
robot -d temps/robot_tangerine_selenium robot_demos/tangerine_selenium

# With GUI (PowerShell)
$env:SELENIUM_HEADLESS='0'
robot -d temps/robot_tangerine_selenium robot_demos/tangerine_selenium
```

## Running in CI

The GitHub Actions workflow automatically sets `SELENIUM_REMOTE_URL` to use Selenium Grid:

```powershell
$env:SELENIUM_REMOTE_URL='http://localhost:4444/wd/hub'
robot -d temps/robot_tangerine_selenium robot_demos/tangerine_selenium
```

## Outputs

Robot output files are generated under `temps/robot_tangerine_selenium/`:
- `output.xml`
- `log.html`
- `report.html`

Failure screenshots are saved under:

- `temps/robot_tangerine_selenium/artifacts/selenium_screenshots/`

## Import Path Note

`selenium_keywords.py` auto-adds project root to `sys.path`, so `-P` is optional for standard local runs.

## Dependencies

- Robot Framework 7.0+
- Selenium 4.0+
- Python 3.10+
