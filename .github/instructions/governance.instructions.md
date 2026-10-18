---
applyTo: "readme.md,ai_stock/**/*.md,apps/**/*.md,tests/**/*.md,AGENTS.md,CLAUDE.md,.github/**,.claude/skills/**,docker/**"
---

# Repository Governance Instructions

These instructions apply to repository documentation, AI instructions, skills,
and deployment files selected by the `applyTo` pattern above.

## Documentation and instruction files

- Keep commands, file paths, workflow names, configuration keys, release paths,
  and directory references aligned with the executable repository state.
- Keep `readme.md` navigable, with the project overview and quick start easy to
  find. Place detailed guides beside the code or tests they describe, such as
  `apps/dsa-web/readme.md`, `ai_stock/llm/llm-providers.md`, and `tests/*.md`.
- `CLAUDE.md` is the shared AI collaboration instruction file and a regular
  Markdown file, not a symlink. If its meaning changes, sync the
  [repository development guide](../../readme.md#repository-development-guide),
  `.github/copilot-instructions.md`, scoped instructions, and repository skills
  as needed.
- The [Stock Analyzer skill guide](../../apps/dsa-web/readme.md#stock-analyzer-skill)
  and `strategies/` describe product behavior, not repository governance.
- If only one language version of a document is updated, explain why its
  counterpart was not synchronized.

## Change impact and rollback

Explain which pipeline, release path, deployment path, review automation, or
governance asset is affected, and describe the rollback path.

## Security and release policy

- Avoid widening permissions, exposing secrets, or adding destructive automation
  without a clearly documented need.
- Preserve the repository's opt-in auto-tag behavior (`#patch`, `#minor`,
  `#major`) unless the change explicitly updates release policy.

## Pull request titles

When creating, reviewing, or suggesting PRs, prefer titles in
`<type>: <change summary>` form and omit tool or agent source prefixes such as
`[codex]`, `codex`, `autocode`, or `copilot`. This is non-blocking guidance, not
a review hard blocker.
