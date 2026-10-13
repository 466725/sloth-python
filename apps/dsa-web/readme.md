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
