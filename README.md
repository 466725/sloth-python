# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sloth Python is an automation and algorithm playground. It includes Robot Framework demos, pytest UI/API examples,
and a small self-healing Playwright locator framework.

## Key Features

- Network security utilities (Nmap integration).
- Algorithms and data structures (machine learning demos included).
- Gaming and simulation (Pygame demos).
- Automation:
  - Robot Framework demos
  - Selenium UI automation demos
  - Playwright UI automation demos
- Testing: pytest demos (UI, API, unit).

## Requirements

- Python (project uses a `.venv` virtual environment)
- Nmap (only required for the Nmap utilities)
- Optional (depending on what you run):
  - WebDriver binaries (for Selenium UI tests)
  - Allure CLI (for Allure report generation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sloth-python.git
   cd sloth-python
   ```

2. Create a virtual environment:
   ```bash
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -V
   ```

3. Install dependencies:
   ```bash
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

Notes:
- `requirements.txt` includes Robot Framework and SeleniumLibrary.
- Some Robot Framework libraries below are optional extras depending on your needs.

## Usage

### Robot Framework

Robot Framework demos live in `robot_demos/`.

#### IDE Support (PyCharm)

For editing `.robot` files in PyCharm, install the JetBrains plugin: **Robot Framework Support** (syntax highlighting, completion, and navigation).

Core install:
```bash
.\.venv\Scripts\python.exe -m pip install robotframework
```

Run Robot suites:
```bash
# Run a single suite
.\.venv\Scripts\python.exe -m robot robot_demos\calculator\keyword_driven.robot

# Run all demos and write outputs to a dedicated folder
.\.venv\Scripts\python.exe -m robot -d temps\robot-results robot_demos
```

Robot outputs (generated automatically):
- `log.html`
- `report.html`
- `output.xml`

#### Web UI Automation

Option A (modern, recommended): Browser Library (Playwright)
```bash
.\.venv\Scripts\python.exe -m pip install robotframework-browser
.\.venv\Scripts\rfbrowser.exe init
```

Notes:
- Browser Library uses Playwright under the hood (stable, auto-waiting, fast).
- `rfbrowser init` downloads Node.js + Playwright browser binaries (first run can take a while).

Option B (classic): SeleniumLibrary (already in `requirements.txt`)
```bash
.\.venv\Scripts\python.exe -m pip install robotframework-seleniumlibrary
```

Example keywords:
```robot
Open Browser    https://example.com    chrome
Click Element   id=login
```

#### API Testing (REST)

```bash
.\.venv\Scripts\python.exe -m pip install robotframework-requests
```

Example keywords (RequestsLibrary):
```robot
GET    https://api.example.com/users
Status Should Be    200
```

#### Mobile Automation

```bash
.\.venv\Scripts\python.exe -m pip install robotframework-appiumlibrary
```

Uses Appium to automate Android and iOS apps.

#### Data-Driven Testing

```bash
.\.venv\Scripts\python.exe -m pip install robotframework-datadriver
```

DataDriver can generate multiple test cases from CSV/Excel inputs (useful for login/validation/API coverage).

#### Reports and Integrations

Robot generates `log.html`, `report.html`, and `output.xml` by default.

Optional integration:
```bash
.\.venv\Scripts\python.exe -m pip install robotframework-reportportal
```

#### Helpful Developer Tools

```bash
.\.venv\Scripts\python.exe -m pip install robotframework-tidy
.\.venv\Scripts\python.exe -m pip install robotframework-lsp
```

Recommended modern stack:
```bash
.\.venv\Scripts\python.exe -m pip install robotframework robotframework-browser robotframework-requests robotframework-datadriver
```

### Pytest UI Automation (Selenium)

Selenium-based UI automation examples are located in `pytest_demo/tests/ui/`.

To run all test cases and generate an Allure report:
```bash
.\.venv\Scripts\python.exe -m pytest --alluredir=temps/allure-results --clean-alluredir
.\.venv\Scripts\python.exe -m pytest --reruns 3 --alluredir=temps/allure-results --clean-alluredir
.\.venv\Scripts\python.exe -m pytest -m ui --reruns 3 --reruns-delay 1 --alluredir=temps/allure-results --clean-alluredir
allure generate temps/allure-results -o temps/allure-report --clean
allure serve temps/allure-results
allure open .\temps\allure-report
```

Run only Amazon or only Tangerine related UI tests (folder-based selection):
```bash
# Amazon only (Selenium + Playwright)
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\amazon_selenium pytest_demo\tests\ui\amazon_playwright -m ui

# Tangerine only (Selenium + Playwright)
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\tangerine_selenium pytest_demo\tests\ui\tangerine_playwright -m ui

# Amazon Playwright only
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\amazon_playwright -m playwright -q

# Tangerine Playwright only
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\tangerine_playwright -m playwright -q
```

Alternative (keyword-based selection with `-k`):
```bash
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui -m ui -k amazon
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui -m ui -k tangerine
```

> Note: Ensure you have the appropriate WebDriver (e.g., ChromeDriver or GeckoDriver) installed and available in your
> system PATH, or use a manager like `webdriver-manager` if configured.

### Playwright Tests

Playwright UI tests are in:
- `pytest_demo/tests/ui/amazon_playwright`
- `pytest_demo/tests/ui/tangerine_playwright`

Install browser binaries:
```bash
.\.venv\Scripts\python.exe -m playwright install chromium
```

Run only Playwright tests:
```bash
.\.venv\Scripts\python.exe -m pytest -m playwright -q
```

Run Playwright tests with headed browser mode:
```bash
$env:PW_HEADLESS=0
.\.venv\Scripts\python.exe -m pytest -m playwright -q
```

### Self-Healing UI Framework (Playwright)

The Playwright UI tests include a self-healing locator framework:
- Framework modules: `pytest_demo/self_healing/`
- Central locator store: `pytest_demo/locators/locators.json`
- Target test packages:
  - `pytest_demo/tests/ui/amazon_playwright`
  - `pytest_demo/tests/ui/tangerine_playwright`

Self-healing flow:
1. Try primary locator.
2. Try configured fallback locators.
3. If all fail, run DOM similarity scan.
4. If a close match is found, generate a new locator and auto-update `locators.json`.

Run self-healing Playwright tests:
```bash
.\.venv\Scripts\python.exe -m pytest -m playwright -q
```

### Writing Logs with `logging` (so they appear in `pytest.log`)

`print()` output does not go to pytest `log_file`. Use Python logging instead:

```python
import logging

logger = logging.getLogger(__name__)

def test_something():
    logger.info("hello from a test")
    assert True
```

Tip: if you want to use `robot`/`pytest` commands directly, activate the virtual environment so `.venv\Scripts` is on
your PATH.
