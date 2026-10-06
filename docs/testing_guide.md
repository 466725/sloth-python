# Running Tests

This guide collects the commands for the repository's Python, Robot Framework,
and Web tests. Run commands from the repository root unless a step changes
directories. Start with the smallest suite that covers your change.

## Python environment

The Python commands below assume the project environment is active. On Windows,
activate the repository's Python 3.11 environment in PowerShell with:

```powershell
.\.venv311\Scripts\Activate.ps1
```

If the environment has not been set up, install the project dependencies using
the repository's normal Python setup instructions before running tests.

## Run all test frameworks

With the Python environment active, npm dependencies installed in both Web
packages, and the DSA application available at `http://localhost:8000` for
Cypress, run this block from the repository root in PowerShell. It runs pytest,
Robot Framework, Cypress, and Vitest in order, continues after failures, and
returns a failing exit code if any framework fails:

```powershell
$failedSuites = @()

python -m pytest
if ($LASTEXITCODE -ne 0) { $failedSuites += "pytest" }

python -m robot --outputdir temps/robot_all tests/robot_tests/
if ($LASTEXITCODE -ne 0) { $failedSuites += "Robot Framework" }

Push-Location apps\dsa-web-cypress-tests
try {
    npm test
    if ($LASTEXITCODE -ne 0) { $failedSuites += "Cypress" }
}
finally {
    Pop-Location
}

Push-Location apps\dsa-web
try {
    npm run test
    if ($LASTEXITCODE -ne 0) { $failedSuites += "Vitest" }
}
finally {
    Pop-Location
}

if ($failedSuites.Count -gt 0) {
    Write-Error "Failed test suites: $($failedSuites -join ', ')"
    exit 1
}

Write-Output "All test frameworks passed."
```

## Pytest

Pytest suites are under `tests/pytest_tests/` and `tests/`. Pytest and its
markers are configured in the root `pyproject.toml`.

```powershell
# Run all pytest tests
python -m pytest

# Fast unit and API checks
python -m pytest -m "unit or api"

# Run one file or one test
python -m pytest tests/pytest_tests/test_csv_reader.py -q
python -m pytest tests/pytest_tests/test_csv_reader.py::test_read_csv_to_list_converts_numeric_cells_to_int -q

# Run UI tests
python -m pytest -m ui
python -m pytest tests/pytest_tests/ui_suites/tangerine -q
```

The root pytest configuration writes Allure results to `temps/allure-results/`.
UI tests may need browser dependencies or an accessible test application; see
the suite fixtures and setup when running a specific UI suite.

## Robot Framework

Robot suites are under `tests/robot_tests/`. These commands run from the
repository root and write reports to the selected directory under `temps/`.

```powershell
# Run the UI suites
python -m robot --outputdir temps/robot_all tests/robot_tests/ui_suites/

# Check syntax and keyword wiring without executing the suite
python -m robot --dryrun --outputdir temps/robot_dryrun tests/robot_tests/ui_suites/

# Run one test by name while retaining the parent suite setup
python -m robot --test "Test Name" --outputdir temps/robot_single tests/robot_tests/
```

Robot creates `output.xml`, `log.html`, and `report.html` in the output
directory. The UI suites may require a browser and a reachable application.

## TypeScript unit tests (Vitest)

The DSA Web unit/component tests use Vitest and are located under
`apps/dsa-web/src/`. Install the locked npm dependencies once, then run tests
from that package directory:

```powershell
Set-Location apps\dsa-web
npm ci

# Run the full Vitest suite
npm run test

# Run one test file or a matching test name
npm run test -- src/pages/__tests__/HomePage.test.tsx
npm run test -- src/pages/__tests__/HomePage.test.tsx -t "loads markdown"
```

Vitest uses the jsdom environment configured in `vitest.config.ts`; these tests
do not normally require a separately running backend.

## Cypress end-to-end tests

Cypress specs are under `apps/dsa-web-cypress-tests/cypress/tests/`. Install
dependencies and run commands from the Cypress package directory:

```powershell
Set-Location apps\dsa-web-cypress-tests
npm ci

# Run all Cypress specs headlessly
npm test

# Run one spec
npm run cypress:run -- --spec "cypress/tests/home.cy.ts"

# Open the Cypress interactive runner
npm run cypress:open
```

By default, Cypress visits `http://localhost:8000`; start the DSA application
before running specs that use the backend. To use another URL, set `BASE_URL`
in the same PowerShell session:

```powershell
$env:BASE_URL = "http://localhost:5173"
npm test
```

The Vite development server can be used for the backend-independent app-shell
smoke spec. In another terminal, start it with:

```powershell
Set-Location apps\dsa-web
npm run dev
```

Then set `BASE_URL` to `http://localhost:5173` in the Cypress terminal.
Cypress screenshots, downloads, and Allure results are written under
`temps/cypress_dsa_web/`.

## Choosing what to run

- Backend or Python behavior: run the related pytest file, then the relevant
  marker group if needed.
- Robot keyword or suite behavior: run the affected suite directory; use
  `--dryrun` for a quick syntax and keyword-wiring check.
- DSA Web component behavior: run the affected Vitest file.
- Full browser flow through the DSA Web application: run the relevant Cypress
  spec against the intended app URL.

The root [README](../readme.md#-running-tests) also has the existing pytest and
Robot examples. Cypress-specific configuration and coverage details are in
[the Cypress package README](../apps/dsa-web-cypress-tests/Readme.md).
