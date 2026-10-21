# DSA Web Playwright Tests

Playwright + TypeScript E2E test automation for the [`apps/dsa-web`](../dsa-web) application.

## Tech Stack

- Node.js 22, 24, or 26+
- npm 9+
- TypeScript 7
- Playwright 1.58
- Auto-starts backend and frontend servers

## Project Structure

```text
dsa-web-playwright-tests/
|-- e2e/
|   |-- backend-command.spec.ts # Cross-platform backend startup regression tests
|   |-- smoke.spec.ts           # Home page, chat flows
|   `-- report-markdown.spec.ts # Report copy and clipboard tests
|-- playwright.config.ts        # Playwright config with auto server startup
|-- tsconfig.json
|-- package.json
`-- Readme.md
```

Test results, screenshots, and videos, along with the HTML report, are written under the repo-root `temps/` folder (already gitignored):

```text
sloth-python/temps/dsa-web-ts-playwright/
|-- results/
`-- html-report/
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
| `npm test` | Run all Playwright tests headlessly and generate an HTML report |
| `npm run test:ui` | Open Playwright UI mode for debugging |
| `npm run test:headed` | Run tests in a visible browser |
| `npm run typecheck` | Check TypeScript types without emitting files |
| `npm run test:report` | Open the latest HTML report from `temps/dsa-web-ts-playwright/html-report/` |

The HTML report is generated after each test run. Run `npm run test:report` from
this package directory to open it.

### Custom Backend Command

Override the backend startup command with `DSA_WEB_SMOKE_BACKEND_CMD`:

```bash
DSA_WEB_SMOKE_BACKEND_CMD="python main.py --webui-only --host 127.0.0.1 --port 18000" npm test
```

In PowerShell:

```powershell
$env:DSA_WEB_SMOKE_BACKEND_CMD = 'python main.py --webui-only --host 127.0.0.1 --port 18000'
npm test
Remove-Item Env:DSA_WEB_SMOKE_BACKEND_CMD
```

Custom commands must serve the backend on `127.0.0.1:18000`.

### Run a Single Spec

```bash
npx playwright test e2e/smoke.spec.ts
```

## Current Test Coverage

- `e2e/smoke.spec.ts`: Home page shows analysis entry and history, chat page allows entering a question.
- `e2e/report-markdown.spec.ts`: Copy exact Markdown/plain-text content to the clipboard and verify both copy buttons are disabled while the report loads. History and report API responses are intercepted with fixed test data, so these UI tests need no existing reports, live analysis, or LLM credentials.

All tests run with Chinese locale (`zh-CN`) and use Chromium browser.
Tests use one worker to avoid contention on the shared Vite dev server and
system clipboard, including when repeating the suite.

## Configuration

`playwright.config.ts` auto-starts two servers:

1. **Backend**: `python main.py --webui-only --host 127.0.0.1 --port 18000` (from repo root).
   Python is selected from the activated `VIRTUAL_ENV`, then the repository's `.venv`,
   then `.venv311`, then `python` on PATH. Executable paths are quoted on all platforms.
2. **Frontend**: `npm run dev -- --host 127.0.0.1 --port 4173 --strictPort` (from `apps/dsa-web`).
   Playwright sets `DSA_WEB_API_PROXY_TARGET=http://127.0.0.1:18000` for this server.
   Normal Vite development still proxies to port 8000.

The dedicated backend port avoids conflicts with Docker/WSL or a normal development
server on port 8000. By default, Playwright starts its own backend and fails if
port 18000 is already occupied. To intentionally reuse a healthy backend on that
port during local runs, set `DSA_WEB_REUSE_BACKEND=1`:

```powershell
$env:DSA_WEB_REUSE_BACKEND = '1'
npm test
Remove-Item Env:DSA_WEB_REUSE_BACKEND
```

CI always starts its own backend. The frontend is always started by Playwright so
it cannot reuse a Vite server that proxies to a different backend. Stop any
other server on port 4173 first.
Server startup output is shown in the terminal. The backend uses UTF-8,
unbuffered output so Chinese log messages work in Windows subprocess pipes.

The base URL for tests is `http://127.0.0.1:4173` (the Vite dev server).

Screenshots and videos are captured on failure only. Traces are recorded on the first retry.

## Comparing with Cypress

This package and [`apps/dsa-web-cypress-tests`](../dsa-web-cypress-tests/Readme.md) both test the same dsa-web application but use different frameworks:

| Feature | Playwright (this package) | Cypress |
|---|---|---|
| Test runner | `@playwright/test` | Cypress 16 |
| Server startup | Auto-starts backend + frontend | Manual `BASE_URL` |
| Locale | Chinese `zh-CN` | Default |
| Reporting | Built-in HTML report, screenshots/video on failure | Allure reporting |
| Page objects | Inline locators | Page Object Model classes |
| Coverage | Home, chat, report copy | App shell renders, analyze button visible |

## Troubleshooting

- **Backend fails to start**: Activate your Python environment (for example, `.venv311\Scripts\Activate.ps1` on Windows), ensure project dependencies are installed, or set `DSA_WEB_SMOKE_BACKEND_CMD` manually.
- **Stuck before tests are listed**: Check `http://127.0.0.1:18000/api/v1/health` with `curl.exe --max-time 5` on Windows. An occupied port that accepts connections but never responds can stall Playwright's initial health check before its startup timeout applies. Inspect the port owner and stop or repair that service; do not terminate unrelated Docker/WSL processes blindly. For startup diagnostics in PowerShell, set `$env:DEBUG = 'pw:webserver'` before `npm test` and remove it afterward with `Remove-Item Env:DEBUG`.
- **Frontend port already in use**: Stop the existing server on port 4173; Playwright deliberately does not reuse it.
- **Frontend fails to start**: Ensure `apps/dsa-web` dependencies are installed (`cd apps/dsa-web && npm install`).
- **Browser not found**: Run `npx playwright install chromium`.

## Next Steps

- Add more specs for additional dsa-web flows (settings, backtest, alerts, decision signals).
- Add a CI workflow for this package.
- Consider adding Allure reporting for parity with the Cypress package.
