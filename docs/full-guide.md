# Daily Stock Analysis (DSA) User Guide

This is the main guide for Daily Stock Analysis (DSA). It covers features, quick start, installation, configuration, run modes, deployment, and feature boundaries. The root `.env.example` and the fields currently visible in the Web settings page define the supported configuration keys; `/docs` and `architecture/api_spec.json` are the API references.

## 1. Overview

DSA reads a watchlist and market data, combines technical indicators, news, and an LLM to generate analysis reports, and can save results to history or send them through notification channels. The Web workspace also provides Ask Stock, backtesting, alerts, and AI decision signals.

### Key Features

| Capability | Coverage |
|---|---|
| AI decision reports | Core conclusion, score, trend, entry/exit levels, risk alerts, catalysts, and action checklist |
| Multi-market data | A-shares, Hong Kong, US, ETFs: quotes, K-lines, technical indicators, capital flow, chips, news, announcements, and fundamentals. Japan/Korea (Yahoo `.T` / `.KS` / `.KQ`): see market coverage below |
| Web / desktop workspace | Manual analysis, task progress, history, full Markdown reports, backtest, settings, and light/dark themes |
| Agent strategy chat | Multi-turn Q&A with 15 built-in strategies across Web/Bot/API |
| Smart import & autocomplete | Image, CSV/Excel, clipboard import; code/name/pinyin/alias autocomplete |
| Automation & notifications | GitHub Actions, Docker, local scheduler, FastAPI service, and WeChat Work / Feishu / Telegram / Discord / Slack / Email delivery |

### Market Coverage

Coverage differs by market. A-shares, Hong Kong, and US stocks have the broadest support. Japan uses the `.T` suffix, Korea KOSPI uses `.KS`, and KOSDAQ uses `.KQ`. Japan/Korea currently use only the YFinance path: daily bars, basic/delayed quotes, and technical indicators. The following are **not guaranteed** for these markets: real-time quotes, full fundamentals, a complete market-wide symbol list, capital flow, dragon-tiger data, sector/board data, and market review. **Missing data is not a zero value and not a bullish/bearish signal.**

### Tech Stack & Data Sources

| Type | Supported |
|---|---|
| AI models | Anspire, AIHubMix, Gemini, OpenAI-compatible providers, DeepSeek, Qwen, Claude, Ollama |
| Market data | TickFlow, AkShare, Tushare, Pytdx, Baostock, YFinance, Longbridge |
| News search | Anspire, SerpAPI, Tavily, Bocha, Brave, MiniMax, SearXNG |
| Social sentiment | Stock Sentiment API for Reddit / X / Polymarket (US stocks only) |

## 2. Quick Start

### Option 1: GitHub Actions (Recommended)

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

**Notification channels (configure at least one).**

| Secret | Description |
|---|---|
| `WECHAT_WEBHOOK_URL` | WeChat Work bot |
| `FEISHU_WEBHOOK_URL` | Feishu bot |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Telegram |
| `DISCORD_WEBHOOK_URL` | Discord webhook |
| `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` | Slack bot |
| `EMAIL_SENDER` + `EMAIL_PASSWORD` | Email push |

More channels, signatures, email groups, and Markdown-to-image settings are in the Notification Guide.

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

### Option 2: Local Installation

Requires Python 3.10 or later (check the project CI for the currently supported versions).

```bash
# Clone the project
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# Create a virtual environment and install dependencies
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env    # then edit .env

# Run analysis
python main.py
```

In `.env`, configure at least one usable LLM provider and `STOCK_LIST`. Notification channels, news search, and additional market-data providers are optional; when not configured, the system uses the available data sources and fallback paths. **Never commit real credentials to Git, issues, logs, or screenshots.**

Common first-run checks: confirm `.env` is in the repository root, variable names are spelled correctly, the model name matches the channel, and review the backend logs in `logs/`. The Web settings page can be used to inspect and maintain supported runtime configuration.

## 3. Run Modes

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

## 4. Docker Deployment

The Compose file provides separate services for different purposes:

```bash
# Web/API service
docker compose -f docker/docker-compose.yml up -d server
# Scheduled analysis service
docker compose -f docker/docker-compose.yml up -d analyzer
# Both services
docker compose -f docker/docker-compose.yml up -d server analyzer
```

- Inside the container, the server must listen on `0.0.0.0`; Compose maps `API_PORT` to the host.
- The database, logs, and reports are persisted through mounted volumes.
- Compose `env_file` injects **startup environment variables**; it does not create a writable `/app/.env` inside the container.
- To keep settings saved through the Web UI across container recreation, point `ENV_FILE` to a writable file on a persistent volume, and avoid stale duplicate values in the startup environment.

For desktop builds, see the Desktop Packaging Guide.

## 5. Configuration

### LLM

Start simple with one model and one API key. Choose the simplest configuration that fits your deployment:

- **Legacy single provider:** one model and its provider key.
- **Channels:** named providers, multiple keys, a primary model, and fallbacks. This is the recommended advanced option and is editable in Web settings. It also supports Agent-specific models.
- **LiteLLM YAML:** expert routing configuration with the highest precedence.

The effective priority is: YAML (`LITELLM_CONFIG` / `LITELLM_CONFIG_YAML`) → `LLM_CHANNELS` → legacy provider keys. Switching modes does not silently migrate or delete old values.

When a connection test fails, check model access, API key, Base URL, provider protocol, quota, and network. Test one provider before adding fallbacks. For multi-channel setups, use the connectivity test on the Web settings page first. See the LLM provider configuration summary for provider-specific notes.

### Notification Channels

