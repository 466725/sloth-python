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
| `AI_GEN_MODEL` | `gpt-4.1` | Model used by the UI test generator |
| `AI_GEN_BASE_URL` | `OPENAI_URL` value | OpenAI-compatible base URL used by generator |
| `AI_GEN_MAX_DOM_CHARS` | `12000` | Max DOM/element-tree size sent to the model |
| `AI_GEN_OUTPUT_DIR` | `pytest_demo/tests/AI/generated_playwright` | Default output folder for generated tests |

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

### AI-Generated UI Scripts (Python + Playwright + MCP + AI)

The project now includes an AI generator that:

- Captures live page context with Playwright
- Packages it in an MCP-style payload (DOM, element tree, screenshot, network events)
- Sends your goal + context to an OpenAI-compatible model
- Writes a runnable pytest + Playwright test file

Set API key:

```powershell
$env:OPENAI_API_KEY = "<your-key>"
```

Generate a Tangerine test script:

```powershell
python -m pytest_demo.ai_generation.cli --url "https://www.tangerine.ca/en" --goal "Verify the homepage loads and sign-in entry point is visible" --test-name "test_tangerine_homepage_generated" --output "pytest_demo/tests/AI/generated_playwright/test_tangerine_homepage_generated.py"
```

Run generated tests:

```powershell
pytest -q pytest_demo/tests/AI/generated_playwright
```

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

## 🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)

This project includes an AI-powered test generation system that automatically creates pytest + Playwright test scripts from live page context.

### How It Works

The system follows a 6-step end-to-end workflow:

1. **Browser Automation** - Playwright opens the target page
2. **Context Collection** - MCP-style context is captured (DOM, screenshots, network events)
3. **Prompt Construction** - Context + goal are packaged into a structured prompt
4. **AI Generation** - OpenAI-compatible model generates Python test code
5. **Code Normalization** - Output is cleaned, validated, and formatted
6. **File Output** - Runnable test file is written to `pytest_demo/tests/AI/generated_playwright/`

### Prerequisites for AI Generation

- `OPENAI_API_KEY` environment variable must be set
- All dependencies in `requirements.txt` installed (includes `mcp` and `openai`)
- Playwright browsers installed: `playwright install`

### Quick Start: Generate Your First Test

**Step 1: Set your API key**

```powershell
$env:OPENAI_API_KEY = "<your-openai-api-key>"
```

Supports OpenAI-compatible endpoints:
- OpenAI (default)
- DeepSeek
- Azure OpenAI
- Other OpenAI API clones

**Step 2: Generate a test (example: Tangerine homepage)**

```powershell
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/en/personal" `
  --goal "Verify homepage loads and Sign In button is visible" `
  --test-name "test_tangerine_homepage" `
  --output "pytest_demo/tests/AI/generated_playwright/test_tangerine_homepage.py"
```

**Step 3: Run the generated test**

```powershell
pytest -q pytest_demo/tests/AI/generated_playwright/test_tangerine_homepage.py
```

### CLI Reference

```
python -m pytest_demo.ai_generation.cli [OPTIONS]

Options:
  --url TEXT              Target page URL (required)
  --goal TEXT             Natural language test goal (required)
  --test-name TEXT        Generated function name (default: test_generated_ui_flow)
  --output TEXT           Output file path (uses AI_GEN_OUTPUT_DIR by default)
  --model TEXT            LLM model name (default: gpt-4.1)
  --base-url TEXT         OpenAI-compatible endpoint (default: OPENAI_URL)
  --headless {true,false} Run Playwright headless (default: from PW_HEADLESS)
  --help                  Show help message
```

### Example Commands

**Generate homepage test:**
```powershell
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/en/personal" `
  --goal "Verify homepage loads and Sign In entry point is visible" `
  --test-name "test_tangerine_homepage"
```

**Generate sign-in page test:**
```powershell
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/app/#/login" `
  --goal "Verify sign-in page loads and username/password fields are present" `
  --test-name "test_tangerine_signin"
```

