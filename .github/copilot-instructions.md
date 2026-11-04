# Copilot Instructions for sloth-python

[CLAUDE.md](../CLAUDE.md) is the canonical shared AI collaboration guide and a
regular Markdown file, not a symlink. Follow it and the applicable scoped
instructions; keep these entry points consistent with
[CONTRIBUTING.md](../CONTRIBUTING.md).

## Scope

- Backend/API: `ai_stock/`, `api/`, and related Python entry points and tests.
  Read [backend instructions](instructions/backend.instructions.md).
- React/Vite client: `apps/dsa-web/`.
  Read [frontend instructions](instructions/frontend.instructions.md).
- Documentation, collaboration, CI, and deployment:
  read [governance instructions](instructions/governance.instructions.md).
- Repository collaboration skills are indexed in
  [.claude/skills/README.md](../.claude/skills/README.md).

## Working rules

- Make focused, complete changes. Reuse existing utilities and preserve public
  behavior, API contracts, defaults, and optional-provider resilience.
- Preserve Python 3.14+ compatibility and existing formatting, types, imports,
  and localization. Prefer existing dependencies; justify additions.
- Preserve unrelated worktree changes. Do not manually edit generated assets or
  `temps/` unless requested, or commit, tag, push, or open a remote PR without
  approval.
- Never hardcode or expose secrets. Update configuration examples and related
  documentation when configuration changes.

## Validation and delivery

Use the smallest meaningful checks from the [testing guide](../tests/testing_guide.md)
or existing [Just recipes](../justfile). Use markers declared in
[pyproject.toml](../pyproject.toml), targeted Ruff checks without unrelated
formatting, and the existing frontend npm scripts. Keep offline tests independent
of live services and credentials.

For documentation-only edits, verify paths/commands and run `git diff --check`.
Report changed files, reasons, validation commands and outcomes, compatibility
impact, and limitations. Do not claim checks passed unless they ran.
