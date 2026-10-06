# Repository Development Guide

This guide describes the repository's default development workflow. Its goals
are to reduce repeated coordination and rework, and to keep changes aligned
with the current project structure.

When this guide differs from executable scripts, workflows, or the code, follow
the executable repository state and update the relevant documentation as part
of the related work.

## 1. Core rules

- Respect the existing directory boundaries:
  - Backend code belongs primarily in `ai_stock/`, `api/`, and their related
    tests.
  - Stock-data providers and adapters live under `ai_stock/stock_data/`.
  - Web frontend changes belong in `apps/dsa-web/`.
  - Deployment and pipeline changes belong in `scripts/`,
    `.github/workflows/`, or `docker/`.
- Do not run `git commit`, `git tag`, or `git push` without explicit approval.
- Write commit messages in English. Do not add a `Co-Authored-By` trailer.
- Never hardcode secrets, credentials, machine-specific paths, model names,
  ports, or environment-specific behavior.
- Prefer existing modules, configuration entry points, scripts, and tests
  over parallel implementations.
- Prefer stability over opportunistic optimization. Keep refactors,
  abstractions, and infrastructure migrations out of a task unless they are
  directly needed.
- When adding configuration, update `.env.example` and the relevant
  documentation.
- For user-visible changes to capabilities, CLI/API behavior, deployment,
  notifications, or report structure, update the relevant documentation and
  the project changelog if one is maintained.
- For report-format, report-rendering, or Web UI changes, include screenshots
  of affected reports or pages in the PR description. Prefer before/after
  comparisons when behavior changes. If screenshots cannot be provided,
  explain why and provide other visual evidence.
- Do not add issue/PR screenshots, review screenshots, one-off acceptance
  screenshots, or temporary visual evidence to the repository. Put them in the
  PR description, PR comments, GitHub attachments, Actions artifacts, or
  another accessible evidence link. Long-lived product diagrams may be
  committed when their filenames and meaning are not tied to a specific
  issue or PR.
- If a root `CHANGELOG.md` is maintained, keep its `[Unreleased]` section flat:
  one entry per line in the form `- [type] Description`. Allowed types are
  `feature`, `improvement`, `fix`, `docs`, `test`, and `chore`. Do not add
  category headings under `[Unreleased]`; maintainers can organize entries
  into headings when preparing a release.
- Keep the root `README.md` focused on the project overview, high-level
  capabilities, quick start, main entry points, and sponsorship or
  collaboration information. Put detailed behavior, configuration,
  troubleshooting, field contracts, implementation semantics, and edge cases
  in the relevant `docs/*.md` files.
- When changing one language version of a document, check whether a
  corresponding translation needs an update. If it does not, explain why in
  the delivery summary.
- Write comments, docstrings, and log messages clearly and accurately. Match
  the language and style of the surrounding file.

### 1.1 Pull request title guidance

- Prefer `<type>: <change summary>`, for example `fix: Correct session history
  loading`. Suggested types include `fix`, `feat`, `refactor`, `docs`,
  `chore`, `test`, and `ci`.
- Describe the actual change. Avoid prefixes that name a tool or agent, such as
  `[codex]`, `codex`, `autocode`, or `copilot`.
- This is a collaboration guideline, not a review blocker.

### 1.2 Contribution quality bar

- Do not substitute larger diffs, extra code, or patching review comments for
  sound design and convergence on the real requirement.
- Evaluate a contribution by whether it solves a clear problem, minimizes
  impact, preserves existing contracts, and covers actual risk paths—not by
  line count, file count, promotional language, or apparent scope.
- Do not use the repository as a low-cost experiment, résumé showcase, or
  contribution-farming venue. Contributors must understand the system
  contracts and complete basic self-review, integration, and validation.
- AI-assisted development is acceptable; submitting generated code without
  semantic review, validation, or refinement is not.
- After review feedback, do not patch only the specifically named line and
  claim the issue is resolved. Recheck all entry points, configuration,
  tests, documentation, workflows, and user-visible paths that implement the
  same behavior.
- If repeated review rounds reveal unresolved contract drift, duplicated
  fallbacks, tests that bypass real risk layers, or PR descriptions that
  contradict the diff, maintainers may ask for the PR to be closed and
  reworked.

