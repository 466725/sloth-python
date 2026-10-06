# Documentation Index (English)

Start with the [project README](README_EN.md) for an overview, or use the [User Guide](full-guide_EN.md) for setup, configuration, run modes, deployment, and feature boundaries.

## Common Tasks

| I want to… | Read |
| --- | --- |
| Install and run DSA | [User Guide](full-guide_EN.md) |
| Configure an LLM provider | [Model Configuration](full-guide_EN.md#model-configuration), [provider notes](llm-providers.md) |
| Configure notifications or troubleshoot delivery | [Notification guide](notifications.md) |
| Deploy Web/API to a cloud server | [User Guide](full-guide_EN.md#docker-deployment), [cloud access notes](deploy-webui-cloud.md) |
| Understand supported markets | [User Guide](full-guide_EN.md#what-dsa-does) |
| Contribute | [Contributing guide](CONTRIBUTING_EN.md) |

## Maintained References

The website uses the analysis, Agent chat, and alert APIs directly. External
messaging bot integrations are not supported; notifications are email-only.
Historical reports and conversations remain available after removal. Restart
or redeploy the backend to apply this change. To restore the old integrations,
restore the bot package, its backend hooks, and dependencies together from the
previous revision.

- [Price change alerts](alerts.md) (English)
- [AnalysisContextPack quality and visibility](analysis-context-pack.md) (English)
- [Tushare stock-list tool](TUSHARE_STOCK_LIST_GUIDE.md) (Chinese)
- [API specification](api_spec.json)
- [Changelog](CHANGELOG.md)

The `guide.md` file is the corresponding concise Chinese user guide. Configuration keys and defaults should be checked against the repository's `.env.example` and current Web settings; API details should be checked against `/docs` or the API specification.
