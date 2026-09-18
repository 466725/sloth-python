from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any, Dict, Optional

import pytest


MODULE_NAME = "ai_stock.stock_data.finnhub_fetcher"


class _FakeDataFrame:
    def __init__(self, data: Any = None, *args: Any, **kwargs: Any) -> None:
        self.data = data or {}
        self.empty = not bool(data)


class _DummyResponse:
    def __init__(self, payload: Any, should_raise: bool = False) -> None:
        self._payload = payload
        self._should_raise = should_raise

    def raise_for_status(self) -> None:
        if self._should_raise:
            raise RuntimeError("http error")

    def json(self) -> Any:
        return self._payload


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")
    module.DataFrame = _FakeDataFrame
    module.to_datetime = lambda *args, **kwargs: None
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class BaseFetcher:
        @staticmethod
        def random_sleep(*args: Any, **kwargs: Any) -> None:
            return None

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class RealtimeSource:
        FALLBACK = "fallback"

    module.UnifiedRealtimeQuote = UnifiedRealtimeQuote
    module.RealtimeSource = RealtimeSource
    return module


def _make_us_index_mapping_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.us_index_mapping")
    module.is_us_stock_code = lambda code: bool(re.match(r"^[A-Z]{1,5}(\.[A-Z])?$", str(code or "").strip().upper()))
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch, *, config_key: Optional[str] = None):
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")
    src_config_module.get_config = lambda: SimpleNamespace(finnhub_api_key=config_key)

    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.us_index_mapping", _make_us_index_mapping_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_init_reads_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "env-key")
    module = _load_module(monkeypatch, config_key=None)

    fetcher = module.FinnhubFetcher()
    assert fetcher._api_key == "env-key"


@pytest.mark.unit
def test_fetch_raw_data_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    module = _load_module(monkeypatch, config_key=None)

    fetcher = module.FinnhubFetcher()
    with pytest.raises(module.DataFetchError, match="API key not configured"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_fetch_raw_data_rejects_non_us_symbol(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    fetcher = module.FinnhubFetcher()
    with pytest.raises(module.DataFetchError, match="not a US stock"):
        fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_fetch_raw_data_parses_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    captured_params: Dict[str, Any] = {}
    payload = {
        "s": "ok",
        "c": [101.0, 102.5],
        "h": [103.0, 104.0],
        "l": [99.0, 100.5],
        "o": [100.0, 101.0],
        "t": [1780000000, 1780086400],
        "v": [1200000, 1500000],
    }

    def _fake_get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 0) -> _DummyResponse:
        captured_params.update(params or {})
        assert url == f"{module._FINNHUB_BASE_URL}/stock/candle"
        assert timeout == 15
        return _DummyResponse(payload)

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.FinnhubFetcher()
    df = fetcher._fetch_raw_data("aapl", "2026-01-01", "2026-01-10")

    assert isinstance(df, _FakeDataFrame)
    assert set(df.data.keys()) == {"c", "h", "l", "o", "t", "v"}
    assert captured_params["symbol"] == "AAPL"
    assert captured_params["resolution"] == "D"
    assert captured_params["token"] == "test-key"


@pytest.mark.unit
def test_fetch_raw_data_handles_empty_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse({"s": "no_data", "c": []}))

    fetcher = module.FinnhubFetcher()
    with pytest.raises(module.DataFetchError, match="No metadata returned"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_get_realtime_quote_returns_none_when_price_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse({"c": 0}))

    fetcher = module.FinnhubFetcher()
    assert fetcher.get_realtime_quote("AAPL") is None


@pytest.mark.unit
def test_get_realtime_quote_parses_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    payload = {
        "c": 150.25,
        "pc": 145.0,
        "dp": 3.62,
        "d": 5.25,
        "h": 151.0,
        "l": 148.5,
        "o": 149.2,
        "v": 2300000,
    }
    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse(payload))

    fetcher = module.FinnhubFetcher()
    quote = fetcher.get_realtime_quote("aapl")

    assert quote is not None
    assert quote.code == "AAPL"
    assert quote.price == 150.25
    assert quote.change_pct == 3.62
    assert quote.change_amount == 5.25
    assert quote.amplitude == round((151.0 - 148.5) / 145.0 * 100, 2)


@pytest.mark.unit
def test_get_stock_name_parses_symbol_search(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    payload = {
        "result": [
            {"symbol": "MSFT", "description": "Microsoft"},
            {"symbol": "AAPL", "description": "Apple Inc."},
        ]
    }
    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse(payload))

    fetcher = module.FinnhubFetcher()
    assert fetcher.get_stock_name("aapl") == "Apple Inc."
