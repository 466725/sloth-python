from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any, Optional

import pytest


MODULE_NAME = "ai_stock.stock_data.yfinance_fetcher"


class _DummyUrlopenResponse:
    def __init__(self, payload: str) -> None:
        self._payload = payload.encode("utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _HistoryIloc:
    def __init__(self, rows: list[dict[str, float]]) -> None:
        self._rows = rows

    def __getitem__(self, idx: int) -> dict[str, float]:
        return self._rows[idx]


class _History:
    def __init__(self, rows: list[dict[str, float]]) -> None:
        self._rows = rows
        self.empty = len(rows) == 0
        self.iloc = _HistoryIloc(rows)

    def __len__(self) -> int:
        return len(self._rows)


class _FakeTicker:
    def __init__(self, *, fast_info: Any = None, info: Optional[dict[str, Any]] = None, history_rows=None) -> None:
        self._fast_info = fast_info
        self.info = info or {}
        self._history_rows = list(history_rows or [])

    @property
    def fast_info(self):
        return self._fast_info

    def history(self, period: str = "2d") -> _History:
        return _History(self._history_rows)


def _make_tenacity_stub() -> ModuleType:
    module = ModuleType("tenacity")

    def _retry(*args: Any, **kwargs: Any):
        def _decorator(func):
            return func

        return _decorator

    def _noop(*args: Any, **kwargs: Any) -> None:
        return None

    module.retry = _retry
    module.stop_after_attempt = _noop
    module.wait_exponential = _noop
    module.retry_if_exception_type = _noop
    module.before_sleep_log = _noop
    return module


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")
    module.DataFrame = object
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class BaseFetcher:
        @staticmethod
        def random_sleep(*args: Any, **kwargs: Any) -> None:
            return None

    def is_bse_code(stock_code: str) -> bool:
        code = (stock_code or "").strip().upper().replace(".", "")
        code = re.sub(r"\D", "", code)
        return code.startswith(("8", "4", "920"))

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.is_bse_code = is_bse_code
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class RealtimeSource:
        FALLBACK = "fallback"
        STOOQ = "stooq"

    module.UnifiedRealtimeQuote = UnifiedRealtimeQuote
    module.RealtimeSource = RealtimeSource
    return module


def _make_us_index_mapping_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.us_index_mapping")

    def get_us_index_yf_symbol(code: str):
        mapping = {
            "SPX": ("^GSPC", "标普500"),
            "DJI": ("^DJI", "道琼斯"),
        }
        return mapping.get((code or "").strip().upper(), (None, None))

    def is_us_stock_code(code: str) -> bool:
        return bool(re.match(r"^[A-Z]{1,5}(\.[A-Z])?$", str(code or "").strip().upper()))

    module.get_us_index_yf_symbol = get_us_index_yf_symbol
    module.is_us_stock_code = is_us_stock_code
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.us_index_mapping", _make_us_index_mapping_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


def _install_yfinance_stub(monkeypatch: pytest.MonkeyPatch, ticker_factory) -> None:
    module = ModuleType("yfinance")
    module.Ticker = ticker_factory
    module.download = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "yfinance", module)


