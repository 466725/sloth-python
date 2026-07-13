from __future__ import annotations

import importlib
import re
import sys
import time
from types import ModuleType
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.pytdx_fetcher"


def _make_tenacity_stub() -> ModuleType:
    module = ModuleType("tenacity")

    def _retry(*args: Any, **kwargs: Any):
        def _decorator(func):
            return func

        return _decorator

    def _noop(*args: Any, **kwargs: Any):
        return None

    module.retry = _retry
    module.stop_after_attempt = _noop
    module.wait_exponential = _noop
    module.retry_if_exception_type = _noop
    module.before_sleep_log = _noop
    return module


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")

    class DataFrame:
        def __init__(self, data: Any = None, *args: Any, **kwargs: Any) -> None:
            self._data = data
            self.empty = not bool(data)

    module.DataFrame = DataFrame
    module.to_datetime = lambda *args, **kwargs: None
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class DataSourceUnavailableError(Exception):
        pass

    class BaseFetcher:
        @staticmethod
        def random_sleep(*args: Any, **kwargs: Any) -> None:
            return None

    def normalize_stock_code(stock_code: str) -> str:
        raw = (stock_code or "").strip()
        if "." in raw:
            raw = raw.split(".")[0]
        if raw.upper().startswith(("SH", "SS", "SZ", "BJ", "HK")):
            raw = raw[2:]
        return re.sub(r"\D", "", raw)

    def is_bse_code(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return code.startswith(("8", "4", "920"))

    def _is_hk_market(stock_code: str) -> bool:
        text = (stock_code or "").strip().upper()
        return text.startswith("HK") or text.endswith(".HK") or (text.isdigit() and len(text) == 5)

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.DataSourceUnavailableError = DataSourceUnavailableError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.is_bse_code = is_bse_code
    module.normalize_stock_code = normalize_stock_code
    module._is_hk_market = _is_hk_market
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_parse_hosts_from_env_prefers_servers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("PYTDX_SERVERS", "127.0.0.1:7709,10.0.0.1:7710")
    monkeypatch.delenv("PYTDX_HOST", raising=False)
    monkeypatch.delenv("PYTDX_PORT", raising=False)

    hosts = module._parse_hosts_from_env()
    assert hosts == [("127.0.0.1", 7709), ("10.0.0.1", 7710)]


@pytest.mark.unit
def test_parse_hosts_from_env_falls_back_to_host_port(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("PYTDX_SERVERS", "")
    monkeypatch.setenv("PYTDX_HOST", "192.168.1.8")
    monkeypatch.setenv("PYTDX_PORT", "7727")

    hosts = module._parse_hosts_from_env()
    assert hosts == [("192.168.1.8", 7727)]


@pytest.mark.unit
def test_is_us_code_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("BRK.B") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_init_uses_env_hosts_when_not_provided(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setenv("PYTDX_SERVERS", "127.0.0.1:7709")
    fetcher = module.PytdxFetcher()
    assert fetcher._hosts == [("127.0.0.1", 7709)]


@pytest.mark.unit
def test_get_market_code_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.PytdxFetcher(hosts=[("127.0.0.1", 7709)])

    assert fetcher._get_market_code("600519") == (1, "600519")
    assert fetcher._get_market_code("000001") == (0, "000001")
    assert fetcher._get_market_code("sh.600519") == (1, "600519")
    assert fetcher._get_market_code("SZ000001") == (0, "000001")


@pytest.mark.unit
def test_cooldown_logic(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.PytdxFetcher(hosts=[("127.0.0.1", 7709)])

    assert fetcher.is_available_for_request("history") is True
    fetcher._mark_connection_cooldown("connect failed")
    assert fetcher.is_available_for_request("history") is False

    fetcher._unavailable_until = time.time() - 1
    assert fetcher.is_available_for_request("history") is True


@pytest.mark.unit
def test_fetch_raw_data_guard_rails(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.PytdxFetcher(hosts=[("127.0.0.1", 7709)])

    with pytest.raises(module.DataFetchError, match="美股"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-31")

    with pytest.raises(module.DataFetchError, match="港股"):
        fetcher._fetch_raw_data("HK00700", "2026-01-01", "2026-01-31")

    with pytest.raises(module.DataFetchError, match="北交所"):
        fetcher._fetch_raw_data("920001", "2026-01-01", "2026-01-31")


@pytest.mark.unit
def test_get_stock_name_hk_returns_none_and_cache_hit(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.PytdxFetcher(hosts=[("127.0.0.1", 7709)])

    assert fetcher.get_stock_name("HK00700") is None

    fetcher._stock_name_cache["600519"] = "Kweichow Moutai"
    assert fetcher.get_stock_name("600519") == "Kweichow Moutai"


@pytest.mark.unit
def test_get_realtime_quote_bse_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.PytdxFetcher(hosts=[("127.0.0.1", 7709)])

    with pytest.raises(module.DataFetchError, match="北交所"):
        fetcher.get_realtime_quote("920001")
