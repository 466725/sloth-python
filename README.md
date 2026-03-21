# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive automation and algorithms reference project demonstrating modern testing patterns and best practices.

Sloth Python combines robust test automation frameworks (Robot Framework, pytest) with AI-powered self-healing capabilities, comprehensive algorithm implementations, and practical CI/CD integration examples.

## 📌 Key Highlights

- **Advanced Test Automation:** Robot Framework and pytest examples for unit, API, and Playwright-based UI testing
- **Self-Healing Locators:** AI-assisted Playwright framework that automatically detects and repairs broken element selectors
- **Algorithm Library:** Curated implementations of algorithms, data structures, and machine learning concepts
- **Production-Ready CI/CD:** GitHub Actions workflows for automated smoke tests and nightly regression suites
- **Comprehensive Examples:** Real-world test scenarios and automation patterns

## 📦 Prerequisites

- **Python 3.12+** (Tested with Python 3.14)
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
   *Note: This installs the packages used by Robot Framework, pytest, Playwright, and the supporting demo utilities.*

4. **Install Playwright Browsers:**
   ```bash
   playwright install
   ```

## Configuration

Runtime settings are centralized in `utils/config.py` and read from environment variables with safe defaults.

| Variable | Default | Description |
|---|---|---|
| `TANGERINE_URL` | `https://www.tangerine.ca/en/personal` | Base URL for Tangerine UI tests |
| `DEEP_SEEK_URL` | `https://api.deepseek.com` | Base URL for DeepSeek-compatible API calls |
| `OPENAI_URL` | `https://api.openai.com` | Base URL for OpenAI API calls |
| `UI_LOCALE` | `en-US` | Browser locale used by Playwright-based UI tests |
| `SLEEP_TIME` | `1` | Generic sleep duration used in selected fixtures |
| `COOKIE_BANNER_TIMEOUT_SECONDS` | `5` | Wait time for Tangerine cookie banner handling |
| `PW_HEADLESS` | `true` | Playwright headless mode (`1/0`, `true/false`, `yes/no`, `on/off`) |

Quick local check:

```bash
python -m utils.config
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

# Run UI tests
pytest -m ui

# Generate Allure Report
pytest --alluredir=temps/allure-results --clean-alluredir
allure serve temps/allure-results
```

**Unit Test Examples:**
```bash
# Run all unit tests
pytest -m unit

# Run only csv reader unit tests
pytest pytest_demo/tests/unit/test_csv_reader.py -q

# Run one unit test case by node id
pytest pytest_demo/tests/unit/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q
```

**Specific UI Suites:**
```bash
# Tangerine (Playwright Only)
pytest pytest_demo/tests/ui/tangerine_playwright
```

For `pytest_demo/tests/ui/tangerine_playwright`, Playwright records video per test and keeps/attaches it only when a test fails. Videos are written under `temps/playwright-videos/tangerine_playwright/`.

### Robot Framework

Robot Framework demos are located in `robot_demos/`.

**Run All Demos:**
```bash
# Output results under temps/robot_all
python -m robot --outputdir temps/robot_all robot_demos/
```

**Run Specific Suite:**
```bash
python -m robot --outputdir temps/robot_calculator robot_demos/calculator/
python -m robot --outputdir temps/robot_tangerine_playwright robot_demos/tangerine_playwright/
```

**Reports:**
Robot generates `output.xml`, `log.html`, and `report.html` in the selected output directory under `temps/`.

**Artifact behavior (Tangerine suite):**
- `robot_demos/tangerine_playwright`: failed tests log screenshot links under `artifacts/playwright/screenshots/`
- `robot_demos/tangerine_playwright`: failed tests log video links under `artifacts/playwright/videos/` (passed-test videos are cleaned up)

**Import path note:**
The Tangerine Robot keyword libraries self-bootstrap the project root import path, so running with `-P` is optional for normal local usage.

## 🤖 Self-Healing Framework (Playwright)

This project includes an advanced self-healing mechanism for Playwright-based UI tests that automatically detects and repairs broken locators.

**Location:** `pytest_demo/self_healing/`
**Locator Store:**
- `pytest_demo/locators/signinpage.json`
- `pytest_demo/locators/signuppage.json`

### How It Works

1. **Primary Locator Failure** → Framework attempts primary locator
2. **Backup Locators** → Tries backup selectors from locator store
3. **DOM Scanning** → Scans page DOM for similar elements using fuzzy matching
4. **Auto-Update** → If a match is found, test passes and the page-specific locator file is automatically updated
5. **Resilience** → Subsequent test runs use the updated selector

### Benefits

- **Reduced Maintenance:** Eliminates manual locator fixes after UI changes
- **Improved Stability:** Tests are more resilient to minor DOM alterations
- **Smart Learning:** System learns from failures and improves over time

## 🔄 CI/CD Pipeline & Automation

Automated testing is orchestrated through GitHub Actions workflows to ensure code quality and early defect detection.

### Workflow Overview

**Smoke Tests (On Pull Request)**
- Runs on every PR merge
- Includes: Unit tests, API tests, and basic Robot Framework suites
- Duration: ~5-10 minutes
- Provides fast feedback on code changes

**Nightly Regression Suite (2 AM UTC)**
- Comprehensive test execution
- Includes: Playwright UI tests, API tests, and integration tests
- Generates Allure reports
- Duration: ~30-45 minutes

### Test Artifacts

All test reports and logs are uploaded to GitHub Actions run artifacts:
- Retention period: 30 days
- Available in the "Artifacts" section of completed workflow runs
- Includes: HTML reports, Allure data, logs, and screenshots