@pytest.mark.unit
def test_is_jp_kr_suffix_stock(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.YfinanceFetcher()

    assert fetcher._is_jp_kr_suffix_stock("7203.T") is True
    assert fetcher._is_jp_kr_suffix_stock("005930.KS") is True
    assert fetcher._is_jp_kr_suffix_stock("005930.KQ") is True
    assert fetcher._is_jp_kr_suffix_stock("AAPL") is False


@pytest.mark.unit
def test_convert_stock_code_cases(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.YfinanceFetcher()

    assert fetcher._convert_stock_code("SPX") == "^GSPC"
    assert fetcher._convert_stock_code("AAPL") == "AAPL"
    assert fetcher._convert_stock_code("7203.T") == "7203.T"
    assert fetcher._convert_stock_code("hk00700") == "0700.HK"
    assert fetcher._convert_stock_code("600519.SH") == "600519.SS"
    assert fetcher._convert_stock_code("510050") == "510050.SS"
    assert fetcher._convert_stock_code("159919") == "159919.SZ"
    assert fetcher._convert_stock_code("920001") == "920001.BJ"
    assert fetcher._convert_stock_code("600519") == "600519.SS"
    assert fetcher._convert_stock_code("300750") == "300750.SZ"


@pytest.mark.unit
def test_fetch_yf_ticker_data_success(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.YfinanceFetcher()

    ticker = _FakeTicker(
        history_rows=[
            {"Close": 100.0, "High": 101.0, "Low": 99.0, "Open": 99.5, "Volume": 1000.0},
            {"Close": 102.0, "High": 104.0, "Low": 98.0, "Open": 100.0, "Volume": 1200.0},
        ]
    )
    yf_stub = SimpleNamespace(Ticker=lambda symbol: ticker)

    item = fetcher._fetch_yf_ticker_data(yf_stub, "000001.SS", "上证指数", "sh000001")

    assert item is not None
    assert item["code"] == "sh000001"
    assert item["current"] == 102.0
    assert item["change"] == 2.0
    assert round(item["change_pct"], 2) == 2.0
    assert round(item["amplitude"], 2) == 6.0


@pytest.mark.unit
def test_get_realtime_quote_non_us_non_suffix_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    _install_yfinance_stub(monkeypatch, ticker_factory=lambda symbol: _FakeTicker())

    fetcher = module.YfinanceFetcher()
    assert fetcher.get_realtime_quote("600519") is None


@pytest.mark.unit
def test_get_realtime_quote_us_index_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    _install_yfinance_stub(monkeypatch, ticker_factory=lambda symbol: _FakeTicker())

    fetcher = module.YfinanceFetcher()
    monkeypatch.setattr(
        fetcher,
        "_get_us_index_realtime_quote",
        lambda user_code, yf_symbol, index_name: {"code": user_code, "yf": yf_symbol, "name": index_name},
    )

    quote = fetcher.get_realtime_quote("SPX")
    assert quote == {"code": "SPX", "yf": "^GSPC", "name": "标普500"}


@pytest.mark.unit
def test_get_realtime_quote_fast_info_success(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    ticker = _FakeTicker(
        fast_info=SimpleNamespace(
            lastPrice=151.0,
            previousClose=145.0,
            open=149.0,
            dayHigh=152.0,
            dayLow=148.0,
            lastVolume=2300000,
            marketCap=3000000000,
        ),
        info={"shortName": "Apple Inc."},
    )
    _install_yfinance_stub(monkeypatch, ticker_factory=lambda symbol: ticker)

    fetcher = module.YfinanceFetcher()
    quote = fetcher.get_realtime_quote("AAPL")

    assert quote is not None
    assert quote.code == "AAPL"
    assert quote.name == "Apple Inc."
    assert quote.price == 151.0
    assert quote.change_amount == 6.0
    assert quote.change_pct == round((6.0 / 145.0) * 100, 2)
    assert quote.amplitude == round((152.0 - 148.0) / 145.0 * 100, 2)
    assert quote.total_mv == 3000000000


@pytest.mark.unit
def test_get_realtime_quote_history_empty_uses_stooq_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    class _BrokenFastInfoTicker(_FakeTicker):
        @property
        def fast_info(self):
            raise RuntimeError("fast_info failed")

    ticker = _BrokenFastInfoTicker(history_rows=[])
    _install_yfinance_stub(monkeypatch, ticker_factory=lambda symbol: ticker)

    fetcher = module.YfinanceFetcher()
    monkeypatch.setattr(fetcher, "_get_us_stock_quote_from_stooq", lambda symbol: {"code": symbol, "from": "stooq"})

    quote = fetcher.get_realtime_quote("MSFT")
    assert quote == {"code": "MSFT", "from": "stooq"}


@pytest.mark.unit
def test_get_us_stock_quote_from_stooq_parses_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.YfinanceFetcher()

    payload_realtime = "Symbol,Date,Time,Open,High,Low,Close,Volume\nAAPL.US,2026-01-10,22:00:00,149.0,151.0,148.0,150.0,123456"
    payload_history = "Date,Open,High,Low,Close,Volume\n2026-01-09,147,149,146,148,100\n2026-01-10,149,151,148,150,110"

    calls = {"count": 0}

    def _fake_urlopen(request: Any, timeout: int = 15):
        calls["count"] += 1
        assert timeout == 15
        if calls["count"] == 1:
            return _DummyUrlopenResponse(payload_realtime)
        return _DummyUrlopenResponse(payload_history)

    monkeypatch.setattr(module, "urlopen", _fake_urlopen)

    quote = fetcher._get_us_stock_quote_from_stooq("aapl")

    assert quote is not None
    assert quote.code == "AAPL"
    assert quote.source == module.RealtimeSource.STOOQ
    assert quote.price == 150.0
    assert quote.pre_close == 148.0
    assert quote.change_amount == 2.0
    assert quote.change_pct == round((2.0 / 148.0) * 100, 2)
    assert quote.amplitude == round((151.0 - 148.0) / 148.0 * 100, 2)
    assert quote.volume == 123456
