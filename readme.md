# Sloth Python

## Documentation

Browse the [documentation index](docs/documentation_index.md) for project,
feature, development, and testing guides.

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

## 🐳 Docker and Database

The local MySQL service is defined in `docker/docker-compose.yml`. It stores data in the named `mysql-data` Docker volume, so stopping or recreating the container does not remove the database.

### Start and manage MySQL

Run these commands from the repository root:

```powershell
# Start MySQL in the background
docker compose -f docker/docker-compose.yml up -d mysql

# Check container and health status
docker compose -f docker/docker-compose.yml ps mysql

# Follow MySQL startup and server logs
docker compose -f docker/docker-compose.yml logs -f mysql

# Stop MySQL while retaining its data volume
docker compose -f docker/docker-compose.yml stop mysql

# Start an existing stopped MySQL container
docker compose -f docker/docker-compose.yml start mysql
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

## 🏃 Running Tests

Run commands from the repository root. Choose the narrowest workflow that matches the change you are validating.
For commands covering pytest, Robot Framework, Vitest, and Cypress, see the
[testing guide](docs/testing_guide.md).

### Run all pytest and Robot tests

Run both test frameworks and return a failure if either suite fails:

```powershell
$pytestExit = 0
$robotExit = 0

python -m pytest
$pytestExit = $LASTEXITCODE

python -m robot --outputdir temps/robot_all tests/robot_tests/ui_suites/
$robotExit = $LASTEXITCODE

if ($pytestExit -ne 0 -or $robotExit -ne 0) {
   exit 1
}
```

Pytest results use the configured Allure output directory; Robot reports are written to `temps/robot_all/`.

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
python -m robot --outputdir temps/robot_all tests/robot_tests/ui_suites/

# Tangerine Playwright suite
python -m robot --outputdir temps/robot_tangerine_playwright tests/robot_tests/ui_suites/

# Dry run (syntax and keyword wiring only)
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun tests/robot_tests/ui_suites/
```

Robot writes `output.xml`, `log.html`, and `report.html` to the selected directory under `temps/`.

For Robot failures:

- failure screenshots are saved under `<outputdir>/artifacts/playwright/screenshots/`
- failure videos are saved under `<outputdir>/artifacts/playwright/videos/`
- for example, `--outputdir temps/robot_all` produces `temps/robot_all/artifacts/playwright/`
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

## 🤖 AI-Generated UI Test Scripts (Python + Playwright + MCP)

Generate runnable pytest + Playwright scripts from a natural-language goal and live page context.

### Generation pipeline

1. Playwright opens the target URL and captures DOM, screenshot, and network context.
2. `utils/ai_gen/mcp_context.py` packages the browser state into a structured snapshot.
3. `utils/ai_gen/prompt_builder.py` creates the generation prompt.
4. An OpenAI-compatible model returns Python test code.
5. `utils/ai_gen/generator.py` normalizes and writes the script to the requested output path.

The command-line entry point is `utils/ai_gen/cli.py`; the original
`python -m ai_gen.cli` command remains supported for compatibility.
Relative `--output` paths are resolved from the repository root, not `utils/`
or the current working directory. Absolute paths are preserved.

### CLI options

| Option | Default | Description |
|---|---|---|
| `--model` | `AI_GEN_MODEL` (`gpt-4.1`) | LLM model name |
| `--base-url` | `AI_GEN_BASE_URL` | OpenAI-compatible API endpoint |
| `--headless` | `false` | Run context collection headlessly (`true`/`false`) |

### Additional examples

```powershell
python -m ai_gen.cli `
   --url "https://www.tangerine.ca/app/#/login" `
   --goal "Verify username, password, and submit controls are present" `
   --test-name "test_tangerine_signin" `
   --output "temps/ai/generated_playwright/test_tangerine_signin.py"

python -m pytest -q temps/ai/generated_playwright/test_tangerine_signin.py
```

For Google search, use single quotes around the goal in PowerShell so the
double quotes around `"Amazon"` are preserved:

```powershell
python -m ai_gen.cli `
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

## 📈 Daily Stock Analysis (DSA) User Guide

This is the main guide for Daily Stock Analysis (DSA), implemented under `ai_stock/`. It covers features, quick start, installation, configuration, run modes, deployment, and feature boundaries. The root `.env.example` and the fields currently visible in the Web settings page define the supported configuration keys; `/docs` and `architecture/api_spec.json` are the API references.

### 1. Overview

