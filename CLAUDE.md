# Repository AI Collaboration Instructions

This is a regular Markdown file, not a symlink. It contains the shared repository
collaboration rules and is the entry point for Claude tooling. Copilot-specific
instructions live in [.github/copilot-instructions.md](.github/copilot-instructions.md).
Keep these entry points consistent with the
[repository development guide](docs/repository_development_guide.md) and scoped
instructions under [.github/instructions/](.github/instructions/).

## Scope and structure

- Backend code belongs in `ai_stock/` and `api/`; data providers belong in
  `ai_stock/stock_data/`.
- The React/Vite application lives in `apps/dsa-web/`.
- Tests live under `tests/` and the project's other configured test directories.
- Deployment assets belong in `scripts/`, `.github/workflows/`, and `docker/`.
- Read the applicable scoped instructions before changing backend, client, or
  governance files.

## Making changes

- Inspect the current implementation and reuse existing services and helpers.
- Make focused, complete changes; avoid unrelated cleanup or broad refactoring.
- Preserve public behavior, API contracts, report formats, and existing defaults
  unless the task explicitly changes them.
- Preserve data-source priority, normalization, caching, timeouts, and fallback.
  One optional provider or notification failure must not break the main analysis.
- Update `.env.example` and relevant documentation when configuration changes.
- Do not manually edit generated assets or files under `temps/` unless requested.
- Preserve unrelated worktree changes. Do not discard work or run destructive Git
  operations without explicit approval.
- Do not commit, tag, push, or create a remote pull request without user approval.
- Never hardcode credentials or expose secrets in logs, examples, or test data.

## Python and frontend conventions

- Preserve Python 3.11+ compatibility and follow the existing file's style.
- Use clear names, proper types, and brief comments only for non-obvious logic.
- Prefer the standard library and existing dependencies; justify new packages.
- Keep Web changes within the existing components, API clients, and state stores.
- Use stable selectors and shared helpers for UI automation.

## Validation

Start with the smallest deterministic checks covering the changed behavior.

```powershell
python -m pytest tests\unit\path\to\test_file.py -q
python -m ruff check path\to\changed_file.py
python -m ruff format path\to\changed_file.py --check
```

For cross-cutting Python changes, expand to the relevant suites or full pytest
run. Use markers actually declared in `pyproject.toml`; do not invent selectors.
Distinguish existing lint or formatting failures from regressions and avoid
formatting unrelated files.

For Web changes, use the existing npm scripts from `apps/dsa-web/`:

```powershell
npm run test -- path/to/affected.test.tsx
npm run lint
npm run build
```

For Robot Framework changes, run the affected suite or a dry run using the
project's configured environment. Do not require live services or credentials
for tests that are intended to be offline.

Documentation-only changes do not require application tests. Verify referenced
paths and commands, run `git diff --check`, and validate governance changes with:

```powershell
python scripts\check_ai_assets.py
```

## Documentation and collaboration

- Keep `readme.md` focused on the overview and quick start; put detailed behavior,
  configuration, troubleshooting, and contracts in `docs/`.
- Keep related translations consistent; explain when no counterpart is updated.
- Repository collaboration skills live in `.claude/skills/`; local review
  artifacts belong in `.claude/reviews/`, not in the shared instruction files.
- `docs/skill.md` and `strategies/` describe DSA runtime skills, not repository
  collaboration instructions.
- Prefer PR titles in `<type>: <change summary>` form without tool-name prefixes.
- Preserve opt-in version tagging through `#patch`, `#minor`, and `#major`.
- Report what changed, validation commands and results, compatibility impact,
  and any limitations. Do not claim unrun checks passed.