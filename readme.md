# Sloth Python

<a id="documentation-index"></a>
## 📚 Documentation Index

Find project guides, feature documentation, development references, and
learning material by topic. Several feature guides now live beside the
application documentation that owns them.

## Project guides

- [Project README](readme.md) — overview, setup, configuration, and primary
  workflows.
- [Repository development guide](contributing.md) — contribution conventions,
  validation guidance, review workflows, and release practices.
- [AI Stock package guide](ai_stock/readme.md) — analysis flow and backend
  package responsibilities.
- [LLM provider configuration](ai_stock/llm/llm-providers.md) — provider
  setup, channels, YAML routing, and connection troubleshooting.
- [OpenAPI schema snapshot](api/api_spec.json) — checked-in API schema used
  by contract tests; the running service also exposes `/openapi.json`.
- [DSA Web guide](apps/dsa-web/readme.md) — Web routes, development, and
  product guides for Web-facing features.

## Product and feature guides

- [Alert Center](apps/dsa-web/readme.md#alert-center) — alert rules,
  evaluation, notifications, and rollback behavior.
- [Email notifications](apps/dsa-web/readme.md#email-notifications) — SMTP
  setup, recipient groups, routing, and delivery diagnostics.
- [Stock autocomplete catalog](apps/dsa-web/readme.md#stock-autocomplete-catalog)
  — local search, remote refresh, and bundled catalog maintenance.
- [Analysis Context Pack](apps/dsa-web/readme.md#analysis-context-pack) —
  analysis inputs, data-quality metadata, prompt summaries, and public overview.
- [Stock Analyzer skill](apps/dsa-web/readme.md#stock-analyzer-skill) —
  built-in skill behavior and custom skill directories.

## Development and testing

- [Testing guide](tests/testing_guide.md) — commands and guidance for pytest,
  Robot Framework, Vitest, Cypress, and Playwright.
- [macOS development environment setup](tests/setup_mac_dev_env.md) —
  Java, Python, Node.js, IDE, and JMeter setup on macOS.
- [Playwright test package guide](apps/dsa-web-playwright-tests/Readme.md) —
  browser test setup and coverage.
- [Cypress test package guide](apps/dsa-web-cypress-tests/Readme.md) —
  browser test setup and coverage.
- [Utilities guide](utils/readme.md) — shared configuration, database helpers,
  browser testing, logging, integrations, and AI test generation.
- [Load runner best practices](tests/performance/load_runner/load_runner_best_practices.md)
  — performance test asset guidance.
- [Playwright locator strategy](<tests/pytest_tests/ui_suites/tangerine/Playwright Locator Strategy Guide.md>)
  — locator selection guidance for UI automation.
- [JSON locator tradeoffs](tests/pytest_tests/ui_suites/locators/Json_locator_pros_and_cons.md)
  — pros and cons of JSON-based locator storage.

## Repository collaboration and security

These documents guide contributors and coding assistants; they are not product
documentation.

- [Shared repository instructions](CLAUDE.md)
- [Copilot instructions](.github/copilot-instructions.md)
- [Backend-specific instructions](.github/instructions/backend.instructions.md)
- [Web client instructions](.github/instructions/client.instructions.md)
- [Governance instructions](.github/instructions/governance.instructions.md)
- [Claude skills index](.claude/skills/README.md)

## Learning material

- [Skill Spring overview](skill_spring/readme.md)
- [Claude Code learning notes](skill_spring/claude_code/claude_code_learning.md)
- [Sorting algorithms: normal-distribution quicksort](skill_spring/algorithms/sorts/normal_distribution_quick_sort.md)
- [Claude Agent SDK guide](skill_spring/claude_code/claude_agent_sdk/README.md)
- [Claude Agent SDK release guide](skill_spring/claude_code/claude_agent_sdk/RELEASING.md)
- [Claude Agent SDK end-to-end tests](skill_spring/claude_code/claude_agent_sdk/e2e-tests/README.md)

The Claude Agent SDK folder also contains individual feature examples, such as
[session stores](skill_spring/claude_code/claude_agent_sdk/examples/session_stores/README.md)
and [plugins](skill_spring/claude_code/claude_agent_sdk/examples/plugins/demo-plugin/commands/greet.md).

<!-- Table of Contents -->
<a id="table-of-contents"></a>
## 📑 Table of Contents

- [📚 Documentation Index](#documentation-index)
- [🛠️ Installation](#installation)
- [⚙️ Configuration](#configuration)
- [🐳 Docker and Database](#docker-and-database)
- [🏃 Running Tests](#running-tests)
- [🤖 Self-Healing Framework (Playwright)](#self-healing-framework-playwright)
- [🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)](#ai-generated-ui-test-scripts-python-playwright-mcp)
- [📈 Daily Stock Analysis (DSA) User Guide](#daily-stock-analysis-dsa-user-guide)
- [🌱 Skill Spring Learning Lab](#skill-spring-learning-lab)
- [📂 Project Structure](#project-structure)
- [🎓 Best Practices & Patterns](#best-practices-patterns)
- [🧭 Repository Development Guide](#repository-development-guide)
- [❤️ Support & Feedback](#support-feedback)
- [📝 License](#license)

<a id="installation"></a>
## 🛠️ Installation

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
```

**Linux/macOS (bash/zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

Choose one package manager after activating the virtual environment:

**Using pip:**
```powershell
python -m pip install -r requirements.txt
```

**Using uv:**
```powershell
uv pip install -r requirements.txt
```

This installs the packages used by Robot Framework, pytest, Playwright, and the supporting demo utilities.

### 3. Install Playwright browsers

```powershell
playwright install
```

<a id="configuration"></a>
## ⚙️ Configuration

Runtime settings are read from environment variables. Shared test and AI-generation settings are centralized in `utils/config`; provider-specific `ai_stock` settings are documented in [ai_stock/readme.md](ai_stock/readme.md).

### Shared URLs

| Variable | Default | Purpose |
|---|---|---|
| `TANGERINE_URL` | `https://www.tangerine.ca/en/personal` | Base URL for Tangerine UI tests |
| `DEEP_SEEK_URL` | `https://api.deepseek.com` | DeepSeek-compatible API endpoint |
| `OPENAI_URL` | `https://api.openai.com/v1` | OpenAI-compatible API endpoint |

### UI and Playwright

| Variable | Default | Purpose |
|---|---|---|
| `UI_LOCALE` | `en-US` | Browser locale for Playwright tests |
| `SLEEP_TIME` | `1` | Generic delay used by selected fixtures |
| `COOKIE_BANNER_TIMEOUT_SECONDS` | `5` | Timeout for Tangerine cookie-banner handling |
| `PW_HEADLESS` | `false` | Run Playwright headlessly (`1/0`, `true/false`, `yes/no`, `on/off`) |

### AI test generation

| Variable | Default | Purpose |
|---|---|---|
| `AI_GEN_MODEL` | `gpt-4.1` | LLM model identifier |
| `AI_GEN_BASE_URL` | `OPENAI_URL` | API endpoint used by the generator |
| `AI_GEN_MAX_DOM_CHARS` | `12000` | Maximum DOM characters sent to the model |
| `AI_GEN_OUTPUT_DIR` | `temps/ai/ai_gen` | Directory for generated tests |

Set the required provider key, such as `OPENAI_API_KEY`, through the environment before using AI features. Never commit credentials to the repository.

### Optional qTest integration

| Variable | Default | Purpose |
|---|---|---|
| `QTEST_BASE_URL` | `https://yourcompany.qtestnet.com` | qTest API base URL |
| `QTEST_PROJECT_ID` | `123456` | qTest project identifier |
| `QTEST_API_TOKEN` | `your_token_here` | qTest authentication token |

Quick local check for shared settings:

```powershell
python -m utils.config.config
```

<a id="docker-and-database"></a>
## 🐳 Docker and Database

The local MySQL service is defined in `docker/docker-compose.yml`. It stores data in the named `mysql-data` Docker volume, so stopping or recreating the container does not remove the database.

### Start and manage Docker services

Run these commands from the repository root. `server` hosts the Web/API app,
`analyzer` runs scheduled analysis, and `mysql` starts the local database.

```powershell
# Rebuild the application images without using the build cache
docker compose -f docker/docker-compose.yml build --no-cache server analyzer

# Start the Web/API and scheduled-analysis services
docker compose -f docker/docker-compose.yml up -d server analyzer

# Start every service, including MySQL
docker compose -f docker/docker-compose.yml up -d

# Follow application logs
docker compose -f docker/docker-compose.yml logs -f server analyzer

# Start an existing stopped MySQL container
docker compose -f docker/docker-compose.yml start mysql

# Follow MySQL logs
docker compose -f docker/docker-compose.yml logs -f mysql
```

The service is exposed at `localhost:3306` by default. Set `SLOTH_MYSQL_PORT` before starting Compose to use another host port.

### Connect to the local database

The default local connection values are:

| Setting | Value |
|---|---|
| Host | `127.0.0.1` |
| Port | `3306` |
| Database | `slothdb` |
| User | `slothuser` |
| Password | `slothpass123` |

Override these local defaults with `SLOTH_MYSQL_DB`, `SLOTH_MYSQL_USER`, `SLOTH_MYSQL_PASSWORD`, and `SLOTH_MYSQL_ROOT_PASSWORD` before the first `docker compose ... up` command. Do not use the default passwords outside local development.

For Python database helper usage and parameterized query examples, see [utils/data_base/README.md](utils/data_base/README.md).

<a id="running-tests"></a>
## 🏃 Running Tests

Run commands from the repository root. Choose the narrowest workflow that matches the change you are validating.
For commands covering pytest, Robot Framework, Vitest, and Cypress, see the
[testing guide](tests/testing_guide.md).

### Run all pytest and Robot tests

Run both test frameworks and return a failure if either suite fails:

```powershell
$pytestExit = 0
$robotExit = 0

python -m pytest
$pytestExit = $LASTEXITCODE

python -m robot --outputdir temps/test-results-robot tests/robot_tests/ui_suites/
$robotExit = $LASTEXITCODE

if ($pytestExit -ne 0 -or $robotExit -ne 0) {
   exit 1
}
```

Pytest results are written to `temps/test-results-pytest/`; Robot reports are written to `temps/test-results-robot/`.

### Pytest suites

`pytest` covers the unit, API, and Playwright UI suites.

```powershell
# Full pytest run
python -m pytest

# Fast unit and API smoke checks
python -m pytest -m "unit or api"

# One file / one test
python -m pytest tests/pytest_tests/test_csv_reader.py -q
python -m pytest tests/pytest_tests/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q

# UI tests
python -m pytest -m ui
python -m pytest tests/pytest_tests/ui_suites/tangerine -q
```

### Playwright recording and debugging

Use Playwright Codegen to record actions and bootstrap UI tests:

```powershell
python -m playwright codegen https://www.tangerine.ca/en/personal
```

Run a UI test visibly for debugging. Configure browser visibility and slow motion through environment variables:

```powershell
$env:PW_HEADLESS = "false"
$env:PW_SLOW_MO = "200"
python -m pytest tests/pytest_tests/ui_suites/tangerine/test_codegen.py -q
```

- `PW_HEADLESS=false` opens a visible browser
- `PW_SLOW_MO=200` slows Playwright actions by 200 milliseconds

> This project uses **Python pytest + Playwright**, so run tests with `python -m pytest ...`, not `npx playwright test`.

For AI-based test generation, see [AI-Generated UI Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp).

### Robot Framework suites

Robot demos live under `tests/robot_tests/ui_suites/`.

```powershell
# All Robot suites
python -m robot --outputdir temps/test-results-robot tests/robot_tests/ui_suites/

# Tangerine Playwright suite
python -m robot --outputdir temps/test-results-robot tests/robot_tests/ui_suites/

# Dry run (syntax and keyword wiring only)
python -m robot --dryrun --outputdir temps/test-results-robot tests/robot_tests/ui_suites/
```

Robot writes `output.xml`, `log.html`, and `report.html` to the selected directory under `temps/`.

For Robot failures:

- failure screenshots are saved under `<outputdir>/artifacts/playwright/screenshots/`
- failure videos are saved under `<outputdir>/artifacts/playwright/videos/`
- for example, `--outputdir temps/test-results-robot` produces `temps/test-results-robot/artifacts/playwright/`
- screenshot/video links appear in Robot `log.html` and `report.html`
- passed-test videos are deleted to keep artifacts small

### Allure results

Generate and serve an Allure report after a pytest run:

```powershell
python -m pytest --alluredir=temps/test-results-pytest --clean-alluredir
allure serve temps/test-results-pytest
```

For pytest UI runs, Playwright records per-test video and keeps/attaches it only for failed tests. Videos are written under `temps/playwright-videos/tangerine_playwright/`.

The Tangerine Robot keyword libraries also bootstrap the project root import path automatically, so `-P` is typically not needed.

<a id="self-healing-framework-playwright"></a>
## 🤖 Self-Healing Framework (Playwright)

The Playwright UI tests use fallback locators and DOM similarity matching to recover from selector changes.

### Try it

Install the Playwright browsers once, then run a Tangerine UI test from the repository root:

```powershell
python -m playwright install
python -m pytest .\tests\pytest_tests\ui_suites\tangerine\test_signinpage.py -q
```

This opens the sign-in flow through the shared UI fixture and self-healing locator support. Set `PW_HEADLESS=false` to watch the browser, or add `PW_SLOW_MO=200` to slow Playwright actions while learning the flow.

### Components

| Component | Responsibility |
|---|---|
| `self_healing/element_finder.py` | Tries the primary locator and configured fallbacks |
| `self_healing/dom_similarity.py` | Finds likely replacements in the current page DOM |
| `self_healing/self_healing.py` | Coordinates recovery and optional locator updates |
| `self_healing/locator_store.py` | Loads and persists keyed locator definitions |
| `tests/pytest_tests` | Stores the Tangerine locator JSON files |

### Recovery flow

1. Try the primary locator and its fallback strategies.
2. If they fail, scan the page DOM for a similar candidate.
3. Reject candidates below the similarity threshold.
4. Build a locator from the best candidate.
5. Update the primary locator when `auto_update=True`.

This reduces manual maintenance after small UI changes while keeping recovery decisions visible in the test logs.

### Robot Framework integration

The Robot Tangerine suite under `tests/robot_tests/ui_suites` uses the same
repository-relative locator store as pytest. Import shared helpers with
`from utils.self_healing import click, find_element`. The keyword library
bootstraps the repository root before importing these helpers, so `-P` is not
required. The locator store currently supports these keys:

- `tangerine.login`
- `tangerine.signup`

Robot integration enables locator updates through `SELF_HEAL_AUTO_UPDATE`. Set that constant to `False` when a run must recover without rewriting locator files.

<a id="ai-generated-ui-test-scripts-python-playwright-mcp"></a>
## 🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)

Generate runnable pytest + Playwright scripts from a natural-language goal and live page context.

### Generation pipeline

1. Playwright opens the target URL and captures DOM, screenshot, and network context.
2. `utils/ai_gen/mcp_context.py` packages the browser state into a structured snapshot.
3. `utils/ai_gen/prompt_builder.py` creates the generation prompt.
4. An OpenAI-compatible model returns Python test code.
5. `utils/ai_gen/generator.py` normalizes and writes the script to the requested output path.

Run the command-line entry point with `python -m utils.ai_gen.cli`.
Relative `--output` paths are resolved from the repository root, not `utils/`
or the current working directory. Absolute paths are preserved.

### CLI options

| Option | Default | Description |
|---|---|---|
| `--model` | `AI_GEN_MODEL` (`gpt-4.1`) | LLM model name |
| `--base-url` | `AI_GEN_BASE_URL` | OpenAI-compatible API endpoint |
| `--headless` | `false` | Run context collection headlessly (`true`/`false`) |

### Additional examples

**Windows (PowerShell):**
```powershell
python -m utils.ai_gen.cli `
   --url "https://www.tangerine.ca/app/#/login" `
   --goal "Verify username, password, and submit controls are present" `
   --test-name "test_tangerine_signin" `
   --output "temps/ai/generated_playwright/test_tangerine_signin.py"

python -m pytest -q temps/ai/generated_playwright/test_tangerine_signin.py
```

**Linux/macOS (bash/zsh):**
```bash
python -m utils.ai_gen.cli \
  --url "https://www.tangerine.ca/app/#/login" \
  --goal "Verify username, password, and submit controls are present" \
  --test-name "test_tangerine_signin" \
  --output "temps/ai/generated_playwright/test_tangerine_signin.py"

python -m pytest -q temps/ai/generated_playwright/test_tangerine_signin.py
```

For Google search, use single quotes around the goal in PowerShell so the
double quotes around `"Amazon"` are preserved:

```powershell
python -m utils.ai_gen.cli `
   --url "https://www.google.com" `
   --goal 'Verify Google search by searching for "Amazon" and pressing Enter' `
   --test-name "test_google_search_for_amazon" `
   --output "temps\ai\generated_playwright\test_google_search_for_amazon.py"
```

Generated tests that accept `page: Page` use the `page` fixture from
`pytest-playwright`, included in `requirements.txt`. If pytest reports
`fixture 'page' not found`, install the project dependencies in the same Python
environment used to run pytest:

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -q temps/ai/generated_playwright --browser chromium
```

The plugin runs headlessly by default; add `--headed` to watch the browser.
Existing Tangerine pytest suites keep their separate `tangerine_homepage` fixture.

Review generated code before committing. DOM input is limited by `AI_GEN_MAX_DOM_CHARS`, and generated tests are plain pytest files; self-healing must be added explicitly when needed.

Validate the generator with:

```powershell
python -m pytest -q tests\unit\test_ai_generation.py
```

<a id="daily-stock-analysis-dsa-user-guide"></a>
## 📈 Daily Stock Analysis (DSA) User Guide

DSA combines market data, technical analysis, news, and language models to produce stock-analysis reports. It also includes a Web workspace for chat, backtesting, alerts, decision signals, and report history. These features are decision-support tools, not investment advice or automated trading.

### Overview

| Area | What it provides |
|---|---|
| Analysis | Reports for A-shares, Hong Kong stocks, U.S. equities, and supported Japan/Korea symbols |
| Data and research | Quotes, historical bars, technical indicators, fundamentals, news, and source-quality context where available |
| Web workspace | Watchlists, reports, history, strategy chat, backtesting, alerts, and settings |
| Operations | CLI, FastAPI/Web service, local scheduler, Docker, and optional email delivery |

Coverage varies by market and provider. Japan (`.T`) and Korea (`.KS` / `.KQ`) rely mainly on YFinance for daily bars, basic or delayed quotes, and technical indicators. Real-time quotes, complete symbol lists, full fundamentals, and region-specific market data may be unavailable. Missing data is not a zero value or a market signal.

### Quick start

From the repository root, install dependencies, copy `.env.example` to `.env`, and configure `STOCK_LIST` plus at least one model provider key. The [LLM provider guide](ai_stock/llm/llm-providers.md) covers provider choices; `.env.example` lists supported settings.

Start the Web/API service:

```bash
python main.py --serve-only
```

Open `http://127.0.0.1:8000`; the interactive API reference is at `/docs`. For a Web-only development server and frontend commands, see the [DSA Web guide](apps/dsa-web/readme.md).

### Run modes

| Goal | Command |
|---|---|
| Analyze the configured watchlist | `python main.py` |
| Analyze selected symbols | `python main.py --stocks 600519,hk00700,AAPL` |
| Review market conditions | `python main.py --market-review` |
| Run scheduled analysis | `python main.py --schedule` |
| Start Web/API without an initial analysis | `python main.py --serve-only` |
| Start Web/API and run an analysis | `python main.py --serve` |
| Run the local Web launcher | `python webui.py` |

### Deployment and configuration

Docker Compose defines separate server and analyzer services. Start the Web/API service with `docker compose -f docker/docker-compose.yml up -d server`; use the `analyzer` service for scheduled analysis. Persist the database, reports, and writable configuration file if settings must survive container replacement. See [`docker/docker-compose.yml`](docker/docker-compose.yml).

`STOCK_LIST` controls the analysis universe. Search and market-data sources use provider keys and fallbacks configured through environment variables or Web Settings. Email is the supported notification transport; configure it only if report or alert delivery is needed. Detailed feature behavior is in the [LLM provider guide](ai_stock/llm/llm-providers.md) and [DSA Web feature guides](apps/dsa-web/readme.md#web-workflows).

The Web/API service has no built-in authentication. Keep it on a trusted private network or place it behind an authenticated HTTPS reverse proxy; do not expose it directly to the public Internet.

### API and Web references

- [DSA Web guide and feature workflows](apps/dsa-web/readme.md#web-workflows)
- [OpenAPI schema snapshot](api/api_spec.json); the running service exposes `/openapi.json` and interactive `/docs`.
- [Email notification guide](apps/dsa-web/readme.md#email-notifications)
- [Alert Center guide](apps/dsa-web/readme.md#alert-center)

<a id="skill-spring-learning-lab"></a>
## 🌱 Skill Spring Learning Lab

`skill_spring` is the repository's learning and research area: a collection of study tracks, experiments, notebooks, and reusable examples spanning software engineering, AI, and exploratory programming.

### Learning paths

| Directory | Focus |
|---|---|
| [`algorithms/`](skill_spring/algorithms/) | Algorithms, data structures, problem-solving patterns, and machine learning exercises |
| [`concepts/`](skill_spring/concepts/) | Practical programming and test-automation concepts, from browser contexts to CI/CD |
| [`claude_code/`](skill_spring/claude_code/) | Claude, MCP, prompting, retrieval, tool use, and agent-oriented research |
| [`web_scraping/`](skill_spring/web_scraping/) | Web scraping, browser utilities, networking, and data collection experiments |
| [`fun_part/`](skill_spring/fun_part/) | Small games, creative programs, exploratory utilities, and learning experiments |

### IDE Setup For `skill_spring/claude_code` Subprojects

`skill_spring` is the repository's learning and research area. It contains algorithms, test-automation concepts, web-scraping exercises, and Claude/MCP experiments.

| Area | Starting point |
|---|---|
| Algorithms and data structures | [skill_spring/algorithms/](skill_spring/algorithms/) |
| Test-automation concepts | [skill_spring/concepts/](skill_spring/concepts/) |
| Claude, MCP, and agent experiments | [skill_spring/claude_code/](skill_spring/claude_code/) |
| Web scraping and small experiments | [skill_spring/web_scraping/](skill_spring/web_scraping/) and [skill_spring/fun_part/](skill_spring/fun_part/) |

Each runnable subproject carries its own setup instructions. For the Claude/MCP index and notebook guide, see [Skill Spring Learning Notes](skill_spring/claude_code/claude_code_learning.md).

<a id="project-structure"></a>
## 📂 Project Structure

```text
sloth-python/
├── utils/ai_gen/               # AI + MCP prompt-to-test generation
├── ai_stock/                   # AI-assisted stock analysis and reporting (storage, templates, cache under ai_stock/stock_data)
├── apps/                       # dsa-web (React/Vite frontend), dsa-web-playwright-tests, and dsa-web-cypress-tests
├── load_tests/                 # JMeter, load-runner, and Postman assets
├── pytest_tests/               # Pytest unit, API, UI, DDT, and AI tests
├── robot_tests/                # Robot Framework API, calculator, UI, DDT, and unit suites
├── self_healing/               # Shared Playwright locator-recovery framework
├── skill_spring/               # Learning and research tracks
├── utils/                      # Domain-oriented shared helpers (shared config lives in utils/config/config.py)
├── temps/                      # Generated reports, logs, videos, static build output, and temporary results
├── .github/workflows/          # GitHub Actions CI/CD definitions
├── .vscode/                    # Workspace settings
├── pyproject.toml              # Python tooling and pytest configuration
├── readme.md                   # Project overview and quick-start guide
├── requirements.txt            # Python dependencies
├── contributing.md            # Repository development conventions and workflows
└── uv.lock                     # uv dependency lock file
```

<a id="best-practices-patterns"></a>
## 🎓 Best Practices & Patterns

Keep changes focused, reusable, and easy to validate.

### Testing and UI Automation

- **Organize by behavior:** Keep pytest suites under `tests/pytest_tests` and Robot suites under `tests/robot_tests`, grouped by `unit`, `api`, `ui`, `ddt`, and `ai` where applicable.
- **Use shared fixtures and page objects:** Centralize setup, browser lifecycle, and page interactions instead of duplicating them in individual tests.
- **Prefer stable selectors:** Reuse shared locator definitions and self-healing helpers for Playwright flows when selector recovery is appropriate.
- **Parameterize repeated scenarios:** Use fixtures, markers, and parameterization to keep test coverage broad without duplicating test logic.

### Python and Configuration

- **Keep code typed and readable:** Use clear names, type hints, focused functions, and useful docstrings.
- **Reuse shared utilities:** Prefer helpers in `utils/`, `utils/config`, and `self_healing/` before introducing duplicates.
- **Externalize settings:** Read URLs, feature flags, and integration settings from environment variables with safe defaults.
- **Protect secrets:** Never commit API keys, tokens, or credentials; use environment variables and keep sensitive values out of logs.
- **Format and lint consistently:** Run Ruff checks and formatting before finalizing substantial Python changes.

### AI and Learning Workflows

- **Review generated code:** Treat `utils/ai_gen/` output as a starting point and validate it with focused pytest runs before committing.
- **Keep research reproducible:** Follow the project README and notebook instructions under `skill_spring/` for learning experiments.
- **Prefer explainable analysis:** Keep stock-analysis conclusions traceable to market data, news, and strategy inputs.

### CI/CD and Reporting

- **Validate in stages:** Run focused tests locally, then the smoke or regression workflow as the change requires.
- **Keep CI headless:** Install Playwright browsers and use `PW_HEADLESS=1` in automated UI runs.
- **Preserve diagnostics:** Use Allure, Robot HTML reports, screenshots, videos, and uploaded artifacts to investigate failures.

<a id="repository-development-guide"></a>
## 🧭 Repository Development Guide

Follow the repository conventions and focused development workflow: preserve
existing contracts, update the relevant documentation, and validate the
affected areas. The detailed guidance covers collaboration assets, project
architecture, common commands, validation by change type, stability guardrails,
review workflows, and delivery practices.

See [contributing.md](contributing.md) for the complete guide.

<a id="support-feedback"></a>
## ❤️ Support & Feedback

If **Sloth Python** helps you learn, automate, or experiment, your support helps keep the project maintained and growing.

### Ways to help

- [Sponsor the project](https://github.com/sponsors/466725) to support maintenance and new examples.
- Report reproducible bugs or request features through [GitHub Issues](https://github.com/466725/sloth-python/issues).
- Ask questions or discuss ideas through [GitHub Discussions](https://github.com/466725/sloth-python/discussions).
- Contribute tests, documentation, algorithms, automation examples, or AI tooling.

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github&style=for-the-badge)](https://github.com/sponsors/466725)

Thank you for helping make the project more useful for the next person who finds it.

### Include useful context

For issues and questions, include:

- Python version, operating system, and relevant package or browser versions
- The smallest reproduction or clear steps to reproduce
- Expected and actual behavior
- Relevant command output or a redacted traceback
- The affected area, such as `pytest`, `robot`, `ai_gen`, `ai_stock`, or `skill_spring`

Report security vulnerabilities privately to the project maintainers, not through a public issue. Never include API keys, tokens, credentials, or other sensitive values in reports.

<a id="license"></a>
## 📝 License

Sloth Python is distributed under the **MIT License**.

### Permissions

| Use | Permitted |
|---|---|
| Commercial use | Yes |
| Private use | Yes |
| Modification | Yes |
| Distribution | Yes |

### Condition

Redistributions must retain the applicable copyright and license notices.
