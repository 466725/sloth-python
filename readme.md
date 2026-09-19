# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/466725/sloth-python/actions/workflows/ci.yml/badge.svg)](https://github.com/466725/sloth-python/actions/workflows/ci.yml)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/466725)

A comprehensive Python reference project covering modern test automation, AI-assisted stock analysis, and algorithms.

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
- [Configuration](#️-configuration)
- [Running Tests](#-running-tests)
- [Self-Healing Framework](#-self-healing-framework-playwright)
- [AI-Generated Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp)
- [Skill Spring Learning Lab](#-skill-spring-learning-lab)
- [CI/CD Pipeline](#️-cicd-pipeline--automation)
- [Project Structure](#-project-structure)
- [Best Practices](#-best-practices--patterns)
- [Troubleshooting](#-troubleshooting)
- [Documentation](#-documentation--resources)
- [License](#-license)
- [Support & Feedback](#-support--feedback)

## 📌 Key Highlights

- **Test Automation:** Robot Framework and pytest examples covering unit, API, and Playwright-based UI testing
- **Self-Healing UI Tests:** AI-assisted locator recovery that detects broken selectors and learns from successful repairs
- **AI Test Generation:** MCP-aware Playwright workflow for generating runnable pytest tests from natural-language goals
- **AI-Assisted Stock Analysis:** Multi-agent pipeline combining market data, news, trading strategies, and report generation ([architecture](ai_stock/readme.md))
- **Algorithms and Machine Learning:** Curated implementations of data structures, algorithms, and ML concepts
- **CI/CD Workflows:** GitHub Actions automation for smoke tests and nightly regression suites

## 📦 Prerequisites

### Required

- **Python 3.11+** for the project libraries and test suites
- **Git** to clone and update the repository

### Needed for Specific Features

- **Playwright browsers** for browser-based UI tests; install them with `playwright install`
- **API credentials** for AI generation and provider-backed stock analysis; configure them through environment variables rather than source files

## 🚀 Quick Start

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/466725/sloth-python.git
   cd sloth-python
   ```

2. **Create an environment and install dependencies:**
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\activate
   python -m pip install -r requirements.txt
   playwright install
   ```

3. **Run the baseline checks:**
   ```powershell
   python -m pytest -m "unit or api"
   ```

See [Installation](#️-installation) for Linux/macOS commands, alternative package installation with `uv`, and additional setup details.

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

## ⚙️ Configuration

Runtime settings are read from environment variables. Shared test and AI-generation settings are centralized in `config/config.py`; provider-specific `ai_stock` settings are documented in [ai_stock/readme.md](ai_stock/readme.md).

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
| `AI_GEN_OUTPUT_DIR` | `pytest/tests/ai/generated_playwright` | Directory for generated tests |

Set the required provider key, such as `OPENAI_API_KEY`, through the environment before using AI features. Never commit credentials to the repository.

### Optional qTest integration

| Variable | Default | Purpose |
|---|---|---|
| `QTEST_BASE_URL` | `https://yourcompany.qtestnet.com` | qTest API base URL |
| `QTEST_PROJECT_ID` | `123456` | qTest project identifier |
| `QTEST_API_TOKEN` | `your_token_here` | qTest authentication token |

Quick local check for shared settings:

```powershell
python -m utils.config
```

## 🏃 Running Tests

Run commands from the repository root. Choose the narrowest workflow that matches the change you are validating.

### Pytest suites

`pytest` covers the unit, API, and Playwright UI suites.

```powershell
# Full pytest run
python -m pytest

# Fast unit and API smoke checks
python -m pytest -m "unit or api"

# One file / one test
python -m pytest pytest/unit/test_csv_reader.py -q
python -m pytest pytest/unit/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q

# UI tests
python -m pytest -m ui
python -m pytest pytest/ui/tangerine -q
```

### API demos

The repository includes three API-testing styles:

| Approach | Example command |
|---|---|
| Pytest + Python | `python -m pytest -q pytest/api/test_deep_seek_api.py` |
| Robot + Python keywords | `python -m robot --outputdir temps/robot_api robot/api/test_deep_seek_api_hybrid.robot` |
| Robot-only `RequestsLibrary` | `python -m robot --outputdir temps/robot_api robot/api/test_deep_seek_api.robot` |

DeepSeek demos use `OPENAI_API_KEY`; `DEEP_SEEK_URL` is optional.

### Playwright recording and debugging

Use Playwright Codegen to record actions and bootstrap UI tests:

```powershell
python -m playwright codegen https://www.tangerine.ca/en/personal
```

Run a UI test visibly for debugging:

```powershell
python -m pytest pytest/ui/tangerine/test_codegen.py --headed --slowmo 200
```

- `--headed` opens a visible browser
- `--slowmo 200` slows actions for easier observation

> This project uses **Python pytest + Playwright**, so run tests with `python -m pytest ...`, not `npx playwright test`.

For AI-based test generation, see [AI-Generated UI Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp).

### Robot Framework suites

Robot demos live under `robot`.

```powershell
# All Robot suites
python -m robot --outputdir temps/robot_all robot/

# Calculator demo
python -m robot --outputdir temps/robot_calculator robot/calculator/

# Tangerine Playwright suite
python -m robot --outputdir temps/robot_tangerine_playwright robot/ui/

# Dry run (syntax and keyword wiring only)
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot/ui/
```

Robot writes `output.xml`, `log.html`, and `report.html` to the selected directory under `temps/`.

For Robot failures:

- failure screenshots are saved under `artifacts/playwright/screenshots/`
- failure videos are saved under `artifacts/playwright/videos/`
- screenshot/video links appear in Robot `log.html` and `report.html`
- passed-test videos are deleted to keep artifacts small

### Allure results

Generate and serve an Allure report after a pytest run:

```powershell
python -m pytest --alluredir=temps/allure-results --clean-alluredir
allure serve temps/allure-results
```

For pytest UI runs, Playwright records per-test video and keeps/attaches it only for failed tests. Videos are written under `temps/playwright-videos/tangerine_playwright/`.

The Tangerine Robot keyword libraries also bootstrap the project root import path automatically, so `-P` is typically not needed.

## 🤖 Self-Healing Framework (Playwright)

The Playwright UI tests use fallback locators and DOM similarity matching to recover from selector changes.

### Components

| Component | Responsibility |
|---|---|
| `self_healing/element_finder.py` | Tries the primary locator and configured fallbacks |
| `self_healing/dom_similarity.py` | Finds likely replacements in the current page DOM |
| `self_healing/self_healing.py` | Coordinates recovery and optional locator updates |
| `self_healing/locator_store.py` | Loads and persists keyed locator definitions |
| `pytest/ui/locators/` | Stores the Tangerine locator JSON files |

### Recovery flow

1. Try the primary locator and its fallback strategies.
2. If they fail, scan the page DOM for a similar candidate.
3. Reject candidates below the similarity threshold.
4. Build a locator from the best candidate.
5. Update the primary locator when `auto_update=True`.

This reduces manual maintenance after small UI changes while keeping recovery decisions visible in the test logs.

### Robot Framework integration

The Robot Tangerine suite uses the same locator store through `robot/ui/playwright_keywords.py` and currently supports these keys:

- `tangerine.login`
- `tangerine.signup`

Robot integration enables locator updates through `SELF_HEAL_AUTO_UPDATE`. Set that constant to `False` when a run must recover without rewriting locator files.

## 🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)

Generate runnable pytest + Playwright scripts from a natural-language goal and live page context.

### Generation pipeline

1. Playwright opens the target URL and captures DOM, screenshot, and network context.
2. `ai_gen/mcp_context.py` packages the browser state into a structured snapshot.
3. `ai_gen/prompt_builder.py` creates the generation prompt.
4. An OpenAI-compatible model returns Python test code.
5. `ai_gen/generator.py` normalizes and writes the script to the requested output path.

The command-line entry point is `ai_gen/cli.py`.

### Requirements

- Set `OPENAI_API_KEY` before generating a test. OpenAI-compatible endpoints are supported through `--base-url`.
- Install project dependencies with `python -m pip install -r requirements.txt`.
- Install Playwright browsers with `playwright install`.

### Generate a test

```powershell
$env:OPENAI_API_KEY = "<your-api-key>"

python -m ai_gen.cli `
   --url "https://www.tangerine.ca/en/personal" `
   --goal "Verify the homepage loads and the Sign In button is visible" `
   --test-name "test_tangerine_homepage" `
   --output "pytest/ai/generated_playwright/test_tangerine_homepage.py"
```

Review the generated script, then run it with pytest:

```powershell
python -m pytest -q pytest/ai/generated_playwright/test_tangerine_homepage.py
```

### CLI options

| Option | Default | Description |
|---|---|---|
| `--url` | *(required)* | Target page URL |
| `--goal` | *(required)* | Natural-language test goal |
| `--test-name` | `test_generated_ui_flow` | Generated pytest function name |
| `--output` | `AI_GEN_OUTPUT_DIR/test_generated_ui_flow.py` | Generated script path |
| `--model` | `AI_GEN_MODEL` (`gpt-4.1`) | LLM model name |
| `--base-url` | `AI_GEN_BASE_URL` | OpenAI-compatible API endpoint |
| `--headless` | `false` | Run context collection headlessly (`true`/`false`) |

### Additional examples

```powershell
python -m ai_gen.cli `
   --url "https://www.tangerine.ca/app/#/login" `
   --goal "Verify username, password, and submit controls are present" `
   --test-name "test_tangerine_signin" `
   --output "pytest/ai/generated_playwright/test_tangerine_signin.py"

python -m pytest -q pytest/ai/generated_playwright
```

Review generated code before committing. DOM input is limited by `AI_GEN_MAX_DOM_CHARS`, and generated tests are plain pytest files; self-healing must be added explicitly when needed.

Validate the generator with:

```powershell
python -m pytest -q pytest/ai/test_ai_generation.py
```

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

### Claude and MCP study track

The main subprojects are organized by numbered learning tracks:

| Directory | Purpose |
|---|---|
| `000_Architect_Foundations_Certification_Exam/` | Community practice exam for Claude Certified Architect (77 scenario-based questions) |
| `001_starter/` | Starter MCP server for document-processing tools |
| `002_cli/` | Interactive Claude CLI with MCP client/server and document retrieval patterns |
| `003_notifications/` | MCP logging, progress, and notification demo |
| `004_roots/` | MCP chat with controlled filesystem roots and video conversion helpers |
| `005_sampling/` | MCP sampling demo with Claude-backed client flow |
| `006_transport_http/` | MCP transport-over-HTTP server example |
| `007_note_book/` | Notebook-based tutorials for prompting, tools, retrieval, evals, and web/search workflows |
| `claude_agent_sdk/` | Local copy of Claude Agent SDK for Python with examples and docs |

### Notebook Tutorials

Notebook tutorials live under `skill_spring/claude_code`:

| Notebook | Focus |
|---|---|
| `001_prompting.ipynb`, `002_prompting.ipynb` | Prompting patterns and prompt iteration |
| `001_thinking.ipynb` | Claude thinking/reasoning examples |
| `001_tools.ipynb` | Multi-tool calling basics |
| `001_prompt_grader_evals.ipynb` | Prompt evaluation datasets, grading, and scoring |
| `001_chunking.ipynb` | Text chunking for retrieval workflows |
| `002_citations.ipynb` | Citation-aware responses |
| `002_embeddings.ipynb` | Embeddings and semantic retrieval |
| `002_images.ipynb` | Image input and multimodal usage patterns |
| `003_vectordb.ipynb`, `004_bm25.ipynb`, `005_hybrid.ipynb` | Vector search, keyword search, and hybrid retrieval |
| `003_caching.ipynb` | Prompt caching examples |
| `003_tool_streaming.ipynb` | Streaming tool-use flows |
| `005_code_execution.ipynb` | Code execution tool examples |
| `005_text_editor_tool.ipynb` | Text editor tool usage |
| `006_web_search.ipynb` | Web search examples |

### MCP Projects

The runnable MCP examples and mini-projects are:

| Directory | Purpose |
|---|---|
| `001_starter/` | Document-processing MCP starter server |
| `002_cli/` | Interactive MCP chat CLI project |
| `003_notifications/` | Logging/progress and notification flow |
| `004_roots/` | Root-restricted filesystem operations + video conversion |
| `005_sampling/` | Sampling patterns and response flow control |
| `006_transport_http/` | HTTP transport setup for MCP server communication |

Most runnable subprojects include their own `README.md`. In general, set `ANTHROPIC_API_KEY`, install dependencies with `uv sync` or `uv pip install -e .`, then run the project-specific command such as `uv run main.py` or `uv run client.py`.

Additional reference files:

- `skill_spring/claude_code/claude_code_learning.md`: curated course and project notes
- `skill_spring/claude_code/`: notebooks and supporting research material

### IDE Setup For `skill_spring/claude_code` Subprojects

Some learning subprojects live under `skill_spring/claude_code` instead of the repository root. If your IDE cannot resolve imports (for example, unresolved imports in `claude_agent_sdk` examples), use the setup below.

**PyCharm**

1. Open the `sloth-python` project.
2. Right-click `skill_spring/claude_code`.
3. Select **Mark Directory As** → **Sources Root**.

**VS Code (recommended workspace settings)**

This is the VS Code equivalent of PyCharm's **Sources Root** behavior.

1. Open the `sloth-python` project folder in VS Code.
2. Create or edit `.vscode/settings.json`.
3. Add/update the settings below:

```jsonc
{
   "python.defaultInterpreterPath": "${workspaceFolder}/.venv311/Scripts/python.exe",
   "python.analysis.extraPaths": [
      "./skill_spring/claude_code/claude_agent_sdk/src",
      "./skill_spring/claude_code/claude_agent_sdk",
      "./skill_spring/claude_code"
   ]
}
```

4. Reload VS Code window: **Developer: Reload Window**.

**Why these paths?**

- `skill_spring/claude_code`: resolves imports for `src`-layout packages in SDK examples
- `skill_spring/claude_code`: resolves local package references in that subproject
- `skill_spring/claude_code`: resolves imports from other learning folders under `skill_spring/claude_code`

**Quick verification checklist**

1. Open a Python file under `skill_spring/claude_code` with previous import warnings.
2. Confirm unresolved import diagnostics disappear.
3. In the VS Code command palette, run **Python: Select Interpreter** and verify it points to `.venv311` (or your chosen project venv).

Note: `python.analysis.extraPaths` improves IDE analysis and autocomplete. It does not make invalid Python identifiers importable at runtime. For example, folders starting with digits such as `001_starter/` still cannot be imported as `claude_code.001_starter...` in a standard `from ... import ...` statement.

## 🔄 CI/CD Pipeline & Automation

The main workflow is [`.github/workflows/ci.yml`](.github/workflows/ci.yml). It separates fast feedback for changes from scheduled or manually triggered regression coverage.

### Triggers

| Event | Branches or schedule | Behavior |
|---|---|---|
| Push | `main`, `master` | Runs smoke tests |
| Pull request | `main`, `master` | Runs smoke tests |
| Schedule | `0 2 * * *` (2:00 UTC daily) | Runs regression tests |
| Manual dispatch | Any selected ref | Runs regression tests |

### Jobs

**Smoke test**

- Uses Ubuntu and Python 3.11.
- Installs dependencies from `requirements.txt`.
- Runs pytest `unit` and `api` tests with `--tb=short`.
- Runs the Robot calculator smoke suite.
- Uploads smoke results with `retention-days: 14`.

**Regression test**

- Runs on the nightly schedule or manual dispatch with a 60-minute timeout.
- Caches and installs Playwright browsers with system dependencies.
- Runs pytest tests excluding the `ai` marker with `PW_HEADLESS=1`.
- Runs the Robot suites with `PW_HEADLESS=1`.
- Generates an Allure report after the test run when possible.
- Uploads regression results with `retention-days: 21`.

### Artifacts

Depending on the job, uploaded artifacts can include:

- `temps/allure-results/`
- `temps/robot_smoke/`
- `allure-report/`
- `temps/log.html`, `temps/report.html`, and `temps/output.xml`

Open a workflow run on GitHub, download the relevant artifact, and open the generated HTML report locally.

### Run the CI checks locally

Run the closest equivalent from the repository root:

```powershell
# Smoke checks
python -m pytest -m "unit or api" --tb=short
python -m robot --outputdir temps/robot_smoke robot/calculator/

# Regression-style checks
python -m playwright install --with-deps
python -m pytest -m "not ai" --tb=short --maxfail=5
python -m robot --outputdir temps robot/
```

The workflow file still references legacy `robot_demo` paths, while the current repository uses `robot/`. Keep those paths synchronized before relying on the Robot steps in GitHub Actions.

## 📂 Project Structure

```
sloth-python/
├── ai_gen/                     # AI + MCP prompt-to-test generation
├── ai_stock/                   # AI-assisted stock analysis and reporting
├── config/                     # Shared and feature-specific configuration
├── load_test/                  # JMeter, load-runner, and Postman assets
├── pytest/                     # Pytest unit, API, UI, DDT, and AI tests
│   ├── ai/
│   ├── api/
│   ├── ddt/
│   ├── ui/
│   └── unit/
├── robot/                      # Robot Framework API, calculator, UI, DDT, and unit suites
│   ├── api/
│   ├── calculator/
│   ├── ddt/
│   ├── ui/
│   └── unit/
├── self_healing/               # Shared Playwright locator-recovery framework
├── skill_spring/               # Learning and research tracks
│   ├── algorithms/
│   ├── claude_code/
│   ├── concepts/
│   ├── fun_part/
│   └── web_scraping/
├── test_data/                  # Test-data creation scripts and fixtures
├── utils/                      # Shared configuration, database, analytics, and integration helpers
├── temps/                      # Generated reports, logs, videos, and temporary results
├── .github/workflows/          # GitHub Actions CI/CD definitions
├── .vscode/                    # Workspace settings
├── pyproject.toml              # Tooling configuration
├── pytest.ini                  # Pytest configuration
├── readme.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── security.md                 # Security policy
└── uv.lock                     # uv dependency lock file
```

### Key Directories Explained

- **ai_gen/** - Generates pytest + Playwright scripts from live page context and natural-language goals
- **ai_stock/** - Combines market data, news, strategies, and AI-generated stock reports
- **load_test/** - Source assets for JMeter, Postman, and load-runner workflows
- **pytest/** - Main pytest test suites, including the `ai`, `api`, `ui`, and `unit` areas
- **robot/** - Robot Framework suites and Python keyword libraries
- **self_healing/** - Locator fallback, DOM similarity, and locator-store update logic
- **skill_spring/** - Learning material for algorithms, concepts, Claude/MCP, scraping, and experiments
- **test_data/** - Utilities and input files used to create or supply test data
- **utils/** - Shared configuration, CSV, database, analytics, qTest, and AI helpers
- **temps/** - Generated output; do not edit it as source documentation

## 🎓 Best Practices & Patterns

Keep changes focused, reusable, and easy to validate.

### Testing and UI Automation

- **Organize by behavior:** Keep pytest suites under `pytest/` and Robot suites under `robot/`, grouped by `unit`, `api`, `ui`, `ddt`, and `ai` where applicable.
- **Use shared fixtures and page objects:** Centralize setup, browser lifecycle, and page interactions instead of duplicating them in individual tests.
- **Prefer stable selectors:** Reuse shared locator definitions and self-healing helpers for Playwright flows when selector recovery is appropriate.
- **Parameterize repeated scenarios:** Use fixtures, markers, and parameterization to keep test coverage broad without duplicating test logic.

### Python and Configuration

- **Keep code typed and readable:** Use clear names, type hints, focused functions, and useful docstrings.
- **Reuse shared utilities:** Prefer helpers in `utils/`, `config/`, and `self_healing/` before introducing duplicates.
- **Externalize settings:** Read URLs, feature flags, and integration settings from environment variables with safe defaults.
- **Protect secrets:** Never commit API keys, tokens, or credentials; use environment variables and keep sensitive values out of logs.
- **Format and lint consistently:** Run Ruff checks and formatting before finalizing substantial Python changes.

### AI and Learning Workflows

- **Review generated code:** Treat `ai_gen/` output as a starting point and validate it with focused pytest runs before committing.
- **Keep research reproducible:** Follow the project README and notebook instructions under `skill_spring/` for learning experiments.
- **Prefer explainable analysis:** Keep stock-analysis conclusions traceable to market data, news, and strategy inputs.

### CI/CD and Reporting

- **Validate in stages:** Run focused tests locally, then the smoke or regression workflow as the change requires.
- **Keep CI headless:** Install Playwright browsers and use `PW_HEADLESS=1` in automated UI runs.
- **Preserve diagnostics:** Use Allure, Robot HTML reports, screenshots, videos, and uploaded artifacts to investigate failures.

## 🐛 Troubleshooting

### Common Issues

### Import or dependency errors

Activate the project environment from the repository root and reinstall dependencies:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

**Linux/macOS (bash/zsh):**
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run tests as modules, for example `python -m pytest`, so the repository root remains available on the import path.

### Playwright browsers or timeouts

Install the browser binaries, then retry a focused UI suite:

```powershell
python -m playwright install
python -m pytest pytest/ui/tangerine -q
```

For CI or other headless environments, set `PW_HEADLESS=1`. For local debugging, use `--headed --slowmo 200` on a focused test.

### Locator not found

- Review the locator definitions under `pytest/ui/locators/`.
- If the test uses the self-healing helpers, inspect the logs for fallback and DOM-similarity recovery messages.
- Run the focused test with `-v` to capture detailed failure output.
- Update the relevant JSON locator only after confirming the replacement is stable.

See [Self-Healing Framework](#-self-healing-framework-playwright) for the recovery flow and supported Robot locator keys.

### AI generation errors

Set `OPENAI_API_KEY` before invoking the generator and verify the CLI is available:

```powershell
$env:OPENAI_API_KEY = "<your-api-key>"
python -m ai_gen.cli --help
```

Use `--base-url` for an OpenAI-compatible provider and review generated scripts before running or committing them.

### Robot or CI path failures

Run Robot suites from the repository root and use the current `robot/` directory:

```powershell
python -m robot --dryrun --outputdir temps/robot_dryrun robot/
```

The GitHub Actions workflow still contains legacy `robot_demo` paths. If those steps fail, update the workflow paths to match the current repository layout before rerunning CI.

## 📖 Documentation & Resources

Use the repository guides for project-specific behavior, then consult the external references for framework details.

### Repository documentation

- [Security Policy](security.md) - Secret handling and vulnerability reporting
- [AI Stock Architecture](ai_stock/readme.md) - Data, news, strategy, and report pipeline design
- [Skill Spring Learning Notes](skill_spring/claude_code/claude_code_learning.md) - Claude, MCP, and study-project index
- [Project Instructions](CLAUDE.md) - Repository conventions and common commands

### Workflows and configuration

- [CI/CD workflow](.github/workflows/ci.yml) - Smoke, regression, scheduling, and artifact steps
- [Project tooling](pyproject.toml) - Ruff, pytest, and Python tooling configuration
- [Configuration module](config/config.py) - Shared environment-backed runtime settings
- [Security scanning manifest](scamanifest.yml) - Repository security-scan configuration

### Framework references

- [Python documentation](https://docs.python.org/)
- [Pytest documentation](https://docs.pytest.org/)
- [Robot Framework User Guide](https://robotframework.org/robotframework/#introduction)
- [Playwright Python API](https://playwright.dev/python/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Allure Report documentation](https://docs.qameta.io/allure/)
- [pytest-html documentation](https://pytest-html.readthedocs.io/)

## ❤️ Support This Project

If **Sloth Python** helps you learn, automate, or experiment, your support helps keep the project maintained and growing.

### Ways to help

- [Sponsor the project](https://github.com/sponsors/466725) to support maintenance and new examples.
- Report bugs or suggest improvements through GitHub issues and discussions.
- Contribute tests, documentation, algorithms, automation examples, or AI tooling.

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github&style=for-the-badge)](https://github.com/sponsors/466725)

Thank you for helping make the project more useful for the next person who finds it.

## 🤝 Contributing

Contributions are welcome across the Python libraries, test suites, AI workflows, learning material, and documentation.

### Contribution workflow

1. Fork the repository and create a focused feature branch:
   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. Make the smallest change that solves the problem and add or update focused tests and documentation.

3. Validate the affected slice from the repository root:
   ```powershell
   python -m ruff check .
   python -m ruff format --check .
   python -m pytest -m "unit or api"
   python -m robot --dryrun --outputdir temps/robot_contributing robot/calculator/
   ```

   Run broader pytest or Robot suites when the change crosses those boundaries.

4. Commit with a clear conventional message and push the branch:
   ```powershell
   git add path/to/changed/files
   git commit -m "feat: describe your changes"
   git push origin feature/your-feature-name
   ```

5. Open a pull request with a clear summary, validation commands, and related issue references such as `Fixes #42`.

### Good contribution areas

- **Algorithms and learning:** Add focused examples under `skill_spring/algorithms/` with tests where appropriate.
- **Test automation:** Improve pytest suites, Robot keywords, Playwright flows, and shared fixtures.
- **Self-healing:** Improve locator recovery, DOM similarity, or locator-store behavior.
- **AI workflows:** Enhance `ai_gen/` or `ai_stock/` while keeping provider settings externalized.
- **Documentation and CI/CD:** Improve guides, examples, workflows, and failure diagnostics.

### Contribution standards

- Keep public behavior stable unless the change is intentional and documented.
- Prefer existing helpers, clear names, type hints, and focused modules.
- Keep secrets out of source code, examples, logs, and commits.
- Update tests and documentation when behavior or workflows change.
- Use conventional commit prefixes such as `feat:`, `fix:`, and `docs:`.

### Questions and support

- Use GitHub Discussions for questions and design ideas.
- Use GitHub Issues for reproducible bugs and feature requests.
- Search existing issues before opening a new one.


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
- **Example Tests** - Review `pytest` and `robot` for working examples

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

- **[SECURITY.md](security.md)** - How to responsibly report security vulnerabilities

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