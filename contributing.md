# Contributing to Sloth Python

Thanks for your interest in contributing.

This guide is intentionally short: set up quickly, make focused changes, test, and open a clean PR.

## Code of Conduct

Please follow `CODE_OF_CONDUCT.md` and keep all discussions respectful, constructive, and inclusive.

## Quick Start

1. Fork the repo on GitHub.
2. Clone your fork and add upstream.
3. Create a virtual environment and install dependencies.
4. Create a feature branch.

```powershell
git clone https://github.com/466725/sloth-python.git
cd sloth-python
git remote add upstream https://github.com/466725/sloth-python.git

python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m playwright install

git fetch upstream
git checkout -b feature/short-description upstream/main
```

For broader project setup, see `GETTING_STARTED.md`.

## Contribution Standards

- Keep changes small and focused.
- Follow PEP 8 and use type hints for new/updated Python code.
- Prefer clear names and simple, maintainable logic.
- Add/update tests for behavior changes.
- Update docs when workflows, commands, or behavior change.

## Run Tests Before Opening a PR

Use commands from the project root:

```powershell
python -m pytest -m "unit or api" --tb=short
python -m pytest --tb=short
python -m robot robot_demo/
```

When changing UI automation, also run relevant UI tests.

## Commit and PR Guidelines

Use Conventional Commits:

```text
feat(scope): short description
fix(scope): short description
docs(scope): short description
test(scope): short description
refactor(scope): short description
chore(scope): short description
```

PR expectations:

- Clear title and purpose
- What changed and why
- How to test (exact commands)
- Screenshots/logs if useful
- Linked issue (for example: `Fixes #42`)

Before creating the PR:

```powershell
git fetch upstream
git rebase upstream/main
git push origin feature/short-description
```

## Review Checklist

- Code style and naming are consistent
- Tests cover the change
- No unrelated refactors in the same PR
- Docs are updated if needed
- CI passes

## Where to Contribute

Common areas:

- `algorithms/`
- `pytest_demo/`
- `robot_demo/`
- `utils/`
- `.github/workflows/`

## Need Help?

- Use GitHub Issues for bugs/feature requests
- Use PR comments for implementation discussion

Thanks for improving Sloth Python.
