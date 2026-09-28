# 使用指南

本文是 DSA 的中文主指南，汇总安装、配置、运行方式和主要能力。精确配置项以项目根目录 `.env.example` 与 Web 设置页当前可见字段为准，API 契约以 `/docs` 和 `architecture/api_spec.json` 为准。

## 1. 项目做什么

DSA 会读取自选股与市场数据，结合技术指标、新闻和大模型生成分析报告，并可将结果保存到历史记录或通过通知渠道发送。Web 界面还提供问股、回测、持仓、告警和 AI 建议信号等工作流。

市场能力并不完全相同：A 股、港股和美股覆盖最广；日股使用 `.T` 后缀，韩国 KOSPI 使用 `.KS`、KOSDAQ 使用 `.KQ`。日韩目前只走 YFinance 日线、基础/延迟行情和技术指标路径，不保证实时行情、完整基本面、全市场股票列表、资金流、龙虎榜、板块或大盘复盘；Portfolio 的 JPY/KRW 汇率与估值也不完整。不要把缺失数据解读为零值或利好/利空结论。

## 2. 首次运行

需要 Python 3.10 或更高版本。推荐先创建虚拟环境，再安装依赖并复制配置模板：

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

在 `.env` 中至少配置一个可用的大模型渠道和 `STOCK_LIST`。通知渠道、新闻搜索和额外行情源均可选；未配置时系统会使用可用的数据源与降级路径。不要把真实密钥提交到 Git、Issue、日志或截图中。

常见首次排查：确认 `.env` 位于仓库根目录、变量名拼写正确、模型名和渠道匹配，并查看 `logs/` 中的后端日志。Web 设置页可用于检查和维护受支持的运行时配置。

## 3. 运行模式

| 目标 | 命令 | 说明 |
| --- | --- | --- |
| 单次分析 | `python main.py` | 分析自选股并按配置发送报告 |
| 定时运行 | `python main.py --schedule` | 在当前进程中运行调度器 |
| 只启动 Web/API | `python main.py --serve-only` | 启动服务，不额外执行一次分析 |
| 启动服务并分析 | `python main.py --serve` | 启动 Web/API 并执行一次分析 |
| 本地 Web 启动器 | `python webui.py` | 直接启动 FastAPI 服务 |
| FastAPI 开发模式 | `uvicorn server:app --reload --host 127.0.0.1 --port 8000` | 适合本机开发；生产环境不要开启 reload |

本机默认访问 `http://127.0.0.1:8000`，API 文档位于 `/docs`。云服务器需将服务绑定到容器或主机可访问的地址，并配置管理员认证、防火墙和 HTTPS 反向代理；不要在无保护的情况下直接公开管理接口。

Docker Compose 提供不同用途的服务：

```bash
# Web/API 服务
docker compose -f docker/docker-compose.yml up -d server
# 定时分析服务
docker compose -f docker/docker-compose.yml up -d analyzer
```

容器内监听地址需要是 `0.0.0.0`；Compose 将服务端口映射到宿主机。数据库、日志和报告通过数据卷持久化。Compose 的 `env_file` 是启动环境变量，不等于容器内可写的 `.env`；若要通过 Web 保存配置并在容器重建后保留，需使用持久化的 `ENV_FILE`。详细说明见 [云服务器 Web 访问](deploy-webui-cloud.md)，桌面端构建见 [桌面端打包说明](desktop-package.md)。

## 4. 大模型、搜索与数据源

- **大模型**：简单场景从一个模型和 API Key 开始。多渠道、主备模型、Agent 专属模型或 LiteLLM YAML 属于进阶配置，参考 [服务商配置摘要](llm-providers.md)。
- **搜索与资讯**：配置新闻搜索源后，分析可补充近期新闻、公告和事件背景；本地 RSS/Atom/NewsNow 资讯池也可作为 best-effort evidence。搜索不可用时检查服务商 Key、网络与配额；单个资讯源失败不应阻断主分析。
- **行情数据**：多个数据源按可用性回退。单一源超时或缺字段不应被当成有效的零值；检查日志中的来源、超时和降级提示。
- **自选股列表**：使用逗号分隔代码；不同市场的代码格式见 `.env.example` 和市场能力说明。Tushare 股票列表工具见 [Tushare 指南](TUSHARE_STOCK_LIST_GUIDE.md)。

## 5. 主要工作流

- **分析报告**：从 Web 首页、CLI、API 或 Bot 提交标的；查看结论、风险、数据来源与报告历史。报告是研究辅助，不是投资建议。
- **大盘复盘**：可从 CLI、Web 或定时任务触发；它与单只股票分析使用不同的市场上下文。
- **问股 Agent**：围绕标的进行多轮问答；模型或搜索源不可用时，回答能力会相应降级。
- **回测与持仓**：回测用于历史规则评估；持仓页汇总账户快照和风险信息。结果受行情覆盖、交易日和数据质量影响。
- **AI 建议信号**：结构化整理报告中的行动倾向、依据、风险和后续观察条件，可查询、反馈并查看日线后验评估；信号不是自动交易或调仓指令。
- **实时告警**：按规则评估行情或组合条件，并记录触发、跳过和通知状态。配置与运行边界见 [告警专题](alerts.md)。
- **通知与 Bot**：可用通知渠道、路由及诊断见 [通知专题](notifications.md)；Bot 使用方式见 [Bot 命令指南](bot-command_EN.md)。
- **智能导入**：图片导入依赖已配置的视觉模型；识别结果应人工复核，尤其是相似代码和市场后缀。

## 6. 配置与能力专题

以下专题页保留为设置界面和维护流程的稳定入口，避免在多个长指南里复制同一份配置说明：

- [LLM 服务商与错误诊断](llm-providers.md)
- [通知渠道与 GitHub Actions 环境变量](notifications.md)
- [云服务器 Web 访问](deploy-webui-cloud.md)
- [AnalysisContextPack 数据质量与可见性](analysis-context-pack.md)
- [实时告警规则](alerts.md)
- [Tushare 股票列表工具](TUSHARE_STOCK_LIST_GUIDE.md)
- [通知渠道与投递诊断](notifications.md)

## 7. 故障排查

1. **服务未启动**：确认端口未被占用，检查 `API_PORT` / `WEBUI_PORT` 与启动日志。
2. **Web 可打开但 API 失败**：访问 `/health` 或 `/api/health`，再查看 `/docs` 是否可用。
3. **模型调用失败**：检查所选渠道、模型名、Key、Base URL、配额和网络；多渠道配置可先用 Web 设置页的连通性测试。
4. **报告缺少数据**：检查具体数据源的警告和回退记录；部分市场或字段可能本来就不支持。
5. **定时或通知未执行**：确认启动的是调度模式、交易日/时间条件满足、通知渠道启用，并查看发送状态。

机器人命令与可用接入方式见 [Bot 指南](bot-command_EN.md)。图片识别使用视觉模型；提交图片后请人工核对代码、名称与市场后缀。

发布变化见 [更新日志](CHANGELOG.md)。API 字段以服务端 OpenAPI 为准，不要依赖旧截图或历史版本中的参数。
