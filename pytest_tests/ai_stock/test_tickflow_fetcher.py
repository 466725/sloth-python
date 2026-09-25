from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.tickflow_fetcher"


class _FakeDataFrame:
    def __init__(self, data: Any = None, *args: Any, **kwargs: Any) -> None:
        self._data = data
        self.empty = not bool(data)


class _FakeQuotes:
    def __init__(self, return_quotes: Any = None, raise_exc: Exception | None = None) -> None:
        self._return_quotes = return_quotes
        self._raise_exc = raise_exc

    def get(self, **kwargs: Any):
        if self._raise_exc is not None:
            raise self._raise_exc
        return self._return_quotes


class _FakeClient:
    def __init__(self, quotes: Any = None) -> None:
        self.quotes = quotes or _FakeQuotes([])
        self.closed = False

    def close(self) -> None:
        self.closed = True


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")
    module.DataFrame = _FakeDataFrame
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class BaseFetcher:
        pass

    def normalize_stock_code(stock_code: str) -> str:
        raw = (stock_code or "").strip().upper()
        if "." in raw:
            raw = raw.split(".")[0]
        if raw.startswith(("SH", "SS", "SZ", "BJ")):
            raw = raw[2:]
        return re.sub(r"\D", "", raw)

    def is_bse_code(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return code.startswith(("8", "4", "920"))

    def is_kc_cy_stock(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return code.startswith(("688", "300", "301"))

    def is_st_stock(name: str) -> bool:
        return "ST" in str(name or "").upper()

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.normalize_stock_code = normalize_stock_code
    module.is_bse_code = is_bse_code
    module.is_kc_cy_stock = is_kc_cy_stock
    module.is_st_stock = is_st_stock
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_init_and_get_client_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key=None)

    assert fetcher.api_key == ""
    assert fetcher._get_client() is None


@pytest.mark.unit
def test_get_client_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key="abc")

    fake_client = _FakeClient()
    monkeypatch.setattr(fetcher, "_build_client", lambda: fake_client)

    c1 = fetcher._get_client()
    c2 = fetcher._get_client()
    assert c1 is fake_client
    assert c2 is fake_client


@pytest.mark.unit
def test_close_resets_client_and_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key="abc")

    fake_client = _FakeClient()
    fetcher._client = fake_client
    fetcher._universe_query_supported = False
    fetcher._universe_query_checked_at = 123.0

    fetcher.close()

    assert fake_client.closed is True
    assert fetcher._client is None
    assert fetcher._universe_query_supported is None
    assert fetcher._universe_query_checked_at is None


@pytest.mark.unit
def test_fetch_and_normalize_not_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key="abc")

    with pytest.raises(module.DataFetchError, match="market review"):
        fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-10")

    with pytest.raises(module.DataFetchError, match="market review"):
        fetcher._normalize_data(_FakeDataFrame([]), "600519")


@pytest.mark.unit
def test_helper_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module.TickFlowFetcher._safe_float("12.5") == 12.5
    assert module.TickFlowFetcher._safe_float("-") is None
    assert module.TickFlowFetcher._ratio_to_percent("0.25") == 25.0

    quote = {"ext": {"name": "  Test Name  "}}
    assert module.TickFlowFetcher._extract_name(quote) == "Test Name"

    assert module.TickFlowFetcher._is_cn_equity_symbol("600519.SH") is True
    assert module.TickFlowFetcher._is_cn_equity_symbol("AAPL.US") is False

    assert module.TickFlowFetcher._round_limit_price(10.0, 0.1) == 11.0
    assert module.TickFlowFetcher._get_limit_ratio("920001", "普通") == 0.30
    assert module.TickFlowFetcher._get_limit_ratio("688001", "普通") == 0.20
    assert module.TickFlowFetcher._get_limit_ratio("600001", "*ST示例") == 0.05
    assert module.TickFlowFetcher._get_limit_ratio("600001", "普通") == 0.10


@pytest.mark.unit
def test_universe_permission_error_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    exc1 = type("E", (), {"status_code": 403, "code": "", "message": ""})()
    exc2 = type("E", (), {"status_code": None, "code": "forbidden", "message": ""})()
    exc3 = Exception("permission denied for universe query")

    assert module.TickFlowFetcher._is_universe_permission_error(exc1) is True
    assert module.TickFlowFetcher._is_universe_permission_error(exc2) is True
    assert module.TickFlowFetcher._is_universe_permission_error(exc3) is True


@pytest.mark.unit
def test_get_main_indices_region_and_missing_data(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key="abc")

    assert fetcher.get_main_indices(region="us") is None

    # missing client
    monkeypatch.setattr(fetcher, "_get_client", lambda: None)
    assert fetcher.get_main_indices(region="cn") is None


@pytest.mark.unit
def test_get_market_stats_permission_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TickFlowFetcher(api_key="abc")

    class _PermissionExc(Exception):
        status_code = 403
        code = "FORBIDDEN"
        message = "permission denied"

    fake_client = _FakeClient(quotes=_FakeQuotes(raise_exc=_PermissionExc("denied")))
    monkeypatch.setattr(fetcher, "_get_client", lambda: fake_client)

    first = fetcher.get_market_stats()
    second = fetcher.get_market_stats()

    assert first is None
    assert second is None
    assert fetcher._universe_query_supported is False