## 2. AI collaboration assets

- `AGENTS.md` is the canonical source for repository AI collaboration rules.
- `CLAUDE.md` must be a symbolic link to `AGENTS.md` for compatibility with
  Claude tooling.
- `.github/copilot-instructions.md` and
  `.github/instructions/*.instructions.md` provide GitHub Copilot instructions
  and scoped additions. If they conflict with `AGENTS.md`, follow
  `AGENTS.md`.
- Repository collaboration skills live in `.claude/skills/`. Analysis
  artifacts belong in `.claude/reviews/`; those artifacts are local by
  default, while the skills may be committed.
- `docs/skill.md` describes product behavior; it is not the source of
  repository collaboration rules.
- If adding `.agents/skills/` or another agent-specific directory, first
  define one source of truth and synchronize other copies with a script or
  equivalent. Do not maintain duplicate content manually over time.
- When changing AI collaboration governance assets, run:

  ```bash
  python scripts/check_ai_assets.py
  ```

## 3. Project overview

- The project is a stock-analysis system covering A-shares, Hong Kong stocks,
  and U.S. equities.
- The main workflow is: fetch data → analyze technicals and search news →
  generate an LLM-assisted analysis/report → optionally send notifications.
- Key entry points:
  - `main.py`: analysis task entry point.
  - `server.py`: FastAPI service entry point.
  - `apps/dsa-web/`: Web frontend.
  - `.github/workflows/`: CI, release, and scheduled workflows.
- Main code areas:
  - `ai_stock/core/`: analysis pipeline and core orchestration.
  - `ai_stock/services/`: application services.
  - `ai_stock/stock_data/`: stock-data sources, adapters, and normalization.
  - `ai_stock/report/`: report generation and notifications.
  - `ai_stock/storage.py`: persistence and database access.
  - `ai_stock/agent/`: LLM agent execution, tool calling, specialist
    orchestration, trading skills, chat context, and deep research.
  - `api/`: FastAPI routes and request/response models.
  - `scripts/`: local and CI scripts.
  - `.github/scripts/`: GitHub automation scripts.
  - `tests/`: pytest suites.
  - `docs/`: project and feature documentation.

### 3.1 Agent paths used by the DSA application

- The stock-analysis pipeline in `ai_stock/core/pipeline.py` can route a
  stock analysis through the Agent factory in `ai_stock/agent/factory.py`.
  The factory selects the single-agent executor or, with `AGENT_ARCH=multi`,
  the multi-agent orchestrator.
- In multi-agent mode, `AGENT_ORCHESTRATOR_MODE` selects `quick`, `standard`,
  `full`, or `specialist`. The orchestrator coordinates technical,
  intelligence, risk, optional skill, and final decision stages.
- The agent tools in `ai_stock/agent/tools/` expose the application's
  existing stock-data, analysis, market, news, and backtest services to the
  model. `ai_stock/agent/runner.py` manages the model/tool execution loop;
  `ai_stock/agent/llm_adapter.py` provides the shared LiteLLM interface.
- The DSA chat API is implemented in `api/v1/endpoints/agent.py` and exposed
  under `/api/v1/agent/`. The Web client calls it through
  `apps/dsa-web/src/api/agent.ts`; streamed chat uses
  `/api/v1/agent/chat/stream`.
- Deep research is a separate endpoint and workflow. Optional agent memory
  and event alerts are supporting features, not required stages in every
  stock-analysis run.

## 4. Common commands

Run commands from the repository root unless a command changes directory.

### Run the application

