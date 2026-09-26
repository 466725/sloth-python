import pytest

import ai_stock.report as notification_sender
from ai_stock.report.notification_capabilities import (
    CHANNEL_PROFILES,
    CHANNEL_RENDERER_PRESETS,
)
from ai_stock.report.notification_routing import (
    ROUTABLE_NOTIFICATION_CHANNELS,
    split_notification_route_channels,
)


@pytest.mark.unit
def test_email_is_the_only_exported_sender():
    assert report.__all__ == ["EmailSender"]
    assert report.EmailSender is not None
    assert not hasattr(report, "TelegramSender")
    assert not hasattr(report, "WechatSender")


@pytest.mark.unit
def test_email_is_the_only_routable_notification_channel():
    assert ROUTABLE_NOTIFICATION_CHANNELS == ("email",)
    assert split_notification_route_channels(["email", "telegram"]) == (
        ["email"],
        ["telegram"],
    )


@pytest.mark.unit
def test_email_is_the_only_notification_capability_and_renderer():
    assert set(CHANNEL_PROFILES) == {"email", "unknown"}
    assert set(CHANNEL_RENDERER_PRESETS) == {"email"}