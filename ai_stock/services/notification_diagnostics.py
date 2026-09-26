# -*- coding: utf-8 -*-
"""Read-only notification configuration diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional, Sequence, Tuple

from ai_stock.config import Config
from ai_stock.report.notification import ChannelDetector, NotificationChannel, NotificationService
from ai_stock.report.notification_noise import (
    NOTIFICATION_SEVERITIES,
    P4_NOISE_ENV_KEYS,
    is_supported_notification_severity,
    parse_notification_quiet_hours,
    validate_notification_timezone,
)
from ai_stock.report.notification_routing import (
    NOTIFICATION_ROUTE_CONFIGS,
    ROUTABLE_NOTIFICATION_CHANNELS,
    split_notification_route_channels,
)

KeyTier = Literal["minimal", "advanced"]
IssueSeverity = Literal["error", "warning", "info"]
ChannelKind = Literal["configured", "fallback", "context"]


@dataclass(frozen=True)
class NotificationKeySpec:
    """Metadata for a notification-related configuration key."""

    key: str
    tier: KeyTier
    description: str
    channel: str


@dataclass(frozen=True)
class NotificationChannelSpec:
    """Baseline metadata for one notification channel."""

    channel: str
    display_name: str
    kind: ChannelKind
    minimal_keys: Tuple[str, ...]
    alternative_minimal_keys: Tuple[Tuple[str, ...], ...] = ()
    advanced_keys: Tuple[str, ...] = ()
    note: str = ""


@dataclass(frozen=True)
class NotificationDiagnosticIssue:
    """One diagnostic message."""

    severity: IssueSeverity
    code: str
    message: str
    key: Optional[str] = None


@dataclass(frozen=True)
class NotificationDiagnosticResult:
    """Structured notification diagnostic result."""

    configured_channels: Tuple[str, ...]
    errors: Tuple[NotificationDiagnosticIssue, ...]
    warnings: Tuple[NotificationDiagnosticIssue, ...]
    info: Tuple[NotificationDiagnosticIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


CHANNEL_SPECS: Tuple[NotificationChannelSpec, ...] = (
    NotificationChannelSpec(
        channel=NotificationChannel.EMAIL.value,
        display_name=ChannelDetector.get_channel_name(NotificationChannel.EMAIL),
        kind="configured",
        minimal_keys=("EMAIL_SENDER", "EMAIL_PASSWORD"),
        advanced_keys=("EMAIL_RECEIVERS", "EMAIL_SENDER_NAME"),
    ),
)

KEY_SPECS: Tuple[NotificationKeySpec, ...] = tuple(
    NotificationKeySpec(key=key, tier="minimal", description="Required to enable the channel.", channel=spec.channel)
    for spec in CHANNEL_SPECS
    for key in (
        spec.minimal_keys
        + tuple(key for key_group in spec.alternative_minimal_keys for key in key_group)
    )
) + tuple(
    NotificationKeySpec(key=key, tier="advanced", description="Optional channel behavior or security setting.", channel=spec.channel)
    for spec in CHANNEL_SPECS
    for key in spec.advanced_keys
) + tuple(
    NotificationKeySpec(
        key=route["env_key"],
        tier="advanced",
        description=route["description"],
        channel="routing",
    )
    for route in NOTIFICATION_ROUTE_CONFIGS.values()
) + tuple(
    NotificationKeySpec(
        key=key,
        tier="advanced",
        description="Optional notification noise-control setting.",
        channel="noise",
    )
    for key in P4_NOISE_ENV_KEYS
)

P0_ACTIONS_ENV_KEYS: Tuple[str, ...] = ()

P3_ROUTE_ENV_KEYS: Tuple[str, ...] = tuple(
    route["env_key"] for route in NOTIFICATION_ROUTE_CONFIGS.values()
)

P4_NOISE_ACTIONS_ENV_KEYS: Tuple[str, ...] = P4_NOISE_ENV_KEYS

P6_CHANNEL_ACTIONS_ENV_KEYS: Tuple[str, ...] = ()


def _value(config: Config, attr: str):
    return getattr(config, attr, None)


def _has(config: Config, attr: str) -> bool:
    value = _value(config, attr)
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return value is not None and str(value).strip() != ""


def _issue(
    severity: IssueSeverity,
    code: str,
    message: str,
    key: Optional[str] = None,
) -> NotificationDiagnosticIssue:
    return NotificationDiagnosticIssue(severity=severity, code=code, message=message, key=key)


def _require_pair(
    config: Config,
    *,
    left_attr: str,
    right_attr: str,
    left_key: str,
    right_key: str,
    channel_name: str,
    errors: List[NotificationDiagnosticIssue],
    warnings: Optional[List[NotificationDiagnosticIssue]] = None,
    severity: IssueSeverity = "error",
) -> None:
    left = _has(config, left_attr)
    right = _has(config, right_attr)
    target = errors if severity == "error" else warnings
    if target is None:
        target = errors
    if left and not right:
        target.append(
            _issue(
                severity,
                "partial_channel_config",
                f"{channel_name} 已配置 {left_key}，但缺少 {right_key}，该渠道不会启用。",
                key=right_key,
            )
        )
    if right and not left:
        target.append(
            _issue(
                severity,
                "partial_channel_config",
                f"{channel_name} 已配置 {right_key}，但缺少 {left_key}，该渠道不会启用。",
                key=left_key,
            )
        )


def run_notification_diagnostics(config: Config) -> NotificationDiagnosticResult:
    """Run read-only diagnostics for notification configuration."""

    configured = tuple(channel.value for channel in NotificationService.detect_configured_channels(config))
    errors: List[NotificationDiagnosticIssue] = []
    warnings: List[NotificationDiagnosticIssue] = []
    info: List[NotificationDiagnosticIssue] = [
        _issue(
            "info",
            "context_channels_runtime_only",
            "通知仅支持邮件发送。",
        ),
        _issue(
            "info",
            "phase_scope",
            "通知诊断会检查邮件配置、路由配置和降噪配置。",
        ),
    ]

    if not configured:
        errors.append(
            _issue(
                "error",
                "no_channels_configured",
                "邮件通知未配置；请设置 EMAIL_SENDER 和 EMAIL_PASSWORD。",
            )
        )

    _require_pair(
        config,
        left_attr="email_sender",
        right_attr="email_password",
        left_key="EMAIL_SENDER",
        right_key="EMAIL_PASSWORD",
        channel_name="邮件",
        errors=errors,
    )

    configured_set = set(configured)
    for route_type, route_config in NOTIFICATION_ROUTE_CONFIGS.items():
        route_channels = getattr(config, route_config["config_attr"], []) or []
        if not route_channels:
            continue

        valid_channels, invalid_channels = split_notification_route_channels(route_channels)
        if invalid_channels:
            errors.append(
                _issue(
                    "error",
                    "invalid_route_channel",
                    (
                        f"{route_config['env_key']} 包含未知通知渠道: {', '.join(invalid_channels)}；"
                        f"允许值: {', '.join(ROUTABLE_NOTIFICATION_CHANNELS)}。"
                    ),
                    key=route_config["env_key"],
                )
            )

        disabled_channels = [channel for channel in valid_channels if channel not in configured_set]
        if disabled_channels:
            warnings.append(
                _issue(
                    "warning",
                    "route_channel_not_configured",
                    (
                        f"{route_config['env_key']} 路由 {route_type} 指向未启用渠道: "
                        f"{', '.join(disabled_channels)}；这些渠道不会收到该类型通知。"
                    ),
                    key=route_config["env_key"],
                )
            )

    if getattr(config, "notification_quiet_hours", ""):
        try:
            parse_notification_quiet_hours(config.notification_quiet_hours)
        except ValueError as exc:
            errors.append(
                _issue(
                    "error",
                    "invalid_quiet_hours",
                    f"NOTIFICATION_QUIET_HOURS 配置无效: {exc}",
                    key="NOTIFICATION_QUIET_HOURS",
                )
            )

    if getattr(config, "notification_timezone", ""):
        try:
            validate_notification_timezone(config.notification_timezone)
        except ValueError as exc:
            errors.append(
                _issue(
                    "error",
                    "invalid_notification_timezone",
                    f"NOTIFICATION_TIMEZONE 配置无效: {exc}",
                    key="NOTIFICATION_TIMEZONE",
                )
            )

    min_severity = getattr(config, "notification_min_severity", "") or ""
    if min_severity and not is_supported_notification_severity(min_severity):
        errors.append(
            _issue(
                "error",
                "invalid_notification_min_severity",
                (
                    "NOTIFICATION_MIN_SEVERITY 配置无效；"
                    f"允许值: {', '.join(NOTIFICATION_SEVERITIES)}。"
                ),
                key="NOTIFICATION_MIN_SEVERITY",
            )
        )

    if getattr(config, "notification_daily_digest_enabled", False):
        warnings.append(
            _issue(
                "warning",
                "reserved_daily_digest",
                (
                    "NOTIFICATION_DAILY_DIGEST_ENABLED 当前为预留配置；"
                    "P4 不会发送每日摘要或持久化摘要内容。"
                ),
                key="NOTIFICATION_DAILY_DIGEST_ENABLED",
            )
        )

    return NotificationDiagnosticResult(
        configured_channels=configured,
        errors=tuple(errors),
        warnings=tuple(warnings),
        info=tuple(info),
    )


def _format_issues(title: str, issues: Sequence[NotificationDiagnosticIssue]) -> List[str]:
    if not issues:
        return [f"{title}: 无"]
    lines = [f"{title}:"]
    for item in issues:
        key_suffix = f" [{item.key}]" if item.key else ""
        lines.append(f"- {item.code}{key_suffix}: {item.message}")
    return lines


def format_notification_diagnostics(result: NotificationDiagnosticResult) -> str:
    """Format diagnostics for CLI output without exposing secret values."""

    lines = [
        "通知配置诊断",
        f"已配置渠道: {len(result.configured_channels)} 个",
    ]
    if result.configured_channels:
        channel_names = [
            ChannelDetector.get_channel_name(NotificationChannel(channel))
            for channel in result.configured_channels
        ]
        lines.append("渠道列表: " + ", ".join(channel_names))
    else:
        lines.append("渠道列表: (无)")

    lines.append("")
    lines.extend(_format_issues("Errors", result.errors))
    lines.append("")
    lines.extend(_format_issues("Warnings", result.warnings))
    lines.append("")
    lines.extend(_format_issues("Info", result.info))
    return "\n".join(lines)
