from __future__ import annotations

import importlib
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


MODULE_NAME = "ai_stock.stock_data.akshare_fetcher"


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
        def __init__(self, data: Any = None, columns: Any = None, *args: Any, **kwargs: Any) -> None:
            self._data = data
            self.columns = columns or []
            self.empty = not bool(data)

    module.DataFrame = DataFrame
    module.to_datetime = lambda *args, **kwargs: DataFrame(data=[{"date": "2024-01-01"}])
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class RateLimitError(Exception):
        pass

    class BaseFetcher:
        name = "BaseFetcher"
        priority = 99

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

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.RateLimitError = RateLimitError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.is_bse_code = is_bse_code
    module.is_st_stock = is_st_stock
    module.is_kc_cy_stock = is_kc_cy_stock
    module.normalize_stock_code = normalize_stock_code
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class ChipDistribution:
        pass

    class RealtimeSource:
        FALLBACK = "fallback"

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
    module.ChipDistribution = ChipDistribution
    module.RealtimeSource = RealtimeSource
    module.get_realtime_circuit_breaker = lambda *args, **kwargs: SimpleNamespace(
        can_execute=lambda: True,
        record_failure=lambda *a, **k: None,
        record_success=lambda *a, **k: None,
    )
    module.get_chip_circuit_breaker = lambda *args, **kwargs: SimpleNamespace(
        can_execute=lambda: True,
        record_failure=lambda *a, **k: None,
        record_success=lambda *a, **k: None,
    )
    module.safe_float = safe_float
    module.safe_int = safe_int
    return module


def _make_us_index_mapping_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.us_index_mapping")
    module.is_us_index_code = lambda code: str(code).upper() in {"SPX", "NDX", "DJI"}
    module.is_us_stock_code = lambda code: bool(re.match(r"^[A-Z]{1,5}(\.[A-Z])?$", str(code).strip().upper()))
    return module


def _load_module(monkeypatch: pytest.MonkeyPatch, enable_patch: bool = False):
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")
    src_patches_module = ModuleType("src.patches")
    src_patches_eastmoney = ModuleType("src.patches.eastmoney_patch")

    patch_state = {"called": 0}

    def _eastmoney_patch() -> None:
        patch_state["called"] += 1

    src_patches_eastmoney.eastmoney_patch = _eastmoney_patch
    src_config_module.get_config = lambda: SimpleNamespace(enable_eastmoney_patch=enable_patch)

    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)
    monkeypatch.setitem(sys.modules, "src.patches", src_patches_module)
    monkeypatch.setitem(sys.modules, "src.patches.eastmoney_patch", src_patches_eastmoney)

    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())
    monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.us_index_mapping", _make_us_index_mapping_stub())

    sys.modules.pop(MODULE_NAME, None)
    module = importlib.import_module(MODULE_NAME)
    return module, patch_state


@pytest.mark.unit
def test_akshare_fetcher_init_respects_eastmoney_patch_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    module, patch_state = _load_module(monkeypatch, enable_patch=False)
    module.AkshareFetcher()
    assert patch_state["called"] == 0

    module, patch_state = _load_module(monkeypatch, enable_patch=True)
    module.AkshareFetcher()
    assert patch_state["called"] == 1


@pytest.mark.unit
def test_code_classification_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    assert module._is_etf_code("510050") is True
    assert module._is_etf_code("600519") is False
    assert module._is_hk_code("hk00700") is True
    assert module._is_hk_code("00700") is True
    assert module._is_hk_code("600519") is False
    assert module.is_hk_stock_code("00700") is True
    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_to_sina_tx_symbol(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    assert module._to_sina_tx_symbol("600519") == "sh600519"
    assert module._to_sina_tx_symbol("510050") == "sh510050"
    assert module._to_sina_tx_symbol("000001") == "sz000001"
    assert module._to_sina_tx_symbol("830000") == "bj830000"


@pytest.mark.unit
def test_normalize_tencent_volume_with_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    fields = [""] * 45
    fields[6] = "12"
    assert module._normalize_tencent_volume(fields) == 1200

    assert module._normalize_tencent_volume([""] * 5) is None


@pytest.mark.unit
def test_normalize_tencent_volume_prefers_closest_estimate(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    fields_raw_closer = [""] * 45
    fields_raw_closer[3] = "10"
    fields_raw_closer[6] = "100"
    fields_raw_closer[38] = "1"
    fields_raw_closer[44] = "0.0001"  # expected volume ~= 10, closer to raw 100 than 10000
    assert module._normalize_tencent_volume(fields_raw_closer) == 100

    fields_hand_closer = [""] * 45
    fields_hand_closer[3] = "10"
    fields_hand_closer[6] = "100"
    fields_hand_closer[38] = "1"
    fields_hand_closer[44] = "0.1"  # expected volume ~= 10000, closer to hand->share 10000
    assert module._normalize_tencent_volume(fields_hand_closer) == 10000


@pytest.mark.unit
def test_parse_tencent_amount(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    precise = [""] * 40
    precise[35] = "10.2/3000/123456.7"
    assert module._parse_tencent_amount(precise) == 123456.7

    fallback = [""] * 40
    fallback[37] = "12.3"
    assert module._parse_tencent_amount(fallback) == 123000.0

    assert module._parse_tencent_amount([""] * 5) is None


@pytest.mark.unit
def test_classify_realtime_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    category, _ = module._classify_realtime_http_error(Exception("Remote end closed connection without response"))
    assert category == "remote_disconnect"

    category, _ = module._classify_realtime_http_error(Exception("request timeout while reading"))
    assert category == "timeout"

    category, _ = module._classify_realtime_http_error(Exception("429 Too Many Requests"))
    assert category == "rate_limit_or_anti_bot"


@pytest.mark.unit
def test_build_realtime_failure_message(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _ = _load_module(monkeypatch)

    msg = module._build_realtime_failure_message(
        source_name="Sina",
        endpoint="https://example.test/realtime",
        stock_code="600519",
        symbol="sh600519",
        category="timeout",
        detail="read timeout",
        elapsed=1.23,
        error_type="Timeout",
    )

    assert "Sina" in msg
    assert "stock_code=600519" in msg
    assert "symbol=sh600519" in msg
    assert "category=timeout" in msg
    assert "elapsed=1.23s" in msg
