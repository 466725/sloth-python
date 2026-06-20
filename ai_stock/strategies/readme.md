# Stock Strategy Playbook

This folder contains YAML strategy definitions used by the AI stock analysis flow. Each file describes when a strategy applies, which analysis tools it needs, how it should reason about signals, and how it should adjust the final recommendation.

These strategies are decision-support rules, not financial advice. Keep every strategy explicit about risk, stop-loss logic, uncertainty, and when to avoid a trade.

## Current Strategies

| File | Strategy | Market Regime | Purpose |
| --- | --- | --- | --- |
| `bull_trend.yaml` | 默认多头趋势 / Default Bull Trend | `trending_up` | Default router strategy for uptrend continuation, pullback entries, and trend risk control. |
| `box_oscillation.yaml` | 箱体震荡 / Box Range Trading | `sideways` | Range-bound strategy for buying near support, reducing near resistance, and handling breakouts. |
| `bottom_volume.yaml` | 底部放量 / Bottom Volume Surge | `trending_down` | Higher-risk reversal strategy for volume expansion after an extended decline. |

## YAML Contract

Use this structure for every strategy file:

```yaml
name: snake_case_unique_id
display_name: Human-readable name
description: One-sentence purpose and ideal use case.
category: trend | reversal | framework | risk | custom
core_rules: [1, 2, 3]
required_tools:
  - get_daily_history
  - analyze_trend
aliases: [short user-facing names]
default_active: true
default_router: true
default_priority: 10
market_regimes: [trending_up]

instructions: |
  Markdown instructions for analysis, scoring, outputs, and risk controls.
```

Required fields:

- `name`: Stable snake_case identifier. Do not rename it casually because other routing or prompts may depend on it.
- `display_name`: User-facing name, usually Chinese plus optional English in the instructions.
- `description`: Clear summary of what the strategy detects.
- `category`: Strategy family. Use existing categories where possible.
- `core_rules`: References to shared trading principles or rule groups.
- `required_tools`: Tools the agent must use or consider before applying the strategy.
- `market_regimes`: Market states where the strategy is appropriate.
- `instructions`: The full strategy playbook, written as actionable Markdown.

Optional fields:

- `aliases`: Terms users may type to select or imply the strategy.
- `default_active`: Whether the strategy is available by default.
- `default_router`: Whether this strategy can be the default choice when no specific strategy is requested.
- `default_priority`: Lower numbers should be treated as more default/general; higher numbers are more specific or conditional.

## Strategy Design Best Practices

Prefer explicit, testable conditions.

- Define the market regime first: uptrend, sideways, downtrend, reversal, breakout, or avoidance.
- Use numeric thresholds where possible, such as MA alignment, distance from support/resistance, volume ratio, drawdown percentage, or breakout confirmation days.
- Separate entry logic, exit logic, invalidation logic, and position sizing.
- Always include a "do nothing" path. A good strategy should know when there is no edge.
- State what evidence would weaken or cancel the signal.

Avoid vague optimism.

- Do not write instructions that only search for bullish evidence.
- Do not treat volume expansion, news, or price movement as automatically positive.
- Do not recommend chasing after extended moves unless the strategy explicitly defines a breakout continuation setup.
- Reversal strategies should be sized smaller and require stricter confirmation than trend-following strategies.

Make risk controls first-class.

- Every strategy should specify a stop-loss reference: structural low, MA20, box boundary, breakout failure level, or volatility-based level.
- Every strategy should mention position sizing expectations.
- Every strategy should distinguish observation, initial entry, add-on entry, reduce, and exit.
- If the setup depends on real-time quotes or news, include a freshness check in the instructions.

## Routing And Priority Guidelines

Use `bull_trend.yaml` as the general default because it has `default_router: true` and a low `default_priority`.

Suggested priority meaning:

- `1-20`: Default or broad market strategies.
- `21-50`: Common conditional frameworks.
- `51-80`: Specific patterns, reversal setups, or higher-risk strategies.
- `81+`: Rare, experimental, or highly specialized strategies.

When multiple strategies match:

1. Match the current `market_regimes`.
2. Prefer the strategy explicitly requested by the user or matched by `aliases`.
3. Prefer the strategy with stronger evidence from required tools.
4. Use `default_priority` as the tie-breaker.
5. If signals conflict, report the conflict instead of forcing a buy/sell conclusion.

## Maintaining Strategies

When adding or changing a strategy:

1. Keep the file name equal to `name`, for example `bottom_volume.yaml`.
2. Keep YAML valid and indentation consistent with the existing files.
3. Add clear `required_tools`; do not reference a tool in `instructions` unless it is available or intentionally optional.
4. Add the strategy to the inventory table in this README.
5. Include at least one risk condition and one invalidation condition.
6. Use thresholds that can be checked from available data.
7. Keep scoring adjustments bounded and explain why they move the recommendation.
8. Review overlap with existing strategies to avoid duplicated or contradictory guidance.

## Instruction Writing Checklist

Each `instructions` block should answer:

