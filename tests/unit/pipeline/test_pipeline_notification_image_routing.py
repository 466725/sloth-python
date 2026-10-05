# -*- coding: utf-8 -*-
"""
Regression tests for pipeline email image routing with stock email groups.
"""

import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tests.unit.llm.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

from ai_stock.core.pipeline import StockAnalysisPipeline, NotificationChannel
from ai_stock.enums import ReportType


class _FakeNotifier:
    def __init__(self):
        self._markdown_to_image_channels = {"email"}
        self._markdown_to_image_max_chars = 15000
        self.generate_dashboard_report = MagicMock(side_effect=self._generate_dashboard_report)
        self.save_report_to_file = MagicMock(return_value="/tmp/report.md")
        self.is_available = MagicMock(return_value=True)
        self.get_available_channels = MagicMock(return_value=[NotificationChannel.EMAIL])
        self.get_channels_for_route = MagicMock(
            side_effect=lambda route_type, channels=None: list(
                channels if channels is not None else self.get_available_channels()
            )
        )
        self.send_to_context = MagicMock(return_value=False)
        self._should_use_image_for_channel = MagicMock(
            side_effect=lambda channel, image_bytes: (
                    channel.value in self._markdown_to_image_channels and image_bytes is not None
            )
        )
        self._send_email_with_inline_image = MagicMock(return_value=True)
        self.send_to_email = MagicMock(return_value=True)

    @staticmethod
    def _generate_dashboard_report(results):
        return "report:" + ",".join(r.code for r in results)


