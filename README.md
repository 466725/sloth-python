# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sloth Python is an automation and algorithm playground. It serves as a reference project for modern test automation patterns, featuring Robot Framework, pytest (UI/API), and a custom self-healing Playwright framework.

## 🚀 Key Features

- **Test Automation:**
  - **Robot Framework:** Keyword-driven testing with Selenium, Requests, and DataDriver.
  - **Pytest:** Comprehensive suite covering Unit, API, and Web UI testing.
  - **Web UI:** Examples using both **Selenium** and **Playwright**.
  - **Self-Healing:** A custom Playwright implementation that automatically repairs broken locators.
- **Algorithms & Math:** Implementations of common algorithms, data structures, and ML basics.
- **Tools:** Network security utilities (Nmap) and fun demos.

## 📋 Prerequisites

- **Python 3.12+** (Project is tested on 3.14)
- **Git**

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sloth-python.git
   cd sloth-python
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   py -3.14 -m venv .venv
   .\.venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This installs all necessary packages for Robot Framework, Pytest, Playwright, and Selenium.*

4. **Install Playwright Browsers:**
   ```bash
   playwright install
   ```

## 🏃 Running Tests

### Pytest (Unit, API, UI)

The project uses `pytest` as the primary test runner. Configuration is handled in `pytest.ini`.

**Common Commands:**
```bash
# Run all tests
pytest

# Run only Unit and API tests (Fast)
pytest -m "unit or api"

# Run UI tests (Selenium & Playwright)
pytest -m ui

# Generate Allure Report
pytest --alluredir=temps/allure-results --clean-alluredir
allure serve temps/allure-results
```

**Specific UI Suites:**
```bash
# Tangerine Website (Selenium & Playwright)
pytest pytest_demo/tests/ui/tangerine_selenium pytest_demo/tests/ui/tangerine_playwright

# Tangerine (Selenium Only)
pytest pytest_demo/tests/ui/tangerine_selenium

# Tangerine (Playwright Only)
pytest pytest_demo/tests/ui/tangerine_playwright
```

### Robot Framework

Robot Framework demos are located in `robot_demos/`.

**Run All Demos:**
```bash
# Output results to 'temps' directory
python -m robot --outputdir temps robot_demos/
```

**Run Specific Suite:**
```bash
python -m robot --outputdir temps robot_demos/calculator/
```

**Reports:**
Checking `temps/` folder for `log.html`, `report.html`, and `output.xml`.

## 🧠 Self-Healing Framework (Playwright)

This project features a self-healing mechanism for Playwright UI tests.
- **Location:** `pytest_demo/self_healing/`
- **Locator Store:** `pytest_demo/locators/locators.json`

**How it works:**
1. If a primary locator fails, the framework tries backup locators.
2. If those fail, it scans the DOM for similar elements.
3. If a match is found, the test passes, and `locators.json` is updated automatically.

## 🐳 Docker Support (Selenium)

You can run Selenium tests in a Docker container to ensure a consistent environment.

1. **Start Selenium Grid:**
   ```bash
   docker-compose up -d
   ```

2. **Run Tests against Docker:**
   ```bash
   # Windows (PowerShell)
   $env:SELENIUM_REMOTE_URL="http://localhost:4444/wd/hub"
   pytest pytest_demo/tests/ui/tangerine_selenium --tb=short

   # Linux/Mac
   export SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
   pytest pytest_demo/tests/ui/tangerine_selenium --tb=short
   ```

3. **Stop Services:**
   ```bash
   docker-compose down
   ```

## 🔄 CI/CD Pipeline

Automated testing is handled via GitHub Actions:

- **Smoke Tests (PR Merge):** Runs Unit, API, and basic Robot tests.
- **Nightly Regression (2 AM UTC):** Runs the full suite (including UI tests via Docker and Playwright) and generates Allure reports.

**Artifacts:** Test reports are uploaded to GitHub Actions run artifacts (retained for 30 days).

## 📂 Project Structure

```text
sloth-python/
├── algorithms/          # Data structures & ML algorithms
├── pytest_demo/         # Pytest suite
│   ├── tests/           # Unit, API, and UI tests
│   ├── self_healing/    # Self-healing engine
│   └── locators/        # JSON locator store
├── robot_demos/         # Robot Framework suites
├── utils/               # Shared utilities (Config, Constants)
├── .github/workflows/   # CI/CD definitions
├── docker-compose.yml   # Selenium Grid config
├── requirements.txt     # Project dependencies
└── README.md            # You are here
```
