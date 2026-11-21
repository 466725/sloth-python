# Trading Strategies

This directory contains natural-language trading strategies. YAML definitions can live directly here; Markdown skill bundles belong in subdirectories containing `skill.md`. Both formats are loaded automatically at runtime.

In the user interface and documentation, these capabilities are called
"strategies". In code, configuration, and API fields, they are called `skill`,
meaning a reusable strategy capability.

Use `AGENT_SKILL_DIR` to add a separate custom skill directory; custom definitions load alongside the built-in strategies.

## How to Write a Custom Strategy Skill

Create a `.yaml` file and describe your trading strategy in English or any
other language. **No code is required.**

### Minimal Template

```yaml
name: my_strategy          # Unique identifier (English, separated by underscores)
display_name: My Strategy  # Display name
description: Briefly describe the strategy's purpose

instructions: |
  Your strategy description...
  Describe assessment criteria, entry conditions, exit conditions, and so on in natural language.
  You can reference tools such as get_daily_history and analyze_trend to guide the AI's data use.
```

### Complete Template

```yaml
name: my_strategy
display_name: My Strategy
description: Briefly describe the market conditions suited to this strategy

# Strategy category: trend, pattern, reversal, or framework
category: trend

# Related core trading principle numbers (1-7), optional
core_rules: [1, 2]

# Tools needed by the strategy, optional
# Available tools: get_daily_history, analyze_trend, get_realtime_quote,
#                  get_sector_rankings, search_stock_news, get_stock_info
required_tools:
  - get_daily_history
  - analyze_trend

# Optional aliases (used for natural-language skill selection, such as /ask)
aliases: [my approach, my model]

# Optional metadata controlling default behavior
# default_active: whether the skill is active by default
# default_router: whether the skill belongs to the router's fallback set
# default_priority: default display/sort priority; lower numbers appear first
# market_regimes: market conditions for which the skill is preferred
default_active: true
default_router: false
default_priority: 100
market_regimes: [trending_up]

# Detailed strategy instructions (natural language; Markdown is supported)
instructions: |
  **My Strategy Name**

  Assessment criteria:

  1. **Condition one**:
     - Use `analyze_trend` to check moving average alignment.
     - Describe the trend characteristics you expect to see...

  2. **Condition two**:
     - Describe the volume requirements...

  Score adjustments:
  - Suggest a sentiment_score adjustment when the conditions are met.
  - Include the strategy name in `buy_reason`.
```

### Core Trading Principles

| Number | Principle |
| ------ | --------- |
| 1 | Strict entry: consider entry only when the deviation rate is below 5%. |
| 2 | Trend trading: bullish alignment of MA5 > MA10 > MA20. |
| 3 | Efficiency first: use volume to confirm the trend. |
| 4 | Entry preference: favor pullbacks to moving average support. |
| 5 | Risk screening: adverse news can veto a trade. |
| 6 | Price-volume alignment: use volume to validate price movements. |
| 7 | Relax standards appropriately for strong-trending sector leaders. |

## Custom Strategy Directory

In addition to the built-in strategies in this directory, you can specify a
custom strategy directory using an environment variable:

```env
AGENT_SKILL_DIR=./my_skills
```

The system loads both built-in and custom strategies. If names conflict, the
custom strategy overrides the built-in one.

The environment variable remains `AGENT_SKILL_DIR` to match the internal
terminology; in product terms, it specifies the custom strategy directory.
