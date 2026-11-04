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

## Just workflows

The root [justfile](../justfile) provides the DSA workflow on Windows
(PowerShell), macOS, and Linux (sh). Install `just` 1.51+,
Python 3.14, Node.js 24.15+ (24 LTS), npm 10+, and uv:

```powershell
python -m pip install uv
just doctor
just verify
```

`just verify` runs setup, the production frontend build, and the complete DSA
test selection in that order. Python setup uses `uv sync --locked --python 3.14`;
npm packages use `npm ci`. It updates the repository `.venv` and each package's
`node_modules`, but not dependency manifests, lockfiles, or your `.env`.
Playwright's `--with-deps` browser install may require sudo on Linux.
Cypress's native system libraries must also be available; see its
[Linux prerequisites](https://docs.cypress.io/app/get-started/install-cypress#Linux-Prerequisites).
Docker, MySQL, Java/Allure CLI, live LLM credentials, and a manually started
backend are not required for this test selection.

| Command | Purpose |
| --- | --- |
| `just` | List recipes |
| `just setup` | Install Python, frontend, browser-test dependencies, Chromium, and Cypress |
| `just verify` | Setup + build + all test recipes below; stops at the first failure |
| `just dsa` | Setup application dependencies, build the frontend, and serve DSA at `http://127.0.0.1:8000` |
| `just dsa 127.0.0.1 8080` | Serve DSA on a different port |
| `just dev-api` / `just dev-web` | Run backend reload and Vite development servers in separate terminals after setup |
| `just analyze --help` | Show the existing DSA CLI options; arguments are forwarded to `main.py` |
| `just build` | Build/type-check the frontend into the backend's configured static-assets directory |
| `just test` | All configured DSA test suites, without reinstalling npm packages |
| `just test-unit` | All `tests/unit` tests, including unmarked unittest cases |
| `just test-api` | `tests/pytest_tests/api_suites`: isolated in-process API and contract tests |
| `just test-web` | All DSA frontend Vitest unit/component tests |
| `just test-ui` | Both DSA Web Playwright and Cypress browser suites |
| `just test-playwright` / `just test-cypress` | Run either browser framework separately |
| `just lint` | Frontend ESLint and both browser packages' TypeScript checks |
| `just report-ui` | Open the most recent Playwright HTML report |

Individual test recipes accept runner arguments, for example:

```powershell
just test-unit -k calculator
just test-api -k health
just test-web src/pages/__tests__/HomePage.test.tsx
just test-playwright "--grep 'home page'"
just test-cypress --spec e2e/home.cy.ts
```

For arguments containing spaces, preserve the runner's inner quotes as in the
Playwright example above.

Python unit and API recipes use separate Allure output directories under
`temps/test-results-pytest/unit` and `temps/test-results-pytest/api`, so the second
run does not clean the first run's results. Existing browser reports remain
under `temps/dsa-web-ts-playwright` and `temps/dsa-web-ts-cypress`.

The Just Playwright recipe runs the backend on port **18000** and Vite on
**4173**, using a per-invocation database under `.pytest_cache/just` and an
`ENV_FILE` there instead of your repository `.env`. Notifications and remote
stock-index refresh are disabled for this recipe. Do not export live provider
credentials when running browser smoke tests; explicitly exported environment
variables and existing Playwright command/server-reuse overrides still apply.
Cypress starts its own Vite server on **4174** and mocks the API calls its specs
exercise. Keep these ports free. Both runners clean up their own servers.
`just verify` finishes after testing; it does not leave DSA running.

The recipes intentionally exclude Python demo/UI, Robot Framework, AI/network,
and performance suites. Run those using the framework-specific instructions
below when their external prerequisites are available. Application startup does
not configure LLM/data/notification providers; use the existing DSA setup UI or
your own `.env` for real analysis.

## One-time setup

### Python tests

Python 3.14 is the minimum and current CI-tested version; later versions are not
yet covered by the test configuration. Install the repository requirements into
a virtual environment. From the repository root:

```powershell
py -3.14 -m venv .venv
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

Use Node.js 22.22.2+, 24.15+, or 26.x and npm 10+. Install each package’s locked dependencies once
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
`http://127.0.0.1:18000` and `http://127.0.0.1:4173`. Activate the Python
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
$env:DSA_WEB_SMOKE_BACKEND_CMD = 'python main.py --serve-only --host 127.0.0.1 --port 18000'
```

### Cypress

Cypress uses `BASE_URL`, which defaults to `http://127.0.0.1:4174`.
`npm test` starts and stops Vite automatically. The existing specs intercept
their API requests, so they do not need a backend or live credentials.

```powershell
Push-Location apps\dsa-web-cypress-tests

# Start Vite, run all Cypress specs, and stop Vite
npm test

# Against an already-running frontend, run one spec or open the interactive runner
npm run cypress:run -- --spec "e2e/home.cy.ts"
npm run cypress:open

Pop-Location
```

To test against another running URL, set `BASE_URL` in the Cypress window
and use the direct runner instead of `npm test`:

```powershell
$env:BASE_URL = 'http://localhost:5173'
npm run cypress:run
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

### GitLab CI

The root [`.gitlab-ci.yml`](../.gitlab-ci.yml) mirrors
[GitHub CI](../.github/workflows/ci.yml): Python 3.14, pip installation from
`requirements.txt`, the same pytest/Robot selections, 25/60-minute timeouts,
and always-uploaded artifacts retained for 14/21 days. It uses the
`python:3.14-bookworm` container and requires a Linux Docker or Kubernetes
GitLab Runner with outbound access to package, browser, and Allure downloads.
The container must permit package installation; no privileged Docker mode is
needed. Set the runner's maximum timeout to at least 60 minutes.

| GitLab event | Jobs |
| --- | --- |
| Push to `main` or `master` | Smoke |
| Merge request targeting `main` or `master` | Smoke |
| **Build > Pipelines > New pipeline** (`web` source) | Smoke and regression |
| Pipeline schedule (`schedule` source) | Regression only |

Other branch pushes, tags, and pipeline sources do not create pipelines.
Interruptible jobs are canceled when GitLab supersedes them with a newer commit.
Pip and Playwright caches are keyed by `requirements.txt`; regression installs
browser OS dependencies even on cache hits. Java and Allure are installed before
tests so `after_script` can generate the HTML report after a test failure.
Report-generation failure emits a warning without overriding the test result.
Download test artifacts from the job page.

GitLab schedules cannot be declared in YAML. Create a schedule under
**Build > Pipeline schedules** with cron `0 2 * * *`, timezone **UTC**, and the
desired `main` or `master` branch to match GitHub's nightly 02:00 UTC run.
Configure any required external-service credentials as masked/protected GitLab
CI/CD variables, not in the YAML. As with GitHub CI, some regression suites need
external services; the pipeline does not provision MySQL or provider accounts.

GitHub's contributor-welcome workflow is platform-specific and is not part of
this GitLab test pipeline. Neither platform's current CI runs the separate DSA
Web npm suites, publishes images, deploys, or creates version tags. The GitHub
workflows remain unchanged. To disable GitLab CI, remove the root configuration
and disable its schedules; this does not affect GitHub Actions.

Performance test assets live in `tests/performance/`. They are not part of the
pytest, Robot, Vitest, Playwright, or Cypress commands above; follow the setup
and environment requirements of JMeter, Postman, or LoadRunner before running
them. See the [load runner guide](performance/load_runner/load_runner_best_practices.md)
for scenario-design practices.

For framework-specific details, see the [Playwright package guide](../apps/dsa-web-playwright-tests/Readme.md)
and [Cypress package guide](../apps/dsa-web-cypress-tests/Readme.md).
