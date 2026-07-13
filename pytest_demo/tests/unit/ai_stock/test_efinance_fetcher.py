from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.efinance_fetcher"


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
            self.columns = []
            self.empty = not bool(data)

    module.DataFrame = DataFrame
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
        if raw.upper().startswith(("SH", "SZ", "SS", "BJ", "HK")):
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
        return text.startswith("HK") or text.endswith(".HK") or (text.isdigit() and len(text) == 5)

    def _is_etf_code(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return len(code) == 6 and code.startswith(("51", "52", "56", "58", "15", "16", "18"))

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.RateLimitError = RateLimitError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.is_bse_code = is_bse_code
    module.is_st_stock = is_st_stock
    module.is_kc_cy_stock = is_kc_cy_stock
    module.normalize_stock_code = normalize_stock_code
    module._is_hk_market = _is_hk_market
    module._is_etf_code = _is_etf_code
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class RealtimeSource:
        EFINANCE = "efinance"

    def safe_float(value: Any) -> Any:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def safe_int(value: Any) -> Any:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    module.UnifiedRealtimeQuote = UnifiedRealtimeQuote
    module.RealtimeSource = RealtimeSource
    module.get_realtime_circuit_breaker = lambda *args, **kwargs: SimpleNamespace(
        is_available=lambda key: True,
        record_success=lambda *a, **k: None,
        record_failure=lambda *a, **k: None,
    )
    module.safe_float = safe_float
    module.safe_int = safe_int
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch, *, enable_patch: bool = False):
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")
    src_patches_module = ModuleType("src.patches")
    src_patch_module = ModuleType("src.patches.eastmoney_patch")

    patch_state = {"called": 0}

    def _eastmoney_patch() -> None:
        patch_state["called"] += 1

    src_patch_module.eastmoney_patch = _eastmoney_patch
    src_config_module.get_config = lambda: SimpleNamespace(enable_eastmoney_patch=enable_patch)

    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)
    monkeypatch.setitem(sys.modules, "src.patches", src_patches_module)
    monkeypatch.setitem(sys.modules, "src.patches.eastmoney_patch", src_patch_module)

    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())

    sys.modules.pop(MODULE_NAME, None)
    module = importlib.import_module(MODULE_NAME)
    return module, patch_state


@pytest.mark.unit
def test_init_respects_eastmoney_patch_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    module, patch_state = _load_module(monkeypatch, enable_patch=False)
    module.EfinanceFetcher()
    assert patch_state["called"] == 0

    module, patch_state = _load_module(monkeypatch, enable_patch=True)
    module.EfinanceFetcher()
    assert patch_state["called"] == 1


@pytest.mark.unit
def test_helper_code_classification(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    assert module._is_etf_code("510050") is True
    assert module._is_etf_code("600519") is False
    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_build_eastmoney_etf_secid(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    assert module._build_eastmoney_etf_secid("510050") == "1.510050"
    assert module._build_eastmoney_etf_secid("159919") == "0.159919"

    with pytest.raises(module.DataFetchError, match="ETF"):
        module._build_eastmoney_etf_secid("600519")


@pytest.mark.unit
def test_classify_eastmoney_error(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    assert module._classify_eastmoney_error(Exception("Remote end closed connection without response"))[0] == "remote_disconnect"
    assert module._classify_eastmoney_error(Exception("request timeout while reading"))[0] == "timeout"
    assert module._classify_eastmoney_error(Exception("429 Too Many Requests"))[0] == "rate_limit_or_anti_bot"


@pytest.mark.unit
def test_build_history_failure_message(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    category, message = module.EfinanceFetcher._build_history_failure_message(
        stock_code="600519",
        beg_date="20260101",
        end_date="20260131",
        exc=Exception("timeout"),
        elapsed=1.23,
        is_etf=True,
    )

    assert category == "timeout"
    assert "stock_code=600519" in message
    assert "market_type=ETF" in message
    assert "elapsed=1.23s" in message


@pytest.mark.unit
def test_fetch_raw_data_guards_us_and_hk(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)
    fetcher = module.EfinanceFetcher()

    with pytest.raises(module.DataFetchError, match="美股"):
        fetcher._fetch_raw_data("AAPL", "2026-01-01", "2026-01-31")

    with pytest.raises(module.DataFetchError, match="港股"):
        fetcher._fetch_raw_data("HK00700", "2026-01-01", "2026-01-31")


@pytest.mark.unit
def test_fetch_raw_data_routes_to_etf_or_stock_path(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)
    fetcher = module.EfinanceFetcher()

    called = {"etf": 0, "stock": 0}

    def _fake_etf(code: str, start: str, end: str) -> str:
        called["etf"] += 1
        return "etf-data"

    def _fake_stock(code: str, start: str, end: str) -> str:
        called["stock"] += 1
        return "stock-data"

    monkeypatch.setattr(fetcher, "_fetch_etf_data", _fake_etf)
    monkeypatch.setattr(fetcher, "_fetch_stock_data", _fake_stock)

    assert fetcher._fetch_raw_data("510050", "2026-01-01", "2026-01-31") == "etf-data"
    assert fetcher._fetch_raw_data("600519", "2026-01-01", "2026-01-31") == "stock-data"
    assert called == {"etf": 1, "stock": 1}


@pytest.mark.unit
def test_ef_call_with_timeout_returns_result(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    result = module._ef_call_with_timeout(lambda x, y: x + y, 2, 3, timeout=1)
    assert result == 5
