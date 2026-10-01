# DSA Web Cypress Tests

Frontend UI test automation package for the [`apps/dsa-web`](../dsa-web) application, using TypeScript. Cypress is the test runner, with Page Object Model classes and Allure reporting.

## Status

This package was bootstrapped from an earlier Tangerine Bank automation project. The specs under `cypress/tests/` and page objects under `cypress/support/pages/` still target `https://www.tangerine.ca/en/personal` and are **placeholders, not `dsa-web` coverage yet**. Real `dsa-web` specs will be added next; until then, use these files as structural references only (Page Object Model layout, Allure wiring, config shape).

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
|   |-- tests/             # *.cy.ts specs (currently Tangerine placeholders)
|   `-- support/
|       |-- commands.ts
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

## Configuration

### Base URL

`cypress.config.ts` reads `BASE_URL`, currently defaulting to the Tangerine placeholder (`https://www.tangerine.ca/en/personal`). Update the default and/or set `BASE_URL` to point at the local `dsa-web` dev server once real specs are added.

PowerShell:

```powershell
$env:BASE_URL="http://localhost:5173"
npm test
```

bash:

```bash
BASE_URL="http://localhost:5173" npm test
```

### Test Credentials

Sample credentials are defined in `cypress/support/config.ts`. Do not commit real secrets; use environment variables for anything resembling production credentials.

## Running Cypress Tests

| Script | Purpose |
|---|---|
| `npm test` / `npm run cypress:run` | Run all Cypress specs headlessly |
| `npm run cypress:open` | Open the Cypress UI |
| `npm run allure:generate` | Build the Allure report from `../../temps/cypress_dsa_web/allure-results` |
| `npm run allure:open` | Open the generated Allure report |

```bash
# Run a single spec
npx cypress run --spec "cypress/tests/login.cy.ts"
```

## Allure Reporting

```bash
npm run allure:generate
npm run allure:open
```

Results: `temps/cypress_dsa_web/allure-results`; report: `temps/cypress_dsa_web/allure-report` (both generated under the repo-root `temps/` folder, gitignored).

## Troubleshooting

- `allure: command not found`: run `npm install` and confirm Java is installed (`java -version`).
- Cypress fails on first page load: confirm `BASE_URL` points at a reachable target (Tangerine placeholder requires internet access; a local `dsa-web` target requires the dev server to be running).

## Next Steps

- Replace the Tangerine placeholder specs and page objects with coverage for `dsa-web` flows.
- Point `cypress.config.ts` `baseUrl` at the `dsa-web` dev/preview server.
- Add a CI workflow for this package once real specs exist.
