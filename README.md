# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/466725/sloth-python/actions/workflows/ci.yml/badge.svg)](https://github.com/466725/sloth-python/actions/workflows/ci.yml)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/466725)

A comprehensive automation and algorithms reference project demonstrating modern testing patterns and best practices.

**Sloth Python** is an educational and professional-grade project combining:
- 🧪 **Advanced test automation frameworks** (Robot Framework, pytest, Playwright)
- 🤖 **AI-powered self-healing test locators** that automatically repair broken selectors
- 🏗️ **Comprehensive algorithm library** (data structures, ML, divide & conquer, and more)
- ⚙️ **Production-ready CI/CD workflows** using GitHub Actions
- 🔧 **AI-driven test script generation** from natural-language goals using MCP

Perfect for learning modern test automation, exploring algorithms, or as a reference for professional test frameworks.

## 📚 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#️-installation)
- [Getting Started as a Contributor](GETTING_STARTED.md)
- [Configuration](#configuration)
- [Running Tests](#-running-tests)
- [Self-Healing Framework](#-self-healing-framework-playwright)
- [AI-Generated Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp)
- [CI/CD Pipeline](#️-cicd-pipeline--automation)
- [Project Structure](#-project-structure)
- [Best Practices](#-best-practices--patterns)
- [Troubleshooting](#-troubleshooting)
- [Documentation](#-documentation--resources)
- [Contributing](#-contributing)
- [License](#-license)
- [Support & Feedback](#-support--feedback)

## 📌 Key Highlights

- **Advanced Test Automation:** Robot Framework and pytest examples for unit, API, and Playwright-based UI testing
- **Self-Healing Locators:** AI-assisted Playwright framework that automatically detects and repairs broken element selectors
- **AI Test Script Generation:** MCP-aware Playwright workflow that generates runnable pytest UI tests from natural-language goals
- **Algorithm Library:** Curated implementations of algorithms, data structures, and machine learning concepts
- **Production-Ready CI/CD:** GitHub Actions workflows for automated smoke tests and nightly regression suites
- **Comprehensive Examples:** Real-world test scenarios and automation patterns

## 📦 Prerequisites

- **Python 3.12+** (Tested with Python 3.14)
- **Git**

## 🚀 Quick Start

**New to open source?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) for a beginner-friendly guide.

**Want to contribute?** Start with the [Contributing Guide](CONTRIBUTING.md).

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/466725/sloth-python.git
   cd sloth-python
   ```

## 🛠️ Installation

2. **Create and activate a virtual environment:**
   **Windows (PowerShell):**
   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\activate
   ```

   **Linux/macOS (bash/zsh):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   *Note: This installs the packages used by Robot Framework, pytest, Playwright, and the supporting demo utilities.*

4. **Install Playwright Browsers:**
   ```powershell
   playwright install
   ```

## Configuration

Runtime settings are centralized in `utils/config.py` and read from environment variables with safe defaults.

| Variable | Default                                     | Description |
|---|---------------------------------------------|---|
| `TANGERINE_URL` | `https://www.tangerine.ca/en/personal`      | Base URL for Tangerine UI tests |
| `DEEP_SEEK_URL` | `https://api.deepseek.com`                  | Base URL for DeepSeek-compatible API calls |
| `OPENAI_URL` | `https://api.openai.com`                    | Base URL for OpenAI API calls |
| `UI_LOCALE` | `en-US`                                     | Browser locale used by Playwright-based UI tests |
| `SLEEP_TIME` | `1`                                         | Generic sleep duration used in selected fixtures |
| `COOKIE_BANNER_TIMEOUT_SECONDS` | `5`                                         | Wait time for Tangerine cookie banner handling |
| `PW_HEADLESS` | `true`                                      | Playwright headless mode (`1/0`, `true/false`, `yes/no`, `on/off`) |
| `AI_GEN_MODEL` | `gpt-4.1`                                   | Model used by the UI test generator |
| `AI_GEN_BASE_URL` | `OPENAI_URL` value                          | OpenAI-compatible base URL used by generator |
| `AI_GEN_MAX_DOM_CHARS` | `12000`                                     | Max DOM/element-tree size sent to the model |
| `AI_GEN_OUTPUT_DIR` | `pytest_demo/tests/ai/generated_playwright` | Default output folder for generated tests |

Quick local check:

```powershell
python -m utils.config
```

## 🏃 Running Tests

### Pytest (Unit, API, UI)

The project uses `pytest` as the primary test runner. Configuration is handled in `pytest.ini`.

**Common Commands:**
```powershell
# Run all tests
python -m pytest

# Run only Unit and API tests (Fast)
python -m pytest -m "unit or api"

# Run UI tests
python -m pytest -m ui

# Generate Allure Report
python -m pytest --alluredir=temps/allure-results --clean-alluredir
allure serve temps/allure-results
```

**Unit Test Examples:**
```powershell
# Run all unit tests
python -m pytest -m unit

# Run only csv reader unit tests
python -m pytest pytest_demo/tests/unit/test_csv_reader.py -q

# Run one unit test case by node id
python -m pytest pytest_demo/tests/unit/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q
```

**Specific UI Suites:**
```powershell
# Tangerine (Playwright Only)
python -m pytest pytest_demo/tests/ui/tangerine_playwright
```

For `pytest_demo/tests/ui/tangerine_playwright`, Playwright records video per test and keeps/attaches it only when a test fails. Videos are written under `temps/playwright-videos/tangerine_playwright/`.

### API Testing Approaches (3 Styles)

This project demonstrates three ways to test APIs. They target different needs and can coexist in the same repo.

| Approach | Location                                     | Strengths | Trade-offs |
|---|----------------------------------------------|---|---|
| Pytest + pure Python (`requests` / SDK) | `test_deep_seek_api.py`                      | Maximum flexibility, strongest Python debugging, easy fixture/parametrize patterns | Less business-readable for non-Python users |
| Robot + Python keyword library | `deep_seek_api_hybrid_test.robot` + `deep_seek_keywords.py` | Readable Robot test flow with reusable Python logic for complex handling | Requires maintaining both `.robot` and `.py` layers |
| Robot-only (`RequestsLibrary`) | `deep_seek_api_test.robot`                   | Fully keyword-driven API checks, easy for Robot-focused contributors | Complex payload/assertion logic can become verbose in `.robot` |

**When to use which:**
- Use **Pytest + Python** when API logic is complex (custom retries, advanced validation, reusable helpers).
- Use **Robot + Python keyword** when you want readable Robot scenarios but still need Python power behind keywords.
- Use **Robot-only RequestsLibrary** for straightforward request/response checks and fully keyword-driven demos.

**Run commands:**
```powershell
# Pytest API demo
python -m pytest -q pytest_demo/tests/api/test_deep_seek_api.py

# Robot API demo (Robot + Python keyword library)
python -m robot --outputdir temps/robot_api robot_demo/api/deep_seek_api_hybrid_test.robot

# Robot API demo (Robot-only RequestsLibrary)
python -m robot --outputdir temps/robot_api robot_demo/api/deep_seek_api_test.robot
```

All DeepSeek demos use `OPENAI_API_KEY`; `DEEP_SEEK_URL` is optional and defaults to `https://api.deepseek.com`.

### AI-Generated UI Scripts (Python + Playwright + MCP + AI)

#### Playwright Recording & Execution Workflow

Use this quick workflow to create and debug Tangerine UI tests.

**1) Record interactions with Playwright Codegen**

`codegen` opens a real browser and records your actions (clicking, typing, navigation). It is useful for discovering stable locators and generating starter snippets.

```powershell
python -m playwright codegen https://www.tangerine.ca/en/personal
```

**What to expect:**
- A browser opens at the target URL.
- Playwright Inspector shows generated Python actions as you interact.
- You can copy the generated steps into your pytest test, then improve locators/assertions before committing.

**2) Run your pytest + Playwright test file**

After creating or refining a test, run it in headed mode with slow motion for visual debugging.

```powershell
python -m pytest pytest_demo/tests/ui/tangerine_playwright/test_codegen_demo.py --headed --slowmo 200
```

**Option details:**
- `--headed`: runs with visible browser UI (not headless)
- `--slowmo 200`: adds ~200 ms delay between actions for easier observation

**Typical use cases:**
- Validate a new test created from Codegen output
- Debug flaky UI interactions step by step
- Demo test behavior to teammates

> Note: This project uses **Python pytest + Playwright**. Use `python -m pytest ...` for execution (not `npx playwright test`).

For generation commands, model configuration, and MCP context details, see [AI-Generated UI Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp).

### Robot Framework

Robot Framework demos are located in `robot_demo/`.

#### Tangerine Playwright Robot Suite

The suite under `robot_demo/tangerine_playwright/` mirrors the Tangerine UI coverage from `pytest_demo/tests/ui/tangerine_playwright`.

**Included checks:**
- Homepage title validation
- Sign-in navigation title validation
- Sign-up navigation title validation

**Suite lifecycle:**
- `Suite Setup`: `Open Browser Session`
- `Test Setup`: `Open Tangerine Homepage`
- `Test Teardown`: `Capture Failure Artifacts`
- `Suite Teardown`: `Close Browser Session`

The shared `Test Setup` always opens the Tangerine homepage and accepts the cookie banner when it is present.

**Run All Demos:**
```powershell
# Output results under temps/robot_all
python -m robot --outputdir temps/robot_all robot_demo/
```

**Run Specific Suite:**
```powershell
python -m robot --outputdir temps/robot_calculator robot_demo/calculator/
python -m robot --outputdir temps/robot_tangerine_playwright robot_demo/tangerine_playwright/
```

**Optional dry run (syntax and keyword wiring only):**
```powershell
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot_demo/tangerine_playwright/
```

**Reports:**
Robot generates `output.xml`, `log.html`, and `report.html` in the selected output directory under `temps/`.

**Artifact behavior (Tangerine suite):**
- For `temps/robot_tangerine_playwright/`, failure screenshots are saved under `artifacts/playwright/screenshots/`
- For `temps/robot_tangerine_playwright/`, failure videos are saved under `artifacts/playwright/videos/`
- Screenshot and video links are logged into Robot `log.html` / `report.html`
- Passed-test videos are deleted to reduce artifact size

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

### Robot Tangerine Suite Scope

The Robot suite in `robot_demo/tangerine_playwright/` uses the same self-healing locator store, but limits healing to these keys in the Playwright keywords:

- `tangerine.login`
- `tangerine.signup`

Locator definitions are shared from:

- `pytest_demo/locators/signinpage.json`
- `pytest_demo/locators/signuppage.json`

Robot mode currently runs with read-only healing (`auto_update=False`) so it can recover using stored locator strategies without silently rewriting the locator files.

## 🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)

An AI-powered pipeline that generates runnable pytest + Playwright test scripts from natural-language goals and live page context.

**How it works:** Playwright captures the page (DOM, screenshot, network events) → context is packaged into a structured prompt → an OpenAI-compatible model generates Python test code → the file is written to `pytest_demo/tests/ai/generated_playwright/`.

**Location:** `pytest_demo/ai_generation/` — modules: `mcp_context.py`, `prompt_builder.py`, `ai_client.py`, `generator.py`, `cli.py`

### Prerequisites

- `OPENAI_API_KEY` set (supports OpenAI, DeepSeek, Azure, OpenRouter, or any OpenAI-compatible endpoint)
- Dependencies installed: `pip install -r requirements.txt`
- Playwright browsers installed: `playwright install`

### Quick Start

```powershell
# 1. Set your API key
$env:OPENAI_API_KEY = "<your-api-key>"

# 2. Generate a test from a live page
python -m pytest_demo.ai_generation.cli `
  --url  "https://www.tangerine.ca/en/personal" `
  --goal "Verify homepage loads and Sign In button is visible" `
  --test-name "test_tangerine_homepage" `
  --output "pytest_demo/tests/ai/generated_playwright/test_tangerine_homepage.py"

# 3. Run the generated test
python -m pytest -q pytest_demo/tests/ai/generated_playwright/test_tangerine_homepage.py
```

### CLI Reference

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | *(required)* | Target page URL |
| `--goal` | *(required)* | Natural-language test goal |
| `--test-name` | `test_generated_ui_flow` | Generated function name |
| `--output` | `AI_GEN_OUTPUT_DIR` | Output file path |
| `--model` | `gpt-4.1` | LLM model name |
| `--base-url` | `OPENAI_URL` | OpenAI-compatible endpoint |
| `--headless` | `true` | Run Playwright headless (`true`/`false`) |

### More Examples

```powershell
# Sign-in page
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/app/#/login" `
  --goal "Verify username/password fields and submit button are present" `
  --test-name "test_tangerine_signin"

# Sign-up page
python -m pytest_demo.ai_generation.cli `
  --url "https://www.tangerine.ca/app/#/signup" `
  --goal "Verify sign-up form is visible and required fields are present" `
  --test-name "test_tangerine_signup"

# Run all generated tests
python -m pytest -q pytest_demo/tests/ai/generated_playwright
```

### Configuration

Key environment variables (see [Configuration](#configuration) for full list):

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_GEN_MODEL` | `gpt-4.1` | LLM model identifier |
| `AI_GEN_BASE_URL` | OpenAI endpoint | API base URL |
| `AI_GEN_MAX_DOM_CHARS` | `12000` | Max DOM size sent to the model |
| `AI_GEN_OUTPUT_DIR` | `pytest_demo/tests/ai/generated_playwright` | Output folder |

### Notes

- **Review before committing** — AI output is a strong starting point, not production-ready by default
- **Model choice** — `gpt-4.1` for best quality; `gpt-4.1-mini` for cost savings
- **Large pages** — DOM is truncated at `AI_GEN_MAX_DOM_CHARS`; increase if needed
- **Self-healing** — Generated tests are plain pytest files; wrap with self-healing helpers manually if needed
- **Validate with:** `python -m pytest -q pytest_demo/tests/ai/test_ai_generation.py`

## 🔄 CI/CD Pipeline & Automation

Automated testing is orchestrated through GitHub Actions workflows to ensure code quality and early defect detection.

### Workflow Overview

**Smoke Tests (Push + Pull Request)**
- Run on pushes to `main` / `master`
- Run on pull requests targeting `main` / `master` while the PR is open
- Include pytest `unit` + `api` coverage and the Robot calculator suite
- Provide fast feedback on core regressions

**Nightly Regression Suite (2 AM UTC)**
- Runs from the scheduled workflow at `0 2 * * *`
- Installs Playwright browsers with dependencies
- Executes the full pytest suite and all Robot suites
- Attempts Allure report generation after the test run

### Test Artifacts

The workflow uploads generated reports when available in the run's **Artifacts** section, including:
- `allure-report/`
- `temps/log.html`
- `temps/report.html`
- `temps/output.xml`

### Viewing Reports

1. Navigate to the workflow run on GitHub
2. Download the artifacts zip file
3. Extract and open `report.html` in your browser

### Local CI/CD Simulation

Use these commands to mimic the core CI flow locally (see `Running Tests` for more command variants):

```powershell
# Run smoke tests
python -m pytest -m "unit or api"
python -m robot robot_demo/calculator/

# Run a nightly-like full pass
playwright install
python -m pytest --tb=short --maxfail=5
python -m robot --outputdir temps robot_demo/
```

## 📂 Project Structure

```
sloth-python/
├── algorithms/                 # Algorithms & Data Structures
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
├── pytest_demo/                # Pytest Test Suite
│   ├── ai_generation/          # AI + MCP context driven script generator
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
│   └── ...
│
├── robot_demo/                 # Robot Framework demo suites (API/UI/keyword patterns)
│   ├── api/                    # API demos (Robot-only RequestsLibrary and Robot + Python keywords)
│   ├── calculator/             # Calculator test suite
│   └── tangerine_playwright/   # Tangerine UI suite (custom Playwright library)
│
├── fun_part/                   # Educational & Fun Examples
│   ├── go_game/                # Game implementations
│   ├── bilibili/               # API demo projects
│   └── web_programming/        # Web examples
│
├── utils/                      # Shared Utilities
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
- **robot_demo/** - Robot demo suites for API and UI automation patterns
- **utils/** - Reusable components (config, constants, helpers)

---

## 🎓 Best Practices & Patterns

This project demonstrates industry best practices:

### Test Automation Patterns
- **Page Object Model (POM)** - Maintainable UI test structure
- **Fixtures & Dependency Injection** - Pytest fixtures for test setup/teardown
- **Marker-Based Organization** - Categorize tests with markers such as `unit`, `api`, `ui`, and `playwright`
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
- **Artifact Management** - Uploaded for debugging and report review

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError" when running tests**
**Windows (PowerShell):**
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/macOS (bash/zsh):**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Issue: Playwright tests timeout**
```powershell
# Solution: Install browsers and retry a focused UI suite first
playwright install
python -m pytest pytest_demo/tests/ui/tangerine_playwright -q
```

**Issue: Locator selector not found in Playwright**
- If the test uses the self-healing helpers, the framework may recover automatically
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

## ❤️ Support This Project

If you find **Sloth Python** useful — whether for learning, professional automation, or as a reference — please consider sponsoring!

Your support helps fund:
- 🛠️ Ongoing maintenance and new features
- 🤖 AI/Playwright tooling improvements
- 📚 More algorithm and test examples
- ⏱️ Faster responses to issues and PRs

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github&style=for-the-badge)](https://github.com/sponsors/466725)

Even a small monthly contribution makes a big difference. Thank you! 🙏

---

## 🤝 Contributing

Contributions are welcome and appreciated! Whether you're fixing bugs, adding features, improving documentation, or sharing new algorithm implementations, we'd love your help.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch** with a descriptive name:
   ```powershell
   git checkout -b feature/add-new-algorithm
   git checkout -b fix/self-healing-bug
   git checkout -b docs/improve-readme
   ```
3. **Make your changes** and ensure code quality:
   - Follow **PEP 8** style guidelines
   - Add **type hints** for new functions
   - Include **docstrings** and comments
   - Write **unit tests** for new functionality
4. **Test your changes** locally:
   ```powershell
   python -m pytest -m "unit or api"  # Quick smoke test
   python -m pytest --tb=short          # Full test suite
   ```
5. **Commit with clear messages**:
   ```powershell
   git commit -m "feat: add new sorting algorithm"
   git commit -m "fix: correct self-healing locator logic"
   ```
6. **Push your branch** and **create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues (e.g., `Fixes #42`)
   - Explanation of changes and why they're needed

### Areas for Contribution

- **Algorithms** - New algorithm implementations in `algorithms/` (with tests)
- **Test Automation** - Enhanced Robot Framework keywords, new UI test examples
- **Self-Healing** - Improvements to the locator recovery mechanism
- **AI Generation** - Enhancements to the MCP-driven test generator
- **Documentation** - README updates, code examples, tutorials
- **CI/CD** - Workflow improvements, additional test coverage

### Development Workflow

```powershell
# Complete initial setup first (see Installation), then:

# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Install dependencies (if adding new packages)
pip install -r requirements.txt

# Make your changes and test
python -m pytest
python -m robot robot_demo/calculator/

# Commit and push
git add .
git commit -m "feat: describe your changes"
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Code Standards

- **Python** - PEP 8, type hints, docstrings
- **Tests** - Pytest or Robot Framework with clear naming
- **Documentation** - Updated README.md or inline comments for complex logic
- **Commit Messages** - Clear, concise, use conventional commits (feat:, fix:, docs:, etc.)

### Questions or Need Help?

- **GitHub Discussions** - Ask questions and share ideas
- **GitHub Issues** - Report bugs or request features
- **Check existing issues** - Your question might already be answered

Thank you for contributing! 🙌

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

- **[GitHub Issues](https://github.com/466725/sloth-python/issues)** - Report bugs and request features
- **[GitHub Discussions](https://github.com/466725/sloth-python/discussions)** - Ask questions, share ideas, and discuss best practices
- **Documentation** - Check `README.md` and inline code comments for implementation details
- **Example Tests** - Review `pytest_demo/` and `robot_demo/` for working examples

### Reporting Bugs

Found a bug? Please open an issue with:
1. **Python version** and **OS** (e.g., Python 3.14 on Windows 11)
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **Error message** and stack trace (if applicable)
5. **Environment details** (e.g., Playwright version, headless/headed mode)

### Feature Requests

Have an idea for improvement? Open an issue with:
1. **Clear description** of the feature or problem
2. **Proposed solution** or use case
3. **Alternative approaches** you've considered (if any)
4. **Examples** or code snippets showing the idea

### Discussions

Have questions or want to discuss testing strategies? Use **GitHub Discussions** to:
- Share test automation patterns and best practices
- Get advice on test framework choices
- Discuss algorithm implementations
- Connect with other contributors

We actively monitor both Issues and Discussions—your feedback helps improve this project!

---

## 📋 Project Governance

### Community & Contribution Resources

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed guidelines for contributing code, algorithms, or documentation
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards and expectations for respectful interaction
- **[SECURITY.md](SECURITY.md)** - How to responsibly report security vulnerabilities
- **[ISSUES_AND_PULL_REQUESTS.md](ISSUES_AND_PULL_REQUESTS.md)** - Templates and guidelines for issues and PRs

### GitHub Issue Templates

We provide issue templates to streamline reporting:
- **Bug Reports** - For issues and problems
- **Feature Requests** - For new functionality ideas
- **Documentation** - For improvements to docs
- **Questions** - For general inquiries (consider using Discussions instead)

---

## ⭐ Acknowledgments

### Built With

- [Python](https://www.python.org/) - Programming language
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Playwright](https://playwright.dev/python/) - Modern browser automation
- [Robot Framework](https://robotframework.org/) - Keyword-driven testing
- [OpenAI API](https://openai.com/api/) - AI-powered test generation

### Inspiration & References

This project draws on industry best practices from:
- Test automation communities
- Software engineering principles
- Algorithm research and implementations

### Community

We welcome feedback, contributions, and ideas from the community. If you find this project useful, please consider:
- ⭐ Starring the repository
- 🔗 Sharing it with others
- 🤝 Contributing improvements
- 💬 Providing feedback via Issues or Discussions
