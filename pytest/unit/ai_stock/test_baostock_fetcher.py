from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType
from typing import Any, Optional

import pytest


MODULE_NAME = "ai_stock.stock_data.baostock_fetcher"


class _FakeDataFrame:
    def __init__(self, data: Optional[list[Any]] = None, columns: Optional[list[str]] = None, **kwargs: Any) -> None:
        self.data = list(data or [])
        self.columns = list(columns or [])
        self.empty = len(self.data) == 0


class _DummyResult:
    def __init__(self, rows: list[list[str]], fields: list[str], error_code: str = "0", error_msg: str = "") -> None:
        self._rows = rows
        self.fields = fields
        self.error_code = error_code
        self.error_msg = error_msg
        self._idx = -1

    def next(self) -> bool:
        self._idx += 1
        return self._idx < len(self._rows)

    def get_row_data(self) -> list[str]:
        return self._rows[self._idx]


class _DummyStatus:
    def __init__(self, error_code: str = "0", error_msg: str = "") -> None:
        self.error_code = error_code
        self.error_msg = error_msg


class _FakeBaoStockModule:
    def __init__(
        self,
        *,
        login_error_code: str = "0",
        login_error_msg: str = "",
        history_result: Optional[_DummyResult] = None,
        stock_basic_result: Optional[_DummyResult] = None,
    ) -> None:
        self.login_error_code = login_error_code
        self.login_error_msg = login_error_msg
        self.history_result = history_result
        self.stock_basic_result = stock_basic_result
        self.login_calls = 0
        self.logout_calls = 0
        self.query_history_calls = 0
        self.query_stock_basic_calls = 0

    def login(self) -> _DummyStatus:
        self.login_calls += 1
        return _DummyStatus(self.login_error_code, self.login_error_msg)

    def logout(self) -> _DummyStatus:
        self.logout_calls += 1
        return _DummyStatus("0", "")

    def query_history_k_data_plus(self, **kwargs: Any) -> _DummyResult:
        self.query_history_calls += 1
        if self.history_result is None:
            return _DummyResult([], [], error_code="1", error_msg="no history configured")
        return self.history_result

    def query_stock_basic(self, **kwargs: Any) -> _DummyResult:
        self.query_stock_basic_calls += 1
        if self.stock_basic_result is None:
            return _DummyResult([], [], error_code="1", error_msg="no stock basic configured")
        return self.stock_basic_result


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
        s = (stock_code or "").strip().upper()
        if s.startswith("HK"):
            return True
        if s.endswith(".HK"):
            return True
        return s.isdigit() and len(s) == 5

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
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
def test_is_us_code_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)

    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("BRK.B") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_convert_stock_code(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.BaostockFetcher()

    assert fetcher._convert_stock_code("600519") == "sh.600519"
    assert fetcher._convert_stock_code("000001") == "sz.000001"
    assert fetcher._convert_stock_code("510050") == "sh.510050"
    assert fetcher._convert_stock_code("159919") == "sz.159919"

    with pytest.raises(module.DataFetchError, match="does not support|不支持"):
        fetcher._convert_stock_code("HK00700")


@pytest.mark.unit
def test_baostock_session_login_failure_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fake_bs = _FakeBaoStockModule(login_error_code="1", login_error_msg="login failed")
    monkeypatch.setitem(sys.modules, "baostock", fake_bs)

    fetcher = module.BaostockFetcher()

    with pytest.raises(module.DataFetchError, match="login|登录"):
        with fetcher._baostock_session():
            pass

    assert fake_bs.login_calls == 1
    assert fake_bs.logout_calls == 1


@pytest.mark.unit
def test_fetch_raw_data_success(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    history = _DummyResult(
        rows=[["2026-01-02", "10", "11", "9", "10.5", "1000", "10000", "1.2"]],
        fields=["date", "open", "high", "low", "close", "volume", "amount", "pctChg"],
    )
    fake_bs = _FakeBaoStockModule(history_result=history)
    monkeypatch.setitem(sys.modules, "baostock", fake_bs)

    fetcher = module.BaostockFetcher()
    df = fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-10")

    assert isinstance(df, _FakeDataFrame)
    assert len(df.data) == 1
    assert fake_bs.query_history_calls == 1


@pytest.mark.unit
def test_fetch_raw_data_rejects_us_hk_bj(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    fetcher = module.BaostockFetcher()

    with pytest.raises(module.DataFetchError, match="US|美股"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-10")

    with pytest.raises(module.DataFetchError, match="HK|港股"):
        fetcher._fetch_raw_data("HK00700", "2026-01-01", "2026-01-10")

    with pytest.raises(module.DataFetchError, match="北交所|BSE"):
        fetcher._fetch_raw_data("920001", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_get_stock_name_success_and_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module(monkeypatch)
    stock_basic = _DummyResult(
        rows=[["sh.600519", "Kweichow Moutai"]],
        fields=["code", "code_name"],
    )
    fake_bs = _FakeBaoStockModule(stock_basic_result=stock_basic)
    monkeypatch.setitem(sys.modules, "baostock", fake_bs)

    fetcher = module.BaostockFetcher()

    first = fetcher.get_stock_name("600519")
    second = fetcher.get_stock_name("600519")

    assert first == "Kweichow Moutai"
    assert second == "Kweichow Moutai"
    assert fake_bs.query_stock_basic_calls == 1