class TestPipelineEmailGroupImageRouting(unittest.TestCase):
    def _build_pipeline(self):
        pipeline = StockAnalysisPipeline.__new__(StockAnalysisPipeline)
        pipeline.notifier = _FakeNotifier()
        pipeline.config = SimpleNamespace(
            stock_email_groups=[
                (["000001"], ["group@example.com"]),
            ]
        )
        return pipeline

    def _make_results(self):
        return [
            SimpleNamespace(code="000001"),
            SimpleNamespace(code="600519"),
        ]

    @patch("ai_stock.md2img.markdown_to_image", return_value=b"png-bytes")
    def test_send_notifications_email_group_uses_inline_image_when_enabled(self, _mock_md2img):
        pipeline = self._build_pipeline()
        results = self._make_results()

        pipeline._send_notifications(results, ReportType.SIMPLE)

        self.assertEqual(pipeline.notifier._send_email_with_inline_image.call_count, 2)
        pipeline.notifier.send_to_email.assert_not_called()
        called_receivers = [kwargs.get("receivers") for _, kwargs in
                            pipeline.notifier._send_email_with_inline_image.call_args_list]
        self.assertIn(["group@example.com"], called_receivers)
        self.assertIn(None, called_receivers)

    @patch("ai_stock.md2img.markdown_to_image", return_value=None)
    def test_send_notifications_email_group_falls_back_to_text_when_image_unavailable(self, _mock_md2img):
        pipeline = self._build_pipeline()
        results = self._make_results()

        pipeline._send_notifications(results, ReportType.SIMPLE)

        pipeline.notifier._send_email_with_inline_image.assert_not_called()
        self.assertEqual(pipeline.notifier.send_to_email.call_count, 2)
        called_receivers = [kwargs.get("receivers") for _, kwargs in pipeline.notifier.send_to_email.call_args_list]
        self.assertIn(["group@example.com"], called_receivers)
        self.assertIn(None, called_receivers)

    @patch("ai_stock.md2img.markdown_to_image", return_value=None)
    def test_send_notifications_email_group_failure_does_not_skip_later_group(self, _mock_md2img):
        pipeline = self._build_pipeline()
        pipeline.notifier.send_to_email.side_effect = [RuntimeError("group failed"), True]
        results = self._make_results()

        pipeline._send_notifications(results, ReportType.SIMPLE)

        self.assertEqual(pipeline.notifier.send_to_email.call_count, 2)
        called_receivers = [kwargs.get("receivers") for _, kwargs in pipeline.notifier.send_to_email.call_args_list]
        self.assertIn(["group@example.com"], called_receivers)
        self.assertIn(None, called_receivers)

    @patch("ai_stock.md2img.markdown_to_image", return_value=None)
    def test_email_group_diagnostics_only_patch_group_results(self, _mock_md2img):
        pipeline = self._build_pipeline()
        pipeline.save_context_snapshot = True
        pipeline.db = MagicMock()
        pipeline.notifier.send_to_email.side_effect = [RuntimeError("group failed"), True]
        results = self._make_results()
        results[0].query_id = "query-group"
        results[1].query_id = "query-default"

        pipeline._send_notifications(results, ReportType.SIMPLE)

        calls = pipeline.db.update_analysis_history_diagnostics.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].kwargs["query_id"], "query-group")
        self.assertEqual(calls[0].kwargs["code"], "000001")
        self.assertEqual(calls[0].kwargs["notification_runs"][0]["status"], "failed")
        self.assertEqual(calls[0].kwargs["notification_runs"][0]["channel"], "email:group@example.com")
        self.assertEqual(calls[1].kwargs["query_id"], "query-default")
        self.assertEqual(calls[1].kwargs["code"], "600519")
        self.assertEqual(calls[1].kwargs["notification_runs"][0]["status"], "success")
        self.assertEqual(calls[1].kwargs["notification_runs"][0]["channel"], "email:default")

    def test_default_email_receives_full_report_without_image(self):
        pipeline = self._build_pipeline()
        pipeline.config.stock_email_groups = []
        pipeline.notifier._markdown_to_image_channels = set()

        pipeline._send_notifications(self._make_results(), ReportType.SIMPLE)

        pipeline.notifier.send_to_email.assert_called_once_with("report:000001,600519")
        pipeline.notifier._send_email_with_inline_image.assert_not_called()

    @patch("ai_stock.md2img.markdown_to_image")
    def test_empty_report_route_skips_email_and_image_conversion(self, convert):
        pipeline = self._build_pipeline()
        pipeline.notifier.get_channels_for_route.return_value = []
        pipeline.notifier.get_channels_for_route.side_effect = None

        pipeline._send_notifications(self._make_results(), ReportType.SIMPLE)

        convert.assert_not_called()
        pipeline.notifier.send_to_email.assert_not_called()
        pipeline.notifier._send_email_with_inline_image.assert_not_called()

    @patch("ai_stock.md2img.markdown_to_image")
    def test_noise_suppression_precedes_email_image_conversion(self, convert):
        pipeline = self._build_pipeline()
        pipeline.notifier.evaluate_noise_control = MagicMock(
            return_value=SimpleNamespace(should_send=False, message="quiet hours")
        )

        pipeline._send_notifications(self._make_results(), ReportType.SIMPLE)

        convert.assert_not_called()
        pipeline.notifier.send_to_email.assert_not_called()
        pipeline.notifier._send_email_with_inline_image.assert_not_called()

    @patch("ai_stock.md2img.markdown_to_image", return_value=None)
    def test_partial_group_success_records_noise_reservation(self, _convert):
        pipeline = self._build_pipeline()
        decision = SimpleNamespace(should_send=True)
        pipeline.notifier.evaluate_noise_control = MagicMock(return_value=decision)
        pipeline.notifier.record_noise_control = MagicMock()
        pipeline.notifier.release_noise_control = MagicMock()
        pipeline.notifier.send_to_email.side_effect = [RuntimeError("group failed"), True]

        pipeline._send_notifications(self._make_results(), ReportType.SIMPLE)

        self.assertEqual(pipeline.notifier.send_to_email.call_count, 2)
        pipeline.notifier.record_noise_control.assert_called_once_with(decision)
        pipeline.notifier.release_noise_control.assert_not_called()

    @patch("ai_stock.md2img.markdown_to_image", return_value=None)
    def test_all_group_failures_release_noise_reservation(self, _convert):
        pipeline = self._build_pipeline()
        decision = SimpleNamespace(should_send=True)
        pipeline.notifier.evaluate_noise_control = MagicMock(return_value=decision)
        pipeline.notifier.record_noise_control = MagicMock()
        pipeline.notifier.release_noise_control = MagicMock()
        pipeline.notifier.send_to_email.side_effect = RuntimeError("SMTP unavailable")

        pipeline._send_notifications(self._make_results(), ReportType.SIMPLE)

        self.assertEqual(pipeline.notifier.send_to_email.call_count, 2)
        pipeline.notifier.release_noise_control.assert_called_once_with(decision)
        pipeline.notifier.record_noise_control.assert_not_called()
