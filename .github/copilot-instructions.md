# Copilot Instructions for sloth-python

## Purpose
This repository contains Python libraries, pytest suites (API/UI/unit), Robot Framework suites, and load testing assets.
Keep changes minimal, task-focused, and easy to review.

## Core Principles
- Prefer small, incremental edits over broad refactors.
- Preserve existing public behavior unless a change is explicitly requested.
- Reuse existing utilities before introducing new helpers.
- Keep code readable and maintainable; optimize only when needed.
- Do not modify generated artifacts unless the task explicitly asks for it.

## Python Standards
- Target Python 3.11+ compatibility.
- Follow existing style conventions in the repository.
- Use clear names and straightforward control flow.
- Add brief comments only for non-obvious logic.
- Avoid adding unnecessary dependencies.

## Formatting and Linting
Run these before finalizing substantial Python changes:

```bash
python -m ruff check .
python -m ruff format .
```

If needed, apply automatic fixes:

```bash
python -m ruff check . --fix
```

## Testing Expectations
Choose the smallest meaningful validation first, then expand scope when needed.

- Targeted pytest run:

```bash
python -m pytest path/to/test_file.py -q
```

- Marker-based runs:

```bash
python -m pytest -m ui
python -m pytest -m api
```

- Full pytest run for cross-cutting changes:

```bash
python -m pytest
```

For Robot Framework changes, run the impacted suite first:

```bash
python -m robot --outputdir temps/robot_calculator robot_demo/calculator/
```

Optional dry run for keyword wiring:

```bash
python -m robot --dryrun --outputdir temps/robot_tangerine_playwright_dryrun robot_demo/tangerine_playwright/
```

## Project-Specific Conventions
- Do not edit files under temps/ unless explicitly requested.
- Prefer stable selectors and shared helpers for UI automation.
- Keep Robot keyword names descriptive and consistent.
- Preserve line length and formatting conventions already configured in pyproject.toml.

## Security and Secrets
- Never hardcode secrets, credentials, API keys, or tokens.
- Use environment variables for sensitive configuration.
- Avoid exposing sensitive values in logs, examples, or test data.

## Dependency and Import Hygiene
- Keep imports clean and remove unused imports.
- Prefer standard library and existing project modules first.
- Add third-party packages only when necessary and justify in PR notes.

## Pull Request Quality Bar
When proposing changes, include:
- What changed and why.
- Files modified.
- Commands run for validation.
- Test outcomes (pass, fail, or not run).
- Known limitations or follow-up work.

## Guidance for Copilot Responses
When generating code in this repository, Copilot should:
- Follow existing patterns before inventing new structure.
- Produce minimal diffs that solve the requested problem.
- Suggest targeted tests for changed behavior.
- Call out assumptions when requirements are ambiguous.
- Prefer safe, deterministic behavior over clever shortcuts.
