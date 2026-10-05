# DSA Web Cypress Tests

Frontend UI test automation package for the [`apps/dsa-web`](../dsa-web) application, using TypeScript. Cypress is the test runner, with Page Object Model classes and Allure reporting.

## Tech Stack

- Node.js 18+
- npm 9+
- TypeScript 5
- Cypress 15
- Allure via `@shelex/cypress-allure-plugin` and `allure-commandline`

## Project Structure

```text
dsa-web-cypress-tests/
|-- cypress/
|   |-- tests/             # *.cy.ts specs
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

- Node.js 20 LTS (minimum supported: Node.js 18)
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

Then run `npm test` against a running app with the appropriate `BASE_URL` (see
below). This package does not yet
have a dedicated CI workflow. To stop these scheduled npm updates, remove this
package's npm entry from the Dependabot configuration; leave the pip entry intact.

## Configuration

### Base URL

`cypress.config.ts` reads `BASE_URL`, defaulting to the local DSA backend (`http://localhost:8000`). The backend serves the built `dsa-web` app; start it before running tests (see the root [readme.md](../../readme.md) run modes, e.g. `python main.py --serve-only`).

PowerShell:

```powershell
$env:BASE_URL="http://localhost:8000"
npm test
```

bash:

```bash
BASE_URL="http://localhost:8000" npm test
```

To instead test against the Vite dev server (`npm run dev` under `apps/dsa-web`, no backend required for static/UI-only checks), set `BASE_URL=http://localhost:5173`.

### Test Config Helpers

`cypress/support/config.ts` exposes `getBaseUrl()` for specs/page objects that need the resolved base URL at runtime.

## Running Cypress Tests

| Script | Purpose |
|---|---|
| `npm test` / `npm run cypress:run` | Run all Cypress specs headlessly |
| `npm run cypress:open` | Open the Cypress UI |
| `npm run allure:generate` | Build the Allure report from `../../temps/cypress_dsa_web/allure-results` |
| `npm run allure:open` | Open the generated Allure report |

```bash
# Run a single spec
npx cypress run --spec "cypress/tests/home.cy.ts"
```

## Current Test Coverage

- `cypress/tests/home.cy.ts` + `cypress/support/pages/DsaHomePage.ts`: home page loads and the "Analyze" button is visible.
- `cypress/tests/dsa_web_smoke.cy.ts`: backend-independent sanity check that the app shell renders and the page title is correct; useful for verifying the Cypress setup itself without requiring the backend or auth to be configured.

## Allure Reporting

```bash
npm run allure:generate
npm run allure:open
```

Results: `temps/cypress_dsa_web/allure-results`; report: `temps/cypress_dsa_web/allure-report` (both generated under the repo-root `temps/` folder, gitignored).

## Troubleshooting

- `allure: command not found`: run `npm install` and confirm Java is installed (`java -version`).
- Cypress fails on first page load: confirm `BASE_URL` points at a reachable target and the DSA backend (or Vite dev server) is running.

## Next Steps

- Add specs/page objects for additional `dsa-web` flows (Ask Stock, Backtest, Alerts, Settings, login/auth).
- Add a CI workflow for this package.
