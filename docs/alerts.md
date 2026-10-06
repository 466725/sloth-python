# 实时告警中心

告警中心仅支持 **涨跌幅（Price change）**。规则使用实时行情中的涨跌幅百分比，
不是固定价格，也不是相对于上一次轮询的价格变化。

## 创建规则

在 Web 的 Alerts 页面填写名称、目标范围、方向、百分比阈值和严重程度。
规则类型固定为 Price change。

| 字段 | 支持值与语义 |
| --- | --- |
| `alert_type` | 仅 `price_change_percent` |
| `target_scope` | `single_symbol` 或 `watchlist` |
| `target` | 单标的股票代码；自选股固定为 `default` |
| `parameters.direction` | `up` 或 `down` |
| `parameters.change_pct` | 有限且大于零的百分比数值；例如 `3` 表示 3% |
| `severity` | `info`、`warning`、`critical` |
| `enabled` | 是否启用后台评估 |

上涨规则在实时涨跌幅 **大于等于** 正阈值时触发；下跌规则在实时涨跌幅
**小于等于** 负阈值时触发。下跌方向的阈值仍填写正数。
缺少行情或有效涨跌幅时不触发，记录 `skipped`；数据源异常记录 `failed`，
诊断内容会脱敏。一次规则失败不会阻止其他规则。

### API 示例

`POST /api/v1/alerts/rules`：

```json
{
  "name": "Daily decline",
  "target_scope": "single_symbol",
  "target": "600519",
  "alert_type": "price_change_percent",
  "parameters": {"direction": "down", "change_pct": 3},
  "severity": "warning",
  "enabled": true
}
```

自选股规则使用 `target_scope=watchlist`、`target=default`，评估时读取最新
`STOCK_LIST`，去重并最多展开 100 个标的。每个标的独立记录触发历史与冷却状态。
空自选股会记录跳过原因。一次性测试有单标的和总时限，并限制返回的明细数量。

## 运行与邮件通知

配置入口：

```dotenv
AGENT_EVENT_MONITOR_ENABLED=true
AGENT_EVENT_MONITOR_INTERVAL_MINUTES=5
AGENT_EVENT_ALERT_RULES_JSON=
```

在 schedule 模式启动应用后，后台 worker 周期性加载已启用的持久化规则。
无需重启即可评估随后通过 Web/API 创建的规则。
通知仅使用邮件，遵守 `NOTIFICATION_ALERT_CHANNELS` 路由和通知网关的噪声控制。
详见 [邮件通知指南](notifications.md)。

数据库规则默认冷却 24 小时；`cooldown_policy.cooldown_seconds` 可覆盖冷却秒数，
`0` 表示不做规则冷却。只有真实邮件发送成功才开始冷却；
发送失败、没有可用渠道或网关抑制不会开始新的冷却窗口。
通知尝试记录渠道、成功状态、错误码与脱敏诊断。

### Legacy JSON

`AGENT_EVENT_ALERT_RULES_JSON` 继续支持单标的涨跌幅规则：

```dotenv
AGENT_EVENT_ALERT_RULES_JSON=[{"stock_code":"600519","alert_type":"price_change_percent","direction":"up","change_pct":3}]
```

Legacy JSON 不支持自选股展开。Web/System 配置保存会严格校验；
运行时跳过无效条目并记录警告，剩余有效规则继续运行。
数据库规则与 legacy JSON 具有相同目标和参数时，数据库规则优先。
Legacy 规则使用进程内 fingerprint 防止重复通知，不提供跨重启持久化冷却。
应用不会改写用户已有环境文件。

## API 与数据记录

| 操作 | 接口 |
| --- | --- |
| 创建 / 列出规则 | `POST /api/v1/alerts/rules` / `GET /api/v1/alerts/rules` |
| 获取 / 更新 / 删除 | `GET` / `PATCH` / `DELETE /api/v1/alerts/rules/{rule_id}` |
| 启用 / 禁用 | `POST /api/v1/alerts/rules/{rule_id}/enable` 或 `/disable` |
| 一次性测试 | `POST /api/v1/alerts/rules/{rule_id}/test` |
| 触发历史 | `GET /api/v1/alerts/triggers` |
| 通知尝试 | `GET /api/v1/alerts/notifications` |

测试接口只评估，不发送邮件，不写入真实触发历史或通知尝试。
规则列表支持状态、目标、来源与分页筛选。
创建、更新或按其他规则类型/目标范围查询会被拒绝。

持久化表仍为 `alert_rules`、`alert_triggers`、`alert_notifications`、
`alert_cooldowns`。触发记录保存观察值、阈值、原因、数据源、数据时间和状态；
不伪造缺失的数据时间。股票告警保留分析阶段摘要、上下文包概览和 AI 信号关联，
不提供新的 AI 自动交易行为。

## 已有数据清理与部署

按照本次移除策略，初始化告警 repository（首次告警 API 访问或创建后台 worker）
时，会在一个事务内**永久删除所有非涨跌幅规则及其关联触发历史、通知尝试和冷却记录**。
重复初始化是幂等的。涨跌幅规则及其数据不受影响；没有规则关联的 legacy 历史不做猜测删除。
私有 `.env` 中的旧规则不会自动删除，但会被拒绝或跳过，应手动清理。

部署时重启后端并更新 Web/桌面所用的前端资源。正在运行的旧进程不会自动加载新代码。
如果需要回滚，请在首次启动新版前备份数据库和私有配置；
恢复旧代码与前端资源只能恢复功能，**无法恢复已删除的数据**，需要数据库备份。
本页同时说明中英文 UI 的相同运行契约；仓库没有单独的英文告警指南。
