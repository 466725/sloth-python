# Sloth Python

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/466725/sloth-python/actions/workflows/ci.yml/badge.svg)](https://github.com/466725/sloth-python/actions/workflows/ci.yml)
[![Sponsor](https://img.shields.io/badge/Sponsor-❤-pink?logo=github)](https://github.com/sponsors/466725)

A practical Python reference repository for test automation, AI-assisted testing workflows, and algorithm implementations.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Self-Healing Playwright Framework](#self-healing-playwright-framework)
- [AI-Generated UI Tests (MCP + Playwright)](#ai-generated-ui-tests-mcp--playwright)
- [Claude Code Learning Projects](#claude-code-learning-projects)
- [CI/CD](#cicd)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [License](#license)
- [Support](#support)

## Overview

This repository combines several learning and production-style tracks:

- Test automation with pytest, Playwright, and Robot Framework
- AI-assisted UI test generation with MCP context collection
- Self-healing locator strategies for UI reliability
- Algorithms and data structure implementations
- Claude/MCP demos and notebooks
- CI workflows for smoke and nightly regression coverage

## Prerequisites

- Python 3.11+
- Git
- Node/Playwright browser dependencies (installed via `playwright install`)

## Quick Start

1. Clone the repository:

```powershell
git clone https://github.com/466725/sloth-python.git
cd sloth-python
```

2. Create and activate a virtual environment.

Windows (PowerShell):

```powershell
py -3.11 -m venv .venv311
.\.venv311\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv311
source .venv311/bin/activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

Optional with uv:

```powershell
uv venv .venv311 --python 3.11
.\.venv311\Scripts\activate
uv pip install -r requirements.txt
```

4. Install Playwright browsers:

```powershell
python -m playwright install
```

## Configuration

Shared runtime settings are defined in `utils/config.py` and read from environment variables.

| Variable | Default | Description |
|---|---|---|
| `TANGERINE_URL` | `https://www.tangerine.ca/en/personal` | Base URL for Tangerine UI examples |
| `DEEP_SEEK_URL` | `https://api.deepseek.com` | DeepSeek-compatible base URL |
| `OPENAI_URL` | `https://api.openai.com/v1` | OpenAI-compatible base URL |
| `UI_LOCALE` | `en-US` | Browser locale for Playwright contexts |
| `SLEEP_TIME` | `1` | Generic sleep duration used by selected demos |
| `COOKIE_BANNER_TIMEOUT_SECONDS` | `5` | Cookie banner wait timeout |
| `PW_HEADLESS` | `false` | Playwright headless mode |
| `AI_GEN_MODEL` | `gpt-4.1` | Model used by AI generation flow |
| `AI_GEN_BASE_URL` | `OPENAI_URL` | AI generation API base URL |
| `AI_GEN_MAX_DOM_CHARS` | `12000` | DOM size cap sent to model |
| `AI_GEN_OUTPUT_DIR` | `pytest_demo/tests/ai/generated_playwright` | Default generated-test output path |

Print resolved settings locally:

```powershell
python -m utils.config
```

## Running Tests

### Pytest

```powershell
# Full run
python -m pytest

# Common subsets
python -m pytest -m "unit or api"
python -m pytest -m ui
python -m pytest -m "not ai"

# Targeted file/test
python -m pytest pytest_demo/tests/unit/test_csv_reader.py -q
python -m pytest pytest_demo/tests/unit/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q
```

### Robot Framework

```powershell
# All robot suites
python -m robot --outputdir temps/robot_all robot_demo/

# Smoke-like calculator suite
python -m robot --outputdir temps/robot_calculator robot_demo/calculator/

# Tangerine UI suite
python -m robot --outputdir temps/robot_tangerine_playwright robot_demo/tangerine_playwright/

# Dry run
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot_demo/tangerine_playwright/
```

### API Demo Flows

| Approach | Run command |
|---|---|
| Pytest API tests | `python -m pytest -q pytest_demo/tests/api/test_deep_seek_api.py` |
| Robot + Python keywords | `python -m robot --outputdir temps/robot_api robot_demo/api/deep_seek_api_hybrid_test.robot` |
| Robot RequestsLibrary only | `python -m robot --outputdir temps/robot_api robot_demo/api/deep_seek_api_test.robot` |

### Playwright Debugging

```powershell
# Record actions
python -m playwright codegen https://www.tangerine.ca/en/personal

# Run one test headed
python -m pytest pytest_demo/tests/ui/tangerine_playwright/test_codegen_demo.py --headed --slowmo 200
```

## Self-Healing Playwright Framework

The self-healing engine lives in `self_healing/` and is used by UI workflows to recover from selector drift.

Primary locator stores:

- `pytest_demo/locators/signinpage.json`
- `pytest_demo/locators/signuppage.json`

High-level flow:

1. Try primary locator.
2. Try backup locators.
3. Scan DOM with similarity heuristics.
4. Reuse recovered strategy (and optionally persist where enabled).

Robot Tangerine suites use the same locator store with controlled update behavior.

## AI-Generated UI Tests (MCP + Playwright)

The generator is implemented in `ai_gen/` and produces pytest + Playwright tests from live page context.

How it works:

1. Capture page context (DOM, screenshot metadata, network events).
2. Build a structured prompt from context and natural-language goal.
3. Generate runnable Python test code through an OpenAI-compatible API.
4. Save to `pytest_demo/tests/ai/generated_playwright/`.

Prerequisites:

- `OPENAI_API_KEY` in environment
- Dependencies installed
- Playwright browsers installed

Example:

```powershell
$env:OPENAI_API_KEY = "<your-api-key>"

python -m ai_gen.cli `
  --url "https://www.tangerine.ca/en/personal" `
  --goal "Verify homepage loads and Sign In button is visible" `
  --test-name "test_tangerine_homepage" `
  --output "pytest_demo/tests/ai/generated_playwright/test_tangerine_homepage.py"

python -m pytest -q pytest_demo/tests/ai/generated_playwright/test_tangerine_homepage.py
```

CLI options:

| Option | Default | Description |
|---|---|---|
| `--url` | required | Target URL |
| `--goal` | required | Natural-language test goal |
| `--test-name` | `test_generated_ui_flow` | Generated function name |
| `--output` | `AI_GEN_OUTPUT_DIR` + filename | Output file path |
| `--model` | `AI_GEN_MODEL` | Model name |
| `--base-url` | `AI_GEN_BASE_URL` | OpenAI-compatible endpoint |
| `--headless` | `true` or `false` from config | Headless browser for context capture |

## Claude Code Learning Projects

`claude_code/` contains Claude and MCP learning tracks:

| Directory | Purpose |
|---|---|
| `000_Architect_Foundations_Certification_Exam/` | Practice exam resources for Claude Architect Foundations |
| `001_starter/` | MCP starter project |
| `002_cli/` | CLI-based MCP chat project |
| `003_notifications/` | Logging and notifications demo |
| `004_roots/` | Root-scoped filesystem and media operations |
| `005_sampling/` | Sampling and response-flow demo |
| `006_transport_http/` | MCP HTTP transport example |
| `007_note_book/` | Notebook tutorials (prompting, tools, RAG, search, evals) |
| `claude_agent_sdk/` | Claude Agent SDK source and examples |

IDE tip for VS Code: configure workspace extra paths in `.vscode/settings.json` so imports resolve cleanly for subprojects under `claude_code/`.

## CI/CD

GitHub Actions workflow: `.github/workflows/ci.yml`

- Smoke job on pushes and pull requests
- Nightly regression job (`0 2 * * *`) and manual `workflow_dispatch`
- Artifacts include Robot output and Allure assets when available

Local CI-style simulation:

```powershell
# Smoke-like
python -m pytest -m "unit or api" --tb=short
python -m robot --outputdir temps/robot_smoke robot_demo/calculator/

# Regression-like
python -m playwright install
python -m pytest -m "not ai" --tb=short --maxfail=5
python -m robot --outputdir temps robot_demo/
```

## Project Structure

```text
sloth-python/
├── ai_gen/                     # AI test generation pipeline (MCP context -> code)
├── ai_stock/                   # Stock analysis, strategy, and report experiments
├── algorithms/                 # Algorithms and data structures
├── claude_code/                # Claude/MCP learning tracks and SDK examples
├── fun_part/                   # Educational and exploratory scripts
├── load_test_demo/             # JMeter and Postman load/API assets
├── pytest_demo/                # Pytest suites, locators, and generated test outputs
├── robot_demo/                 # Robot Framework suites (API, unit, calculator, UI)
├── self_healing/               # Shared self-healing locator framework
├── temps/                      # Local test/report artifacts
├── utils/                      # Shared project utilities
├── web_scraping/               # Scraping and networking examples
├── .github/workflows/          # CI workflows
├── .vscode/settings.json       # Workspace Python/Pylance settings
├── pyproject.toml              # Tool formatting/linting configuration
├── pytest.ini                  # Pytest settings and markers
├── requirements.txt            # Runtime dependencies
└── security.md                 # Security policy
```

## Contributing

Contributions are welcome for code, tests, and documentation.

Recommended workflow:

1. Create a branch.
2. Make focused changes.
3. Run local checks.
4. Open a pull request with a clear description.

Example checks:

```powershell
python -m pytest -m "unit or api" --tb=short
python -m robot --outputdir temps/robot_smoke robot_demo/calculator/
```

## Troubleshooting

### Module import errors

```powershell
.\.venv311\Scripts\activate
pip install -r requirements.txt
```

### Playwright browser errors/timeouts

```powershell
python -m playwright install
python -m pytest pytest_demo/tests/ui/tangerine_playwright -q
```

### Claude subproject imports unresolved in VS Code

Set workspace interpreter and analysis paths in `.vscode/settings.json`:

```jsonc
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv311/Scripts/python.exe",
  "python.analysis.extraPaths": [
    "./claude_code/claude_agent_sdk/src",
    "./claude_code/claude_agent_sdk",
    "./claude_code"
  ]
}
```

## Security

Report vulnerabilities according to `security.md`.

## License

Licensed under the MIT License.

## Support

- Issues: https://github.com/466725/sloth-python/issues
- Discussions: https://github.com/466725/sloth-python/discussions
- Sponsor: https://github.com/sponsors/466725