**Generate sign-up page test:**
```powershell
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/app/#/signup" `
  --goal "Verify sign-up page loads and registration form is visible" `
  --test-name "test_tangerine_signup"
```

**Run all generated tests:**
```powershell
pytest -q pytest_demo/tests/AI/generated_playwright
```

### Configuration

AI generation settings are read from `utils/config.py` and environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_GEN_MODEL` | `gpt-4.1` | LLM model identifier |
| `AI_GEN_BASE_URL` | OpenAI endpoint | API base URL (OpenAI-compatible) |
| `AI_GEN_MAX_DOM_CHARS` | `12000` | Max DOM size sent to model |
| `AI_GEN_OUTPUT_DIR` | `pytest_demo/tests/AI/generated_playwright` | Default output folder |

Override defaults via environment variables:

```powershell
$env:AI_GEN_MODEL = "gpt-4.1-mini"
$env:AI_GEN_BASE_URL = "https://api.deepseek.com"
$env:AI_GEN_OUTPUT_DIR = "pytest_demo/tests/AI/my_generated_tests"
```

### Modules & Architecture

| Module | Purpose |
|--------|---------|
| `mcp_context.py` | Collects Playwright page context (MCP protocol) |
| `prompt_builder.py` | Constructs structured prompts for the AI model |
| `ai_client.py` | OpenAI-compatible chat client |
| `generator.py` | Orchestrates generation: context → AI → file |
| `cli.py` | Command-line interface for test generation |

Location: `pytest_demo/ai_generation/`

### Example Generated Test

When you run the generator with the homepage goal, it produces:

```python
from playwright.sync_api import Page
import pytest

@pytest.mark.ui
def test_tangerine_homepage(page: Page):
    page.goto("https://www.tangerine.ca/en/personal", wait_until="domcontentloaded")
    
    # Verify page loads with correct title
    assert page.title() == "Tangerine"
    
    # Verify Sign In button is visible
    login_button = page.locator("#login")
    assert login_button.is_visible()
    
    # Verify main heading is present
    heading = page.locator("h1")
    assert heading.is_visible()
    assert "Welcome" in heading.text_content()
```

**Key features of generated tests:**

- ✅ Fully runnable pytest + Playwright code
- ✅ Uses resilient locator strategies (id, css, text)
- ✅ Includes meaningful assertions based on page context
- ✅ Safe fallback template if AI response is malformed
- ✅ Automatically adds missing imports
- ✅ Ready to integrate with CI/CD

### Integration with Self-Healing

Generated tests work seamlessly with the self-healing framework:

1. Generated tests use stable locators from the live page
2. If locators break over time, self-healing automatically repairs them
3. Updated selectors are saved to `pytest_demo/locators/*.json`
4. Subsequent test runs use the healed locators

### Testing & Validation

The feature includes full unit test coverage:

```powershell
pytest -q pytest_demo/tests/AI/test_ai_generation.py
```

Tests validate:
- Prompt structure includes goal and MCP context
- Code extraction from markdown blocks
- Fallback template generation
- Configuration defaults and overrides
- CLI argument parsing

### Notes & Best Practices

- **API Costs**: OpenAI API calls are charged per token. Monitor usage during testing.
- **Model Selection**: `gpt-4.1` recommended for best results; `gpt-4.1-mini` for cost savings
- **Headless Mode**: Use `--headless false` during development to watch test generation
- **DOM Size**: Large pages (>12000 chars) are truncated. Adjust with `AI_GEN_MAX_DOM_CHARS`
- **Test Quality**: Review generated tests before committing. AI is powerful but not perfect.
- **Custom Endpoints**: Use `--base-url` for DeepSeek, Azure, or self-hosted OpenAI clones

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
│   ├── ai_generation/           # AI + MCP context driven script generator
│   ├── tests/                  # Test cases
│   │   ├── AI/                 # AI-generation tests and generated Playwright scripts
│   │   │   └── generated_playwright/
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
