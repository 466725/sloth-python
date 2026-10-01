# Tangerine Bank UI Test Automation Framework

[![CI](https://github.com/466725/sloth-javascript/actions/workflows/ci.yml/badge.svg)](https://github.com/466725/sloth-javascript/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

UI test automation project for https://www.tangerine.ca/ using TypeScript. The primary runner is Cypress with Page Object Model classes and Allure reporting. The repository also includes Playwright specs and a separate SQLite query utility package.

## What Is In This Repository

- Cypress end-to-end tests for homepage, login, and registration flows.
- POM classes in `cypress/support/pages` used by Cypress tests.
- Allure integration for local reports and CI artifacts.
- Playwright specs in `playwright/tests`.
- A standalone `queries` package for SQLite-related utilities.

## Tech Stack

- Node.js 18+
- npm 9+
- TypeScript 5
- Cypress 15
- Playwright Test 1.61
- Allure via `@shelex/cypress-allure-plugin` and `allure-commandline`

## Project Structure

```text
sloth-javascript/
|-- cypress/
|   |-- tests/
|   |-- support/
|   |   |-- config.ts
|   |   `-- pages/
|   |-- downloads/
|   |-- screenshots/
|   |-- allure-results/   # generated test result files
|   `-- allure-report/    # generated report output
|-- playwright/
|   |-- concepts/
|   `-- tests/
|-- queries/              # separate package with its own package.json
|-- cypress.config.ts
|-- playwright.config.ts
|-- tsconfig.json
|-- package.json
`-- Readme.md
```

## Setup For A New Machine

### Prerequisites

Install these tools before running tests:

- Node.js 20 LTS (or newer; minimum supported is Node.js 18)
- npm 9+
- Git
- Java Runtime (required to generate/open Allure HTML reports)

Quick checks:

```bash
node -v
npm -v
java -version
```

### 1. Clone And Install

```bash
git clone https://github.com/466725/sloth-javascript.git
cd dsa-web-cypress-tests
npm install
```

### 2. Install Playwright Browsers (One Time)

```bash
npx playwright install
```

If your machine is Linux and Playwright reports missing OS libraries:

```bash
npx playwright install --with-deps
```

### 3. Optional: Install Queries Subproject Dependencies

Only needed if you plan to run anything in `queries/`.

```bash
npm --prefix queries install
```

### 4. Verify Setup With A Fast Smoke Run

```bash
npx cypress run --spec "cypress/tests/login.cy.ts"
npx playwright test playwright/tests/login.spec.ts
```

If both commands pass, your machine is ready.

## Configuration

### Base URL

Tests use `BASE_URL` when provided; otherwise they default to:

`https://www.tangerine.ca/en/personal`

PowerShell:

```powershell
$env:BASE_URL="https://www.tangerine.ca/en/personal"
npm test
```

bash:

```bash
BASE_URL="https://www.tangerine.ca/en/personal" npm test
```

### Test Credentials

Sample credentials are defined in `cypress/support/config.ts` as:

- `testCredentials.user`
- `testCredentials.invalidUser`

Do not use real secrets in source code for production-like environments.

### Optional Environment Variable

You can override the default base URL for both Cypress and Playwright with `BASE_URL`.

PowerShell:

```powershell
$env:BASE_URL="https://www.tangerine.ca/en/personal"
```

bash:

```bash
export BASE_URL="https://www.tangerine.ca/en/personal"
```

## Running Cypress Tests

### NPM Scripts (root package)

- `npm run cypress:open` - open Cypress app.
- `npm run cypress:run` - run all Cypress specs headlessly.
- `npm test` - alias for `npm run cypress:run`.
- `npm run allure:generate` - build Allure report from `cypress/allure-results`.
- `npm run allure:open` - open generated report.

### Common Cypress Commands

```bash
# Run all Cypress tests
npm test

# Open Cypress UI
npm run cypress:open

# Run a single spec
npx cypress run --spec "cypress/tests/login.cy.ts"
```

Generate and open Cypress Allure report:

```bash
npm run allure:generate
npm run allure:open
```

## Running And Debugging Playwright Specs

Playwright is installed in root dev dependencies with dedicated npm scripts.

### NPM Scripts (Playwright)

- `npm run playwright:test` - run all Playwright specs.
- `npm run playwright:debug` - run all Playwright specs in debug mode (Inspector).
- `npm run playwright:allure:generate` - build Allure report from `playwright/allure-results`.
- `npm run playwright:allure:open` - open generated Playwright Allure report.

If Playwright browsers are not installed yet:

```bash
npx playwright install
```

Run all Playwright specs in this project:

```bash
npx playwright test playwright/tests/*.spec.ts
```

Run one Playwright spec:

```bash
npx playwright test playwright/tests/login.spec.ts
```

Debug one TypeScript Playwright spec in Inspector (slow-motion step-through):

```powershell
$env:PWDEBUG="1"; npx playwright test playwright/tests/login.spec.ts
```

Debug all TypeScript Playwright specs:

```powershell
$env:PWDEBUG="1"; npx playwright test playwright/tests/*.spec.ts
```

Generate and open Playwright Allure report:

```bash
npm run playwright:allure:generate
npm run playwright:allure:open
```

## Current Test Coverage

### Cypress

- `cypress/tests/homepage.cy.ts`
  - homepage/logo visibility
  - app download links visibility
  - hover behavior for Save menu
  - analytics request capture check
- `cypress/tests/login.cy.ts`
  - login flow entry and login input interaction
- `cypress/tests/register.cy.ts`
  - visible Sign Up or Become a Client link check

### Playwright

Equivalent checks exist in:

- `playwright/tests/homepage.spec.ts`
- `playwright/tests/login.spec.ts`
- `playwright/tests/register.spec.ts`

## Allure Reporting

After running Cypress tests:

```bash
npm run allure:generate
npm run allure:open
```

Paths used by this project:

- Results: `cypress/allure-results`
- Report: `cypress/allure-report`

After running Playwright tests:

```bash
npm run playwright:allure:generate
npm run playwright:allure:open
```

Playwright paths used by this project:

- Results: `playwright/allure-results`
- Report: `playwright/allure-report`
- Screenshots/artifacts: `playwright/screenshots`

## Troubleshooting

- `allure: command not found`:
  - Run `npm install` at project root.
  - Confirm Java is installed (`java -version`).
- Playwright fails before tests start:
  - Run `npx playwright install`.
  - On Linux, run `npx playwright install --with-deps`.
- Cypress opens but test fails on first page load:
  - Confirm internet access to `https://www.tangerine.ca`.
  - Retry with explicit `BASE_URL` set for your environment.

## CI Pipeline

GitHub Actions workflow: `.github/workflows/ci.yml`

Current pipeline behavior:

- Triggers on push, pull request, schedule, and manual dispatch.
- Runs on Ubuntu with Node.js 20.
- Executes Cypress tests on Chrome.
- Generates Allure report.
- Uploads Allure results and report artifacts.
- Uploads Cypress screenshots when failures occur.

## Queries Subproject

The `queries` folder is a standalone package with its own dependencies and scripts.

Install dependencies for that package:

```bash
npm --prefix queries install
```

Run its SDK entry:

```bash
npm --prefix queries run sdk
```

Run its setup script:

```bash
npm --prefix queries run setup
```

## Contributing And Policies

- Contribution guide: `CONTRIBUTING.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- Security policy: `SECURITY.md`
- Changelog: `CHANGELOG.md`

## License

MIT. See `LICENSE`.
