---
applyTo: "readme.md,ai_stock/**/*.md,apps/**/*.md,tests/**/*.md,AGENTS.md,CLAUDE.md,.github/**,.claude/skills/**,docker/**"
---

# Governance Instructions

- Keep commands, file paths, workflow names, config keys, release paths, and directory references aligned with the executable repository state.
- `CLAUDE.md` is the shared AI collaboration instruction file and a regular Markdown file, not a symlink. If its meaning changes, sync the [repository development guide](../../readme.md#repository-development-guide), `.github/copilot-instructions.md`, scoped instructions, and repository skills as needed.
- The [Stock Analyzer skill guide](../../apps/dsa-web/readme.md#stock-analyzer-skill) and `strategies/` describe product behavior, not repository governance.
- Explain which pipeline, release path, deployment path, review automation, or governance asset is affected and what the rollback path is.
- Keep `readme.md` navigable, with the project overview and quick start easy to find. Put detailed guides beside the code or tests they describe, such as `apps/dsa-web/readme.md`, `ai_stock/llm/llm-providers.md`, and `tests/*.md`.
- Avoid widening permissions, secret exposure, or destructive automation without a clearly documented need.
- Preserve the repository's opt-in auto-tag behavior (`#patch`, `#minor`, `#major`) unless the change explicitly updates release policy.
- When creating, reviewing, or suggesting PRs, prefer PR titles in `<type>: <change summary>` form and omit tool/agent source prefixes such as `[codex]`, `codex`, `autocode`, or `copilot`; treat this as non-blocking guidance, not a review hard blocker.
- If only one language version of a document is updated, explain why the counterpart was not synchronized.