DSA reads a watchlist and market data, combines technical indicators, news, and an LLM to generate analysis reports, and can save results to history or send them through notification channels. The Web workspace also provides Ask Stock, backtesting, alerts, and AI decision signals.

#### Key Features

| Capability | Coverage |
|---|---|
| AI decision reports | Core conclusion, score, trend, entry/exit levels, risk alerts, catalysts, and action checklist |
| Multi-market data | A-shares, Hong Kong, US, ETFs: quotes, K-lines, technical indicators, capital flow, chips, news, announcements, and fundamentals. Japan/Korea (Yahoo `.T` / `.KS` / `.KQ`): see market coverage below |
| Web workspace | Manual analysis, task progress, history, full Markdown reports, backtest, settings, and light/dark themes |
| Agent strategy chat | Multi-turn Q&A with 15 built-in strategies across Web/API |
| Smart import & autocomplete | Image, CSV/Excel, clipboard import; code/name/pinyin/alias autocomplete |
| Automation & notifications | GitHub Actions, Docker, local scheduler, FastAPI service, and SMTP email delivery |

#### Market Coverage

Coverage differs by market. A-shares, Hong Kong, and US stocks have the broadest support. Japan uses the `.T` suffix, Korea KOSPI uses `.KS`, and KOSDAQ uses `.KQ`. Japan/Korea currently use only the YFinance path: daily bars, basic/delayed quotes, and technical indicators. The following are **not guaranteed** for these markets: real-time quotes, full fundamentals, a complete market-wide symbol list, capital flow, dragon-tiger data, sector/board data, and market review. **Missing data is not a zero value and not a bullish/bearish signal.**

#### Tech Stack & Data Sources

| Type | Supported |
|---|---|
| AI models | Anspire, AIHubMix, Gemini, OpenAI-compatible providers, DeepSeek, Qwen, Claude, Ollama |
| Market data | TickFlow, AkShare, Pytdx, Baostock, YFinance, Longbridge |
| News search | Anspire, SerpAPI, Tavily, Bocha, Brave, MiniMax, SearXNG |
| Social sentiment | Stock Sentiment API for Reddit / X / Polymarket (US stocks only) |

### 2. Quick Start - GitHub Actions (Recommended)

Deploy in about 5 minutes, with no server and no infrastructure cost.

**1. Fork this repository.** Click **Fork** in the upper-right corner. A star is very welcome if this project helps you.

**2. Configure Secrets.** In your fork, go to **Settings → Secrets and variables → Actions → New repository secret**.

