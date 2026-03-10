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

### Docker Setup (Selenium Tests)

Running Selenium tests with Docker provides a consistent, isolated browser environment. This project includes a `docker-compose.yml` configuration for easy local testing with selenium/standalone-chrome.

#### Prerequisites

- Docker Desktop installed and running
- docker-compose command available

#### Quick Start

Start the Docker services:
```bash
docker-compose up -d
```

Verify the container is running and healthy:
```bash
docker-compose ps
```

#### Run Selenium Tests with Docker

Set the `SELENIUM_REMOTE_URL` environment variable and run tests:

**Windows (CMD):**
```cmd
set SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
.\.venv\Scripts\python.exe -m pytest pytest_demo/tests/ui/amazon_selenium pytest_demo/tests/ui/tangerine_selenium --tb=short
```

**Windows (PowerShell):**
```powershell
$env:SELENIUM_REMOTE_URL="http://localhost:4444/wd/hub"
.\.venv\Scripts\python.exe -m pytest pytest_demo/tests/ui/amazon_selenium pytest_demo/tests/ui/tangerine_selenium --tb=short
```

**Linux/macOS:**
```bash
export SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
python -m pytest pytest_demo/tests/ui/amazon_selenium pytest_demo/tests/ui/tangerine_selenium --tb=short
```

#### Stop Docker Services

```bash
docker-compose down
```

#### View Docker Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f selenium
```

#### Docker Configuration Details

The `docker-compose.yml` includes:
- **Image**: `selenium/standalone-chrome:18c17c7d95c2`
- **Port**: 4444 (WebDriver protocol)
- **Shared Memory**: 2GB (ensures Chrome stability)
- **Health Check**: Automatic container health monitoring
- **Concurrency**: 3 max instances and 3 max sessions per node

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 4444 already in use | Edit `docker-compose.yml` and change `ports` to `- "5555:4444"`, then set `SELENIUM_REMOTE_URL=http://localhost:5555/wd/hub` |
| Container won't start | Run `docker-compose logs selenium` to check logs; try `docker-compose down` and `docker-compose up -d` again |
| Tests can't connect to Selenium | Verify container is running (`docker-compose ps`), wait 30+ seconds for health check to pass, and confirm environment variable is set |

For more detailed Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

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

## CI/CD Pipeline (GitHub Actions)

This project includes automated testing via GitHub Actions with two distinct workflows:

### Smoke Tests (On PR Merge)

Triggered when a pull request is **merged** to `main` or `master` branch.

**Tests Executed:**
- Unit tests (`pytest -m unit`)
- API tests (`pytest -m api`)
- Robot Framework calculator tests (basic validation)

**Purpose:** Quick validation of critical functionality before code reaches production.

**Execution Time:** ~2-3 minutes

```yaml
trigger: Pull Request merged to main/master
tests: unit + api + robot framework smoke tests
```

### Regression Tests (Nightly Schedule)

Triggered automatically **every night at 2 AM UTC** (configurable via cron in `.github/workflows/ci.yml`).

**Services:**
- selenium/standalone-chrome Docker container (port 4444)
- Shared memory: 2GB

**Tests Executed:**
- All pytest tests (unit, API, Selenium UI, Playwright UI)
- All Robot Framework tests
- Allure report generation
- Test artifacts uploaded

**Environment Variables:**
- `PW_HEADLESS: 1` - Playwright runs in headless mode
- `SELENIUM_REMOTE_URL: http://localhost:4444/wd/hub` - Connect to Docker Selenium grid

**Execution Time:** ~10-15 minutes

**Generated Artifacts:**
- Allure report
- HTML test reports (pytest, Robot Framework)
- Test output XML files

### Workflow Configuration

The workflow is defined in `.github/workflows/ci.yml`:

| Component | Details |
|-----------|---------|
| **Trigger Events** | PR merge to main/master + Nightly schedule (2 AM UTC) |
| **Python Version** | 3.14 |
| **Test Framework** | pytest + Robot Framework |
| **Selenium** | Docker container (standalone-chrome) for nightly runs |
| **Playwright** | Local browser installation for nightly runs |
| **Reporting** | Allure + HTML reports + XML output |
| **Artifacts** | Automatically uploaded to GitHub Actions (30-day retention) |

### How to View Results

1. Navigate to **Actions** tab in GitHub repository
2. Click on a workflow run to see details
3. View test output in the **Logs** section
4. Download test artifacts from the **Artifacts** section

### Modifying the Schedule

To change the nightly test schedule, edit `.github/workflows/ci.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Current: 2 AM UTC daily
    # Examples:
    # - cron: '0 3 * * MON-FRI'  # 3 AM UTC weekdays only
    # - cron: '30 1 * * *'       # 1:30 AM UTC daily
```

Cron format: `minute hour day month day_of_week`

### Local Testing vs CI

| Aspect | Local | CI/CD |
|--------|-------|-------|
| Selenium Tests | Uses local Chrome + chromedriver | Docker selenium grid |
| Playwright | Local browser installation | Auto-installed in pipeline |
| Environment Setup | Manual via docker-compose | Automated via GitHub Actions |
| Reporting | Manual allure command | Auto-generated |
| Artifacts | Local file system | GitHub Actions storage (30 days) |

### CI/CD Best Practices

1. **Keep Smoke Tests Fast**: Only essential unit/API tests on PR merge
2. **Nightly Regression**: Full suite including UI tests via Docker Selenium
3. **Monitor Artifacts**: Download reports from failed runs for debugging
4. **Check Logs**: Always review GitHub Actions logs for detailed error info
5. **Docker Health**: Selenium container includes health checks for reliability
