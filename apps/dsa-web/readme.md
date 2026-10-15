# DSA Web

React + TypeScript frontend for Daily Stock Analysis (DSA). It is the Web workspace described in the root [readme.md](../../readme.md#-daily-stock-analysis-dsa-user-guide), served by the FastAPI backend (`server.py` / `main.py --serve-only`) or run standalone against it via Vite.

## Main Functions

| Route | Page | Purpose |
|---|---|---|
| `/` | `HomePage` | Watchlist, manual analysis entry, task progress, market review, history, and full Markdown reports |
| `/chat` | `ChatPage` | Ask Stock / Agent strategy chat (multi-turn Q&A over built-in strategies) |
| `/decision-signals` | `DecisionSignalsPage` | AI decision signals: action tendency, evidence, risks, follow-up watch conditions |
| `/backtest` | `BacktestPage` | Backtesting of historical rules against market data |
| `/alerts` | `AlertsPage` | Real-time alert rules and their triggered/skipped/degraded results |
| `/usage` | `TokenUsagePage` | LLM token usage tracking |
| `/settings` | `SettingsPage` | LLM providers, notification channels, data sources, and other runtime configuration |
| `/login` | `LoginPage` | Password-based auth, shown only when the backend has auth enabled |

Cross-cutting features available from the shell: smart import (image/CSV/Excel/clipboard), code/name/pinyin/alias autocomplete, light/dark theme, and English/Chinese UI language toggle.

## Stock Autocomplete Catalog

The Web app searches a local catalog served at `/stocks.index.json`. The bundled
[`stocks.index.json`](public/stocks.index.json) supports stock codes, names,
aliases, full pinyin, and pinyin initials. Searching this catalog does not call
a market-data provider or require a provider token.

### Remote updates

Set `STOCK_INDEX_REMOTE_UPDATE_ENABLED=true` (the default) to enable best-effort
updates from the built-in GitHub main source. The backend caches the downloaded
catalog locally. If an update fails, it keeps using the existing cache or the
bundled index. Remote updates are separate from quote retrieval and stock
analysis; disabling them does not disable autocomplete.

### Updating the bundled catalog

The generated index is checked in at
[`public/stocks.index.json`](public/stocks.index.json) and served by the Web app.
The repository no longer includes a catalog generation script. To change the
bundled catalog, update the JSON asset through the project's chosen
data-maintenance process and review the change before deploying it.

If a rebuild is incorrect, restore the previous bundled index from version
control and redeploy the Web assets. Disable remote updates while investigating
if needed. Market-data provider routing and analysis configuration are unchanged
by an index rebuild.

## Alert Center

The alert center currently supports one rule type: **percentage price change**
(`price_change_percent`). It evaluates the percentage change reported by the
current real-time quote. It does not compare the current price with the previous
polling cycle, and it is not a fixed-price alert.

### Create a rule

Create rules from the Web app's **Alerts** page or through the API. The Web form
supports the following fields:

| Field | Supported values and meaning |
| --- | --- |
| `alert_type` | `price_change_percent` only |
| `target_scope` | `single_symbol` or `watchlist` |
| `target` | A stock symbol for `single_symbol`; `default` for `watchlist` |
| `parameters.direction` | `up` or `down` |
| `parameters.change_pct` | A finite number greater than zero, in percent; `3` means 3% |
| `severity` | `info`, `warning`, or `critical` |
| `enabled` | Whether the background worker evaluates the rule |

An `up` rule triggers when the quote's change percentage is greater than or equal
to the positive threshold. A `down` rule triggers when it is less than or equal to
the negative threshold; enter the threshold as a positive number for either
direction. If a quote or valid change percentage is unavailable, evaluation is
skipped. Evaluation errors are recorded as failures with sanitized diagnostics.
A failed rule does not stop the worker from evaluating other rules.

Example request for `POST /api/v1/alerts/rules`:

```json
{
  "name": "Daily decline",
  "target_scope": "single_symbol",
  "target": "600519",
  "alert_type": "price_change_percent",
  "parameters": {"direction": "down", "change_pct": 3},
  "severity": "warning",
  "enabled": true
}
```

For a watchlist rule, send `"target_scope": "watchlist"` and
`"target": "default"`. Each worker cycle refreshes the configured `STOCK_LIST`,
removes duplicate symbols, and expands the rule to at most 100 symbols. Trigger
history and cooldowns are tracked per expanded symbol. An empty watchlist is
recorded as skipped. A dry run has a 10-second per-target timeout and a 30-second
total timeout; its response includes at most 20 target details.

### Background evaluation and notifications

The alert worker runs only in schedule mode. Enable it and choose its polling
interval with:

```dotenv
AGENT_EVENT_MONITOR_ENABLED=true
AGENT_EVENT_MONITOR_INTERVAL_MINUTES=5
AGENT_EVENT_ALERT_RULES_JSON=
```

The worker runs immediately when schedule mode starts, then polls at the configured
interval (default: five minutes). It loads enabled rules from the database and
legacy rules from `AGENT_EVENT_ALERT_RULES_JSON`. Rules created or changed through
the Web app or API are picked up on a subsequent poll without restarting the
application.

Triggered alerts use the configured email notification route. Configure
`NOTIFICATION_ALERT_CHANNELS` and SMTP settings as described in the
[email notification guide](../../docs/email_notifications.md). Notification noise
controls also apply to alerts.

Database rules use a 24-hour cooldown by default. Set
`cooldown_policy.cooldown_seconds` to override it; `0` disables the rule
cooldown. A new database cooldown starts only after a real notification channel
succeeds. Failed delivery, no available channel, or gateway suppression does not
start a new cooldown. Cooldown-suppressed alerts are still recorded as notification
attempts. Legacy JSON rules use a 24-hour in-process duplicate-suppression
fingerprint; this state is not persisted across application restarts.

### Legacy JSON rules

`AGENT_EVENT_ALERT_RULES_JSON` accepts a JSON array of single-symbol percentage
change rules. It does not support watchlist expansion:

```dotenv
AGENT_EVENT_ALERT_RULES_JSON=[{"stock_code":"600519","alert_type":"price_change_percent","direction":"up","change_pct":3}]
```

The runtime skips invalid legacy entries and logs a warning while continuing with
valid rules. If a database rule and a legacy rule have the same target, type, and
parameters, the database rule takes precedence. Existing environment files are
not rewritten automatically.

### API and stored records

| Operation | Endpoint |
| --- | --- |
| Create / list rules | `POST /api/v1/alerts/rules` / `GET /api/v1/alerts/rules` |
| Get / update / delete a rule | `GET` / `PATCH` / `DELETE /api/v1/alerts/rules/{rule_id}` |
| Enable / disable a rule | `POST /api/v1/alerts/rules/{rule_id}/enable` or `/disable` |
| Dry-run a rule | `POST /api/v1/alerts/rules/{rule_id}/test` |
| List trigger history | `GET /api/v1/alerts/triggers` |
| List notification attempts | `GET /api/v1/alerts/notifications` |

The rule-list endpoint supports filters for `enabled`, `alert_type`,
`target_scope`, `target`, and `source`. Trigger history can be filtered by
`rule_id`, `target`, and `status`; notification attempts can be filtered by
`trigger_id`, `channel`, and `success`. All three list endpoints are paginated.
Unsupported alert types and target scopes are rejected.

The dry-run endpoint evaluates the rule without sending email or writing trigger
history or notification attempts. Background evaluation records triggered,
skipped, degraded, and failed results.

Alert data is stored in `alert_rules`, `alert_triggers`, `alert_notifications`,
and `alert_cooldowns`. Trigger records include the observed value, threshold,
reason, data source, available quote timestamp, and status. Alert history may
also include analysis-stage summaries and decision-signal context; alerts do not
introduce automatic trading behavior.

### Cleanup, deployment, and rollback

When the alert repository is initialized (for example, on an alert API request or
when the background worker starts), it permanently deletes rules whose
`alert_type` is not `price_change_percent`, together with their associated
trigger history, notification attempts, and cooldown records. The deletion is
performed transactionally and is idempotent. Supported percentage-change rules
and their records are preserved. Unlinked legacy history is not deleted.

Unsupported rules in private environment configuration are not removed from the
file; invalid entries are skipped at runtime and should be cleaned up manually.
After deploying, restart the backend and update the Web/Desktop frontend assets.
An already running process does not load the new application code automatically.

If rollback may be needed, back up the database and private configuration before
starting the new version. Restoring the previous code and frontend assets restores
the old behavior, but **cannot recover data already deleted by the new version**.
Recovery of deleted database records requires a database backup.

## Tech Stack

- React 19 + TypeScript, React Router
- Vite 7 (dev server and build), Tailwind CSS 4
- Zustand for state, Axios for API calls, Recharts for charts
- Vitest + Testing Library for unit/component tests
- E2E tests live in separate packages: [`apps/dsa-web-playwright-tests`](../dsa-web-playwright-tests/Readme.md) (Playwright, authenticated flows) and [`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md) (Cypress, Page Object Model)

## Running Locally

```bash
cd apps/dsa-web
npm install
npm run dev        # Vite dev server at http://localhost:5173
```

The dev server proxies `/api` to a backend (see `vite.config.ts`). Start the backend separately for any page that calls the API (most pages do):

```powershell
# from the repo root, in a separate terminal
python main.py --serve-only --host 127.0.0.1 --port 8000
```

Other scripts (run from `apps/dsa-web`):

```bash
npm run build       # type-check (tsc -b) and production build
npm run preview      # preview the production build
npm run lint         # ESLint
```

## Maintaining Tests

All commands below are run from `apps/dsa-web`:

```bash
cd apps/dsa-web
```

### Unit / Component Tests (Vitest)

```bash
npm test                 # vitest run
```

- Specs live beside the code under `src/**/__tests__/` and in `tests/` (e.g. i18n fallback, theme tokens, UI governance checks).
- Uses `jsdom` + Testing Library; setup file is `src/setupTests.ts` (see `vitest.config.ts`).
- Add new tests next to the component/module they cover, following the existing `*.test.ts(x)` naming.

### E2E Tests

E2E tests live in separate sibling packages, not in this folder:

- **Playwright** ([`apps/dsa-web-playwright-tests`](../dsa-web-playwright-tests/Readme.md)): Authenticated smoke tests covering login, home dashboard, chat, and report flows. Auto-starts backend and frontend servers.
- **Cypress** ([`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md)): Page Object Model tests with Allure reporting.

Start the backend and/or `npm run dev` here first, then follow the respective package's README to run or add specs.

### Adding New Tests

- Prefer Vitest + Testing Library for component/unit behavior that doesn't need a real backend.
- For E2E tests, choose the appropriate package: Playwright for authenticated backend flows, Cypress for page-object-based UI coverage.
- Keep assertions on stable text/roles/ids rather than styling classes, and avoid hardcoding secrets — use environment variables.
