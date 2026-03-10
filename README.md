# Sloth Python 🦥

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sloth Python is a comprehensive automation and algorithm playground. Designed for the "efficiently lazy," this
repository contains a variety of tools ranging from network security scanners to machine learning implementations and
automated testing suites.

## 🚀 Key Features

- **Network Security:** Built-in Nmap integration for port scanning and host discovery.
- **Algorithms:** Extensive library of algorithms covering machine learning (K-Means), data structures, and more.
- **Gaming & Simulation:** Includes interactive games like Go and Soccer game built with Pygame.
- **Automation:** Support for Robot Framework and Selenium:
    - **Web:** UI testing with Selenium and HTTP/HTTPS testing.
    - **Services:** SOAP & REST API automation.
    - **Databases:** JDBC connectivity.
- **Testing:** `pytest` is included for unit/integration tests (demo available).
- **Performance Testing:** Utilities for load testing many server/protocol types.

## 🛠️ Requirements

- **Python 3.12**
- **Nmap** (Required for the `nmapscanner.py` utility)
- **PyCharm** (Recommended IDE)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sloth-python.git
   cd sloth-python
   ```

2. **Set up a virtual environment:**
   ```bash
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -V
   ```

3. **Install dependencies:**
   ```bash
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **(Optional) Install test dependencies:**
   ```bash
   .\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
   ```

## 🖥️ Usage

### Running Robot Framework Tests

You can execute automated tests using the `.\.venv\Scripts\python.exe -m robot` command. For example, to run the calculator demo:

```bash
.\.venv\Scripts\python.exe -m robot robot_demos\calculator\keyword_driven.robot
```

### Running Selenium Web Automation

The project includes Selenium-based UI automation examples located in `pytest_demo/tests/ui/`. These demos showcase
browser interaction and integration with SauceLabs.

To run all test cases and generate an Allure report:

```bash
.\.venv\Scripts\python.exe -m pytest --alluredir=temps/allure-results --clean-alluredir
.\.venv\Scripts\python.exe -m pytest --reruns 3 --alluredir=temps/allure-results --clean-alluredir
.\.venv\Scripts\python.exe -m pytest -m ui --reruns 3 --reruns-delay 1 --alluredir=temps/allure-results --clean-alluredir
allure generate temps/allure-results -o temps/allure-report --clean
allure serve temps/allure-results
allure open .\temps\allure-report
```

To run only Amazon or only Tangerine related UI tests (folder-based selection):

```bash
# Amazon Playwright only
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\amazon_playwright -m playwright -q

# Tangerine Playwright only
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui\tangerine_playwright -m playwright -q
```

Alternative (keyword-based selection):

```bash
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui -m ui -k amazon
.\.venv\Scripts\python.exe -m pytest pytest_demo\tests\ui -m ui -k tangerine
```

### Run Playwright Tests

The project also includes Playwright UI tests in:

- `pytest_demo/tests/ui/amazon_playwright`
- `pytest_demo/tests/ui/tangerine_playwright`

Install dependencies and browser binaries:

```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

Run only Playwright tests:

```bash
.\.venv\Scripts\python.exe -m pytest -m playwright -q
```

Run Playwright tests with headed browser mode (optional):

```bash
$env:PW_HEADLESS=0
.\.venv\Scripts\python.exe -m pytest -m playwright -q
```

### Self-Healing UI Framework (Playwright)

The Playwright UI tests now use a self-healing locator framework:

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

### Writing logs with `logging` (so they appear in `pytest.log`)

`print()` output does **not** go to `log_file`. If you want messages in `pytest.log`

logger = logging.getLogger(__name__)

def test_something():
logger.info("hello from a test")
assert True


> **Note:** Ensure you have the appropriate WebDriver (e.g., ChromeDriver or GeckoDriver) installed and available in
> your system's PATH, or use a manager like `webdriver-manager` if configured.

> **💡 Tip:** If you want to use the `robot` command directly, ensure your Python `Scripts` directory is in your system's
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