### Viewing Reports

1. Navigate to the workflow run on GitHub
2. Download the artifacts zip file
3. Extract and open `report.html` in your browser

### Local CI/CD Simulation

Use these commands to mimic the core CI flow locally (see `Running Tests` for more command variants):

```bash
# Run smoke tests
pytest -m "unit or api"

# Run full regression
pytest -m "not slow"
```

## 📂 Project Structure

```
sloth-python/
├── algorithms/                  # Algorithms & Data Structures
│   ├── backtracking/           # Backtracking algorithms
│   ├── divide_and_conquer/     # Divide & conquer patterns
│   ├── machine_learning/       # ML implementations (KNN, SVM, Decision Trees, etc.)
│   ├── maths/                  # Mathematical algorithms
│   ├── searches/               # Search algorithms (binary, linear, etc.)
│   ├── sorts/                  # Sorting algorithms
│   ├── strings/                # String manipulation algorithms
│   ├── conversions/            # Number system conversions
│   └── data_structures/        # Trees, heaps, queues, stacks, tries, etc.
│
├── pytest_demo/                 # Pytest Test Suite
│   ├── tests/                  # Test cases
│   │   ├── unit/               # Unit tests
│   │   ├── api/                # API tests (Requests)
│   │   └── ui/                 # UI tests
│   │       └── tangerine_playwright/
│   ├── self_healing/           # Self-healing Playwright framework
│   ├── locators/               # Locator repository (signinpage.json, signuppage.json)
│   ├── conftest.py             # Pytest fixtures & configuration
│   └── pytest.ini              # Pytest settings
│
├── robot_demos/                 # Robot Framework Test Suites
│   ├── calculator/             # Calculator test suite
│   └── tangerine_playwright/   # Tangerine UI suite (custom Playwright library)
│
├── fun_part/                    # Educational & Fun Examples
│   ├── go_game/                # Game implementations
│   ├── bilibili/               # API demo projects
│   └── web_programming/        # Web examples
│
├── utils/                       # Shared Utilities
│   ├── config.py               # Configuration management
│   ├── constants.py            # Application constants
│   └── csv_reader.py           # CSV utilities
│
├── .github/workflows/          # GitHub Actions CI/CD definitions
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── pyproject.toml              # Project metadata
└── README.md                   # This file
```

### Key Directories Explained

- **algorithms/** - Production-ready implementations for learning and reference
- **pytest_demo/** - Complete test automation examples with best practices
- **robot_demos/** - Keyword-driven test automation patterns
- **utils/** - Reusable components (config, constants, helpers)

---

## 🎓 Best Practices & Patterns

This project demonstrates industry best practices:

### Test Automation Patterns
- **Page Object Model (POM)** - Maintainable UI test structure
- **Fixtures & Dependency Injection** - Pytest fixtures for test setup/teardown
- **Marker-Based Organization** - Categorize tests (unit, api, ui, slow, etc.)
- **Parameterization** - Run same test with multiple data sets
- **Self-Healing** - AI-powered locator recovery mechanism

### Code Quality
- **Type Hints** - Type annotations for better IDE support and documentation
- **Docstrings** - Comprehensive module and function documentation
- **Error Handling** - Proper exception handling and logging
- **Configuration Management** - Externalized config for different environments
- **DRY Principle** - Reusable utilities and helper functions

### CI/CD & DevOps
- **Automated Testing** - Smoke tests on PRs, full regression nightly
- **Report Generation** - HTML and Allure reports for test visibility
- **Artifact Management** - Retained for compliance and debugging

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError" when running tests**
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue: Playwright tests timeout**
```bash
# Solution: Install browsers and check network connectivity
playwright install
pytest pytest_demo/tests/ui/tangerine_playwright --timeout=30000
```

**Issue: Locator selector not found in Playwright**
- The self-healing mechanism should auto-fix this
- Check `pytest_demo/locators/signinpage.json` and `pytest_demo/locators/signuppage.json` for updated selectors
- Manual fix: Update the JSON or run with `-v` flag for detailed logs

## 📖 Documentation & Resources

### Test Frameworks
- [Pytest Documentation](https://docs.pytest.org/)
- [Robot Framework User Guide](https://robotframework.org/robotframework/#introduction)
- [Playwright Python API](https://playwright.dev/python/)

### Technologies
- [Python Official Documentation](https://docs.python.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Related Tools
- [Allure Report Framework](https://docs.qameta.io/allure/)
- [Pytest HTML Plugin](https://pytest-html.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow PEP 8** style guidelines
3. **Add tests** for new functionality
4. **Run the test suite** locally before submitting PR
5. **Update documentation** as needed
6. **Submit a pull request** with clear description of changes

### Development Setup

```bash
# Complete initial setup first (see Installation), then:

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, test, and commit
pytest  # Run tests
git commit -m "feat: describe your changes"
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 📝 License

This project is licensed under the **MIT License**.

The MIT License permits:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

With the conditions:
- ⚠️ License and copyright notice must be included

## 📧 Support & Feedback

### Getting Help

- **GitHub Issues** - Report bugs and request features
- **Discussions** - Ask questions and share ideas
- **Documentation** - Check `README.md` and inline code comments for implementation details

### Reporting Bugs

When reporting bugs, please include:
1. Python version and OS
2. Steps to reproduce
3. Expected vs actual behavior
4. Relevant logs or screenshots

### Feature Requests

Please include:
1. The problem you're trying to solve
2. Proposed solution or use case
3. Alternative approaches considered

---

## ⭐ Acknowledgments

Built with modern Python testing tools and best practices.
