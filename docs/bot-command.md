# Bot Guide

DSA bots connect messaging platforms to analysis commands. For one-way report delivery, configure a notification channel instead; see [Notifications](notifications.md). Keep bot credentials and webhook secrets in `.env` or a secret manager, never in source control or screenshots.

## Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `/analyze` | Analyze a symbol | `/analyze 600519` |
| `/ask` | Ask a stock or market question | `/ask AAPL RSI` |
| `/batch` | Analyze the configured watchlist | `/batch` |
| `/chat` | Continue a multi-turn strategy conversation | `/chat` |
| `/market` | Request a market review | `/market` |
| `/help` | Show available commands | `/help` |
| `/status` | Inspect service readiness | `/status` |

Supported commands and symbol formats can vary by transport. Confirm the running adapter's help output and the repository's `.env.example`; do not assume every transport supports every command.

## Choose a Connection Mode

- **Notification Webhook**: simplest option when DSA only needs to send reports to a group. Configure the channel's notification URL and any required signature or keyword settings. See [Notifications](notifications.md).
- **Application or Stream Bot**: use when users need to send commands to DSA or when the platform integration requires a long-lived stream connection. Configure that platform's application credentials, receive target, and event/stream settings in `.env.example`.
- **HTTP callback**: requires a public HTTPS endpoint, valid platform signature checks, and a deployed route. Do not expose a callback without authentication or request verification.

Feishu group Webhooks are distinct from Feishu App Bot credentials. DingTalk Stream and platform-specific slash-command callbacks also have different setup flows. Use the platform's official documentation for creating the application and granting the minimum required permissions.

## Troubleshooting

1. Confirm the selected transport is implemented and enabled in the current deployment.
2. Check application ID/token, destination chat or channel ID, required scopes, and bot membership.
3. For Webhooks, verify the URL and any configured signature/keyword restrictions.
4. For inbound callbacks, verify public HTTPS reachability, platform verification settings, and request-signature validation.
5. Check backend logs for transport/API errors; use `/status` to inspect general runtime readiness.

For project setup and safe deployment, see the [User Guide](full-guide_EN.md) and [Chinese guide](GUIDE.md).