**AI model (configure at least one).** Start with one provider and one API key. For multi-model routing, image recognition, local models, and advanced routing, see [Model Configuration](#5-configuration).

| Secret | Description | Required |
|---|---|---|
| `ANSPIRE_API_KEYS` | Anspire API key: one key for popular LLMs and web search, with free quota for this project | Recommended |
| `AIHUBMIX_KEY` | AIHubMix API key: one key for multiple model families, with a 10% top-up discount for this project | Recommended |
| `GEMINI_API_KEY` | Google Gemini API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Optional |
| `OPENAI_API_KEY` | OpenAI-compatible API key, including DeepSeek and Qwen-compatible services | Optional |
| `OPENAI_BASE_URL` / `OPENAI_MODEL` | Fill these when using an OpenAI-compatible provider | Optional |

> Ollama is better suited for local or Docker deployment. GitHub Actions is usually smoother with a cloud API.

**Email notifications (optional).**

| Secret | Description |
|---|---|
| `EMAIL_SENDER` + `EMAIL_PASSWORD` | Email push |

Recipient groups, email testing, and Markdown-to-image settings are in the [Notification Guide](docs/email_notifications.md).

**Watchlist (required).**

| Secret | Description | Required |
|---|---|---|
| `STOCK_LIST` | Comma-separated codes, e.g. `600519,hk00700,AAPL,7203.T,005930.KS` | ✅ |

**News sources (recommended).** News search strongly improves sentiment, announcements, events, and catalyst quality. Configure at least one search provider if possible.

| Secret | Description | Required |
|---|---|---|
| `ANSPIRE_API_KEYS` | Anspire AI Search, optimized for Chinese content and A-share analysis; the same key can also be used for Anspire LLM fallback | Recommended |
| `SERPAPI_API_KEYS` | SerpAPI: search-engine results for real-time financial news | Recommended |
| `TAVILY_API_KEYS` | Tavily: general news search API | Optional |
| `BOCHA_API_KEYS` | Bocha: Chinese search with AI summaries | Optional |
| `BRAVE_API_KEYS` | Brave Search: privacy-first search and US-stock news enrichment | Optional |
| `MINIMAX_API_KEYS` | MiniMax: structured search results | Optional |
| `SEARXNG_BASE_URLS` | Self-hosted SearXNG instances for quota-free fallback | Optional |

More search providers, social sentiment, and fallback behavior are in the Search Configuration guide.

**3. Enable Actions.** Open the **Actions** tab and click **I understand my workflows, go ahead and enable them**.

**4. Manual test.** **Actions → Daily Stock Analysis → Run workflow → Run workflow**.

**Done.** By default, the workflow runs every weekday at 18:00 Beijing time and skips non-trading days. Forced runs, trading-day checks, and resume rules depend on the workflow configuration (see [Scheduled Tasks](#scheduled-tasks)).

### 3. Run Modes

| Goal | Command | Behavior |
|---|---|---|
| Analyze once | `python main.py` | Analyze the watchlist and send reports as configured |
| Analyze specific stocks | `python main.py --stocks 600519,hk00700,AAPL` | Analyze only the listed codes |
| Market review | `python main.py --market-review` | Run the market review |
| Debug / dry run | `python main.py --debug` / `python main.py --dry-run` | Debug logging / run without side effects |
| Run scheduler | `python main.py --schedule` | Run the scheduler in the current process |
| Web/API only | `python main.py --serve-only` | Start the service without an initial analysis |
| Web/API and analyze | `python main.py --serve` | Start the Web/API and run one analysis |
| Local Web launcher | `python webui.py` | Launch the FastAPI service directly |
| FastAPI dev mode | `uvicorn server:app --reload --host 127.0.0.1 --port 8000` | For local development; do not enable reload in production |

Locally, open `http://127.0.0.1:8000`; interactive API documentation is at `/docs`.

For a cloud server, bind the service to an address reachable by the container or host, and configure administrator authentication, firewall rules, and an HTTPS reverse proxy. Do not expose an unprotected settings/API service directly to the Internet. See Cloud Web Access.

### 4. Docker Deployment

The Compose file provides separate services for different purposes:

```bash
docker-compose -f ./docker/docker-compose.yml build --no-cache
# Start the Web/API service and follow logs
docker logs -f stock-server
docker logs -f stock-analyzer
# Web/API service
docker compose -f docker/docker-compose.yml up -d server
# Scheduled analysis service
docker compose -f docker/docker-compose.yml up -d analyzer
# Both services
docker-compose -f ./docker/docker-compose.yml up -d            # Start both modes
```

- Inside the container, the server must listen on `0.0.0.0`; Compose maps `API_PORT` to the host.
- The database, logs, and reports are persisted through mounted volumes.
- Compose `env_file` injects **startup environment variables**; it does not create a writable `/app/.env` inside the container.
- To keep settings saved through the Web UI across container recreation, point `ENV_FILE` to a writable file on a persistent volume, and avoid stale duplicate values in the startup environment.

### 5. Configuration

#### LLM

Start simple with one model and one API key. Choose the simplest configuration that fits your deployment:

- **Legacy single provider:** one model and its provider key.
- **Channels:** named providers, multiple keys, a primary model, and fallbacks. This is the recommended advanced option and is editable in Web settings. It also supports Agent-specific models.
- **LiteLLM YAML:** expert routing configuration with the highest precedence.

The effective priority is: YAML (`LITELLM_CONFIG` / `LITELLM_CONFIG_YAML`) → `LLM_CHANNELS` → legacy provider keys. Switching modes does not silently migrate or delete old values.

When a connection test fails, check model access, API key, Base URL, provider protocol, quota, and network. Test one provider before adding fallbacks. For multi-channel setups, use the connectivity test on the Web settings page first. See the LLM provider configuration summary for provider-specific notes.

#### Notification Channels

Configure SMTP email in `.env` or Web settings. Email is the only notification transport; delivery failures do not invalidate analysis reports. To diagnose delivery, use the email test action on the settings page or run `python main.py --check-notify`. See the [Notification Guide](docs/email_notifications.md).

#### Search and News

Once a news search provider is configured, analysis can add recent news, announcements, and event context. Local RSS/Atom and NewsNow sources can also be managed as a best-effort evidence pool. Availability, quota, region, and timeouts can affect results. If search is unavailable, check the provider key, network, and quota. A single source failing should not block the core analysis.

#### Market Data

Multiple data sources fall back according to availability. A single source timing out or missing a field must not be treated as a valid zero value. Check the logs for the source, timeout, and degradation messages, and check the report's data-source and quality notes when a field is absent or stale. Do not infer values from missing data. Detailed fields, fundamental P0 timeout semantics, trading rules, and data-source priority are covered in Data Source Configuration.

#### Watchlist

`STOCK_LIST` is a comma-separated list of codes. Code formats for each market are described in `.env.example` and the market coverage notes above. See the [stock catalog guide](docs/stock-index.md) for autocomplete index maintenance.

#### Scheduled Tasks

- **Local:** start with `python main.py --schedule`. `SCHEDULE_ENABLED` controls the legacy startup behavior.
- **GitHub Actions:** has its own schedule and repository secrets/variables. The default project schedule is weekday-oriented in Beijing time; trading-day checks and manual dispatch behavior depend on the workflow configuration.
- If scheduled jobs do not run, verify the Actions runs, secrets, and workflow logs.

### 6. Web UI and Main Workflows

The Web workspace supports settings, task monitoring, manual analysis, history, full Markdown reports, Agent strategy chat, backtesting, alerts, decision signals, smart import, and light/dark themes. Authentication, smart import, autocomplete, report copying, and cloud-server access are documented in Local WebUI Management.

- **Analysis report:** submit a symbol from the Web home page, CLI, or API. Review the conclusion, risks, data sources, and report history. Reports are research aids, not investment advice.
- **Market review:** can be triggered from the CLI, Web, or a scheduled task. It uses a different market context from single-stock analysis.
- **Ask Stock / Agent strategy chat:** see below.
- **Backtesting:** evaluates historical rules. Results depend on market coverage, trading days, and data quality, and are not guarantees of future performance.
- **AI decision signals:** organize the action tendency, evidence, risks, and follow-up watch conditions from a report in a structured way. They can be queried, given feedback, and evaluated against subsequent daily bars. Signals are research aids; they do not place orders.
- **Real-time alerts:** evaluate symbol, watchlist, or market conditions against rules, and record triggered, skipped, and degraded results along with notification attempts. See the alert guide for configuration and operating boundaries.
- **Email notifications:** see the Notification Guide for routing and delivery diagnostics.
- **Smart import:** supports image, CSV/Excel, and clipboard import, with code/name/pinyin/alias autocomplete. Image import requires a configured vision-capable model. Always verify recognized codes, names, and market suffixes manually, especially for similar-looking codes.
- **AnalysisContextPack:** summarizes available data blocks and quality states. It improves visibility into missing, stale, or fallback data, but does not make unavailable data reliable.

> Analysis and alerts are decision-support tools, not investment advice or an automated trading system.

#### Agent Strategy Chat

After configuring any available AI API key, the Web `/chat` page can use strategy chat. Set `AGENT_MODE=false` only if you want to disable it explicitly. If the model or search source is unavailable, answer capability degrades accordingly.

- Built-in strategies include moving-average crossovers, Chan theory, Elliott wave, bull trend, hot themes, event-driven, growth quality, expectation repricing, and more.
- Calls real-time quotes, K-line data, technical indicators, news, and risk context.
- Supports follow-up questions, session export, notification sending, and background execution.
- Supports custom strategy files and experimental multi-agent orchestration.

Agent parameters, skill naming compatibility, multi-agent mode, and budget guards are covered in the LLM configuration guide.

### 7. Sample Output

**Decision Dashboard**

```
🎯 2026-02-08 Decision Dashboard
Analyzed 3 stocks | 🟢 Buy:0 🟡 Watch:2 🔴 Sell:1

📊 Summary
🟡 000657: Watch | Score 65 | Bullish
🟡 600105: Watch | Score 48 | Range-bound
🔴 300260: Sell | Score 35 | Bearish

🚨 Risk Alerts:
Risk 1: Main-force funds showed notable outflow.
Risk 2: Chip concentration suggests short-term resistance.

✨ Positive Catalysts:
Catalyst 1: AI-server supply-chain exposure remains a market focus.
Catalyst 2: Recent earnings growth provides fundamental support.
```

**Market Review**

```
🎯 2026-01-10 Market Review

📊 Major Indices
- SSE Composite: 3250.12 (+0.85%)
- SZSE Component: 10521.36 (+1.02%)
- ChiNext: 2156.78 (+1.35%)

📈 Market Breadth
Up: 3920 | Down: 1349 | Limit up: 155 | Limit down: 3
```

### 8. Topic Guides

These topic pages are the stable entry points for the settings UI and maintenance workflows, so the same configuration details are not duplicated across long guides:

- LLM provider and error diagnostics
- Notification channels and GitHub Actions environment variables
- Cloud server Web access
- AnalysisContextPack data quality and visibility
- Real-time alert rules
- [Stock autocomplete catalog](docs/stock-index.md)
- Notification channels and delivery diagnostics

### 9. Troubleshooting

- **Service does not start:** confirm the port is free; check `API_PORT`, `WEBUI_PORT`, the selected host, and startup logs.
- **Web page loads but API calls fail:** visit `/health` or `/api/health`, then check that `/docs` is available and inspect backend logs.
- **LLM calls fail:** verify the channel, model name, key, Base URL, account access, quota, and network. Use the Web settings connectivity test for multi-channel setups.
- **Reports have missing fields:** inspect the specific source warnings and fallback records; some markets or fields may simply not be supported.
- **Scheduled runs or notifications missing:** confirm the process is in scheduler mode, the time/trading-day condition is met, the notification channel is enabled, and the relevant workflow or delivery log shows a result.

### 10. Related Projects

DSA focuses on daily analysis reports. [AlphaEvo](https://github.com/) explores strategy backtesting and evolution for users who want to extend the workflow; it is maintained independently.

| Project | Focus |
|---|---|
| AlphaEvo | Strategy backtesting and self-evolution experiments for validating rules and iteratively exploring strategy parameters and combinations |

### 11. Release Notes and API Reference

See the changelog for release and migration notes. API fields are defined by the server's OpenAPI schema (`/docs`, `architecture/api_spec.json`); do not rely on old screenshots or parameters from earlier versions.

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

## 📂 Project Structure

```text
sloth-python/
├── ai_gen/                     # AI + MCP prompt-to-test generation
├── ai_stock/                   # AI-assisted stock analysis and reporting (storage, templates, cache under ai_stock/stock_data)
├── apps/                       # dsa-web (React/Vite frontend) and dsa-web-cypress-tests
├── load_tests/                 # JMeter, load-runner, and Postman assets
├── pytest_tests/               # Pytest unit, API, UI, DDT, and AI tests
├── robot_tests/                # Robot Framework API, calculator, UI, DDT, and unit suites
├── self_healing/               # Shared Playwright locator-recovery framework
├── skill_spring/               # Learning and research tracks
├── utils/                      # Domain-oriented shared helpers (shared config lives in utils/config/config.py)
├── temps/                      # Generated reports, logs, videos, static build output, and temporary results
├── .github/workflows/          # GitHub Actions CI/CD definitions
├── .vscode/                    # Workspace settings
├── docs/                       # Guides, including the security policy
├── pyproject.toml              # Python tooling and pytest configuration
├── readme.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── uv.lock                     # uv dependency lock file
```

<a id="feature-guides"></a>
## Feature Guides

| Area | Guide |
|---|---|
| Self-healing locators | [Self-Healing Framework](#-self-healing-framework-playwright) |
| AI-assisted test generation | [AI-Generated UI Test Scripts](#-ai-generated-ui-test-scripts-python--playwright--mcp) |
| Stock analysis | [AI Stock Architecture](ai_stock/readme.md), [DSA User Guide](#-daily-stock-analysis-dsa-user-guide) |
| DSA Web frontend | [dsa-web Readme](apps/dsa-web/readme.md) |
| DSA Web Cypress tests | [dsa-web-cypress-tests Readme](apps/dsa-web-cypress-tests/Readme.md) |
| Database utilities | [Database Utilities](utils/data_base/README.md) |
| Learning material | [Skill Spring Learning Notes](skill_spring/claude_code/claude_code_learning.md) |

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

- **Review generated code:** Treat `ai_gen/` output as a starting point and validate it with focused pytest runs before committing.
- **Keep research reproducible:** Follow the project README and notebook instructions under `skill_spring/` for learning experiments.
- **Prefer explainable analysis:** Keep stock-analysis conclusions traceable to market data, news, and strategy inputs.

### CI/CD and Reporting

- **Validate in stages:** Run focused tests locally, then the smoke or regression workflow as the change requires.
- **Keep CI headless:** Install Playwright browsers and use `PW_HEADLESS=1` in automated UI runs.
- **Preserve diagnostics:** Use Allure, Robot HTML reports, screenshots, videos, and uploaded artifacts to investigate failures.

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

Report security vulnerabilities through the [Security Policy](docs/security.md), not a public issue. Never include API keys, tokens, credentials, or other sensitive values in reports.

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
