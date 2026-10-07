"""Shared intelligence fixtures: keep source URL validation offline."""

from __future__ import annotations

import socket
from typing import Any

import pytest

PUBLIC_TEST_HOST = "feeds.example.test"


@pytest.fixture(autouse=True)
def stub_source_host_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    """Resolve intelligence source hostnames to a public address without real DNS.

    Source creation runs an SSRF guard that resolves the URL host, so built-in
    templates and the suite's placeholder host would otherwise require network
    access. Only name resolution is stubbed: literal private IPs and reserved
    hostnames are still rejected by the guard itself.
    """
    import ai_stock.services.intelligence_service as intelligence_service

    def _fake_getaddrinfo(host: str, *args: Any, **kwargs: Any) -> list[tuple[Any, ...]]:
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]

    monkeypatch.setattr(intelligence_service.socket, "getaddrinfo", _fake_getaddrinfo)