```bash
python main.py
python main.py --debug
python main.py --dry-run
python main.py --stocks 600519,hk00700,AAPL
python main.py --market-review
python main.py --schedule
python main.py --serve
python main.py --serve-only
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Backend validation

```bash
pip install -r requirements.txt
python -m ruff check .
python -m ruff format .
./scripts/ci_gate.sh
python -m pytest -m "not network"
python -m py_compile <changed_python_files>
```

### Web validation

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

### Pull request and CI evidence

```bash
gh pr view <pr_number>
gh pr checks <pr_number>
gh run view <run_id> --log-failed
```

## 5. Default workflow

1. Classify the task: `fix`, `feat`, `refactor`, `docs`, `chore`, `test`, or
   `review`.
2. Read the relevant implementation, configuration, tests, scripts,
   workflows, and documentation before editing.
3. Identify the affected areas: backend, API, Web, workflows, documentation,
   or AI collaboration assets.
4. Check for high-risk surfaces: configuration semantics, API/schema
   contracts, data-source fallback, report structure, authentication,
   scheduling, and release workflows.
5. Make the smallest change that fully addresses the task. Do not bundle
   unrelated refactoring.
6. When documentation, scripts, or workflows disagree, trust executable code
   and workflows first, then decide whether the related documentation should
   be corrected.
7. Run the applicable checks in the validation matrix below.
8. In the final delivery, explain what changed and why, validation performed,
   anything not validated, risks, and how to roll back.

## 6. Validation matrix

### CI coverage

The active `.github/workflows/ci.yml` workflow currently has two jobs:

| Job | Trigger | Description |
| --- | --- | --- |
| `smoke-test` | Pushes and pull requests to `main` or `master` | Runs selected pytest and Robot Framework smoke suites. |
| `regression-test` | Scheduled runs and manual dispatch | Installs Playwright browsers, then runs broader pytest and Robot Framework suites. |

The workflow also runs on a schedule and supports manual dispatch. Other
workflow files under `.github/workflows/disabled/` are inactive; do not
describe them as current CI checks. If the PR already has relevant CI results,
reference them. If CI does not cover the changed behavior, or local and CI
environments differ materially, state what was validated locally and what
remains uncovered.

### By change area

- **Python backend**
  - Scope: `main.py`, `ai_stock/`, `api/`, and `tests/`.
  - Prefer `scripts/ci_gate.sh`.
  - Minimum syntax check: `python -m py_compile <changed_python_files>`.
  - For API, task orchestration, report generation, notifications,
    data-source fallback, authentication, or scheduling changes, state
    whether the affected path was covered.
- **Web frontend**
  - Scope: `apps/dsa-web/`.
  - Default checks: `cd apps/dsa-web && npm ci && npm run lint && npm run build`.
  - For API integration, routing, state management, Markdown/chart rendering,
    or authentication changes, identify related components and uncovered
    risks.
- **API/schema/authentication integration**
  - Scope: `api/**`, relevant `ai_stock/services/**` or model definitions,
    and `apps/dsa-web/**`.
  - Run the applicable backend validation and build the affected client.
  - Explicitly describe compatibility impact for changes to login, cookies,
    sessions, polling state, fields, or enums.
- **Documentation and governance**
  - Scope: `README.md`, `docs/**`, `AGENTS.md`,
    `.github/copilot-instructions.md`, `.github/instructions/**`, and
    `.claude/skills/**`.
  - Code tests are not required for documentation-only changes.
  - Confirm that commands, configuration keys, filenames, and workflow names
    match the repository.
  - When AI collaboration governance assets change, run
    `python scripts/check_ai_assets.py`.
- **Workflows, scripts, and Docker**
  - Scope: `.github/**`, `scripts/**`, and `docker/**`.
  - Run the closest local validation.
  - State which pipeline, release path, or deployment path is affected.
  - If Docker or GitHub Actions validation was not run, explain why and note
    relevant risks.
- **Network or third-party dependency changes**
  - Start with offline or deterministic checks.
  - Verify timeout, retry, fallback, error-message, and degradation behavior.
  - If online validation was not run, explain why.

## 7. Stability guardrails

- **Configuration and entry points**
  - For changes to `.env` semantics, defaults, CLI options, service startup,
    or scheduling, assess effects on local runs, Docker, GitHub Actions, API,
    and Web.
  - Prefer new configuration that preserves a usable default and adds
    capabilities when enabled. Avoid unnecessary overlapping switches and
    mutually exclusive modes.
- **Data sources and fallback**
  - Changes in `ai_stock/stock_data/` must preserve provider priority,
    failure fallback, field normalization, caching, and timeout behavior.
  - A single data-source failure should not break the entire analysis flow
    unless fail-fast behavior is explicitly required.
- **API and Web compatibility**
  - Check backend and Web compatibility when changing APIs, schemas,
    authentication, or report payloads.
  - Prefer additive fields, retaining existing fields, or providing a
    compatibility layer over silently breaking clients.
- **Reports, prompts, and notifications**
  - When changing report structure, prompts, extractors, notification
    templates, or Web/API flows, check that upstream inputs and downstream
    consumers remain compatible.
  - Failure of one notification channel should not break the main analysis
    flow unless fail-fast behavior is explicitly required.
  - When changing `EXTRACT_PROMPT` in
    `ai_stock/services/image_stock_extractor.py`, include the complete updated
    prompt in the PR description.
- **Workflows, releases, and packaging**
  - For changes to automatic tags, releases, Docker publishing, or scheduled
    analysis, assess trigger conditions, artifact paths, permissions, and
    rollback steps.
  - Keep automatic tagging opt-in: only commit titles containing `#patch`,
    `#minor`, or `#major` should trigger version updates unless release policy
    is explicitly changed.

## 8. Issue, PR, and skill workflows

- Reuse repository skills where applicable:
  - `.claude/skills/analyze-issue/SKILL.md`
  - `.claude/skills/analyze-pr/SKILL.md`
  - `.claude/skills/fix-issue/SKILL.md`
- For issue analysis, PR review, or issue fixes, follow the relevant skill
  and save its output under `.claude/reviews/`.
- Keep skill commands, templates, validation order, and delivery structure
  aligned with `AGENTS.md`.
- Skills should inspect CI/workflow evidence before deciding whether
  additional local validation is needed.
- Do not run operations that change remote or branch state—such as
  `git pull`, `git push`, `git tag`, or `gh pr create`—without user approval.
- Use this default PR review order:
  1. Necessity.
  2. Relevance.
  3. Suggested title (`<type>: <change summary>`, without tool/agent prefixes;
     not a hard blocker).
  4. Description completeness, checked against the repository PR template
     when one is present.
  5. Validation evidence.
  6. Implementation correctness.
  7. Merge decision.
- For `fix` PRs, explain the original problem, root cause, fix, and regression
  risks.
- Block merging for correctness or security issues, failed blocking CI,
  material contradictions between the PR description and diff, missing
  rollback steps, or repeated unresolved contract drift, patch stacking, or
  unreliable validation evidence.

### 8.1 Addressing review feedback without patch stacking

Do not add a local patch only at the line named by a reviewer and then claim
that all feedback is resolved. First understand the business contract behind
the feedback, then inspect every entry point, configuration, test, document,
workflow, and user-visible path that implements the same behavior.

After receiving review feedback:

1. List each original issue raised by the reviewer.
2. Explain its root cause, not just which lines changed.
3. Identify all affected paths, such as runtime, API/Web, CLI, diagnostics,
   workflows, documentation, and tests.
4. Fix the complete contract, not just the currently failing test or
   commented line.
5. Add regression coverage for the reviewer's counterexample, validate the
   real entry point, or state clearly why validation was not possible.
6. Update the PR body so its scope, validation, compatibility, risks, and
   rollback steps match the current head.

If this convergence cannot be completed, do not keep stacking patches or
claim the PR is ready to merge. Explain whether the PR should be split, closed
and reworked, or reduced to a newly agreed minimum scope.

The following are low-quality PR patterns:

- Using broad fallbacks, silent degradation, or `return False/None/[]` to hide
  an unclear contract.
- Mocking away the actual risk layer and proving only a local implementation.
- Claiming that CI closed an issue without covering the reviewer's
  counterexample.
- Allowing the PR body to disagree with the diff, validation results, or
  compatibility risks.
- Continuing to add isolated patches after review instead of converging on
  the complete behavior.
- Letting the same behavior differ across runtime, Web/API, documentation,
  workflows, and tests.

Passing CI proves that automated checks passed. It does not replace semantic
review or independently prove that a reviewer's counterexample has been
addressed.

## 9. Delivery and releases

- Use this default delivery summary:
  - What changed.
  - Why it changed.
  - Validation performed.
  - Items not validated.
  - Risks.
  - Rollback steps.
- For documentation-only work, `Docs only, tests not run` is acceptable, but
  still state whether commands and filenames were checked.
- Automatic tagging should remain opt-in: only commit titles containing
  `#patch`, `#minor`, or `#major` trigger version updates.
- Create annotated tags when tagging manually.
- Prefer merging user-visible changes through a PR, with appropriate labels
  and validation notes.
