# Repository AI Collaboration Instructions

This regular Markdown file (not a symlink) is the shared AI collaboration
entry point for Claude. Keep the
[Copilot entry point](.github/copilot-instructions.md) and scoped instructions
consistent with it. Detailed contributor rules live in
[CONTRIBUTING.md](CONTRIBUTING.md); setup and product guides start at
[readme.md](readme.md).

## Find the relevant instructions

Read the applicable scoped guide before editing.

| Area | Location | Instructions |
| --- | --- | --- |
| Backend and API | `ai_stock/`, `api/`, `main.py`, `server.py` | [Backend](.github/instructions/backend.instructions.md) |
| Data and news providers | `ai_stock/stock_data/`, `ai_stock/stock_news/` | [Backend](.github/instructions/backend.instructions.md) |
| React/Vite client | `apps/dsa-web/` | [Frontend](.github/instructions/frontend.instructions.md) |
| Tests | `tests/` and other configured test directories | [Testing guide](tests/testing_guide.md) and applicable backend/client instructions |
| Documentation and collaboration | Root guides, `.github/`, `.claude/skills/` | [Governance](.github/instructions/governance.instructions.md) |
| CI and deployment | `.github/workflows/`, `.gitlab-ci.yml`, `docker/` | [Governance](.github/instructions/governance.instructions.md) and [CI guide](tests/testing_guide.md#test-results-and-ci) |

## Change safely

- Inspect the implementation first; reuse existing services, helpers, components,
  API clients, and state stores. Make focused, complete changes without unrelated
  cleanup or broad refactoring.
- Preserve public behavior, API contracts, report formats, and defaults unless
  the task explicitly changes them.
- Preserve provider priority, normalization, caching, timeouts, and fallback.
  An optional provider or notification failure must not break the main analysis.
- Preserve Python 3.14+ compatibility and the existing file's style. Use clear
  names, proper types, and brief comments only for non-obvious logic.
- Prefer the standard library and existing dependencies; justify new packages.
  Use stable selectors and shared helpers for UI automation.
- Never hardcode credentials or expose secrets in logs, examples, or test data.
  Update [.env.example](.env.example) and related guides when configuration changes.
- Do not manually edit generated assets or files under `temps/` unless requested.
  Preserve unrelated worktree changes; do not discard work or perform destructive
  Git operations without explicit approval.
- Do not commit, tag, push, or create a remote pull request without user approval.
  Preserve opt-in version tagging through `#patch`, `#minor`, and `#major`.

## Validate the affected behavior

Start with the smallest deterministic check; expand to relevant suites or full
pytest for cross-cutting changes. Use the configured environment and existing
[Just recipes](justfile) or commands in the [testing guide](tests/testing_guide.md).

- **Python:** run the affected pytest file, `python -m py_compile` on changed
  Python files, and targeted Ruff lint/format checks. Use markers declared in
  [pyproject.toml](pyproject.toml), not invented selectors. Do not format unrelated
  files; distinguish existing failures from regressions.
- **Web:** run the affected Vitest tests and the existing `npm run lint` and
  `npm run build` scripts from `apps/dsa-web/`. Run impacted browser suites when
  relevant.
- **Robot Framework:** run the affected suite or a dry run. Offline tests must
  not require live services or credentials.
- **Documentation:** verify referenced paths and commands and run
  `git diff --check`; application tests are not required. For governance edits,
  check the collaboration entry points and scoped guides for consistency.

`just verify` performs setup, build, and the configured DSA test suites; it is
not a substitute for choosing focused checks or for testing unrelated demo suites.

## Keep documentation and handoffs useful

- Keep the root README navigable, with the overview and quick start easy to find.
  Place detailed guides beside their code or tests, for example the
  [Web guide](apps/dsa-web/readme.md) and
  [LLM provider guide](ai_stock/llm/llm-providers.md).
- Keep related translations consistent; explain when no counterpart is updated.
- [Repository collaboration skills](.claude/skills/README.md) live in
  `.claude/skills/`; local review artifacts belong in `.claude/reviews/`, not
  shared instruction files. The
  [Stock Analyzer skill](apps/dsa-web/readme.md#stock-analyzer-skill) and
  [strategies](strategies/) are DSA runtime features, not collaboration rules.
- Prefer PR titles in `<type>: <change summary>` form without tool-name prefixes.
- Report what changed and why, validation commands/results, compatibility impact,
  and limitations. Never claim unrun checks passed.
