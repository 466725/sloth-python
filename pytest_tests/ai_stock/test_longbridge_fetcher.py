from __future__ import annotations

import importlib
import os
import re
import sys
import time
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.longbridge_fetcher"


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")

    class DataFrame:
        def __init__(self, data: Any = None, *args: Any, **kwargs: Any) -> None:
            self._data = data
            self.empty = not bool(data)

    module.DataFrame = DataFrame
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class BaseFetcher:
        pass

    module.BaseFetcher = BaseFetcher
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class RealtimeSource:
        LONG_BRIDGE = "longbridge"

    def safe_float(value: Any) -> Any:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    module.UnifiedRealtimeQuote = UnifiedRealtimeQuote
    module.RealtimeSource = RealtimeSource
    module.safe_float = safe_float
    return module


def _make_us_index_mapping_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.us_index_mapping")
    module.is_us_stock_code = lambda code: bool(re.match(r"^[A-Z]{1,5}(\.[A-Z])?$", str(code or "").strip().upper()))
    module.is_us_index_code = lambda code: str(code or "").strip().upper() in {"SPX", "NDX", "DJI"}
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.us_index_mapping", _make_us_index_mapping_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_ttl_parsing_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("LONGBRIDGE_STATIC_INFO_TTL_SECONDS", "120")
    assert module._static_info_ttl_seconds() == 120

    monkeypatch.setenv("LONGBRIDGE_STATIC_INFO_TTL_SECONDS", "invalid")
    assert module._static_info_ttl_seconds() == 86400

    monkeypatch.setenv("LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS", "20")
    assert module._connection_cooldown_seconds() == 20

    monkeypatch.setenv("LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS", "bad")
    assert module._connection_cooldown_seconds() == 15


@pytest.mark.unit
def test_clean_optional_and_credential_checks(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._clean_optional(None) is None
    assert module._clean_optional("   ") is None
    assert module._clean_optional(" value ") == "value"

    creds = {
        "app_key": "k",
        "app_secret": "s",
        "access_token": "t",
        "oauth_client_id": None,
    }
    assert module._has_legacy_credentials(creds) is True
    assert module._has_oauth_credentials(creds) is False

    creds["oauth_client_id"] = "oauth-id"
    assert module._has_oauth_credentials(creds) is True


@pytest.mark.unit
def test_longbridge_credentials_collects_env_and_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("LONGBRIDGE_APP_KEY", "app-key")
    monkeypatch.setenv("LONGBRIDGE_APP_SECRET", "app-secret")
    monkeypatch.delenv("LONGBRIDGE_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("LONGBRIDGE_OAUTH_CLIENT_ID", raising=False)

    creds = module._longbridge_credentials()
    assert creds["app_key"] == "app-key"
    assert creds["app_secret"] == "app-secret"
    # alias path: app_key can become oauth_client_id when access token is absent
    assert creds["oauth_client_id"] == "app-key"


@pytest.mark.unit
def test_code_and_symbol_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("SPX") is True
    assert module._is_us_code("600519") is False

    assert module._is_hk_code("HK00700") is True
    assert module._is_hk_code("00700") is True
    assert module._is_hk_code("0700.HK") is True
    assert module._is_hk_code("600519") is False

    assert module._to_longbridge_symbol("AAPL") == "AAPL.US"
    assert module._to_longbridge_symbol("HK00700") == "0700.HK"
    assert module._to_longbridge_symbol("00700") == "0700.HK"
    assert module._to_longbridge_symbol("0700.HK") == "0700.HK"
    assert module._to_longbridge_symbol("600519") is None


@pytest.mark.unit
def test_sanitize_env_removes_empty_and_applies_region_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("LONGBRIDGE_HTTP_URL", "")
    monkeypatch.setenv("LONGBRIDGE_REGION", "cn")
    monkeypatch.delenv("LONGPORT_REGION", raising=False)
    monkeypatch.delenv("LONGBRIDGE_QUOTE_WS_URL", raising=False)
    monkeypatch.delenv("LONGBRIDGE_TRADE_WS_URL", raising=False)

    module._sanitize_longbridge_env()

    assert os.environ.get("LONGPORT_REGION") == "cn"
    assert os.environ.get("LONGBRIDGE_HTTP_URL", "").startswith("https://openapi.longbridge")
    assert "LONGBRIDGE_QUOTE_WS_URL" in os.environ
    assert "LONGBRIDGE_TRADE_WS_URL" in os.environ
    assert os.environ.get("LONGBRIDGE_PRINT_QUOTE_PACKAGES") == "false"


@pytest.mark.unit
def test_fetcher_availability_and_cooldown(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    # Provide config module for _is_available path
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")
    src_config_module.get_config = lambda: SimpleNamespace(
        longbridge_app_key="k",
        longbridge_app_secret="s",
        longbridge_access_token="t",
        longbridge_oauth_client_id=None,
    )
    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)

    fetcher = module.LongbridgeFetcher()
    assert fetcher.is_available_for_request("quote") is True

    fetcher._cooldown_until = time.time() + 3
    assert fetcher.is_available_for_request("quote") is False


@pytest.mark.unit
def test_connection_error_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.LongbridgeFetcher()

    assert fetcher._is_connection_error(Exception("Client is closed")) is True
    assert fetcher._is_connection_error(Exception("normal error")) is False
