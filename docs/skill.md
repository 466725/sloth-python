# Stock Analyzer Skill

The runtime skill bundle is [strategies/stock-analyzer/skill.md](../strategies/stock-analyzer/skill.md). The Agent loads it automatically from the built-in `strategies/` directory; setting `AGENT_SKILL_DIR` is not required.

The skill is user-invocable and appears in the Web app's skill selector. It is not part of the default active skill set, so users can choose it explicitly in chat or analysis without changing the behavior of all existing default analyses.

For custom skill bundles, set `AGENT_SKILL_DIR` to a separate directory containing YAML definitions or nested `skill.md` bundles. The runtime loads those in addition to built-in strategies.
