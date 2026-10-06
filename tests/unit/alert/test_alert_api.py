# -*- coding: utf-8 -*-
"""Integration tests for Alert API MVP (Issue #1202 P1)."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

try:
    import litellm  # noqa: F401
except ModuleNotFoundError:
    sys.modules["litellm"] = MagicMock()

import ai_stock.auth as auth
from ai_stock.config import Config
from ai_stock.repositories.alert_repo import AlertRepository
from ai_stock.services.alert_service import AlertService
from ai_stock.storage import (
    AlertCooldownRecord,
    AlertNotificationRecord,
    AlertRuleRecord,
    AlertTriggerRecord,
    Base,
    DatabaseManager,
)
from api.app import create_app


def _reset_auth_globals() -> None:
    auth._auth_enabled = None
    auth._session_secret = None
    auth._password_hash_salt = None
    auth._password_hash_stored = None
    auth._rate_limit = {}


class AlertApiTestCase(unittest.TestCase):
    """Alert API contract tests for P1 rule and history endpoints."""

    def setUp(self) -> None:
        _reset_auth_globals()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)
        self.env_path = self.data_dir / ".env"
        self.db_path = self.data_dir / "alert_api_test.db"
        self.env_path.write_text(
            "\n".join(
                [
                    "STOCK_LIST=600519",
                    "GEMINI_API_KEY=test",
                    "ADMIN_AUTH_ENABLED=false",
                    'AGENT_EVENT_ALERT_RULES_JSON=[{"stock_code":"000001","alert_type":"price_change_percent","direction":"up","change_pct":10}]',
                    f"DATABASE_PATH={self.db_path}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        os.environ["ENV_FILE"] = str(self.env_path)
        os.environ["DATABASE_PATH"] = str(self.db_path)
        Config.reset_instance()
        DatabaseManager.reset_instance()
        app = create_app(static_dir=self.data_dir / "empty-static")
        self.client = TestClient(app)
        self.db = DatabaseManager.get_instance()

    def tearDown(self) -> None:
        DatabaseManager.reset_instance()
        Config.reset_instance()
        os.environ.pop("ENV_FILE", None)
        os.environ.pop("DATABASE_PATH", None)
        self.temp_dir.cleanup()
        _reset_auth_globals()

    def _create_rule(self, payload: dict | None = None) -> dict:
        body = {
            "name": "Moutai price change",
            "target_scope": "single_symbol",
            "target": "600519",
            "alert_type": "price_change_percent",
            "parameters": {"direction": "up", "change_pct": 1800},
            "severity": "warning",
            "enabled": True,
        }
        if payload:
            body.update(payload)
        resp = self.client.post("/api/v1/alerts/rules", json=body)
        self.assertEqual(resp.status_code, 200, resp.text)
        return resp.json()

    def test_only_price_change_is_accepted_by_create_update_and_filters(self) -> None:
        rule = self._create_rule()
        for retired in (
            "price_cross", "volume_spike", "ma_price_cross", "rsi_threshold",
            "macd_cross", "kdj_cross", "cci_threshold", "market_light_status",
            "market_light_score_drop", "sentiment_shift", "risk_flag", "custom",
        ):
            with self.subTest(alert_type=retired):
                body = {
                    "target": "600519", "alert_type": retired,
                    "parameters": {"direction": "up", "change_pct": 3},
                }
                self.assertEqual(self.client.post("/api/v1/alerts/rules", json=body).status_code, 422)
                self.assertEqual(self.client.patch(
                    f"/api/v1/alerts/rules/{rule['id']}", json={"alert_type": retired},
                ).status_code, 422)
                self.assertEqual(self.client.get(
                    "/api/v1/alerts/rules", params={"alert_type": retired},
                ).status_code, 422)
        self.assertEqual(self.client.get("/api/v1/alerts/rules").json()["total"], 1)
        self.assertEqual(self.client.post("/api/v1/alerts/rules", json={
            "target_scope": "market", "target": "cn", "alert_type": "price_change_percent",
            "parameters": {"direction": "up", "change_pct": 3},
        }).status_code, 422)

    def test_retired_rule_cleanup_is_idempotent_and_preserves_price_change_history(self) -> None:
        retained = self._create_rule()
        repo = AlertRepository(self.db)
        retired_types = (
            "price_cross", "volume_spike", "ma_price_cross", "rsi_threshold",
            "macd_cross", "kdj_cross", "cci_threshold", "market_light_status",
            "market_light_score_drop",
        )
        retired_ids = []
        for alert_type in retired_types:
            row = repo.create_rule({
                "name": "Retired rule", "target_scope": "single_symbol", "target": "600519",
                "alert_type": alert_type, "parameters": "{}", "enabled": False,
            })
            retired_ids.append(row.id)
        for rule_id in [retained["id"], *retired_ids]:
            trigger = repo.create_trigger({
                "rule_id": rule_id, "target": "600519", "status": "triggered",
            })
            repo.record_notification_attempt({
                "trigger_id": trigger.id, "channel": "email", "success": True,
            })
            repo.upsert_cooldown(
                rule_id=rule_id, rule_key=str(rule_id), target="600519", severity="warning",
                last_triggered_at=datetime.now(),
                cooldown_until=datetime.now() + timedelta(hours=1),
                reason="test",
            )

        with self.assertLogs("ai_stock.repositories.alert_repo", level="WARNING"):
            cleaned_repo = AlertRepository(self.db)
        self.assertEqual(cleaned_repo.delete_retired_rules(), 0)
        with self.db.get_session() as session:
            self.assertEqual([row.id for row in session.query(AlertRuleRecord).all()], [retained["id"]])
            triggers = session.query(AlertTriggerRecord).all()
            self.assertEqual([row.rule_id for row in triggers], [retained["id"]])
            self.assertEqual(
                [row.trigger_id for row in session.query(AlertNotificationRecord).all()],
                [triggers[0].id],
            )
            self.assertEqual(
                [row.rule_id for row in session.query(AlertCooldownRecord).all()],
                [retained["id"]],
            )

    def test_price_change_threshold_rejects_nonfinite_or_nonpositive_values(self) -> None:
        service = AlertService(self.db)
        for value in (0, -3, "nan", "inf", "-inf", None):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "change_pct"):
                service.create_rule({
                    "target": "600519", "alert_type": "price_change_percent",
                    "parameters": {"direction": "up", "change_pct": value},
                })

    def test_retired_cleanup_rolls_back_all_deletions_on_error(self) -> None:
        repo = AlertRepository(self.db)
        retired = repo.create_rule({
            "name": "Retired", "target": "600519", "alert_type": "price_cross",
            "parameters": "{}", "enabled": True,
        })
        trigger = repo.create_trigger({
            "rule_id": retired.id, "target": "600519", "status": "triggered",
        })
        repo.record_notification_attempt({
            "trigger_id": trigger.id, "channel": "email", "success": True,
        })
        repo.upsert_cooldown(
            rule_id=retired.id, rule_key="retired", target="600519", severity="warning",
            last_triggered_at=datetime.now(),
            cooldown_until=datetime.now() + timedelta(hours=1), reason="test",
        )
        original_execute = Session.execute
        calls = 0

        def fail_after_dependent_deletes(session, *args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise RuntimeError("cleanup interrupted")
            return original_execute(session, *args, **kwargs)

        with patch.object(Session, "execute", new=fail_after_dependent_deletes):
            with self.assertRaisesRegex(RuntimeError, "cleanup interrupted"):
                repo.delete_retired_rules()
        with self.db.get_session() as session:
            for model in (AlertRuleRecord, AlertTriggerRecord, AlertNotificationRecord, AlertCooldownRecord):
                self.assertEqual(session.query(model).count(), 1)

    def test_price_change_up_and_down_threshold_boundaries(self) -> None:
        for direction, observed, triggered in (
            ("up", 3.0, True), ("up", 2.99, False), ("up", -3.0, False),
            ("down", -3.0, True), ("down", -2.99, False), ("down", 3.0, False),
        ):
            with self.subTest(direction=direction, observed=observed):
                rule = self._create_rule({"parameters": {"direction": direction, "change_pct": 3}})
                with patch(
                    "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                    new=AsyncMock(return_value=SimpleNamespace(change_pct=observed)),
                ):
                    response = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(response.json()["triggered"], triggered)
                self.assertEqual(response.json()["observed_value"], observed)

    def test_rule_crud_enable_disable_and_delete(self) -> None:
        created = self._create_rule()
        rule_id = created["id"]
        self.assertEqual(created["target"], "600519")
        self.assertEqual(created["alert_type"], "price_change_percent")
        self.assertEqual(created["parameters"]["change_pct"], 1800.0)
        self.assertTrue(created["enabled"])
        self.assertEqual(created["source"], "api")
        self.assertIsNone(created["last_triggered_at"])
        self.assertIsNone(created["cooldown_until"])
        self.assertFalse(created["cooldown_active"])
        self.assertIsNotNone(created["created_at"])
        self.assertIsNotNone(created["updated_at"])

        list_resp = self.client.get("/api/v1/alerts/rules")
        self.assertEqual(list_resp.status_code, 200)
        payload = list_resp.json()
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["items"][0]["id"], rule_id)

        detail_resp = self.client.get(f"/api/v1/alerts/rules/{rule_id}")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertEqual(detail_resp.json()["id"], rule_id)

        patch_resp = self.client.patch(
            f"/api/v1/alerts/rules/{rule_id}",
            json={"enabled": False, "parameters": {"direction": "down", "change_pct": 1600}},
        )
        self.assertEqual(patch_resp.status_code, 200, patch_resp.text)
        self.assertFalse(patch_resp.json()["enabled"])
        self.assertEqual(patch_resp.json()["parameters"], {"direction": "down", "change_pct": 1600.0})

        enable_resp = self.client.post(f"/api/v1/alerts/rules/{rule_id}/enable")
        self.assertEqual(enable_resp.status_code, 200)
        self.assertTrue(enable_resp.json()["enabled"])

        disable_resp = self.client.post(f"/api/v1/alerts/rules/{rule_id}/disable")
        self.assertEqual(disable_resp.status_code, 200)
        self.assertFalse(disable_resp.json()["enabled"])

        delete_resp = self.client.delete(f"/api/v1/alerts/rules/{rule_id}")
        self.assertEqual(delete_resp.status_code, 200)
        self.assertEqual(delete_resp.json(), {"deleted": 1})

        missing_resp = self.client.get(f"/api/v1/alerts/rules/{rule_id}")
        self.assertEqual(missing_resp.status_code, 404)

    def test_rule_response_includes_server_cooldown_active_flag(self) -> None:
        created = self._create_rule()
        repo = AlertRepository(self.db)
        now_dt = datetime.now()
        cooldown_until = now_dt + timedelta(minutes=5)
        repo.upsert_cooldown(
            rule_id=created["id"],
            rule_key="single_symbol:600519:price_change_percent:{}",
            target="600519",
            severity="warning",
            last_triggered_at=now_dt,
            cooldown_until=cooldown_until,
            reason="active cooldown",
        )

        list_resp = self.client.get("/api/v1/alerts/rules")
        self.assertEqual(list_resp.status_code, 200, list_resp.text)
        item = list_resp.json()["items"][0]
        self.assertEqual(item["id"], created["id"])
        self.assertEqual(item["cooldown_until"], cooldown_until.isoformat())
        self.assertTrue(item["cooldown_active"])

        expired_at = datetime.now() - timedelta(minutes=5)
        repo.upsert_cooldown(
            rule_id=created["id"],
            rule_key="single_symbol:600519:price_change_percent:{}",
            target="600519",
            severity="warning",
            last_triggered_at=expired_at,
            cooldown_until=expired_at,
            reason="expired cooldown",
        )

        detail_resp = self.client.get(f"/api/v1/alerts/rules/{created['id']}")
        self.assertEqual(detail_resp.status_code, 200, detail_resp.text)
        self.assertFalse(detail_resp.json()["cooldown_active"])

    def test_rule_update_rejects_empty_payload(self) -> None:
        rule = self._create_rule()

        resp = self.client.patch(f"/api/v1/alerts/rules/{rule['id']}", json={})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"], "validation_error")

    def test_rule_update_rejects_null_for_non_nullable_fields(self) -> None:
        rule = self._create_rule()

        for field_name in ("enabled", "severity", "name"):
            resp = self.client.patch(f"/api/v1/alerts/rules/{rule['id']}", json={field_name: None})
            self.assertEqual(resp.status_code, 400, resp.text)
            self.assertEqual(resp.json()["error"], "validation_error")

        detail_resp = self.client.get(f"/api/v1/alerts/rules/{rule['id']}")
        self.assertEqual(detail_resp.status_code, 200)
        detail = detail_resp.json()
        self.assertTrue(detail["enabled"])
        self.assertEqual(detail["severity"], "warning")
        self.assertEqual(detail["name"], "Moutai price change")

    def test_rule_update_allows_null_for_reserved_policy_fields(self) -> None:
        rule = self._create_rule(
            {
                "cooldown_policy": {"cooldown_seconds": 60},
                "notification_policy": {"channels": ["wechat"]},
            }
        )

        resp = self.client.patch(
            f"/api/v1/alerts/rules/{rule['id']}",
            json={"cooldown_policy": None, "notification_policy": None},
        )

        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertIsNone(resp.json()["cooldown_policy"])
        self.assertIsNone(resp.json()["notification_policy"])

    def test_supported_rule_types_and_filters(self) -> None:
        self._create_rule()
        self._create_rule(
            {
                "name": "CATL drop",
                "target": "300750",
                "alert_type": "price_change_percent",
                "parameters": {"direction": "down", "change_pct": 3.5},
                "enabled": False,
            }
        )

        resp = self.client.get(
            "/api/v1/alerts/rules",
            params={"alert_type": "price_change_percent", "enabled": False},
        )
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["items"][0]["target"], "300750")
        self.assertEqual(payload["items"][0]["parameters"]["change_pct"], 3.5)




    def test_retired_portfolio_alert_scopes_are_rejected(self) -> None:
        for target_scope in ("portfolio_holdings", "portfolio_account"):
            resp = self.client.post(
                "/api/v1/alerts/rules",
                json={
                    "target_scope": target_scope,
                    "target": "all",
                    "alert_type": "price_change_percent",
                    "parameters": {"direction": "up", "change_pct": 10},
                },
            )
            self.assertEqual(resp.status_code, 422, resp.text)

    def test_p6_watchlist_dry_run_aggregates_targets_without_stock_code_validation(self) -> None:
        rule = self._create_rule({
            "name": "Watchlist breakout",
            "target_scope": "watchlist",
            "target": "default",
            "alert_type": "price_change_percent",
            "parameters": {"direction": "up", "change_pct": 10},
        })

        async def _quote(_monitor, stock_code):
            return SimpleNamespace(change_pct=11.0 if stock_code == "600519" else 9.0)

        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertEqual(payload["target_scope"], "watchlist")
        self.assertTrue(payload["triggered"])
        self.assertGreaterEqual(payload["evaluated_count"], 1)
        self.assertEqual(payload["triggered_count"], 1)
        self.assertEqual(payload["target_results"][0]["target"], "600519")

    def test_p6_watchlist_dry_run_timeout_counts_target_as_skipped(self) -> None:
        rule = self._create_rule({
            "name": "Watchlist slow",
            "target_scope": "watchlist",
            "target": "default",
            "alert_type": "price_change_percent",
            "parameters": {"direction": "up", "change_pct": 10},
        })

        async def _slow_quote(_monitor, _stock_code):
            await asyncio.sleep(0.05)
            return SimpleNamespace(change_pct=11.0)

        with patch("ai_stock.services.alert_service.DRY_RUN_TARGET_TIMEOUT_SECONDS", 0.001), patch(
            "ai_stock.agent.events.EventMonitor._get_realtime_quote",
            new=_slow_quote,
        ):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertEqual(payload["status"], "not_triggered")
        self.assertFalse(payload["triggered"])
        self.assertEqual(payload["evaluated_count"], 1)
        self.assertEqual(payload["skipped_count"], 1)
        self.assertEqual(payload["target_results"][0]["record_status"], "skipped")
        self.assertIn("timed out", payload["target_results"][0]["message"])

    def test_rejects_unsupported_and_invalid_rules(self) -> None:
        unsupported = self.client.post(
            "/api/v1/alerts/rules",
            json={
                "target_scope": "single_symbol",
                "target": "600519",
                "alert_type": "sentiment_shift",
                "parameters": {},
            },
        )
        self.assertEqual(unsupported.status_code, 422)

        invalid_price = self.client.post(
            "/api/v1/alerts/rules",
            json={
                "target_scope": "single_symbol",
                "target": "600519",
                "alert_type": "price_change_percent",
                "parameters": {"direction": "sideways", "change_pct": 0},
            },
        )
        self.assertEqual(invalid_price.status_code, 400)
        self.assertEqual(invalid_price.json()["error"], "validation_error")

        missing_target = self.client.post(
            "/api/v1/alerts/rules",
            json={"target_scope": "single_symbol", "alert_type": "price_change_percent", "parameters": {"change_pct": 10}},
        )
        self.assertEqual(missing_target.status_code, 422)



    def test_dry_run_price_change_percent_uses_mocked_quote_and_does_not_write_history(self) -> None:
        rule = self._create_rule()

        with patch(
            "ai_stock.agent.events.EventMonitor._get_realtime_quote",
            new=AsyncMock(return_value=SimpleNamespace(change_pct=1800.0)),
        ) as quote:
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertTrue(payload["triggered"])
        self.assertEqual(payload["status"], "triggered")
        self.assertEqual(payload["observed_value"], 1800.0)
        quote.assert_awaited_once_with("600519")

        self.assertEqual(self.client.get("/api/v1/alerts/triggers").json()["total"], 0)
        self.assertEqual(self.client.get("/api/v1/alerts/notifications").json()["total"], 0)

    def test_dry_run_price_change_percent_not_triggered_keeps_observed_value(self) -> None:
        rule = self._create_rule()

        with patch(
            "ai_stock.agent.events.EventMonitor._get_realtime_quote",
            new=AsyncMock(return_value=SimpleNamespace(change_pct=1700.0)),
        ):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertFalse(payload["triggered"])
        self.assertEqual(payload["status"], "not_triggered")
        self.assertEqual(payload["observed_value"], 1700.0)

    def test_dry_run_quote_exception_returns_evaluation_error_and_sanitizes_message(self) -> None:
        rule = self._create_rule()

        async def _raise_quote_error(_stock_code):
            raise RuntimeError("token=secret-token failed at https://example.com/webhook")

        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_raise_quote_error):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertFalse(payload["triggered"])
        self.assertEqual(payload["status"], "evaluation_error")
        self.assertNotIn("secret-token", payload["message"])
        self.assertNotIn("example.com/webhook", payload["message"])

    def test_dry_run_price_change_supports_quote_aliases(self) -> None:
        rule = self._create_rule(
            {
                "target": "300750",
                "alert_type": "price_change_percent",
                "parameters": {"direction": "down", "change_pct": 3.25},
            }
        )

        with patch(
            "ai_stock.agent.events.EventMonitor._get_realtime_quote",
            new=AsyncMock(return_value={"pct_chg": " -3.25% "}),
        ):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200, resp.text)
        payload = resp.json()
        self.assertTrue(payload["triggered"])
        self.assertEqual(payload["observed_value"], -3.25)

    def test_dry_run_missing_data_returns_not_triggered(self) -> None:
        rule = self._create_rule()

        with patch(
            "ai_stock.agent.events.EventMonitor._get_realtime_quote",
            new=AsyncMock(return_value=None),
        ):
            resp = self.client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "not_triggered")
        self.assertFalse(resp.json()["triggered"])

    def test_legacy_json_config_is_not_rewritten(self) -> None:
        before = self.env_path.read_text(encoding="utf-8")
        self._create_rule()
        after = self.env_path.read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertIn("AGENT_EVENT_ALERT_RULES_JSON", after)

    def test_trigger_and_notification_queries_are_paginated_and_sanitized(self) -> None:
        rule = self._create_rule()
        with self.db.get_session() as session:
            trigger = AlertTriggerRecord(
                rule_id=rule["id"],
                target="600519",
                observed_value=1810.0,
                threshold=1800.0,
                reason="breakout",
                data_source="unit-test",
                triggered_at=datetime(2026, 1, 1, 9, 30),
                status="triggered",
                diagnostics="url=https://example.com/hook?token=secret-token",
            )
            session.add(trigger)
            session.commit()
            session.refresh(trigger)
            notification = AlertNotificationRecord(
                trigger_id=trigger.id,
                channel="wechat",
                attempt=1,
                success=False,
                error_code="timeout",
                retryable=True,
                latency_ms=123,
                diagnostics="Bearer secret-token timeout at https://example.com/webhook?key=secret",
            )
            session.add(notification)
            session.commit()

        trigger_resp = self.client.get("/api/v1/alerts/triggers", params={"page": 1, "page_size": 10})
        self.assertEqual(trigger_resp.status_code, 200)
        trigger_payload = trigger_resp.json()
        self.assertEqual(trigger_payload["total"], 1)
        self.assertNotIn("secret-token", str(trigger_payload))
        self.assertNotIn("example.com/hook", str(trigger_payload))
        self.assertIsNone(trigger_payload["items"][0]["market_phase_summary"])
        self.assertIsNone(trigger_payload["items"][0]["analysis_context_pack_overview"])
        self.assertEqual(trigger_payload["items"][0]["analysis_visibility_source"], "legacy_text")

        notification_resp = self.client.get("/api/v1/alerts/notifications", params={"channel": "wechat"})
        self.assertEqual(notification_resp.status_code, 200)
        notification_payload = notification_resp.json()
        self.assertEqual(notification_payload["total"], 1)
        self.assertTrue(notification_payload["items"][0]["retryable"])
        self.assertNotIn("secret-token", str(notification_payload))
        self.assertNotIn("example.com/webhook", str(notification_payload))

    def test_trigger_query_derives_analysis_visibility_from_json_diagnostics(self) -> None:
        rule = self._create_rule()
        diagnostics = {
            "existing": "keep",
            "analysis_visibility": {
                "source": "analysis_history_snapshot",
                "market_phase_summary": {
                    "phase": "postmarket",
                    "market": "cn",
                    "trigger_source": "alert",
                    "is_partial_bar": False,
                },
                "analysis_context_pack_overview": {
                    "pack_version": "1.0",
                    "subject": {"code": "600519", "market": "cn"},
                    "data_quality": {
                        "overall_score": 88,
                        "level": "good",
                        "limitations": ["news: missing"],
                    },
                    "blocks": [
                        {"key": "quote", "label": "行情", "status": "available"},
                        {"key": "news", "label": "新闻", "status": "missing"},
                    ],
                },
            },
        }
        with self.db.get_session() as session:
            session.add(
                AlertTriggerRecord(
                    rule_id=rule["id"],
                    target="600519",
                    observed_value=1810.0,
                    threshold=1800.0,
                    reason="breakout",
                    data_source="unit-test",
                    triggered_at=datetime(2026, 1, 1, 9, 30),
                    status="triggered",
                    diagnostics=json.dumps(diagnostics),
                )
            )
            session.commit()

        resp = self.client.get("/api/v1/alerts/triggers", params={"page": 1, "page_size": 10})

        self.assertEqual(resp.status_code, 200, resp.text)
        item = resp.json()["items"][0]
        self.assertEqual(item["analysis_visibility_source"], "analysis_history_snapshot")
        self.assertEqual(item["market_phase_summary"]["phase"], "postmarket")
        self.assertEqual(item["analysis_context_pack_overview"]["data_quality"]["level"], "good")

    def test_alert_cooldowns_table_create_all_is_idempotent(self) -> None:
        constraint_names = {constraint.name for constraint in AlertCooldownRecord.__table__.constraints}
        self.assertIn("uix_alert_cooldown_rule_target_severity", constraint_names)

        Base.metadata.create_all(self.db._engine)
        Base.metadata.create_all(self.db._engine)

        with self.db.get_session() as session:
            session.add(
                AlertCooldownRecord(
                    rule_id=1,
                    rule_key="single_symbol:600519:price_change_percent:{}",
                    target="600519",
                    severity="warning",
                    state="active",
                )
            )
            session.commit()
            count = session.query(AlertCooldownRecord).count()

        self.assertEqual(count, 1)

    def test_alert_cooldown_upsert_keeps_one_row_per_rule_target_severity(self) -> None:
        repo = AlertRepository(self.db)
        first = repo.upsert_cooldown(
            rule_id=1,
            rule_key="single_symbol:600519:price_change_percent:{}",
            target="600519",
            severity="warning",
            last_triggered_at=datetime(2026, 5, 18, 10, 0, 0),
            cooldown_until=datetime(2026, 5, 18, 11, 0, 0),
            reason="first trigger",
        )
        second = repo.upsert_cooldown(
            rule_id=1,
            rule_key="single_symbol:600519:price_change_percent:{}",
            target="600519",
            severity="warning",
            last_triggered_at=datetime(2026, 5, 18, 10, 30, 0),
            cooldown_until=datetime(2026, 5, 18, 11, 30, 0),
            reason="updated trigger",
        )

        with self.db.get_session() as session:
            rows = session.query(AlertCooldownRecord).all()

        self.assertEqual(first.id, second.id)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].reason, "updated trigger")
        self.assertEqual(rows[0].cooldown_until, datetime(2026, 5, 18, 11, 30, 0))


if __name__ == "__main__":
    unittest.main()
