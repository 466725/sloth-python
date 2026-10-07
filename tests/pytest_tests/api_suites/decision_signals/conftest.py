"""Shared decision-signal fixtures for the API suites."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient


def valid_signal_payload(**overrides: Any) -> dict[str, Any]:
    """Return a complete, schema-valid decision-signal creation payload."""
    payload: dict[str, Any] = {
        "stock_code": "600519",
        "stock_name": "贵州茅台",
        "market": "cn",
        "source_type": "analysis",
        "trigger_source": "api-suite",
        "action": "buy",
        "confidence": 0.75,
        "score": 80,
        "horizon": "5d",
        "entry_low": 1500.0,
        "entry_high": 1550.0,
        "stop_loss": 1450.0,
        "target_price": 1700.0,
        "plan_quality": "complete",
        "status": "active",
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def create_signal(api_client: TestClient) -> Callable[..., dict[str, Any]]:
    """Create a decision signal and return the stored item."""

    def _create(**overrides: Any) -> dict[str, Any]:
        response = api_client.post(
            "/api/v1/decision-signals", json=valid_signal_payload(**overrides)
        )
        assert response.status_code == 200, response.text
        return response.json()["item"]

    return _create
