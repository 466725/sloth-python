"""Email-only notification contracts, configuration, and dispatch regression tests."""
# ruff: noqa: E402 -- The LiteLLM stub must be installed before application imports.

from dataclasses import fields
from unittest.mock import patch

import pytest

from tests.unit.llm.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

from ai_stock.config import Config
from ai_stock.core.config_manager import ConfigManager
from ai_stock.core.config_registry import build_schema_response, get_registered_field_keys
from ai_stock.report.notification import NotificationChannel, NotificationService
from ai_stock.report.notification_contracts import is_retired_notification_key
from ai_stock.services.system_config_service import ConfigValidationError, SystemConfigService

RETIRED_KEYS = (
    "WECHAT_WEBHOOK_URL",
    "FEISHU_APP_ID",
    "FEISHU_WEBHOOK_URL",
    "DINGTALK_APP_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "PUSHOVER_USER_KEY",
    "NTFY_URL",
    "GOTIFY_TOKEN",
    "PUSHPLUS_TOKEN",
    "SERVERCHAN3_SENDKEY",
    "CUSTOM_WEBHOOK_URLS",
    "WEBHOOK_VERIFY_SSL",
    "DISCORD_CHANNEL_ID",
    "SLACK_BOT_TOKEN",
    "ASTRBOT_URL",
    "BOT_ENABLED",
)


@pytest.fixture
def service(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "EMAIL_SENDER=sender@example.com\nEMAIL_PASSWORD=app-password\n"
        + "\n".join(f"{key}=old-value" for key in RETIRED_KEYS)
        + "\n",
        encoding="utf-8",
    )
    return SystemConfigService(manager=ConfigManager(env_path=env_path))


@pytest.mark.parametrize("include_schema", [True, False])
def test_config_values_do_not_resurrect_retired_keys(service, include_schema):
    with patch.dict("os.environ", {key: "runtime-value" for key in RETIRED_KEYS}):
        payload = service.get_config(include_schema=include_schema)
    keys = {item["key"] for item in payload["items"]}
    assert keys.isdisjoint(RETIRED_KEYS)
    assert {"EMAIL_SENDER", "EMAIL_PASSWORD", "EMAIL_RECEIVERS", "EMAIL_SENDER_NAME"} <= keys


def test_registry_and_schema_contain_no_retired_channels():
    keys = get_registered_field_keys()
    assert not any(is_retired_notification_key(key) for key in keys)
    assert not any(is_retired_notification_key(field.name) for field in fields(Config))
    schema = build_schema_response()
    notification = next(c for c in schema["categories"] if c["category"] == "notification")
    assert not any(is_retired_notification_key(f["key"]) for f in notification["fields"])
    for field in notification["fields"]:
        if field["key"].endswith("_CHANNELS"):
            assert field["validation"]["allowed_values"] == ["email"]


@pytest.mark.parametrize("key", RETIRED_KEYS)
def test_retired_settings_are_rejected_without_persistence(service, key):
    version = service._manager.get_config_version()
    result = service.validate([{"key": key, "value": "new-value"}])
    assert not result["valid"]
    assert result["issues"][0]["code"] == "unsupported_notification_setting"
    with pytest.raises(ConfigValidationError):
        service.update(version, [{"key": key, "value": "new-value"}], reload_now=False)
    with pytest.raises(ConfigValidationError):
        service.import_env(config_version=version, content=f"{key}=new-value", reload_now=False)
    assert service._manager.get_config_version() == version


@pytest.mark.parametrize(
    "key",
    [
        "NOTIFICATION_REPORT_CHANNELS",
        "NOTIFICATION_ALERT_CHANNELS",
        "NOTIFICATION_SYSTEM_ERROR_CHANNELS",
        "MARKDOWN_TO_IMAGE_CHANNELS",
    ],
)
def test_route_and_image_settings_accept_only_email(service, key):
    assert service.validate([{"key": key, "value": "email"}])["valid"]
    assert service.validate([{"key": key, "value": ""}])["valid"]
    assert not service.validate([{"key": key, "value": "telegram,email"}])["valid"]


def test_old_environment_settings_are_ignored_and_warn_without_values(caplog):
    with (
        patch("ai_stock.config.setup_env"),
        patch.dict(
            "os.environ",
            {
                "TELEGRAM_BOT_TOKEN": "private-token",
                "DISCORD_CHANNEL_ID": "private-channel",
                "MARKDOWN_TO_IMAGE_CHANNELS": "telegram,email",
                "EMAIL_SENDER": "sender@example.com",
                "EMAIL_PASSWORD": "app-password",
            },
            clear=True,
        ),
    ):
        config = Config._load_from_env()
    assert NotificationService.detect_configured_channels(config) == [NotificationChannel.EMAIL]
    assert config.markdown_to_image_channels == ["email"]
    assert not hasattr(config, "telegram_bot_token")
    assert "TELEGRAM_BOT_TOKEN" in caplog.text
    assert "private-token" not in caplog.text
    assert "private-channel" not in caplog.text


def test_email_send_keeps_recipient_groups():
    config = Config(
        email_sender="sender@example.com",
        email_password="app-password",
        stock_email_groups=[(["600519"], ["group@example.com"])],
    )
    with patch("ai_stock.report.notification.get_config", return_value=config):
        notifier = NotificationService()
    with patch.object(notifier, "send_to_email", return_value=True) as send:
        result = notifier.send_with_results(
            "report", email_stock_codes=["600519"], route_type="report"
        )
    assert result.success
    assert [attempt.channel for attempt in result.channel_results] == ["email"]
    send.assert_called_once_with("report", receivers=["group@example.com"])


def test_email_failure_is_reported():
    config = Config(email_sender="sender@example.com", email_password="app-password")
    with patch("ai_stock.report.notification.get_config", return_value=config):
        notifier = NotificationService()
    with patch.object(notifier, "send_to_email", side_effect=RuntimeError("SMTP unavailable")):
        result = notifier.send_with_results("report")
    assert not result.success
    assert result.status == "all_failed"
    assert result.channel_results[0].channel == "email"


def test_no_email_credentials_do_not_enable_another_transport():
    assert NotificationService.detect_configured_channels(Config()) == []
    assert {channel.value for channel in NotificationChannel} == {"email", "unknown"}
