# Documentation Index

Use this page to find project guides, feature references, testing instructions,
and learning material across the repository.

## Project overview and architecture

- [Project README](../readme.md) — project overview, setup, configuration, and
  main workflows.
- [AI Stock architecture and package guide](../ai_stock/readme.md) — current
  analysis flow and responsibilities of the `ai_stock` modules.
- [DSA Web guide](../apps/dsa-web/readme.md) — frontend routes, development,
  and Web test strategy.
- [Cypress test package guide](../apps/dsa-web-cypress-tests/readme.md) — setup
  and configuration for the DSA Web Cypress suite.

## User and feature guides

- [LLM provider configuration](llm-providers.md) — provider setup, channels,
  and connection troubleshooting.
- [Alert center](alerts.md) — alert rules, evaluation, and notifications.
- [Email notifications](email_notifications.md) — SMTP configuration and
  delivery diagnostics.
- [Stock autocomplete catalog](stock-index.md) — catalog updates and rebuilds.
- [Analysis context pack](analysis-context-pack.md) — analysis input context,
  quality metadata, and data flow.
- [Product skills guide](skill.md) — DSA runtime skills and their usage.

## Development and testing

- [Testing guide](testing_guide.md) — commands for pytest, Robot Framework,
  Vitest, Cypress, and running all four.
- [Repository development guide](repository_development_guide.md) — repository
  structure, collaboration practices, and development conventions.
- [Database utilities guide](../utils/data_base/readme.md) — database helper
  usage and query examples.
- [Load runner best practices](../tests/performance/load_runner/load_runner_best_practices.md)
  — guidance for performance test assets.
- [Playwright locator strategy](../tests/pytest_tests/ui_suites/tangerine/Playwright%20Locator%20Strategy%20Guide.md)
  — locator selection guidance for UI automation.
- [JSON locator pros and cons](../tests/pytest_tests/ui_suites/locators/Json_locator_pros_and_cons.md)
  — tradeoffs of JSON-based locator storage.

## Repository collaboration instructions

These documents guide contributors and coding assistants; they are not product
documentation:

- [Shared repository instructions](../claude.md)
- [Copilot instructions](../.github/copilot-instructions.md)
- [Backend-specific instructions](../.github/instructions/backend.instructions.md)
- [Web client instructions](../.github/instructions/client.instructions.md)
- [Governance instructions](../.github/instructions/governance.instructions.md)
- [Security instructions](../.github/instructions/security.instructions.md)
- [Claude skills index](../.claude/skills/README.md)

## Learning material

- [Skill Spring overview](../skill_spring/readme.md)
- [Claude Code learning notes](../skill_spring/claude_code/claude_code_learning.md)
- [Sorting algorithms: normal-distribution quicksort](../skill_spring/algorithms/sorts/normal_distribution_quick_sort.md)
- [Claude Agent SDK guide](../skill_spring/claude_code/claude_agent_sdk/README.md)
- [Claude Agent SDK release guide](../skill_spring/claude_code/claude_agent_sdk/RELEASING.md)
- [Claude Agent SDK end-to-end tests](../skill_spring/claude_code/claude_agent_sdk/e2e-tests/README.md)

The Claude Agent SDK folder also contains individual feature examples, such as
[session stores](../skill_spring/claude_code/claude_agent_sdk/examples/session_stores/README.md)
and [plugins](../skill_spring/claude_code/claude_agent_sdk/examples/plugins/demo-plugin/commands/greet.md).
