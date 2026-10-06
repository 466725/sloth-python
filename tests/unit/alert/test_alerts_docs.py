"""Documentation contract for the price-change-only alert center."""

from pathlib import Path

DOC = Path(__file__).resolve().parents[3] / "docs" / "alerts.md"


def test_alert_guide_only_documents_price_change_rules():
    text = DOC.read_text(encoding="utf-8")
    assert "price_change_percent" in text
    assert "single_symbol" in text
    assert "watchlist" in text
    for retired in (
        "price_cross",
        "volume_spike",
        "ma_price_cross",
        "rsi_threshold",
        "macd_cross",
        "kdj_cross",
        "cci_threshold",
        "market_light_status",
        "market_light_score_drop",
    ):
        assert retired not in text


def test_alert_guide_documents_delivery_cleanup_and_rollback():
    text = DOC.read_text(encoding="utf-8")
    for required in (
        "AGENT_EVENT_ALERT_RULES_JSON",
        "AGENT_EVENT_MONITOR_ENABLED",
        "NOTIFICATION_ALERT_CHANNELS",
        "cooldown_policy.cooldown_seconds",
        "alert_rules",
        "alert_triggers",
        "alert_notifications",
        "alert_cooldowns",
        "/api/v1/alerts/rules/{rule_id}/test",
        "permanently deletes rules",
        "database backup",
    ):
        assert required in text
