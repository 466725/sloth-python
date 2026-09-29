# -*- coding: utf-8 -*-
"""Tests for market review lock stale cleanup on platforms without fcntl."""

import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import ai_stock.core.market_review_lock as market_review_lock


class MarketReviewNoFcntlLockTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_running = market_review_lock._market_review_running
        market_review_lock._market_review_running = False

    def tearDown(self) -> None:
        market_review_lock._market_review_running = self._orig_running

    @staticmethod
    def _write_lock_file(path: Path, pid: int, started_at: datetime) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"pid={pid}\nstarted_at={started_at.isoformat()}\n",
            encoding="utf-8",
        )

    def test_windows_liveness_probe_does_not_call_os_kill(self) -> None:
        with patch.object(market_review_lock.os, "name", "nt"), \
                patch.object(
                    market_review_lock,
                    "_is_windows_process_alive",
                    return_value=True,
                ) as windows_probe, \
                patch.object(market_review_lock.os, "kill") as os_kill:
            self.assertTrue(market_review_lock._is_process_alive(12345))

        windows_probe.assert_called_once_with(12345)
        os_kill.assert_not_called()

    def test_windows_liveness_probe_treats_invalid_pid_as_dead(self) -> None:
        kernel32 = SimpleNamespace(OpenProcess=lambda *_args: 0)
        with patch("ctypes.WinDLL", return_value=kernel32, create=True), \
                patch("ctypes.get_last_error", return_value=87, create=True):
            self.assertFalse(market_review_lock._is_windows_process_alive(99999))

    def test_windows_liveness_probe_keeps_access_denied_lock_active(self) -> None:
        kernel32 = SimpleNamespace(OpenProcess=lambda *_args: 0)
        with patch("ctypes.WinDLL", return_value=kernel32, create=True), \
                patch("ctypes.get_last_error", return_value=5, create=True):
            self.assertTrue(market_review_lock._is_windows_process_alive(12345))
