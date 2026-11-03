set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command"]

uv := "python -m uv"
web_dir := join("apps", "dsa-web")
playwright_dir := join("apps", "dsa-web-playwright-tests")
cypress_dir := join("apps", "dsa-web-cypress-tests")
ui_state_dir := join(justfile_directory(), ".pytest_cache", "just", uuid())

# List available commands.
default:
    @just --list

# Install locked dependencies and browser assets, build DSA, and run all DSA checks.
verify: setup build test

# Configure Python, the DSA frontend, and both DSA browser test packages.
setup: setup-python setup-web setup-ui

# Show tool versions (requires Python 3.14+, uv, Node.js 24.15+ LTS, npm, and just).
doctor:
    python --version
    {{ uv }} --version
    node --version
    npm --version
    just --version

# Create/update .venv using the checked-in Python lockfile.
setup-python:
    {{ uv }} sync --locked --python 3.14

# Install the frontend's locked npm dependencies.
setup-web:
    npm --prefix "{{ web_dir }}" ci

# Install both DSA browser runners and their browsers; Linux may request sudo.
setup-ui: _setup-playwright _setup-cypress

[private]
[working-directory(playwright_dir)]
_setup-playwright:
    npm ci
    npx --no-install playwright install --with-deps chromium

[private]
[working-directory(cypress_dir)]
_setup-cypress:
    npm ci
    npx --no-install cypress install
    npx --no-install cypress verify

# Build the frontend into the backend's configured static-assets directory.
build:
    npm --prefix "{{ web_dir }}" run build

# Set up and launch the built DSA Web/API app; Ctrl+C stops it.
dsa host="127.0.0.1" port="8000": setup-python setup-web build
    {{ uv }} run --locked --python 3.14 python main.py --serve-only --host "{{ host }}" --port "{{ port }}"

# Start only the backend for development (run dev-web in a second terminal).
dev-api:
    {{ uv }} run --locked --python 3.14 python -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload

# Start Vite on loopback; proxies API requests to dev-api on port 8000.
dev-web:
    npm --prefix "{{ web_dir }}" run dev -- --host 127.0.0.1

# Run the DSA CLI (for example: just analyze --stocks 600519 --dry-run).
analyze *args:
    {{ uv }} run --locked --python 3.14 python main.py {{ args }}

# Run Python unit/API tests, frontend unit/component tests, and both UI suites.
test: test-unit test-api test-web test-ui

# Run all Python unit tests, including unmarked unittest-style tests.
test-unit *args:
    {{ uv }} run --locked --python 3.14 python -m pytest "{{ join('tests', 'unit') }}" -q --alluredir="{{ join('temps', 'test-results-pytest', 'unit') }}" {{ args }}

# Run isolated, in-process DSA API/contract tests (temporary SQLite; no live service).
test-api *args:
    {{ uv }} run --locked --python 3.14 python -m pytest "{{ join('tests', 'pytest_tests', 'api_suites') }}" -q --alluredir="{{ join('temps', 'test-results-pytest', 'api') }}" {{ args }}

# Run DSA frontend unit/component tests with Vitest.
test-web *args:
    npm --prefix "{{ web_dir }}" run test -- {{ args }}

# Run only DSA Web browser tests, not unrelated Python/demo UI suites.
test-ui: test-playwright test-cypress

# Auto-start/stop the API and Vite using an isolated database and no local .env.
[env("DATABASE_PATH", join(ui_state_dir, "dsa.db"))]
[env("ENABLE_NOTIFICATION", "false")]
[env("ENV_FILE", join(ui_state_dir, ".env"))]
[env("STOCK_INDEX_REMOTE_UPDATE_ENABLED", "false")]
[env("VIRTUAL_ENV", join(justfile_directory(), ".venv"))]
[working-directory(playwright_dir)]
test-playwright *args:
    npm test -- {{ args }}

# Auto-start/stop Vite; these UI tests intercept API requests.
[working-directory(cypress_dir)]
test-cypress *args:
    npm test -- {{ args }}

# Lint the frontend and type-check both browser test packages.
lint:
    npm --prefix "{{ web_dir }}" run lint
    npm --prefix "{{ playwright_dir }}" run typecheck
    npm --prefix "{{ cypress_dir }}" run typecheck

# Open the latest Playwright HTML report.
[working-directory(playwright_dir)]
report-ui:
    npm run test:report
