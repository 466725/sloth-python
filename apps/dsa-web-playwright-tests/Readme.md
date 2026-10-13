# DSA Web Playwright Tests

Playwright + TypeScript E2E test automation for the [`apps/dsa-web`](../dsa-web) application, with backend-authenticated smoke tests.

## Tech Stack

- Node.js 22, 24, or 26+
- npm 9+
- TypeScript 5.8
- Playwright 1.58
- Auto-starts backend and frontend servers when `DSA_WEB_SMOKE_PASSWORD` is set

## Project Structure

```text
dsa-web-playwright-tests/
|-- e2e/
|   |-- smoke.spec.ts           # Login, home page, chat flows
|   `-- report-markdown.spec.ts # Report copy and clipboard tests
|-- playwright.config.ts        # Playwright config with auto server startup
|-- tsconfig.json
|-- package.json
`-- Readme.md
```

Test results, screenshots, and videos are written to the repo-root `temps/` folder (already gitignored):

```text
sloth-python/temps/playwright_dsa_web/
|-- test-results/
`-- playwright-report/
```

## Setup

### Prerequisites

- Node.js 24 LTS recommended (supported: Node.js 22, 24, or 26+)
- npm 9+
- Python 3.11+ with project dependencies installed (for backend auto-start)

```bash
node -v
npm -v
```

### Install

```bash
cd apps/dsa-web-playwright-tests
npm install
npx playwright install chromium
```

## Running Tests

| Script | Purpose |
|---|---|
| `npm test` | Run all Playwright tests headlessly |
| `npm run test:ui` | Open Playwright UI mode for debugging |
| `npm run test:headed` | Run tests in a visible browser |
| `npm run test:report` | Open the HTML report |

### Authenticated Smoke Tests

Tests require the `DSA_WEB_SMOKE_PASSWORD` environment variable to run authenticated flows. When set, the config auto-starts both the backend and the Vite dev server:

**PowerShell:**

```powershell
$env:DSA_WEB_SMOKE_PASSWORD="your_password"
npm test
```

**bash:**

```bash
DSA_WEB_SMOKE_PASSWORD="your_password" npm test
```

Without the password, tests are skipped automatically.

### Custom Backend Command

Override the backend startup command with `DSA_WEB_SMOKE_BACKEND_CMD`:

```bash
DSA_WEB_SMOKE_PASSWORD="your_password" DSA_WEB_SMOKE_BACKEND_CMD="python main.py --serve-only" npm test
```

### Run a Single Spec

```bash
npx playwright test e2e/smoke.spec.ts
```

## Current Test Coverage

- `e2e/smoke.spec.ts`: Login page renders, home page shows analysis entry and history after login, chat page allows entering a question.
- `e2e/report-markdown.spec.ts`: Copy Markdown source code to clipboard, copy plain text to clipboard.

All tests run with Chinese locale (`zh-CN`) and use Chromium browser.

## Configuration

`playwright.config.ts` auto-starts two servers when `DSA_WEB_SMOKE_PASSWORD` is set:

1. **Backend**: `python main.py --webui-only --host 127.0.0.1 --port 8000` (from repo root)
2. **Frontend**: `npm run dev -- --host 127.0.0.1 --port 4173` (from `apps/dsa-web`)

The base URL for tests is `http://127.0.0.1:4173` (the Vite dev server).

Screenshots and videos are captured on failure only. Traces are recorded on the first retry.

## Comparing with Cypress

This package and [`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md) both test the same dsa-web application but use different frameworks:

| Feature | Playwright (this package) | Cypress |
|---|---|---|
| Test runner | `@playwright/test` | Cypress 16 |
| Auth | Backend login via `DSA_WEB_SMOKE_PASSWORD` | None |
| Server startup | Auto-starts backend + frontend | Manual `BASE_URL` |
| Locale | Chinese `zh-CN` | Default |
| Reporting | Built-in HTML report, screenshots/video on failure | Allure reporting |
| Page objects | Inline locators | Page Object Model classes |
| Coverage | Authenticated flows: login, home, chat, report copy | App shell renders, analyze button visible |

## Troubleshooting

- **Tests are skipped**: Set `DSA_WEB_SMOKE_PASSWORD` environment variable.
- **Backend fails to start**: Ensure Python dependencies are installed and the `.venv` exists, or set `DSA_WEB_SMOKE_BACKEND_CMD` manually.
- **Frontend fails to start**: Ensure `apps/dsa-web` dependencies are installed (`cd apps/dsa-web && npm install`).
- **Browser not found**: Run `npx playwright install chromium`.

## Next Steps

- Add more specs for additional dsa-web flows (settings, backtest, alerts, decision signals).
- Add a CI workflow for this package.
- Consider adding Allure reporting for parity with the Cypress package.
