from __future__ import annotations

import importlib
import json
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any, Optional

import pytest


MODULE_NAME = "ai_stock.stock_data.tushare_fetcher"


class _FakeDataFrame:
    def __init__(self, data: Any = None, columns: Any = None, *args: Any, **kwargs: Any) -> None:
        self.data = data
        self.columns = list(columns or [])
        self.empty = not bool(data)


class _DummyResponse:
    def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
        self.status_code = status_code
        self.text = json.dumps(payload)


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
    module.DataFrame = _FakeDataFrame
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class RateLimitError(Exception):
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

    def is_st_stock(name: str) -> bool:
        return "ST" in str(name or "").upper()

    def is_kc_cy_stock(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return code.startswith(("688", "300", "301"))

    def _is_hk_market(stock_code: str) -> bool:
        text = (stock_code or "").strip().upper()
        if text.startswith("HK") or text.endswith(".HK"):
            return True
        return text.isdigit() and len(text) == 5

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.RateLimitError = RateLimitError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.is_bse_code = is_bse_code
    module.is_st_stock = is_st_stock
    module.is_kc_cy_stock = is_kc_cy_stock
    module.normalize_stock_code = normalize_stock_code
    module._is_hk_market = _is_hk_market
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class ChipDistribution:
        pass

    module.UnifiedRealtimeQuote = UnifiedRealtimeQuote
    module.ChipDistribution = ChipDistribution
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch, *, token: Optional[str] = None):
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")
    src_config_module.get_config = lambda: SimpleNamespace(tushare_token=token)

    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)
    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_top_level_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._is_etf_code("510050") is True
    assert module._is_etf_code("600519") is False
    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_tushare_http_client_query_success(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    def _fake_post(url: str, json: dict[str, Any], timeout: int):
        assert url == "http://api.tushare.pro"
        assert json["api_name"] == "daily"
        assert timeout == 30
        payload = {
            "code": 0,
            "metadata": {
                "fields": ["ts_code", "trade_date"],
                "items": [["600519.SH", "20260101"]],
            },
        }
        return _DummyResponse(200, payload)

    monkeypatch.setattr(module.requests, "post", _fake_post)

    client = module._TushareHttpClient(token="token")
    df = client.query("daily", ts_code="600519.SH")

    assert isinstance(df, _FakeDataFrame)
    assert df.columns == ["ts_code", "trade_date"]
    assert df.data == [["600519.SH", "20260101"]]


@pytest.mark.unit
def test_tushare_http_client_query_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    monkeypatch.setattr(module.requests, "post", lambda *args, **kwargs: _DummyResponse(500, {"code": 0}))
    client = module._TushareHttpClient(token="token")

    with pytest.raises(Exception, match="HTTP 500"):
        client.query("daily", ts_code="600519.SH")


@pytest.mark.unit
def test_fetcher_init_and_availability(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch, token=None)
    fetcher = module.TushareFetcher()

    assert fetcher.is_available() is False
    assert fetcher.priority == 2

    module = _load_module(monkeypatch, token="ts-token")
    fetcher = module.TushareFetcher()
    assert fetcher.is_available() is True
    assert fetcher.priority == -1


@pytest.mark.unit
def test_convert_stock_code(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TushareFetcher()

    assert fetcher._convert_stock_code("600519") == "600519.SH"
    assert fetcher._convert_stock_code("159919") == "159919.SZ"
    assert fetcher._convert_stock_code("920001") == "920001.BJ"
    assert fetcher._convert_stock_code("600519.SS") == "600519.SH"
    assert fetcher._convert_stock_code("HK00700") == "00700"

    with pytest.raises(module.DataFetchError, match="美股"):
        fetcher._convert_stock_code("AAPL")


@pytest.mark.unit
def test_convert_hk_stock_code_for_tushare(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TushareFetcher()

    assert fetcher._convert_hk_stock_code_for_tushare("HK00700") == "00700.HK"
    assert fetcher._convert_hk_stock_code_for_tushare("00700.HK") == "00700.HK"
    assert fetcher._convert_hk_stock_code_for_tushare("600519") == "600519.SH"


@pytest.mark.unit
def test_get_legacy_realtime_symbol(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module.TushareFetcher._get_legacy_realtime_symbol("SH000001") == "sh000001"
    assert module.TushareFetcher._get_legacy_realtime_symbol("399001") == "sz399001"
    assert module.TushareFetcher._get_legacy_realtime_symbol("920001") == "bj920001"
    assert module.TushareFetcher._get_legacy_realtime_symbol("600519") == "600519"


@pytest.mark.unit
def test_fetch_raw_data_routing_and_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TushareFetcher()

    with pytest.raises(module.DataFetchError, match="未初始化"):
        fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-31")

    fetcher._api = SimpleNamespace(
        daily=lambda **kwargs: {"route": "daily", **kwargs},
        fund_daily=lambda **kwargs: {"route": "fund_daily", **kwargs},
        hk_daily=lambda **kwargs: {"route": "hk_daily", **kwargs},
    )

    called = {"count": 0}

    def _fake_check_rate_limit() -> None:
        called["count"] += 1

    monkeypatch.setattr(fetcher, "_check_rate_limit", _fake_check_rate_limit)

    with pytest.raises(module.DataFetchError, match="美股"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-31")

    etf = fetcher._fetch_raw_data("510050", "2026-01-01", "2026-01-31")
    assert etf["route"] == "fund_daily"

    hk = fetcher._fetch_raw_data("HK00700", "2026-01-01", "2026-01-31")
    assert hk["route"] == "hk_daily"
    assert hk["ts_code"] == "00700.HK"

    stock = fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-31")
    assert stock["route"] == "daily"
    assert stock["ts_code"] == "600519.SH"

    assert called["count"] == 3


@pytest.mark.unit
def test_fetch_raw_data_rate_limit_error_translation(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TushareFetcher()

    fetcher._api = SimpleNamespace(
        daily=lambda **kwargs: (_ for _ in ()).throw(Exception("quota exceeded")),
        fund_daily=lambda **kwargs: None,
        hk_daily=lambda **kwargs: None,
    )
    monkeypatch.setattr(fetcher, "_check_rate_limit", lambda: None)

    with pytest.raises(module.RateLimitError, match="配额"):
        fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-31")


@pytest.mark.unit
def test_pick_trade_date(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module.TushareFetcher._pick_trade_date([], use_today=True) is None
    assert module.TushareFetcher._pick_trade_date(["20260110"], use_today=False) == "20260110"
    assert module.TushareFetcher._pick_trade_date(["20260110", "20260109"], use_today=False) == "20260109"
    assert module.TushareFetcher._pick_trade_date(["20260110", "20260109"], use_today=True) == "20260110"
