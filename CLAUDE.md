# Sloth Python Project Guide

## Project Focus

This repository combines Python utilities, pytest and Playwright tests, Robot Framework suites, AI-assisted test generation, AI stock analysis, learning material, and load-test assets.

Keep changes small, focused, and compatible with the existing project structure. Prefer current repository paths and existing helpers over introducing parallel abstractions.

## Main Areas

- `ai_gen/`: AI + MCP generation of pytest/Playwright test scripts.
- `ai_stock/`: Stock data, news, strategies, deterministic prediction, and report generation.
- `config/`: Environment-backed shared runtime settings.
- `pytest_tests/`: Python tests grouped by `unit`, `api`, `ui`, `ddt`, and `ai`.
- `robot_tests/`: Robot Framework suites and Python keyword libraries.
- `self_healing/`: Playwright locator fallback, DOM similarity, and locator persistence.
- `skill_spring/`: Learning and research material, including algorithms and Claude/MCP studies.
- `utils/`: Domain-oriented helpers under `data/`, `browser/`, `integrations/`, `observability/`, `data_base/`, and `qtest_utilities/`.
- `load_tests/`: JMeter, Postman, and load-runner assets.
- `temps/`: Generated reports, logs, videos, and test results. Never edit or treat this as source.

## Configuration

- Python tooling and pytest configuration live in `pyproject.toml`.
- RobotCode project Python-path configuration lives in `robot.toml`.
- Runtime environment settings live in `config/config.py` and use environment variables.
- Keep secrets, API keys, tokens, and credentials out of source, tests, logs, and documentation.
- Use `.env.example` as the template for local environment variables.

## Validation Commands

Run commands from the repository root with the project environment active.

### Python and pytest

```powershell
python -m pytest --collect-only -q
python -m pytest -m "unit or api" --tb=short --maxfail=5
python -m pytest path/to/test_file.py -q
python -m ruff check .
python -m ruff format --check .
```

### Robot Framework

```powershell
python -m robot --dryrun --outputdir temps/robot_calculator_dryrun robot_tests/calculator/
python -m robot --outputdir temps/robot_calculator robot_tests/calculator/
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot_tests/ui/
python -m robot --outputdir temps/robot_tangerine_playwright robot_tests/ui/
```

### Run Everything

```powershell
$pytestExit = 0
$robotExit = 0

python -m pytest
$pytestExit = $LASTEXITCODE

python -m robot --outputdir temps/robot_all robot_tests/
$robotExit = $LASTEXITCODE

if ($pytestExit -ne 0 -or $robotExit -ne 0) {
    exit 1
}
```

Install Playwright browsers before UI execution:

```powershell
python -m playwright install
```

## Implementation Guidance

- Preserve public behavior unless the task explicitly changes it.
- Add focused tests for behavior changes.
- Use stable selectors and shared page objects/helpers for UI tests.
- Keep Robot keyword libraries importable from the project root and validate with a dry run first.
- Treat generated AI code as untrusted output: review it, run focused tests, and do not commit secrets.
- Keep `ai_stock` documentation honest about implemented deterministic behavior versus future LLM-agent work.
- Preserve compatibility shims when moving shared utilities into domain-specific packages.
- Do not modify generated files under `temps/` unless explicitly requested.

## Working Conventions

- Keep changes scoped to the requested task.
- Prefer small, incremental edits over broad refactors.
- Reuse existing utilities before introducing new helpers.
- Keep Robot keyword names descriptive and consistent.
- Preserve line length and formatting conventions configured in `pyproject.toml`.
- Keep generated output, reports, logs, and videos under `temps/` and out of source review.

## Change Completion Checklist

1. Inspect nearby implementation and tests before editing.
2. Make the smallest focused change.
3. Run the narrowest meaningful validation first.
4. Run broader tests when the change crosses package boundaries.
5. Report files changed, commands run, outcomes, and known limitations.
