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
- Playwright for backend-authenticated smoke tests (`e2e/`)
- A separate Cypress package, [`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md), owns the broader UI end-to-end suite

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

### Backend-Authenticated Smoke Tests (Playwright)

```bash
npm run test:smoke       # playwright test
```

- Specs live in `e2e/` (`smoke.spec.ts`, `report-markdown.spec.ts`).
- Skipped automatically unless `DSA_WEB_SMOKE_PASSWORD` is set, since they log in against a real backend.
- `playwright.config.ts` auto-starts the backend (`main.py --webui-only`) and the Vite dev server (port 4173) when `DSA_WEB_SMOKE_PASSWORD` is present; override the backend start command with `DSA_WEB_SMOKE_BACKEND_CMD` if needed.
- Use these for flows that require a logged-in session end-to-end (login, home dashboard, report rendering).

### Cypress UI Tests

Broader click-through UI coverage (page objects, Allure reporting) lives in the sibling package [`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md), not in this folder. Run the backend and/or `npm run dev` here first, then follow that package's README to run or add specs.

### Adding New Tests

- Prefer Vitest + Testing Library for component/unit behavior that doesn't need a real backend.
- Prefer the Cypress package for new user-facing flows and page objects.
- Reserve Playwright `e2e/` specs for scenarios that specifically need an authenticated session against the real backend.
- Keep assertions on stable text/roles/ids rather than styling classes, and avoid hardcoding secrets — use environment variables (`DSA_WEB_SMOKE_PASSWORD`, etc.).
