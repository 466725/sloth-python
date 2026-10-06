# -*- coding: utf-8 -*-
"""Alert worker tests for Issue #1202 P2."""

from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from ai_stock.config import Config
from ai_stock.report.notification import ChannelAttemptResult, NotificationDispatchResult
from ai_stock.services.alert_service import AlertService
from ai_stock.services.alert_worker import AlertWorker
from ai_stock.services.decision_signal_service import DecisionSignalService
from ai_stock.storage import DatabaseManager


class AlertWorkerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)
        self.env_path = self.data_dir / ".env"
        self.db_path = self.data_dir / "alert_worker_test.db"
        self.env_path.write_text(
            "\n".join([
                "STOCK_LIST=600519",
                "GEMINI_API_KEY=test",
                "ADMIN_AUTH_ENABLED=false",
                f"DATABASE_PATH={self.db_path}",
            ])
            + "\n",
            encoding="utf-8",
        )
        os.environ["ENV_FILE"] = str(self.env_path)
        os.environ["DATABASE_PATH"] = str(self.db_path)
        Config.reset_instance()
        DatabaseManager.reset_instance()
        self.service = AlertService()

    def tearDown(self) -> None:
        DatabaseManager.reset_instance()
        Config.reset_instance()
        os.environ.pop("ENV_FILE", None)
        os.environ.pop("DATABASE_PATH", None)
        self.temp_dir.cleanup()

    def _config(self, raw_rules: str = "") -> SimpleNamespace:
        return SimpleNamespace(
            agent_event_monitor_enabled=True,
            agent_event_alert_rules_json=raw_rules,
            trading_day_check_enabled=False,
        )

    def _create_rule(self, **overrides) -> dict:
        payload = {
            "name": "Moutai price change",
            "target_scope": "single_symbol",
            "target": "600519",
            "alert_type": "price_change_percent",
            "parameters": {"direction": "up", "change_pct": 1800},
            "severity": "warning",
            "enabled": True,
        }
        payload.update(overrides)
        return self.service.create_rule(payload)

    def _triggers(self, **filters) -> list[dict]:
        return self.service.list_triggers(page_size=100, **filters)["items"]

    def _notifications(self, **filters) -> list[dict]:
        return self.service.list_notifications(page_size=100, **filters)["items"]

    def _dispatch_result(
            self,
            success: bool = True,
            *,
            dispatched: bool = True,
            status: str | None = None,
            channel: str = "custom",
            error_code: str | None = None,
    ) -> NotificationDispatchResult:
        if status is None:
            status = "sent" if success else "all_failed"
        channel_results = []
        if dispatched:
            channel_results.append(
                ChannelAttemptResult(
                    channel=channel,
                    success=success,
                    error_code=error_code if error_code is not None else (None if success else "send_failed"),
                    retryable=not success,
                )
            )
        return NotificationDispatchResult(
            dispatched=dispatched,
            success=success,
            status=status,
            channel_results=channel_results,
        )

    def _notifier(self, *results) -> MagicMock:
        notifier = MagicMock()
        if not results:
            results = (self._dispatch_result(True),)
        if len(results) == 1:
            notifier.send_with_results.return_value = results[0]
        else:
            notifier.send_with_results.side_effect = list(results)
        return notifier

    def test_p6_triggered_stock_alert_links_latest_active_decision_signal(self) -> None:
        self._create_rule(target="600519")
        signal_service = DecisionSignalService()
        signal_service.create_signal({
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "market": "cn",
            "source_type": "analysis",
            "source_report_id": 1390,
            "trace_id": "analysis-1390",
            "trigger_source": "api",
            "action": "sell",
            "reason": "跌破关键支撑",
            "watch_conditions": "观察能否收回均线",
            "risk_summary": "下行风险扩大",
        })
        notifier = self._notifier()
        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            decision_signal_service=signal_service,
            notifier=notifier,
        )

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        all_signals = signal_service.list_signals(stock_code="600519", market="cn", page_size=10)["items"]
        self.assertEqual(len(all_signals), 1)
        self.assertEqual(all_signals[0]["source_type"], "analysis")
        trigger = self._triggers(status="triggered")[0]
        summary = trigger["decision_signal_summary"]
        self.assertEqual(summary["id"], all_signals[0]["id"])
        self.assertEqual(summary["action"], "sell")
        alert_text = notifier.send_with_results.call_args.args[0]
        self.assertIn("AI 决策信号", alert_text)
        self.assertIn("跌破关键支撑", alert_text)
        self.assertIn("观察能否收回均线", alert_text)

    def test_p6_triggered_stock_alert_creates_alert_signal_when_no_active_signal(self) -> None:
        self._create_rule(target="600519")
        signal_service = DecisionSignalService()
        notifier = self._notifier()
        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            decision_signal_service=signal_service,
            notifier=notifier,
        )

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        signals = signal_service.list_signals(source_type="alert", stock_code="600519", market="cn", page_size=10)[
            "items"
        ]
        self.assertEqual(len(signals), 1)
        item = signals[0]
        self.assertEqual(item["action"], "alert")
        self.assertEqual(item["trigger_source"], "alert")
        self.assertEqual(item["source_agent"], "alert_worker")
        self.assertIsNone(item["market_phase"])
        self.assertTrue(str(item["trace_id"]).startswith("alert-rule-"))
        self.assertEqual(item["metadata"]["rule_id"], 1)
        self.assertEqual(item["metadata"]["alert_type"], "price_change_percent")
        self.assertEqual(self._triggers(status="triggered")[0]["decision_signal_summary"]["id"], item["id"])

    def test_p6_alert_signal_trace_id_is_idempotent_for_same_rule(self) -> None:
        self._create_rule(target="600519")
        signal_service = DecisionSignalService()
        notifier = self._notifier(
            self._dispatch_result(False, dispatched=True),
            self._dispatch_result(False, dispatched=True),
        )
        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            decision_signal_service=signal_service,
            notifier=notifier,
        )

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            worker.run_once()
            worker.run_once()

        signals = signal_service.list_signals(source_type="alert", stock_code="600519", market="cn", page_size=10)[
            "items"
        ]
        self.assertEqual(len(signals), 1)
        self.assertIsNone(signals[0]["market_phase"])
        self.assertEqual(len(self._triggers(status="triggered")), 2)

    def test_p6_non_stock_alert_targets_skip_decision_signal_write(self) -> None:
        signal_service = MagicMock()
        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            decision_signal_service=signal_service,
        )
        for runtime_rule in (
                SimpleNamespace(
                    key="market:cn",
                    rule=SimpleNamespace(target_scope="market", target="cn", metadata={}),
                    source="db",
                    severity="warning",
                    effective_target="cn",
                    display_target="cn",
                ),
                SimpleNamespace(
                    key="single_symbol:SPX",
                    rule=SimpleNamespace(
                        target_scope="single_symbol",
                        stock_code="SPX",
                        metadata={},
                    ),
                    source="db",
                    severity="warning",
                    effective_target="SPX",
                    display_target="SPX",
                ),
        ):
            worker._attach_decision_signal_summary_safely(runtime_rule, {"record_status": "triggered"})

        signal_service.get_latest_active.assert_not_called()
        signal_service.create_signal.assert_not_called()

    def test_p6_notification_failure_does_not_block_alert_signal_write(self) -> None:
        self._create_rule(target="600519")
        signal_service = DecisionSignalService()

        class FailingNotifier:
            def send_with_results(self, *_args, **_kwargs):
                raise RuntimeError("webhook token=secret failed")

        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            decision_signal_service=signal_service,
            notifier=FailingNotifier(),
        )

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        self.assertEqual(stats["recorded"], 1)
        self.assertEqual(stats["notified"], 0)
        self.assertEqual(len(self._triggers(status="triggered")), 1)
        signals = signal_service.list_signals(source_type="alert", stock_code="600519", market="cn", page_size=10)[
            "items"
        ]
        self.assertEqual(len(signals), 1)


    def test_enabled_db_rule_triggers_and_disabled_rule_is_ignored(self) -> None:
        enabled_rule = self._create_rule(target="600519")
        self._create_rule(
            name="Disabled",
            target="000001",
            parameters={"direction": "up", "change_pct": 10},
            enabled=False,
        )
        notifier = self._notifier()
        seen_codes = []

        async def _quote(_monitor, stock_code):
            seen_codes.append(stock_code)
            return SimpleNamespace(change_pct=1810.0)

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)
        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            stats = worker.run_once()

        self.assertEqual(stats["loaded"], 1)
        self.assertEqual(stats["triggered"], 1)
        self.assertEqual(seen_codes, ["600519"])
        triggers = self._triggers(rule_id=enabled_rule["id"])
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0]["status"], "triggered")
        self.assertEqual(triggers[0]["target"], "600519")
        self.assertEqual(triggers[0]["observed_value"], 1810.0)
        self.assertEqual(triggers[0]["threshold"], 1800.0)
        notifier.send_with_results.assert_called_once()
        self.assertEqual(notifier.send_with_results.call_args.kwargs["route_type"], "alert")
        notifications = self._notifications(trigger_id=triggers[0]["id"])
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["channel"], "custom")
        self.assertTrue(notifications[0]["success"])

    def test_create_trigger_if_absent_rejects_non_dedupable_history(self) -> None:
        cases = [
            {
                "name": "non_triggered_status",
                "fields": {
                    "rule_id": 1,
                    "target": "600519",
                    "status": "skipped",
                    "data_timestamp": date(2026, 5, 15),
                },
            },
            {
                "name": "missing_rule_id",
                "fields": {
                    "target": "600519",
                    "status": "triggered",
                    "data_timestamp": date(2026, 5, 15),
                },
            },
            {
                "name": "missing_data_timestamp",
                "fields": {
                    "rule_id": 1,
                    "target": "600519",
                    "status": "triggered",
                    "data_timestamp": None,
                },
            },
        ]
        for case in cases:
            with self.subTest(case["name"]):
                with self.assertRaisesRegex(ValueError, "requires triggered status"):
                    self.service.repo.create_trigger_if_absent(case["fields"])

    def test_legacy_rules_coexist_with_db_rules_and_db_rule_wins_duplicate_key(self) -> None:
        self._create_rule(target="600519")
        legacy_rules = (
            '[{"stock_code":"600519","alert_type":"price_change_percent","direction":"up","change_pct":1800},'
            '{"stock_code":"300750","alert_type":"price_change_percent","direction":"down","change_pct":3.5}]'
        )

        async def _quote(_monitor, stock_code):
            if stock_code == "300750":
                return {"pct_chg": "-3.75%"}
            return SimpleNamespace(change_pct=1810.0)

        worker = AlertWorker(
            config_provider=lambda: self._config(legacy_rules),
            service=self.service,
            notifier=self._notifier(),
        )
        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            stats = worker.run_once()

        self.assertEqual(stats["loaded"], 2)
        self.assertEqual(stats["triggered"], 2)
        targets = {item["target"] for item in self._triggers()}
        self.assertEqual(targets, {"600519", "300750"})

    def test_legacy_rules_keep_existing_duplicate_trigger_history(self) -> None:
        legacy_rules = (
            '[{"stock_code":"600519","alert_type":"price_change_percent","direction":"up","change_pct":1800}]'
        )
        notifier = self._notifier()

        async def _quote(_monitor, _stock_code):
            return SimpleNamespace(change_pct=1810.0)

        worker = AlertWorker(
            config_provider=lambda: self._config(legacy_rules),
            service=self.service,
            notifier=notifier,
        )
        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            first = worker.run_once()
            second = worker.run_once()

        self.assertEqual(first["triggered"], 1)
        self.assertEqual(first["recorded"], 1)
        self.assertEqual(second["triggered"], 1)
        self.assertEqual(second["recorded"], 1)
        triggers = self._triggers(status="triggered")
        self.assertEqual(len(triggers), 2)
        self.assertTrue(all(item["rule_id"] is None for item in triggers))
        self.assertTrue(all(item["data_timestamp"] is None for item in triggers))
        notifier.send_with_results.assert_called_once()

    def test_legacy_json_parse_failure_does_not_crash_or_block_persisted_rules(self) -> None:
        before = self.env_path.read_text(encoding="utf-8")
        self._create_rule(target="600519")
        notifier = self._notifier()
        worker = AlertWorker(config_provider=lambda: self._config("[invalid"), service=self.service, notifier=notifier)

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["loaded"], 1)
        self.assertEqual(stats["triggered"], 1)
        self.assertEqual(len(self._triggers()), 1)
        self.assertEqual(self.env_path.read_text(encoding="utf-8"), before)

    def test_all_invalid_legacy_rules_do_not_crash(self) -> None:
        invalid_rules = (
            '[{"stock_code":"600519","alert_type":"price_change_percent","direction":"sideways","change_pct":1800},'
            '{"stock_code":"300750","alert_type":"price_change_percent","direction":"down","change_pct":0}]'
        )
        worker = AlertWorker(config_provider=lambda: self._config(invalid_rules), service=self.service)

        stats = worker.run_once()

        self.assertEqual(stats["loaded"], 0)
        self.assertEqual(stats["evaluated"], 0)
        self.assertEqual(self._triggers(), [])

    def test_empty_sources_are_a_noop(self) -> None:
        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service)

        stats = worker.run_once()

        self.assertEqual(stats["loaded"], 0)
        self.assertEqual(stats["evaluated"], 0)
        self.assertEqual(self._triggers(), [])

    def test_missing_quote_writes_skipped_trigger_without_notification(self) -> None:
        self._create_rule(target="600519")
        notifier = self._notifier()
        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)

        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=AsyncMock(return_value=None)):
            stats = worker.run_once()

        self.assertEqual(stats["skipped"], 1)
        triggers = self._triggers(status="skipped")
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0]["target"], "600519")
        self.assertIn("No realtime quote", triggers[0]["diagnostics"])
        notifier.send_with_results.assert_not_called()

    def test_price_change_percent_numeric_yyyymmdd_quote_date_writes_correct_timestamp(self) -> None:
        rule = self._create_rule(target="600519")
        notifier = self._notifier()
        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0, date=20260517)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        triggers = self._triggers(rule_id=rule["id"], status="triggered")
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0]["data_timestamp"], "2026-05-17T00:00:00")

    def test_price_change_percent_space_separated_quote_time_writes_timestamp(self) -> None:
        rule = self._create_rule(target="600519")
        notifier = self._notifier()
        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0, quote_time="2026-05-17 15:00:00")),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        triggers = self._triggers(rule_id=rule["id"], status="triggered")
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0]["data_timestamp"], "2026-05-17T15:00:00")

    def test_ambiguous_numeric_quote_timestamp_is_not_written_as_epoch(self) -> None:
        rule = self._create_rule(target="600519")
        notifier = self._notifier()
        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)

        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0, timestamp=1700000000)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 1)
        triggers = self._triggers(rule_id=rule["id"], status="triggered")
        self.assertEqual(len(triggers), 1)
        self.assertIsNone(triggers[0]["data_timestamp"])

    def test_service_test_rule_exception_uses_same_sanitized_reason_and_message(self) -> None:
        rule = self._create_rule(target="600519")

        async def _raise(_rule, _monitor, **_kwargs):
            raise RuntimeError("token=secret-token failed at https://example.com/webhook")

        with patch.object(self.service, "_evaluate_rule", new=_raise):
            result = self.service.test_rule(rule["id"])

        self.assertEqual(result["status"], "evaluation_error")
        self.assertEqual(result["record_status"], "failed")
        self.assertEqual(result["reason"], result["message"])
        self.assertNotIn("secret-token", result["reason"])
        self.assertNotIn("example.com/webhook", result["message"])

    def test_non_triggered_status_history_is_not_deduplicated(self) -> None:
        self._create_rule(name="Skipped", target="600519")
        self._create_rule(
            name="Degraded",
            target="000858",
            alert_type="price_change_percent",
            parameters={"direction": "up", "change_pct": 2.5},
        )
        self._create_rule(
            name="Failed",
            target="300750",
            alert_type="price_change_percent",
            parameters={"direction": "down", "change_pct": 3.0},
        )
        status_by_target = {
            "600519": "skipped",
            "000858": "degraded",
            "300750": "failed",
        }

        async def _evaluate(rule, _monitor, **_kwargs):
            status = status_by_target[rule.stock_code]
            return {
                "rule_id": self.service._runtime_rule_id(rule),
                "record_status": status,
                "triggered": False,
                "observed_value": None,
                "threshold": self.service._threshold_for_rule(rule),
                "data_source": self.service._data_source_for_rule(rule),
                "data_timestamp": None,
                "reason": f"{status} test",
                "message": f"{status} test",
            }

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=self._notifier())
        with patch.object(self.service, "_evaluate_rule", new=_evaluate):
            first = worker.run_once()
            second = worker.run_once()

        self.assertEqual(first["recorded"], 3)
        self.assertEqual(second["recorded"], 3)
        for status in ("skipped", "degraded", "failed"):
            self.assertEqual(len(self._triggers(status=status)), 2)

    def test_unsupported_persisted_rule_is_skipped_without_crashing_worker(self) -> None:
        self.service.repo.create_rule({
            "name": "Future rule",
            "target_scope": "single_symbol",
            "target": "600519",
            "alert_type": "future_indicator",
            "parameters": "{}",
            "severity": "warning",
            "enabled": True,
            "source": "api",
        })

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service)
        stats = worker.run_once()

        self.assertEqual(stats["loaded"], 0)
        self.assertEqual(stats["evaluated"], 0)
        self.assertEqual(self._triggers(), [])



    def test_single_rule_failure_does_not_block_other_rules(self) -> None:
        self._create_rule(target="600519")
        self._create_rule(
            name="CATL drop",
            target="300750",
            alert_type="price_change_percent",
            parameters={"direction": "down", "change_pct": 3.0},
        )
        notifier = self._notifier()

        async def _quote(_monitor, stock_code):
            if stock_code == "600519":
                raise RuntimeError("token=secret-token failed at https://example.com/webhook")
            return {"pct_chg": "-3.25%"}

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)
        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            stats = worker.run_once()

        self.assertEqual(stats["failed"], 1)
        self.assertEqual(stats["triggered"], 1)
        failed = self._triggers(status="failed")
        self.assertEqual(len(failed), 1)
        self.assertNotIn("secret-token", failed[0]["diagnostics"])
        self.assertNotIn("example.com/webhook", failed[0]["diagnostics"])
        self.assertEqual(len(self._triggers(status="triggered")), 1)

    def test_notification_failure_does_not_block_other_rules(self) -> None:
        self._create_rule(target="600519")
        self._create_rule(
            name="CATL drop",
            target="300750",
            alert_type="price_change_percent",
            parameters={"direction": "down", "change_pct": 3.0},
        )
        notifier = self._notifier(RuntimeError("webhook secret failed"), self._dispatch_result(True))

        async def _quote(_monitor, stock_code):
            if stock_code == "600519":
                return SimpleNamespace(change_pct=1810.0)
            return {"pct_chg": "-3.25%"}

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=notifier)
        with patch("ai_stock.agent.events.EventMonitor._get_realtime_quote", new=_quote):
            stats = worker.run_once()

        self.assertEqual(stats["triggered"], 2)
        self.assertEqual(stats["recorded"], 2)
        self.assertEqual(stats["notified"], 1)
        self.assertEqual(len(self._triggers(status="triggered")), 2)
        self.assertEqual(notifier.send_with_results.call_count, 2)

    def test_notification_dispatch_results_are_recorded_and_success_updates_cooldown(self) -> None:
        rule = self._create_rule(target="600519", cooldown_policy={"cooldown_seconds": 60})

        class FakeNotifier:
            def send_with_results(self, *_args, **_kwargs):
                return NotificationDispatchResult(
                    dispatched=True,
                    success=True,
                    status="partial_failed",
                    channel_results=[
                        ChannelAttemptResult(channel="wechat", success=False, error_code="send_failed", retryable=True),
                        ChannelAttemptResult(channel="custom", success=True, latency_ms=12),
                    ],
                )

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=FakeNotifier())
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["notified"], 1)
        triggers = self._triggers(rule_id=rule["id"], status="triggered")
        self.assertEqual(len(triggers), 1)
        notifications = self._notifications(trigger_id=triggers[0]["id"])
        by_channel = {item["channel"]: item for item in notifications}
        self.assertEqual(set(by_channel), {"wechat", "custom"})
        self.assertFalse(by_channel["wechat"]["success"])
        self.assertTrue(by_channel["custom"]["success"])
        cooldown = self.service.repo.get_rule_cooldown_summary(
            rule_id=rule["id"],
            target="600519",
            severity="warning",
        )
        self.assertIsNotNone(cooldown)

    def test_noise_suppression_records_synthetic_attempt_without_upserting_cooldown(self) -> None:
        rule = self._create_rule(target="600519", cooldown_policy={"cooldown_seconds": 60})

        class FakeNotifier:
            def send_with_results(self, *_args, **_kwargs):
                return NotificationDispatchResult(
                    dispatched=False,
                    success=False,
                    status="noise_suppressed",
                    message="cooldown: duplicated static notification",
                )

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=FakeNotifier())
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            stats = worker.run_once()

        self.assertEqual(stats["notified"], 0)
        triggers = self._triggers(rule_id=rule["id"], status="triggered")
        self.assertEqual(len(triggers), 1)
        notifications = self._notifications(trigger_id=triggers[0]["id"])
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["channel"], "__noise_suppressed__")
        self.assertEqual(notifications[0]["error_code"], "noise_suppressed")
        cooldown = self.service.repo.get_rule_cooldown_summary(
            rule_id=rule["id"],
            target="600519",
            severity="warning",
        )
        self.assertIsNone(cooldown)

    def test_no_channel_and_all_failed_do_not_upsert_cooldown(self) -> None:
        rule = self._create_rule(target="600519", cooldown_policy={"cooldown_seconds": 60})
        dispatches = [
            NotificationDispatchResult(dispatched=False, success=False, status="no_channel", message="no channel"),
            NotificationDispatchResult(
                dispatched=True,
                success=False,
                status="all_failed",
                channel_results=[ChannelAttemptResult(channel="wechat", success=False, error_code="send_failed")],
            ),
        ]

        class FakeNotifier:
            def send_with_results(self, *_args, **_kwargs):
                return dispatches.pop(0)

        worker = AlertWorker(config_provider=lambda: self._config(), service=self.service, notifier=FakeNotifier())
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            first = worker.run_once()
            second = worker.run_once()

        self.assertEqual(first["notified"], 0)
        self.assertEqual(second["notified"], 0)
        channels = {item["channel"] for item in self._notifications()}
        self.assertEqual(channels, {"__no_channel__", "wechat"})
        cooldown = self.service.repo.get_rule_cooldown_summary(
            rule_id=rule["id"],
            target="600519",
            severity="warning",
        )
        self.assertIsNone(cooldown)

    def test_db_cooldown_suppresses_duplicate_notifications_but_expires(self) -> None:
        self._create_rule(target="600519", cooldown_policy={"cooldown_seconds": 60})
        notifier = self._notifier()
        now = {"value": 1000.0}

        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            notifier=notifier,
            now_provider=lambda: now["value"],
            fingerprint_ttl_seconds=60,
        )
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            worker.run_once()
            now["value"] += 30
            worker.run_once()
            now["value"] += 61
            worker.run_once()

        self.assertEqual(notifier.send_with_results.call_count, 2)
        self.assertEqual(len(self._triggers(status="triggered")), 3)
        cooldown_attempts = self._notifications(channel="__cooldown__")
        self.assertEqual(len(cooldown_attempts), 1)
        self.assertEqual(cooldown_attempts[0]["error_code"], "cooldown_active")

    def test_db_rule_with_cooldown_zero_is_not_suppressed_by_fingerprint(self) -> None:
        self._create_rule(target="600519", cooldown_policy={"cooldown_seconds": 0})
        notifier = self._notifier()
        now = {"value": 1000.0}

        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            notifier=notifier,
            now_provider=lambda: now["value"],
            fingerprint_ttl_seconds=60,
        )
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            worker.run_once()
            now["value"] += 10
            worker.run_once()

        self.assertEqual(notifier.send_with_results.call_count, 2)
        self.assertEqual(len(self._triggers(status="triggered")), 2)
        self.assertEqual(self._notifications(channel="__cooldown__"), [])

    def test_legacy_rule_still_uses_fingerprint_suppression(self) -> None:
        raw_rules = '[{"stock_code":"600519","alert_type":"price_change_percent","direction":"up","change_pct":1800}]'
        notifier = self._notifier()
        now = {"value": 1000.0}

        worker = AlertWorker(
            config_provider=lambda: self._config(raw_rules),
            service=self.service,
            notifier=notifier,
            now_provider=lambda: now["value"],
            fingerprint_ttl_seconds=60,
        )
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            worker.run_once()
            now["value"] += 10
            worker.run_once()
            now["value"] += 61
            worker.run_once()

        self.assertEqual(notifier.send_with_results.call_count, 2)
        self.assertEqual(len(self._triggers(status="triggered")), 3)

    def test_failed_db_notification_attempts_do_not_start_cooldown_window(self) -> None:
        self._create_rule(target="600519")
        notifier = self._notifier(
            self._dispatch_result(False),
            RuntimeError("temporary webhook failure"),
            self._dispatch_result(True),
        )
        now = {"value": 1000.0}

        worker = AlertWorker(
            config_provider=lambda: self._config(),
            service=self.service,
            notifier=notifier,
            now_provider=lambda: now["value"],
            fingerprint_ttl_seconds=60,
        )
        with patch(
                "ai_stock.agent.events.EventMonitor._get_realtime_quote",
                new=AsyncMock(return_value=SimpleNamespace(change_pct=1810.0)),
        ):
            first = worker.run_once()
            now["value"] += 10
            second = worker.run_once()
            now["value"] += 10
            third = worker.run_once()
            now["value"] += 10
            fourth = worker.run_once()

        self.assertEqual(first["notified"], 0)
        self.assertEqual(second["notified"], 0)
        self.assertEqual(third["notified"], 1)
        self.assertEqual(fourth["notified"], 0)
        self.assertEqual(notifier.send_with_results.call_count, 3)
        self.assertEqual(len(self._triggers(status="triggered")), 4)

    def test_p6_empty_watchlist_writes_skipped_trigger(self) -> None:
        self._create_rule(
            name="Watchlist",
            target_scope="watchlist",
            target="default",
            alert_type="price_change_percent",
            parameters={"direction": "up", "change_pct": 10},
        )
        config = self._config()
        config.stock_list = []
        worker = AlertWorker(config_provider=lambda: config, service=self.service, notifier=self._notifier())

        stats = worker.run_once()

        self.assertEqual(stats["skipped"], 1)
        triggers = self._triggers(status="skipped")
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0]["target"], "watchlist:default")
        self.assertIn("No watchlist targets", triggers[0]["diagnostics"])

    def test_p6_overflow_payload_is_dry_run_only_and_worker_does_not_write_degraded_history(self) -> None:
        rule = self._create_rule(
            name="Large watchlist",
            target_scope="watchlist",
            target="default",
            alert_type="price_change_percent",
            parameters={"direction": "up", "change_pct": 10},
        )
        row = self.service.repo.get_rule(rule["id"])
        config = self._config()
        config.stock_list = [f"{index:06d}" for index in range(1, 102)]

        dry_run_payloads = self.service.build_runtime_payloads(row, config=config)
        worker_payloads = self.service.build_runtime_payloads(row, config=config, include_overflow_payload=False)

        self.assertEqual(len(dry_run_payloads), 101)
        self.assertTrue(dry_run_payloads[-1].effective_target.endswith(":overflow"))
        self.assertEqual(len(worker_payloads), 100)
        self.assertFalse(any(payload.effective_target.endswith(":overflow") for payload in worker_payloads))

        async def _not_triggered(rule_obj, *_args, **_kwargs):
            return {
                "rule_id": self.service._runtime_rule_id(rule_obj),
                "status": "not_triggered",
                "record_status": None,
                "triggered": False,
                "observed_value": 9.0,
                "threshold": 10.0,
                "data_source": "realtime_quote",
                "data_timestamp": None,
                "reason": "below threshold",
                "message": "below threshold",
            }

        worker = AlertWorker(config_provider=lambda: config, service=self.service, notifier=self._notifier())
        with patch.object(self.service, "_evaluate_rule", new=_not_triggered):
            stats = worker.run_once()

        self.assertEqual(stats["loaded"], 100)
        self.assertEqual(stats["degraded"], 0)
        self.assertEqual(self._triggers(status="degraded"), [])

if __name__ == "__main__":
    unittest.main()