- When is this strategy applicable?
- What data should be fetched?
- What conditions confirm the setup?
- What conditions reject the setup?
- What should the output include?
- How should `sentiment_score` or recommendation strength change?
- Where is the stop-loss or invalidation level?
- What position size or risk level is appropriate?
- What should be written in `buy_reason`, `pattern_analysis`, or equivalent output fields?

## Validation Checklist

Before committing a strategy change:

- YAML parses successfully.
- `name` is unique.
- `required_tools` are spelled consistently.
- `market_regimes` are meaningful and not overly broad.
- Instructions do not contain stale assumptions about market data availability.
- Strategy has both positive and negative signal handling.
- Risk guidance is concrete enough to act on.
- README inventory is updated.

Quick local validation idea:

```powershell
python - <<'PY'
import pathlib, yaml

for path in pathlib.Path("ai_stock/strategies").glob("*.yaml"):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["name"] == path.stem, f"{path}: name must match file stem"
    for key in ["display_name", "description", "category", "required_tools", "market_regimes", "instructions"]:
        assert key in data, f"{path}: missing {key}"
    print(f"ok: {path}")
PY
```

## Review Cadence

Review strategies periodically against actual analysis outcomes:

- Monthly: remove stale thresholds, clarify ambiguous wording, and check tool names.
- After major market regime changes: verify that trend, range, and reversal strategies still route correctly.
- After adding new data tools: update `required_tools` and instructions so strategies use better evidence.
- After bad recommendations: add explicit invalidation rules rather than only reducing score values.

Good strategy maintenance should make the system more cautious, more explainable, and easier to audit over time.



# 交易策略目录 / Trading Strategies

本目录存放 **自然语言交易策略文件**（YAML 格式）。系统启动时自动加载此目录下所有 `.yaml` 文件。

对用户和文档，我们继续把这些能力称为“策略”；在代码、配置和 API 字段里，它们统一命名为 `skill`，你可以把它理解为“可复用的策略能力包”。

## 如何编写自定义策略（Strategy Skill）

只需创建一个 `.yaml` 文件，用中文（或任意语言）描述你的交易策略即可，**无需编写任何代码**。

### 最简模板

```yaml
name: my_strategy          # 唯一标识（英文，下划线连接）
display_name: 我的策略      # 显示名称（中文）
description: 简短描述策略用途

instructions: |
  你的策略描述...
  用自然语言写出判断标准、入场条件、出场条件等。
  可以引用工具名称（如 get_daily_history、analyze_trend）来指导 AI 使用哪些数据。
```

### 完整模板

```yaml
name: my_strategy
display_name: 我的策略
description: 简短描述策略适用的市场场景

# 策略分类：trend（趋势）、pattern（形态）、reversal（反转）、framework（框架）
category: trend

# 关联的核心交易理念编号（1-7），可选
core_rules: [1, 2]

# 策略需要使用的工具列表，可选
# 可用工具：get_daily_history, analyze_trend, get_realtime_quote,
#           get_sector_rankings, search_stock_news, get_stock_info
required_tools:
  - get_daily_history
  - analyze_trend

# 可选别名（用于 /ask 等自然语言技能选择）
aliases: [我的战法, 我的模型]

# 以下元数据用于驱动默认行为（可选）
# default_active: 是否属于默认激活技能集
# default_router: 是否属于路由 fallback 技能集
# default_priority: 默认展示/排序优先级，数值越小越靠前
# market_regimes: 该技能优先适配的市场状态标签
default_active: true
default_router: false
default_priority: 100
market_regimes: [trending_up]

# 策略详细说明（自然语言，支持 Markdown 格式）
instructions: |
  **我的策略名称**

  判断标准：

  1. **条件一**：
     - 使用 `analyze_trend` 检查均线排列。
     - 描述你期望看到的趋势特征...

  2. **条件二**：
     - 描述量能要求...

  评分调整：
  - 满足条件时建议的 sentiment_score 调整
  - 在 `buy_reason` 中注明策略名称
```

### 核心交易理念参考

| 编号 | 理念 |
|------|------|
| 1 | 严进策略：乖离率 < 5% 才考虑入场 |
| 2 | 趋势交易：MA5 > MA10 > MA20 多头排列 |
| 3 | 效率优先：量能确认趋势有效性 |
| 4 | 买点偏好：优先回踩均线支撑 |
| 5 | 风险排查：利空新闻一票否决 |
| 6 | 量价配合：成交量验证价格运动 |
| 7 | 强势趋势股放宽：龙头股可适当放宽标准 |

## 自定义策略目录

除了本目录（内置策略），你还可以通过环境变量指定额外的自定义策略目录：

```env
AGENT_SKILL_DIR=./my_skills
```

系统会同时加载内置策略和自定义策略。如果名称冲突，自定义策略覆盖内置策略。

环境变量名仍然是 `AGENT_SKILL_DIR`，这是内部统一命名后的配置入口；在产品语义上，它依然表示“自定义策略目录”。
