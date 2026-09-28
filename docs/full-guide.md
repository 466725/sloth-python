# DSA User Guide

This is the English user guide for Daily Stock Analysis (DSA). It consolidates setup, configuration, deployment, and feature boundaries. The root `.env.example` and current Web settings define supported configuration keys; `/docs` and `architecture/api_spec.json` are the API references.

## What DSA Does

DSA collects market data for a watchlist, builds technical and news context, generates AI-assisted analysis reports, stores report history, and can deliver notifications. The Web workspace also provides Ask Stock, backtesting, portfolio views, alerts, and structured decision signals.

Coverage differs by market. A-shares, Hong Kong, and US stocks have the broadest data support. Japan uses `.T`, Korea KOSPI uses `.KS`, and KOSDAQ uses `.KQ`. Japan/Korea currently use YFinance daily, basic/delayed quotes, and technical indicators. Real-time quotes, full fundamentals, a complete market-wide symbol index, capital flow, dragon-tiger data, boards, market review, and JPY/KRW portfolio valuation are not guaranteed. Missing data is not a zero value or a trading signal.

## First Run

Use a Python version supported by the current project CI. Create a virtual environment, install dependencies, and copy the environment template:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then configure at least one LLM provider and `STOCK_LIST`. Search, notification, and additional market-data providers are optional. Keep credentials out of Git, logs, issues, and screenshots.

## Run Modes

| Goal | Command | Behavior |
| --- | --- | --- |
| Analyze once | `python main.py` | Run analysis using the configured watchlist |
| Run scheduler | `python main.py --schedule` | Keep the local scheduler running |
| Start Web/API only | `python main.py --serve-only` | Start the service without an initial analysis |
| Start Web/API and analyze | `python main.py --serve` | Start the service and run analysis |
| Start through the Web launcher | `python webui.py` | Launch the FastAPI service directly |
| Local ASGI development | `uvicorn server:app --reload --host 127.0.0.1 --port 8000` | Enables reload; do not use reload for production |

Open `http://127.0.0.1:8000`; interactive API documentation is at `/docs`.

## Docker Deployment

The Compose file has separate `server` and `analyzer` services:

```bash
# Web/API
 docker compose -f docker/docker-compose.yml up -d server
# Scheduled analysis
 docker compose -f docker/docker-compose.yml up -d analyzer
# Both services
 docker compose -f docker/docker-compose.yml up -d server analyzer
```

Inside the container, the server must bind to `0.0.0.0`; Compose maps `API_PORT` to the host. Database, logs, and reports are mounted for persistence. Compose `env_file` injects startup environment variables; it does not create a writable `/app/.env`. To persist settings saved through the Web UI across container recreation, configure `ENV_FILE` to a writable file on a mounted volume, and avoid stale duplicate values in the startup environment. See [cloud Web access](deploy-webui-cloud.md).

For a public server, configure administrator authentication, restrict network access, and use HTTPS through a reverse proxy. Do not expose an unprotected settings/API service directly to the Internet.

## Model Configuration

Choose the simplest configuration that fits the deployment:

- **Legacy single provider**: one model and its provider key.
- **Channels**: named providers, multiple keys, a primary model, and fallbacks; this is the recommended advanced option and is editable in Web settings.
- **LiteLLM YAML**: expert routing configuration with the highest precedence.

The effective priority is YAML (`LITELLM_CONFIG` / `LITELLM_CONFIG_YAML`), then `LLM_CHANNELS`, then legacy provider keys. Switching modes does not silently migrate or delete old values. Check model access, API key, Base URL, provider protocol, quota, and network when a connection test fails. Provider-specific notes are in [LLM provider configuration](llm-providers.md).

## Notification Channel Configuration

Configure one or more supported channels in `.env` or Web settings. The notification service routes report, alert, and error messages independently; a failing channel should not invalidate the analysis report. Use the settings page's test action or `python main.py --check-notify` to diagnose delivery. Some channels have different modes: for example, Feishu group Webhook delivery is distinct from App Bot credentials and Stream Bot events. See [notification configuration](notifications.md).

## Search Service Configuration

Search providers enrich analysis with recent news and catalysts. Configure provider keys in `.env` or Web settings; availability, quota, region, and timeout can affect results. Local RSS/Atom and NewsNow sources can also be managed as a best-effort evidence pool. One source failing should not block the core report workflow.

## Data Source Configuration

Market-data providers use fallback behavior where supported. Check the report's data-source and quality notes when a field is absent or stale. Do not infer a value from missing data. Tushare stock-list tools and refresh steps are in the [Tushare guide](TUSHARE_STOCK_LIST_GUIDE.md).

## Scheduled Task Configuration

Local scheduling is started with `python main.py --schedule`; `SCHEDULE_ENABLED` controls the legacy startup behavior. GitHub Actions has its own schedule and repository secrets/variables. The default project schedule is weekday-oriented in Beijing time; trading-day checks and workflow dispatch behavior depend on the workflow configuration. Verify Actions runs, secrets, and workflow logs when scheduled jobs do not execute.

## Local WebUI Management Interface

The Web workspace supports manual stock analysis, task progress, history, Ask Stock, backtesting, portfolios, alerts, decision signals, settings, and smart import. Image-based import requires a configured vision-capable model; verify recognized stock codes and names before analysis.

- **AnalysisContextPack** summarizes available data blocks and quality states. It improves visibility into missing, stale, or fallback data; it does not make unavailable data reliable. See [context-pack boundaries](analysis-context-pack.md).
- **Decision signals** organize an analysis recommendation, evidence summary, risk, and watch conditions. They do not place orders or rebalance a portfolio. Feedback and daily-bar outcome evaluation are research aids.
- **Alerts** evaluate configured rules and record triggered/skipped/degraded results and notification attempts. See [alert boundaries](alerts.md).
- **Backtesting and portfolio analysis** depend on historical coverage, prices, and market support; results are not guarantees of future performance.
- **Bot integrations** expose selected analysis workflows through supported messaging transports. Command and setup overview: [Bot guide](bot-command_EN.md).

Analysis and alerts are decision-support tools, not investment advice or an automated trading system.

## Troubleshooting

1. **Service does not start**: check that the port is free and review startup logs; verify `API_PORT`, `WEBUI_PORT`, and the selected host.
2. **Web page loads but API calls fail**: check `/health` or `/api/health`, then open `/docs` and inspect backend logs.
3. **LLM calls fail**: verify provider, model, key, Base URL, account access, quota, and network. Test one provider before adding fallbacks.
4. **Reports have missing fields**: inspect source/quality warnings and check whether that market supports the requested data.
5. **Scheduled runs or notifications are missing**: confirm the process is in scheduler mode, the time/trading-day condition is met, the channel is enabled, and the relevant workflow or delivery log shows a result.

See the [changelog](CHANGELOG.md) for release and migration notes. For packaging, use the maintained [desktop guide](desktop-package.md).
