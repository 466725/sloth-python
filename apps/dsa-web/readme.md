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

## Web Workflows

### Analysis and reports

From the home page, select a symbol to start an analysis and follow its task
progress. Reports include the conclusion, risks, data-source context, and any
available quality details; completed reports are available in history. Reports
are research aids and do not guarantee future results.

Market review is a separate workflow from single-stock analysis. It can be
started from the Web app or CLI and uses market-wide context where supported.

### Ask Stock chat

The `/chat` page supports multi-turn questions using configured models and the
application's existing stock-data, analysis, and strategy tools. Built-in
strategies can be selected explicitly; custom strategies and experimental
multi-agent modes depend on the backend configuration. Provider setup is covered
in the [LLM provider guide](../../ai_stock/llm/llm-providers.md).

### Backtesting and decision signals

Backtesting evaluates historical rules against available market data. Results
depend on market coverage, trading calendars, and data quality; they are not
guarantees of future performance.

Decision signals organize an analysis into an action tendency, evidence, risks,
and follow-up watch conditions. Signals can be queried and evaluated against
subsequent daily bars. They do not place orders.

### Alerts and notifications

The [Alert Center](#alert-center) supports percentage price-change rules for a
single symbol or the configured watchlist. Alert evaluation and email delivery
are described in that guide and the [email notification guide](#email-notifications).

### Import and symbol lookup

Smart import accepts images, CSV/Excel files, and clipboard content. Image
recognition requires a configured vision-capable model. Review recognized names,
codes, and market suffixes before submitting. Autocomplete searches the local
catalog by symbol, name, alias, full pinyin, or pinyin initials; see the
[stock autocomplete catalog guide](#stock-autocomplete-catalog).

### Access and troubleshooting

When running the frontend separately, start the FastAPI backend and use the
configured Vite proxy. If a page loads but API calls fail, check `/health` or
`/api/health`, confirm `/docs` is available, and inspect backend logs. For
remote access, enable administrator authentication and protect the service with
firewall rules and an HTTPS reverse proxy; do not expose an unprotected settings
or API service to the public Internet.

## Stock Analyzer Skill

The runtime skill bundle is
[`strategies/stock-analyzer/skill.md`](../../strategies/stock-analyzer/skill.md).
The Agent loads it automatically from the built-in `strategies/` directory;
setting `AGENT_SKILL_DIR` is not required.

The skill is user-invocable and appears in the Web app's skill selector. It is
not part of the default active skill set, so users can choose it explicitly in
chat or analysis without changing the behavior of all existing default
analyses.

For custom skill bundles, set `AGENT_SKILL_DIR` to a separate directory
containing YAML definitions or nested `skill.md` bundles. The runtime loads
those in addition to built-in strategies.

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
[email notification guide](#email-notifications). Notification noise
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

## Analysis Context Pack

The `AnalysisContextPack` is an internal, versioned envelope that describes the
inputs available to a stock analysis and the quality or limitations of those
inputs. The pipeline builds it from artifacts it has already fetched. It does
not introduce another data-fetching path.

The full pack is used to create two separate outputs:

1. A low-sensitivity `analysis_context_pack_summary` for ordinary and Agent
   analysis prompts.
2. A whitelisted `analysis_context_pack_overview` for reports and history APIs.

The full pack is not itself a public API contract. Its version is currently
`PACK_VERSION = "1.0"`. There is no dedicated environment switch for disabling
pack construction or prompt-summary generation.

### Data flow

For ordinary and Agent analysis, `StockAnalysisPipeline` assembles
`PipelineAnalysisArtifacts`, calls `AnalysisContextBuilder.build()`, then
renders the prompt summary and public overview. If pack output generation fails,
the pipeline logs a warning and continues without those outputs.

The builder is an assembler: it consumes the pipeline's current artifacts and
does not independently call the database, fetchers, search services, Agent
tools, or market-data providers. Its main input fields are:

| Artifact | Used for |
| --- | --- |
| `code`, `stock_name`, `market` | The pack subject |
| `phase` | The market-phase context already resolved by the caller |
| `base_context` | Recent daily-bar context |
| `enhanced_context` | Intraday/estimated-bar indicators and quote metadata |
| `realtime_quote` | Quote data and its source/timestamp |
| `trend_result` | Technical-analysis block |
| `chip_data` | Chip-distribution block |
| `fundamental_context` | Fundamental status, coverage, and source chain |
| `news_context`, `news_result_count` | News availability and result count |
| `metadata` | Additional non-payload metadata, including trigger source |

The builder also offers `build_batch()` to assemble multiple packs from the
same artifact structure.

### Pack structure and block behavior

The top-level envelope contains `pack_version`, `subject`, `phase`, `blocks`,
`data_quality`, `metadata`, and `created_at`. The subject contains `code`,
optional `stock_name`, and optional `market`. `created_at` is a datetime
serialized as ISO 8601; item and block timestamps, when present, must also be
ISO 8601 datetimes. A calendar date by itself is kept as a value or metadata,
not as a timestamp.

Each block has a status, items, optional source and timestamp, warnings, and
metadata. Each item has a status and may carry a value, source, timestamp,
fallback source, missing reason, warnings, and metadata. The builder currently
creates these blocks:

| Block | Current inputs and behavior |
| --- | --- |
| `quote` | Uses the existing real-time quote. Explicit stale markers take precedence over fallback markers; otherwise a quote with a fallback source is `fallback`, and an ordinary quote is `available`. Missing quotes are `missing`. |
| `daily_bars` | Uses `base_context.today`, `base_context.yesterday`, and `base_context.date`. Both bars present means `available`; only one means `partial`; neither or an explicit `data_missing` means `missing`. |
| `technical` | Uses `trend_result`. A real-time overlay or an explicitly partial/estimated current bar marks the block `partial`, with an `intraday_realtime_overlay` warning. Missing trend data is `missing`. |
| `chip` | Uses `chip_data`. Missing data is `missing`, unless input metadata explicitly marks chip data unsupported, in which case it is `not_supported`. |
| `fundamentals` | Maps input statuses `ok`/`available`, `not_supported`, `partial`, and `failed` to the corresponding pack states. A failed fundamental pipeline uses the stable reason `fundamental_pipeline_failed`; raw error text is not included. |
| `news` | Non-empty `news_context` is `available`; absent or blank content is `missing`. `news_result_count`, when provided, is recorded in pack metadata. |

`phase` remains a dictionary supplied by the caller; the pack does not define a
separate market-phase enum. Daily market context is a related but separate
pipeline feature: its prompt summary and guardrails are not the same field as
the pack's `phase`.

### Data-quality states and score

The states below describe the quality or availability of input data. They do not
indicate whether the analysis, alert, backtest, or notification operation
succeeded.

| State | Meaning |
| --- | --- |
| `available` | Data is present and usable in the current path. |
| `missing` | Data expected by the current path was not available. |
| `not_supported` | The market, source, or path does not support this data. |
| `fallback` | A secondary source or fallback path supplied the data. |
| `stale` | Data is present but explicitly marked as not fresh enough. |
| `estimated` | The value is an estimate, not a complete observation. |
| `partial` | A block is only partly available, or uses an intraday overlay. |
| `fetch_failed` | A data fetch was attempted and explicitly failed. |

The builder assigns status scores of `available` 100, `partial` 75,
`estimated` 75, `not_supported` 70, `fallback` 65, `stale` 50, `missing` 35,
and `fetch_failed` 25. It calculates the weighted overall score using these
block weights:

| Block | Weight |
| --- | ---: |
| `quote` | 25 |
| `daily_bars` | 25 |
| `technical` | 25 |
| `news` | 10 |
| `fundamentals` | 10 |
| `chip` | 5 |

The overall score is rounded to an integer from 0 to 100. Levels are `good` at
85 or above, `usable` at 70–84, `limited` at 55–69, and `poor` below 55.
Limitations are selected from block states using a separate rule: core blocks
(`quote`, `daily_bars`, `technical`) report stale, fallback, missing,
fetch-failed, partial, or estimated states; auxiliary blocks (`news`,
`fundamentals`, `chip`) report stale, fallback, or fetch-failed states. At most
five limitations are emitted.

These scores are comparative quality signals, not probabilities or guarantees
about the correctness of an analysis.

### Prompt summary and public overview

#### Prompt summary

The prompt renderer intentionally ignores item `value` fields. The
`analysis_context_pack_summary` can include the subject, pack version, block
statuses, sources, warning codes, missing reasons, news result count, quality
score/level, limitations, and phase-related data constraints. It is rendered in
the selected report language and passed to ordinary analysis and Agent
workflows.

This restriction applies to the pack summary only. Other analysis prompt
sections may contain input data under their existing contracts.

#### Public overview

`render_analysis_context_pack_overview()` projects a whitelist rather than
returning the full pack or prompt summary. The overview includes:

- Pack version, creation time, and subject identifiers.
- Per-block key, label, status, source, warnings, and missing reasons.
- Counts by data-quality status.
- Overall score, quality level, approved block scores, and limitations.
- Top-level warnings and safe metadata such as trigger source and news result
  count.

Persisted overviews are validated and sanitized again when extracted from a
context snapshot. The raw `context_snapshot` API view removes the top-level
overview and market-phase summary because they are exposed as separate
structured fields; it also removes selected context-only fields such as
portfolio and daily-market summaries.

The overview can appear in report details, history responses, analysis
responses, completed task results, and Web report views when available. The Web
report uses the `AnalysisContextSummary` component and presents the overview in
a collapsible panel. Older records or analyses without a saved snapshot may not
have an overview.

### Persistence and configuration

The full pack and `analysis_context_pack_summary` are not written into the
history snapshot. The separately rendered public overview may be stored at the
top level of `analysis_history.context_snapshot` alongside existing diagnostic
and analysis context data.

`SAVE_CONTEXT_SNAPSHOT` defaults to `true`. Setting it to `false`, or using the
CLI option `--no-context-snapshot`, stops saving the history context snapshot.
It does **not** disable pack construction or prompt-summary generation for the
current analysis. With snapshot persistence disabled, historical API responses
may therefore lack the persisted overview and other snapshot-derived context.

No database migration is required for the pack overview. Older snapshots without
the overview or newer data-quality fields remain readable; absent values are
returned as empty or optional fields.

### Related contracts and compatibility

- `analysis_history.context_snapshot.enhanced_context.date` is still consumed
  when the backtest service parses an analysis date. Preserve this legacy
  location unless a migration updates its readers.
- Alert evaluation statuses such as `triggered`, `skipped`, `degraded`, and
  `failed` describe rule evaluation/recording, not input quality. See the
  [alert guide](#alert-center).
- Notification statuses such as `sent`, `no_channel`, and delivery failures
  describe notification outcomes, not input quality. See the
  [notification guide](#email-notifications).
- The separate daily market context feature can add a low-sensitivity summary
  and apply decision guardrails. It is not a pack block and can be disabled
  independently with `DAILY_MARKET_CONTEXT_ENABLED`.

### Privacy and safe serialization

The complete pack can contain raw analysis values, including quote, technical,
chip, fundamental, and news inputs. Do not expose the full pack or its
`items.value` fields through APIs, Web views, notifications, or logs. Use the
public overview renderer for client-facing summaries.

`AnalysisContextPack.to_safe_dict()` is an internal helper that redacts
sensitive mapping keys recursively. It is not a general secret scanner: it does
not inspect arbitrary string contents or scrub URLs by pattern. Never use it as
a substitute for the public overview projection or for safe handling of
credentials.

### Source map

| Area | Current source |
| --- | --- |
| Pack schema and status enum | [`ai_stock/schemas/analysis_context_pack.py`](../../ai_stock/schemas/analysis_context_pack.py) |
| Artifact assembly and quality scoring | [`ai_stock/services/analysis_context_builder.py`](../../ai_stock/services/analysis_context_builder.py) |
| Prompt-summary formatting | [`ai_stock/analysis_context_pack_prompt.py`](../../ai_stock/analysis_context_pack_prompt.py) |
| Public overview and snapshot sanitization | [`ai_stock/analysis_context_pack_overview.py`](../../ai_stock/analysis_context_pack_overview.py) |
| Pipeline integration | [`ai_stock/core/pipeline.py`](../../ai_stock/core/pipeline.py) |
| History and analysis API projection | [`api/v1/endpoints/history.py`](../../api/v1/endpoints/history.py), [`api/v1/endpoints/analysis.py`](../../api/v1/endpoints/analysis.py), [`api/v1/schemas/history.py`](../../api/v1/schemas/history.py) |
| Web report overview | [`apps/dsa-web/src/components/report/AnalysisContextSummary.tsx`](src/components/report/AnalysisContextSummary.tsx) |
| Backtest date compatibility | [`ai_stock/repositories/backtest_repo.py`](../../ai_stock/repositories/backtest_repo.py) |

The focused contract tests are under `tests/unit/analyzer/`, including tests
for the schema, builder, prompt renderer, and public overview.

## Email notifications

SMTP email is the only supported notification transport for analysis reports and
event-driven alerts. Other channel senders, settings, and notification test options
have been removed. Local report saving remains available without email credentials.

### Configuration

Set these values in `.env`, the process environment, or Web Settings → Notifications:

```dotenv
EMAIL_SENDER=sender@example.com
EMAIL_PASSWORD=your_smtp_authorization_code
EMAIL_RECEIVERS=recipient@example.com
EMAIL_SENDER_NAME=DSA
```

Use an SMTP authorization/app password where required. Never commit real
credentials. The SMTP host is detected from the sender's domain. Supported
providers include QQ, 163, and Gmail. OAuth2-only Outlook/Exchange tenants are
not supported.

`EMAIL_SENDER` and `EMAIL_PASSWORD` must both be configured. `EMAIL_RECEIVERS` is a
comma-separated list; leaving it empty sends to the sender. `EMAIL_SENDER_NAME`
controls the displayed sender name.

### Testing and delivery diagnostics

The Web notification test sends a real email using the current settings draft.
It does not save the draft. Only `email` is accepted by
`POST /api/v1/system/config/notification/test-channel`; other channel names fail
request validation.

Run `python main.py --check-notify` for read-only configuration diagnostics.
SMTP delivery failures are reported without exposing credentials or invalidating
the analysis report. Report history retains delivery diagnostics.

### Recipient groups and report options

Numbered stock/email groups are supported in `.env` or the process environment:

```dotenv
STOCK_GROUP_1=600519,300750
EMAIL_GROUP_1=team@example.com
```

Groups select recipients, not the analysis universe: `STOCK_LIST` still controls
which stocks are analyzed. Unmatched stocks use the default recipients. Aggregate
reports are generated separately for each recipient group; a failed group does
not prevent later groups from receiving their reports.

Existing report controls remain supported: `SINGLE_STOCK_NOTIFY`, `REPORT_TYPE`,
`REPORT_LANGUAGE`, `REPORT_SUMMARY_ONLY`, `REPORT_SHOW_LLM_MODEL`, and
`MERGE_EMAIL_NOTIFICATION`. Template, integrity, and history-comparison controls
are unchanged.

For inline-image emails, set `MARKDOWN_TO_IMAGE_CHANNELS=email` and install the
conversion tool required by `MD2IMG_ENGINE`. Conversion failures fall back to the
regular email report. `MARKDOWN_TO_IMAGE_MAX_CHARS` limits conversion size.

### Routing and noise controls

`NOTIFICATION_REPORT_CHANNELS`, `NOTIFICATION_ALERT_CHANNELS`, and
`NOTIFICATION_SYSTEM_ERROR_CHANNELS` accept only `email` or an empty value.
Empty means use the configured email transport. The system-error route remains
reserved for future producers.

Deduplication, cooldown, quiet hours/timezone, and minimum severity remain
available through `NOTIFICATION_DEDUP_TTL_SECONDS`,
`NOTIFICATION_COOLDOWN_SECONDS`, `NOTIFICATION_QUIET_HOURS`,
`NOTIFICATION_TIMEZONE`, and `NOTIFICATION_MIN_SEVERITY`.
`NOTIFICATION_DAILY_DIGEST_ENABLED` is reserved and does not send a daily digest.

### Migration and deployment

- Remove old bot, webhook, and push-provider notification variables from local,
  Docker, Desktop, and GitHub Actions configurations. Existing `.env` files are
  not automatically rewritten; retired variables are ignored at startup with a
  warning and excluded from both settings values and the schema.
- Update/import requests containing retired channel settings are rejected with
  `unsupported_notification_setting`. Clean old backups before importing them.
  Raw `.env` export remains a backup of the original file, including obsolete
  assignments that have not yet been removed.
- Replace old route lists and image-channel lists with `email` or clear them.
  An old route containing only removed channels does not enable email implicitly.
- The [disabled daily-analysis workflow](../../.github/workflows/disabled/00-daily-analysis.yml)
  now maps only email transport settings plus routing/noise controls. It remains
  disabled; this change does not enable scheduling or add permissions.
- Restart/rebuild the backend and Web app after deployment to replace previously
  served settings/UI assets. Desktop uses the same configuration API.

To roll back this intentional removal, restore the preceding application version
and its frontend assets. Retain a private configuration backup if needed; do not
restore obsolete secrets into source control.

### GitHub Actions environment mapping

This table describes the disabled daily-analysis workflow, not an active schedule.

<!-- notification-actions-env-table:start -->

| Key | Tier | Channel / feature | Actions source | Default |
| --- | --- | --- | --- | --- |
| `EMAIL_SENDER` | minimal | email | Variable or Secret | - |
| `EMAIL_PASSWORD` | minimal | email | Secret | - |
| `EMAIL_RECEIVERS` | advanced | email | Variable or Secret | - |
| `EMAIL_SENDER_NAME` | advanced | email | Variable or Secret | `daily_stock_analysis股票分析助手` |
| `NOTIFICATION_REPORT_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_ALERT_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | advanced | noise | Variable or Secret | `0` |
| `NOTIFICATION_COOLDOWN_SECONDS` | advanced | noise | Variable or Secret | `0` |
| `NOTIFICATION_QUIET_HOURS` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_TIMEZONE` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_MIN_SEVERITY` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | advanced | noise | Variable or Secret | `false` |

<!-- notification-actions-env-table:end -->
