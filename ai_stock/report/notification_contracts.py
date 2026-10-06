"""Configuration policy for the email-only notification transport."""

from __future__ import annotations

RETIRED_NOTIFICATION_KEY_PREFIXES = (
    "WECHAT_",
    "WECOM_",
    "FEISHU_",
    "DINGTALK_",
    "TELEGRAM_",
    "DISCORD_",
    "SLACK_",
    "PUSHOVER_",
    "NTFY_",
    "GOTIFY_",
    "PUSHPLUS_",
    "SERVERCHAN",
    "ASTRBOT_",
    "CUSTOM_WEBHOOK_",
    "BOT_",
)


def is_retired_notification_key(key: str) -> bool:
    """Identify obsolete channel settings, including legacy unregistered keys."""
    normalized = key.upper()
    return (
        normalized.startswith(RETIRED_NOTIFICATION_KEY_PREFIXES)
        or normalized in {"WEBHOOK_VERIFY_SSL", "AGENT_NL_ROUTING"}
    )
