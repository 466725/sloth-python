from __future__ import annotations

import importlib
import re
import sys
from datetime import datetime
from types import ModuleType
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.tencent_fetcher"


class _FakeDataFrame:
    def __init__(self, data: Any = None, columns: Any = None, *args: Any, **kwargs: Any) -> None:
        self.data = data
        self.columns = list(columns or [])
        self.empty = not bool(data)


def _make_pandas_stub() -> ModuleType:
    module = ModuleType("pandas")
    module.DataFrame = _FakeDataFrame
    module.to_datetime = lambda *args, **kwargs: []
    module.to_numeric = lambda value, errors=None: value
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class BaseFetcher:
        pass

    def normalize_stock_code(stock_code: str) -> str:
        raw = (stock_code or "").strip()
        if "." in raw:
            raw = raw.split(".")[0]
        if raw.upper().startswith(("SH", "SZ", "SS", "BJ", "HK")):
            raw = raw[2:]
        return re.sub(r"\D", "", raw)

    def is_bse_code(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return code.startswith(("8", "4", "920"))

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.normalize_stock_code = normalize_stock_code
    module.is_bse_code = is_bse_code
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())

    sys.modules.pop(MODULE_NAME, None)
    return importlib.import_module(MODULE_NAME)


@pytest.mark.unit
def test_to_tencent_symbol_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._to_tencent_symbol("600519") == "sh600519"
    assert module._to_tencent_symbol("510050") == "sh510050"
    assert module._to_tencent_symbol("000001") == "sz000001"
    assert module._to_tencent_symbol("920001") == "bj920001"
    assert module._to_tencent_symbol("AAPL") == ""


@pytest.mark.unit
def test_estimate_lookback_days(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._estimate_lookback_days(start_date="2026-01-01", end_date="2026-01-05") >= 30
    assert module._estimate_lookback_days(start_date="invalid", end_date="invalid") == 182


@pytest.mark.unit
def test_format_tencent_date(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._format_tencent_date("2026-07-13") == "2026-07-13"
    assert module._format_tencent_date("2026/07/13") is None


@pytest.mark.unit
def test_lots_to_shares(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._lots_to_shares("12") == 1200.0
    assert module._lots_to_shares(1.5) == 150.0
    assert module._lots_to_shares("x") == "x"


@pytest.mark.unit
def test_extract_kline_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    payload = {
        "metadata": {
            "sh600519": {
                "qfqday": [
                    ["2026-01-02", "10", "11", "12", "9", "100", "10000"],
                    ["2026-01-03", "11", "12", "13", "10", "200"],
                ]
            }
        }
    }
    rows = module._extract_kline_rows(payload, symbol="sh600519")

    assert len(rows) == 2
    assert rows[0]["date"] == "2026-01-02"
    assert rows[0]["volume"] == 10000.0
    assert rows[0]["amount"] == "10000"
    assert rows[1]["amount"] is None


@pytest.mark.unit
def test_extract_kline_rows_handles_invalid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._extract_kline_rows({}, symbol="sh600519") == []
    assert module._extract_kline_rows({"metadata": {}}, symbol="sh600519") == []


@pytest.mark.unit
def test_is_capped_history_incomplete(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._is_capped_history_incomplete(
        first_returned_date="2026-02-01",
        start_date="2026-01-01",
        lookback=800,
        returned_rows=800,
    ) is True

    assert module._is_capped_history_incomplete(
        first_returned_date="2026-01-01",
        start_date="2026-01-01",
        lookback=100,
        returned_rows=100,
    ) is False


@pytest.mark.unit
def test_first_trading_date_on_or_after_weekend(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    saturday = datetime(2026, 1, 3)
    result = module._first_trading_date_on_or_after(saturday)
    assert result.weekday() < 5


@pytest.mark.unit
def test_fetch_raw_data_rejects_unsupported_code(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.TencentFetcher()

    with pytest.raises(module.DataFetchError, match="unsupported stock code"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-31")


@pytest.mark.unit
def test_empty_daily_frame_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    df = module._empty_daily_frame()
    assert isinstance(df, _FakeDataFrame)
    assert df.columns == module.STANDARD_COLUMNS
