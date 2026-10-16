# DSA Web Cypress Tests

Frontend UI test automation package for the [`apps/dsa-web`](../dsa-web) application, using TypeScript. Cypress is the test runner, with Page Object Model classes and Allure reporting.

## Tech Stack

- Node.js 22, 24, or 26+
- npm 9+
- TypeScript 7
- Cypress 16
- Allure via `allure-cypress`, `allure-js-commons`, and `allure-commandline`

## Project Structure

```text
dsa-web-cypress-tests/
|-- e2e/
|   |-- *.cy.ts             # test specs
|   `-- support/
|       |-- config.ts
|       |-- e2e.ts
|       `-- pages/          # Page Object Model classes
|-- cypress.config.ts
|-- tsconfig.json
|-- package.json
`-- Readme.md
```

Screenshots, videos, downloads, and Allure results are not written inside this package. They go to the repo-root `temps/` folder (already gitignored there), alongside the other test frameworks' output:

```text
sloth-python/temps/cypress_dsa_web/
|-- screenshots/
|-- videos/
|-- downloads/
|-- allure-results/
`-- allure-report/
```

## Setup

### Prerequisites

- Node.js 24 LTS recommended (supported: Node.js 22, 24, or 26+)
- npm 9+
- Java Runtime (required to generate/open Allure HTML reports)

```bash
node -v
npm -v
java -version
```

### Install

```bash
cd apps/dsa-web-cypress-tests
npm install
```

## Dependency Updates

The repository's [Dependabot configuration](../../.github/dependabot.yml) checks this
package's npm dependencies, including development dependencies such as Cypress,
TypeScript, and Allure tooling, every Monday at 03:00 UTC.

Dependabot opens up to five version-update pull requests at a time, requests review
from `466725`, and applies the `type/dependencies` and `priority/low` labels. Major
updates are not excluded, so review breaking changes before merging. Updates are
not automatically merged.

After an update, install dependencies from the repository root:

```powershell
cd apps\dsa-web-cypress-tests
npm install
```

Then run `npm test` (it starts an isolated frontend automatically). To test an
already-running app, set `BASE_URL` and run `npm run cypress:run` (see below).
This package does not yet
have a dedicated CI workflow. To stop these scheduled npm updates, remove this
package's npm entry from the Dependabot configuration; leave the pip entry intact.

## Configuration

### Base URL

`npm test` starts Vite on `http://127.0.0.1:4174`, waits until it responds,
runs Cypress, and stops Vite even if tests fail. Install the frontend dependencies
under `apps/dsa-web` first. The small `start-server-and-test` development dependency
handles readiness and process cleanup across Windows, macOS, and Linux.

No backend, Python environment, or Docker service is required for these two UI
specs: the support file intercepts their auth, history, task, watchlist, skills,
and setup-status API requests. Application exceptions still fail tests.

`cypress.config.ts` reads `BASE_URL`, defaulting to `http://127.0.0.1:4174`.
For an already-running app, use `cypress:run` or `cypress:open` rather than
`npm test` to skip automatic startup:

PowerShell:

```powershell
$env:BASE_URL="http://localhost:8000"
npm run cypress:run
Remove-Item Env:BASE_URL
```

bash:

```bash
BASE_URL="http://localhost:8000" npm run cypress:run
```

To instead test against the Vite dev server (`npm run dev` under `apps/dsa-web`, no backend required for static/UI-only checks), set `BASE_URL=http://localhost:5173`.

### Test Config Helpers

`e2e` exposes `getBaseUrl()` for specs/page objects that need the resolved base URL at runtime.

## Running Cypress Tests

| Script | Purpose |
|---|---|
| `npm test` | Start isolated Vite, run all specs headlessly, stop Vite |
| `npm run cypress:run` | Run all specs against an already-running app |
| `npm run cypress:open` | Open the Cypress UI |
| `npm run allure:generate` | Build the Allure report from `../../temps/cypress_dsa_web/allure-results` |
| `npm run allure:open` | Open the generated Allure report |

```bash
# Run a single spec
npx cypress run --spec "e2e/home.cy.ts"
```

## Current Test Coverage

- `e2e/home.cy.ts`: home page loads and the "Analyze" button is visible.
- `e2e/dsa_web_smoke.cy.ts`: backend-independent sanity check that the app shell renders and the page title is correct; useful for verifying the Cypress setup itself without requiring the backend or auth to be configured.

## Allure Reporting

```bash
npm run allure:generate
npm run allure:open
```

Results: `temps/cypress_dsa_web/allure-results`; report: `temps/cypress_dsa_web/allure-report` (both generated under the repo-root `temps/` folder, gitignored).

## Troubleshooting

- `allure: command not found`: run `npm install` and confirm Java is installed (`java -version`).
- Cypress fails on first page load: for `npm test`, ensure port 4174 is free and frontend dependencies are installed (`npm install` under `apps/dsa-web`). For `cypress:run`, confirm `BASE_URL` points at a responsive app. A Docker/WSL service on port 8000 may accept connections without serving HTTP; use `curl.exe --max-time 5 http://localhost:8000/` to check before targeting it.
- `Cannot read properties of undefined (reading 'state')` from the old
  `@shelex/cypress-allure-plugin`: run `npm install` to use the current
  `allure-cypress` integration. Reporting is initialized in `setupNodeEvents`
  and the support file; test metadata uses `allure-js-commons`, not `cy.allure()`.
- Cypress 16 warns that Electron is deprecated. Use an installed Chrome browser
  with `npm run cypress:run -- --browser chrome`.

## Next Steps

- Add specs/page objects for additional `dsa-web` flows (Ask Stock, Backtest, Alerts, Settings, login/auth).
- Add a CI workflow for this package.
