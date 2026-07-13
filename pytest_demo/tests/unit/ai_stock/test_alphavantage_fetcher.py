from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any, Dict, Optional

import pytest


MODULE_NAME = "ai_stock.stock_data.alphavantage_fetcher"


class _FakeIndex(list):
    def __init__(self, values: list[Any]):
        super().__init__(values)
        self.name = None


class _FakeDataFrame:
    def __init__(self, rows: Optional[list[dict[str, Any]]] = None, **kwargs: Any) -> None:
        self.rows = list(rows or [])
        self.index = None

    @property
    def empty(self) -> bool:
        return len(self.rows) == 0

    def __getitem__(self, key: str) -> list[Any]:
        return [row.get(key) for row in self.rows]

    def drop(self, columns: list[str]) -> "_FakeDataFrame":
        for row in self.rows:
            for col in columns:
                row.pop(col, None)
        return self


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
    module.to_datetime = lambda values, *args, **kwargs: _FakeIndex(list(values))
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
    src_config_module.get_config = lambda: SimpleNamespace(alphavantage_api_key=config_key)

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
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "env-key")
    module = _load_module(monkeypatch, config_key=None)

    fetcher = module.AlphaVantageFetcher()
    assert fetcher._api_key == "env-key"


@pytest.mark.unit
def test_fetch_raw_data_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    module = _load_module(monkeypatch, config_key=None)

    fetcher = module.AlphaVantageFetcher()
    with pytest.raises(module.DataFetchError, match="API key not configured"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_fetch_raw_data_rejects_non_us_symbol(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    fetcher = module.AlphaVantageFetcher()
    with pytest.raises(module.DataFetchError, match="is not a US stock"):
        fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_fetch_raw_data_parses_and_filters_date_range(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    captured_params: Dict[str, Any] = {}
    payload = {
        "Time Series (Daily)": {
            "2026-01-03": {
                "1. open": "10",
                "2. high": "11",
                "3. low": "9",
                "4. close": "10.5",
                "5. volume": "1000",
            },
            "2025-12-31": {
                "1. open": "8",
                "2. high": "9",
                "3. low": "7",
                "4. close": "8.5",
                "5. volume": "800",
            },
        }
    }

    def _fake_get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 0) -> _DummyResponse:
        captured_params.update(params or {})
        assert url == module._AV_BASE_URL
        assert timeout == 30
        return _DummyResponse(payload)

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.AlphaVantageFetcher()
    df = fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-05")

    assert isinstance(df, _FakeDataFrame)
    assert len(df.rows) == 1
    assert "date" not in df.rows[0]
    assert captured_params["function"] == "TIME_SERIES_DAILY"
    assert captured_params["symbol"] == "AAPL"
    assert captured_params["apikey"] == "test-key"


@pytest.mark.unit
def test_fetch_raw_data_handles_rate_limit_note(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse({"Note": "slow down"}))

    fetcher = module.AlphaVantageFetcher()
    with pytest.raises(module.DataFetchError, match="Rate limited"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-05")


@pytest.mark.unit
def test_get_realtime_quote_returns_none_without_price(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse({"Global Quote": {}}))

    fetcher = module.AlphaVantageFetcher()
    assert fetcher.get_realtime_quote("AAPL") is None


@pytest.mark.unit
def test_get_realtime_quote_parses_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    payload = {
        "Global Quote": {
            "05. price": "123.45",
            "08. previous close": "120.00",
            "10. change percent": "2.88%",
            "09. change": "3.45",
            "06. volume": "345678",
            "02. open": "121.00",
            "03. high": "124.00",
            "04. low": "120.50",
        }
    }
    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse(payload))

    fetcher = module.AlphaVantageFetcher()
    quote = fetcher.get_realtime_quote("AAPL")

    assert quote is not None
    assert quote.code == "AAPL"
    assert quote.price == 123.45
    assert quote.change_pct == 2.88
    assert quote.volume == 345678


@pytest.mark.unit
def test_get_stock_name_parses_symbol_search(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")
    module = _load_module(monkeypatch)

    payload = {
        "bestMatches": [
            {"1. symbol": "MSFT", "2. name": "Microsoft"},
            {"1. symbol": "AAPL", "2. name": "Apple Inc."},
        ]
    }
    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _DummyResponse(payload))

    fetcher = module.AlphaVantageFetcher()
    assert fetcher.get_stock_name("aapl") == "Apple Inc."
