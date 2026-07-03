# CLAUDE.md

Global context for working in this monorepo with Claude Code.

## Purpose

This repository combines:
- Python libraries and demos
- Pytest + Playwright automation
- Robot Framework suites
- Load-testing artifacts (JMeter/Postman)
- Shared utility modules

When making changes, prefer minimal, targeted edits and avoid broad refactors unless requested.

## Environment

- OS used most often: Windows (PowerShell)
- Python: 3.11+ supported; tooling config targets Python 3.12
- Install deps:
  - `pip install -r requirements.txt`
- Install Playwright browsers when needed:
  - `playwright install`

## Common Commands

### Lint and format

Use Ruff (configured in pyproject.toml):
- `python -m ruff check .`
- `python -m ruff check . --fix`
- `python -m ruff format .`

### Pytest

- Full run:
  - `python -m pytest`
- Marker-based run:
  - `python -m pytest -m ui`
  - `python -m pytest -m api`
- Single file:
  - `python -m pytest pytest_demo/tests/unit/test_csv_reader.py -q`

Notes:
- pytest.ini writes Allure output to `temps/allure-results`
- Default testpaths include:
  - `pytest_demo/tests`
  - `robot_demo/calculator/tests`

### Robot Framework

- Run all Robot demos:
  - `python -m robot --outputdir temps/robot_all robot_demo/`
- Run calculator suite:
  - `python -m robot --outputdir temps/robot_calculator robot_demo/calculator/`
- Run Tangerine Playwright suite:
  - `python -m robot --outputdir temps/robot_tangerine_playwright robot_demo/tangerine_playwright/`
- Dry run (syntax/keyword wiring):
  - `python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot_demo/tangerine_playwright/`

### Allure report

- Generate results via pytest:
  - `python -m pytest --alluredir=temps/allure-results --clean-alluredir`
- Open report:
  - `allure serve temps/allure-results`

## Repo Map

- `pytest_demo/`: pytest-based tests (ui/api/unit/ddt/playwright)
- `robot_demo/`: Robot Framework suites and keyword libraries
- `self_healing/`: locator healing logic for UI automation
- `ai_gen/`: AI-based test/code generation helpers
- `utils/`: shared helpers and integrations (config, analytics, qTest, DB)
- `algorithms/`: algorithm and data-structure examples
- `load_test_demo/`: JMeter and Postman assets
- `temps/`: generated logs, reports, videos, and temporary artifacts

## Working Conventions

- Keep changes scoped to the requested task.
- Do not edit generated outputs in `temps/` unless explicitly asked.
- Prefer stable selectors and reusable helpers for UI tests.
- For Robot keyword/library changes, keep keyword names descriptive and consistent.
- Reuse shared helpers in `utils/` before adding duplicate logic.
- Preserve existing style rules from pyproject.toml:
  - line length 100
  - double quotes
  - sorted imports via Ruff/isort profile

## Test Strategy After Changes

Pick the smallest meaningful validation first, then broaden only if needed.

- Python utility/module change:
  - run targeted pytest file(s)
- Pytest UI/API change:
  - run impacted test module and marker subset
- Robot change:
  - run target suite, optionally dry run first
- Cross-cutting change:
  - run `python -m pytest` and at least one relevant Robot suite

## Load Test Assets Guidance

- JMeter and Postman files in `load_test_demo/` are source artifacts.
- Avoid mass reformatting JSON/JMX files unless task requires it.
- If environments are modified, keep variable names backward compatible when possible.

## Safety and Secrets

- Never hardcode secrets or tokens.
- Use environment variables for API keys and endpoints.
- Keep defaults in `utils/config.py` and override through env vars.

## PR/Change Notes

When summarizing work, include:
- files changed
- commands run
- result status (pass/fail/not run)
- follow-up actions if validation was partial