Configure one or more supported channels in `.env` or Web settings. The notification service routes report, alert, and error messages independently, so a failing channel should not invalidate the analysis report. To diagnose delivery, use the test action on the settings page or run `python main.py --check-notify`. Some channels have distinct modes; for example, Feishu group Webhook delivery is different from App Bot credentials and Stream Bot events. See the Notification Guide.

### Search and News

Once a news search provider is configured, analysis can add recent news, announcements, and event context. Local RSS/Atom and NewsNow sources can also be managed as a best-effort evidence pool. Availability, quota, region, and timeouts can affect results. If search is unavailable, check the provider key, network, and quota. A single source failing should not block the core analysis.

### Market Data

Multiple data sources fall back according to availability. A single source timing out or missing a field must not be treated as a valid zero value. Check the logs for the source, timeout, and degradation messages, and check the report's data-source and quality notes when a field is absent or stale. Do not infer values from missing data. Detailed fields, fundamental P0 timeout semantics, trading rules, and data-source priority are covered in Data Source Configuration.

### Watchlist

`STOCK_LIST` is a comma-separated list of codes. Code formats for each market are described in `.env.example` and the market coverage notes above. Tushare stock-list tools and refresh steps are in the Tushare guide.

### Scheduled Tasks

- **Local:** start with `python main.py --schedule`. `SCHEDULE_ENABLED` controls the legacy startup behavior.
- **GitHub Actions:** has its own schedule and repository secrets/variables. The default project schedule is weekday-oriented in Beijing time; trading-day checks and manual dispatch behavior depend on the workflow configuration.
- If scheduled jobs do not run, verify the Actions runs, secrets, and workflow logs.

## 6. Web UI and Main Workflows

The Web workspace supports settings, task monitoring, manual analysis, history, full Markdown reports, Agent strategy chat, backtesting, alerts, decision signals, smart import, and light/dark themes. Authentication, smart import, autocomplete, report copying, and cloud-server access are documented in Local WebUI Management.

- **Analysis report:** submit a symbol from the Web home page, CLI, API, or Bot. Review the conclusion, risks, data sources, and report history. Reports are research aids, not investment advice.
- **Market review:** can be triggered from the CLI, Web, or a scheduled task. It uses a different market context from single-stock analysis.
- **Ask Stock / Agent strategy chat:** see below.
- **Backtesting:** evaluates historical rules. Results depend on market coverage, trading days, and data quality, and are not guarantees of future performance.
- **AI decision signals:** organize the action tendency, evidence, risks, and follow-up watch conditions from a report in a structured way. They can be queried, given feedback, and evaluated against subsequent daily bars. Signals are research aids; they do not place orders.
- **Real-time alerts:** evaluate symbol, watchlist, or market conditions against rules, and record triggered, skipped, and degraded results along with notification attempts. See the alert guide for configuration and operating boundaries.
- **Notifications and Bots:** see the Notification Guide for channels, routing, and diagnostics, and the Bot Guide for commands and supported messaging transports.
- **Smart import:** supports image, CSV/Excel, and clipboard import, with code/name/pinyin/alias autocomplete. Image import requires a configured vision-capable model. Always verify recognized codes, names, and market suffixes manually, especially for similar-looking codes.
- **AnalysisContextPack:** summarizes available data blocks and quality states. It improves visibility into missing, stale, or fallback data, but does not make unavailable data reliable.

> Analysis and alerts are decision-support tools, not investment advice or an automated trading system.

### Agent Strategy Chat

After configuring any available AI API key, the Web `/chat` page can use strategy chat. Set `AGENT_MODE=false` only if you want to disable it explicitly. If the model or search source is unavailable, answer capability degrades accordingly.

- Built-in strategies include moving-average crossovers, Chan theory, Elliott wave, bull trend, hot themes, event-driven, growth quality, expectation repricing, and more.
- Calls real-time quotes, K-line data, technical indicators, news, and risk context.
- Supports follow-up questions, session export, notification sending, and background execution.
- Supports custom strategy files and experimental multi-agent orchestration.

Agent parameters, skill naming compatibility, multi-agent mode, and budget guards are covered in the LLM configuration guide.

## 7. Sample Output

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

## 8. Topic Guides

These topic pages are the stable entry points for the settings UI and maintenance workflows, so the same configuration details are not duplicated across long guides:

- LLM provider and error diagnostics
- Notification channels and GitHub Actions environment variables
- Cloud server Web access
- AnalysisContextPack data quality and visibility
- Real-time alert rules
- Tushare stock-list tool
- Notification channels and delivery diagnostics
- Bot command guide

## 9. Troubleshooting

- **Service does not start:** confirm the port is free; check `API_PORT`, `WEBUI_PORT`, the selected host, and startup logs.
- **Web page loads but API calls fail:** visit `/health` or `/api/health`, then check that `/docs` is available and inspect backend logs.
- **LLM calls fail:** verify the channel, model name, key, Base URL, account access, quota, and network. Use the Web settings connectivity test for multi-channel setups.
- **Reports have missing fields:** inspect the specific source warnings and fallback records; some markets or fields may simply not be supported.
- **Scheduled runs or notifications missing:** confirm the process is in scheduler mode, the time/trading-day condition is met, the notification channel is enabled, and the relevant workflow or delivery log shows a result.

## 10. Related Projects

DSA focuses on daily analysis reports. [AlphaEvo](https://github.com/) explores strategy backtesting and evolution for users who want to extend the workflow; it is maintained independently.

| Project | Focus |
|---|---|
| AlphaEvo | Strategy backtesting and self-evolution experiments for validating rules and iteratively exploring strategy parameters and combinations |

## 11. Release Notes and API Reference

See the changelog for release and migration notes. API fields are defined by the server's OpenAPI schema (`/docs`, `architecture/api_spec.json`); do not rely on old screenshots or parameters from earlier versions.