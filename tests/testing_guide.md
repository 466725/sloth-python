# Sloth Python Testing Guide

This guide explains how to run the Sloth Python project’s automated tests on
Windows from PowerShell. Run commands from the repository root unless a step
explicitly changes directories. Start with the smallest suite that covers your
change; browser and integration suites may need additional services or
configuration.

## Test suites

| Suite | Location | What it covers |
| --- | --- | --- |
| pytest | `pytest_tests/`, `tests/`, and other Python test modules | Python unit, API, integration, UI, AI, and data-driven tests |
| Robot Framework | `robot_tests/` and `tests/robot_tests/` | Keyword-driven API, UI, and behavior tests |
| Vitest | `apps/dsa-web/src/` and `apps/dsa-web/tests/` | DSA Web unit and component tests |
| Playwright | `apps/dsa-web-playwright-tests/e2e/` | DSA Web browser end-to-end tests; starts the backend and Vite server |
| Cypress | `apps/dsa-web-cypress-tests/e2e/` | DSA Web browser end-to-end tests against a running app |
| Performance assets | `tests/performance/` | JMeter, Postman, and LoadRunner scenarios; these require their respective tools and environment setup |

## One-time setup

### Python tests

Use Python 3.11 and install the repository requirements into a virtual
environment. From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Install Playwright's Python browser when running Python UI tests:

```powershell
python -m playwright install chromium
```

### DSA Web tests

Use Node.js 22 or 24 and npm. Install each package’s locked dependencies once
from the repository root:

```powershell
Push-Location apps\dsa-web
npm ci
Pop-Location

Push-Location apps\dsa-web-playwright-tests
npm ci
npx playwright install chromium
Pop-Location

Push-Location apps\dsa-web-cypress-tests
npm ci
Pop-Location
```

## pytest

Pytest settings and markers are configured in the root `pyproject.toml`. The
configuration writes Allure results and logs under `temps/test-results-pytest/`.

```powershell
# Run all discovered Python tests
python -m pytest

# Run the unit and API smoke selection used by CI
python -m pytest -m "unit or api" --tb=short

# Run the broader CI regression selection (excludes AI-marked tests)
python -m pytest -m "not ai" --tb=short --maxfail=5

# Run one test file or one test case
python -m pytest tests\unit\test_calculator.py -q
python -m pytest tests\pytest_tests\test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q

# Run UI-marked tests or the Tangerine browser suite
python -m pytest -m ui
python -m pytest tests\pytest_tests\ui_suites\tangerine -q
```

AI and network tests may require provider credentials, network access, or
external services. Run them separately when their prerequisites are available.

## Robot Framework

Robot suites are under `robot_tests/` and `tests/robot_tests/`. Reports are
written to the directory passed to `--outputdir`.

```powershell
# Run the API and keyword-driven smoke suites used by CI
python -m robot --outputdir temps\test-results-robot `
  tests\robot_tests\api_suites `
  tests\robot_tests\test_basics.robot `
  tests\robot_tests\test_data_driven.robot `
  tests\robot_tests\test_data_driven_with_csv.robot `
  tests\robot_tests\test_keyword_driven.robot

# Run all Robot suites
python -m robot --outputdir temps\test-results-robot tests\robot_tests

# Check suite syntax and keyword wiring without running the tests
python -m robot --dryrun --outputdir temps\test-results-robot tests\robot_tests

# Select a test by its Robot test-case name
python -m robot --test "Test Name" --outputdir temps\test-results-robot tests\robot_tests
```

Robot writes `output.xml`, `log.html`, and `report.html` to the output
directory. Some API suites need service credentials or network access; check
the selected suite before running it.

## DSA Web unit and component tests (Vitest)

Vitest runs from the `apps/dsa-web` package. These tests use the configured
jsdom environment and normally do not need a running backend.

```powershell
Push-Location apps\dsa-web

# Run the full Vitest suite
npm run test

# Run a single test file or matching test name
npm run test -- src/pages/__tests__/HomePage.test.tsx
npm run test -- src/pages/__tests__/HomePage.test.tsx -t "loads markdown"

Pop-Location
```

## DSA Web browser tests

### Playwright

The Playwright configuration starts the backend and Vite dev server at
`http://127.0.0.1:8000` and `http://127.0.0.1:4173`. Activate the Python
virtual environment first so the auto-started backend uses the project’s
installed dependencies.

```powershell
Push-Location apps\dsa-web-playwright-tests

# Run the full Playwright suite
npm test

# Run one spec or open the interactive runner
npx playwright test e2e\smoke.spec.ts
npm run test:ui

Pop-Location
```

Results, screenshots, and videos are written under `temps/` at the repository
root. To override the backend startup command for the current PowerShell
session, set `DSA_WEB_SMOKE_BACKEND_CMD` before running Playwright:

```powershell
$env:DSA_WEB_SMOKE_BACKEND_CMD = 'python main.py --serve-only'
```

### Cypress

Cypress uses `BASE_URL`, which defaults to `http://localhost:8000`. Start the
DSA Web/API service before running the suite, for example in a separate
PowerShell window from the repository root:

```powershell
python main.py --serve-only
```

Then, in another PowerShell window:

```powershell
Push-Location apps\dsa-web-cypress-tests

# Run all Cypress specs
npm test

# Run one spec or open the interactive runner
npm run cypress:run -- --spec "e2e/home.cy.ts"
npm run cypress:open

Pop-Location
```

To test against another running URL, set `BASE_URL` in the Cypress window
before running the suite:

```powershell
$env:BASE_URL = 'http://localhost:5173'
npm test
```

Cypress output is written under `temps/dsa-web-ts-cypress/` at the repository
root. See the [Cypress package guide](../apps/dsa-web-cypress-tests/Readme.md)
for package-specific details.

## Test results and CI

Python test output and Robot reports are stored under `temps/`. DSA Web browser
test output is also stored under `temps/`; these generated results should not
be committed.

The GitHub Actions smoke job runs pytest with `unit or api` markers and a
selected set of Robot suites. The scheduled/manual regression job runs pytest
with `not ai` and all suites under `tests/robot_tests/`. Use those selections
when reproducing CI locally. The browser suites described above are run
separately from those CI jobs.

Performance test assets live in `tests/performance/`. They are not part of the
pytest, Robot, Vitest, Playwright, or Cypress commands above; follow the setup
and environment requirements of JMeter, Postman, or LoadRunner before running
them. See the [load runner guide](performance/load_runner/load_runner_best_practices.md)
for scenario-design practices.

For framework-specific details, see the [Playwright package guide](../apps/dsa-web-playwright-tests/Readme.md)
and [Cypress package guide](../apps/dsa-web-cypress-tests/Readme.md).
