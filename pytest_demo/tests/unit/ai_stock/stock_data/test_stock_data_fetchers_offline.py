from __future__ import annotations

import importlib
import os
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


FETCHER_MODULES = [
    "ai_stock.stock_data.akshare_fetcher",
    "ai_stock.stock_data.alphavantage_fetcher",
    "ai_stock.stock_data.baostock_fetcher",
    "ai_stock.stock_data.efinance_fetcher",
    "ai_stock.stock_data.finnhub_fetcher",
    "ai_stock.stock_data.longbridge_fetcher",
    "ai_stock.stock_data.pytdx_fetcher",
    "ai_stock.stock_data.tencent_fetcher",
    "ai_stock.stock_data.tickflow_fetcher",
    "ai_stock.stock_data.tushare_fetcher",
    "ai_stock.stock_data.yfinance_fetcher",
]


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

        def __getitem__(self, key: Any):
            return self

        def dropna(self):
            return self

        def min(self):
            class _Date:
                @staticmethod
                def strftime(fmt: str) -> str:
                    return "2024-01-01"

            return _Date()

    module.DataFrame = DataFrame
    module.to_datetime = lambda *args, **kwargs: DataFrame(data=[{"date": "2024-01-01"}])
    return module


def _make_base_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.base")

    class DataFetchError(Exception):
        pass

    class RateLimitError(Exception):
        pass

    class DataSourceUnavailableError(Exception):
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

    def _is_hk_market(stock_code: str) -> bool:
        text = (stock_code or "").strip().upper()
        return text.startswith("HK") or text.endswith(".HK")

    def _is_etf_code(stock_code: str) -> bool:
        code = normalize_stock_code(stock_code)
        return len(code) == 6 and code.startswith(("51", "52", "56", "58", "15", "16", "18"))

    module.BaseFetcher = BaseFetcher
    module.DataFetchError = DataFetchError
    module.RateLimitError = RateLimitError
    module.DataSourceUnavailableError = DataSourceUnavailableError
    module.STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount", "pct_chg"]
    module.normalize_stock_code = normalize_stock_code
    module.is_bse_code = is_bse_code
    module.is_st_stock = is_st_stock
    module.is_kc_cy_stock = is_kc_cy_stock
    module._is_hk_market = _is_hk_market
    module._is_etf_code = _is_etf_code
    return module


def _make_realtime_types_stub() -> ModuleType:
    module = ModuleType("ai_stock.stock_data.realtime_types")

    class UnifiedRealtimeQuote:
        def __init__(self, **kwargs: Any) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    class ChipDistribution:
        pass

    class CircuitBreaker:
        pass

    class RealtimeSource:
        FALLBACK = "fallback"
        PRIMARY = "primary"

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
    module.CircuitBreaker = CircuitBreaker
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

    def _is_us_stock_code(stock_code: str) -> bool:
        return bool(re.match(r"^[A-Z]{1,5}(\.[A-Z])?$", str(stock_code or "").strip().upper()))

    def _is_us_index_code(stock_code: str) -> bool:
        return str(stock_code or "").strip().upper() in {"SPX", "NDX", "DJI"}

    module.is_us_stock_code = _is_us_stock_code
    module.is_us_index_code = _is_us_index_code
    module.get_us_index_yf_symbol = lambda code: (None, None)
    return module


def _install_import_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
    src_module = ModuleType("src")
    src_config_module = ModuleType("src.config")

    config_obj = SimpleNamespace(
        finnhub_api_key=None,
        alphavantage_api_key=None,
        tushare_token=None,
        longbridge_app_key=None,
        longbridge_app_secret=None,
        longbridge_access_token=None,
        longbridge_oauth_client_id=None,
    )

    src_config_module.get_config = lambda: config_obj

    src_patches_module = ModuleType("src.patches")
    src_patches_eastmoney = ModuleType("src.patches.eastmoney_patch")
    src_patches_eastmoney.eastmoney_patch = lambda *args, **kwargs: None

    src_data_module = ModuleType("src.data")
    src_data_mapping_module = ModuleType("src.data.stock_mapping")
    src_data_mapping_module.STOCK_NAME_MAP = {}
    src_data_mapping_module.is_meaningful_stock_name = lambda name, stock_code: bool(name)
    src_data_index_loader_module = ModuleType("src.data.stock_index_loader")
    src_data_index_loader_module.get_index_stock_name = lambda *args, **kwargs: None

    src_services_module = ModuleType("src.services")
    src_services_diag_module = ModuleType("src.services.run_diagnostics")
    src_services_diag_module.record_provider_run = lambda *args, **kwargs: None
    src_services_diag_module.record_provider_run_started = lambda *args, **kwargs: None

    src_report_language_module = ModuleType("src.report_language")
    src_report_language_module.normalize_report_language = lambda value=None: "en"

    monkeypatch.setitem(sys.modules, "src", src_module)
    monkeypatch.setitem(sys.modules, "src.config", src_config_module)
    monkeypatch.setitem(sys.modules, "src.patches", src_patches_module)
    monkeypatch.setitem(sys.modules, "src.patches.eastmoney_patch", src_patches_eastmoney)
    monkeypatch.setitem(sys.modules, "src.data", src_data_module)
    monkeypatch.setitem(sys.modules, "src.data.stock_mapping", src_data_mapping_module)
    monkeypatch.setitem(sys.modules, "src.data.stock_index_loader", src_data_index_loader_module)
    monkeypatch.setitem(sys.modules, "src.services", src_services_module)
    monkeypatch.setitem(sys.modules, "src.services.run_diagnostics", src_services_diag_module)
    monkeypatch.setitem(sys.modules, "src.report_language", src_report_language_module)

    monkeypatch.setitem(sys.modules, "tenacity", _make_tenacity_stub())

    if "pandas" not in sys.modules:
        monkeypatch.setitem(sys.modules, "pandas", _make_pandas_stub())

    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.base", _make_base_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.realtime_types", _make_realtime_types_stub())
    monkeypatch.setitem(sys.modules, "ai_stock.stock_data.us_index_mapping", _make_us_index_mapping_stub())


def _load_fetcher_module(monkeypatch: pytest.MonkeyPatch, module_name: str):
    _install_import_stubs(monkeypatch)
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


@pytest.mark.unit
@pytest.mark.parametrize("module_name", FETCHER_MODULES)
def test_stock_data_fetchers_import_offline(monkeypatch: pytest.MonkeyPatch, module_name: str) -> None:
    module = _load_fetcher_module(monkeypatch, module_name)
    assert module is not None


@pytest.mark.unit
def test_akshare_fetcher_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.akshare_fetcher")

    assert module._is_etf_code("510050") is True
    assert module._is_hk_code("hk00700") is True
    assert module._is_hk_code("00700") is True
    assert module._is_us_code("AAPL") is True
    assert module._to_sina_tx_symbol("600519") == "sh600519"
    assert module._to_sina_tx_symbol("000001") == "sz000001"
    assert module._to_sina_tx_symbol("830000") == "bj830000"


@pytest.mark.unit
def test_alphavantage_fetcher_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.alphavantage_fetcher")

    fetcher = module.AlphaVantageFetcher()
    assert fetcher.get_realtime_quote("AAPL") is None


@pytest.mark.unit
def test_baostock_fetcher_convert_stock_code(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.baostock_fetcher")

    fetcher = module.BaostockFetcher()
    assert fetcher._convert_stock_code("600519") == "sh.600519"
    assert fetcher._convert_stock_code("000001") == "sz.000001"
    assert fetcher._convert_stock_code("510050") == "sh.510050"

    with pytest.raises(module.DataFetchError):
        fetcher._convert_stock_code("HK00700")


@pytest.mark.unit
def test_efinance_fetcher_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.efinance_fetcher")

    assert module._is_etf_code("510050") is True
    assert module._is_etf_code("600519") is False
    assert module._is_us_code("TSLA") is True
    assert module._build_eastmoney_etf_secid("510050") == "1.510050"
    assert module._build_eastmoney_etf_secid("159919") == "0.159919"

    with pytest.raises(module.DataFetchError):
        module._build_eastmoney_etf_secid("600519")


@pytest.mark.unit
def test_finnhub_fetcher_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.finnhub_fetcher")

    fetcher = module.FinnhubFetcher()
    assert fetcher.get_realtime_quote("AAPL") is None


@pytest.mark.unit
def test_longbridge_fetcher_symbol_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.longbridge_fetcher")

    assert module._to_longbridge_symbol("AAPL") == "AAPL.US"
    assert module._to_longbridge_symbol("HK00700") == "0700.HK"
    assert module._to_longbridge_symbol("00700") == "0700.HK"
    assert module._to_longbridge_symbol("0700.HK") == "0700.HK"
    assert module._to_longbridge_symbol("600519") is None


@pytest.mark.unit
def test_pytdx_fetcher_parse_hosts_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.pytdx_fetcher")

    monkeypatch.setenv("PYTDX_SERVERS", "127.0.0.1:7709,10.0.0.1:7710")
    assert module._parse_hosts_from_env() == [("127.0.0.1", 7709), ("10.0.0.1", 7710)]

    monkeypatch.setenv("PYTDX_SERVERS", "")
    monkeypatch.setenv("PYTDX_HOST", "192.168.0.10")
    monkeypatch.setenv("PYTDX_PORT", "7727")
    assert module._parse_hosts_from_env() == [("192.168.0.10", 7727)]

    assert module._is_us_code("AAPL") is True
    assert module._is_us_code("600519") is False


@pytest.mark.unit
def test_tencent_fetcher_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.tencent_fetcher")

    assert module._to_tencent_symbol("600519") == "sh600519"
    assert module._to_tencent_symbol("000001") == "sz000001"
    assert module._to_tencent_symbol("830000") == "bj830000"
    assert module._format_tencent_date("2026-07-13") == "2026-07-13"
    assert module._format_tencent_date("not-a-date") is None
    assert module._lots_to_shares("12") == 1200.0
    assert module._estimate_lookback_days(start_date="2026-01-01", end_date="2026-01-31") >= 30


@pytest.mark.unit
def test_tickflow_fetcher_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.tickflow_fetcher")

    fetcher = module.TickFlowFetcher(api_key=None)
    assert fetcher._get_client() is None

    assert module.TickFlowFetcher._safe_float("12.5") == 12.5
    assert module.TickFlowFetcher._ratio_to_percent("0.12") == 12.0
    assert module.TickFlowFetcher._is_cn_equity_symbol("600519.SH") is True
    assert module.TickFlowFetcher._is_cn_equity_symbol("AAPL.US") is False
    assert module.TickFlowFetcher._get_limit_ratio("920001", "普通") == 0.30
    assert module.TickFlowFetcher._get_limit_ratio("688001", "普通") == 0.20
    assert module.TickFlowFetcher._get_limit_ratio("600001", "*ST测试") == 0.05


@pytest.mark.unit
def test_tushare_fetcher_code_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.tushare_fetcher")

    fetcher = module.TushareFetcher()
    assert module._is_etf_code("510050") is True
    assert module._is_us_code("AAPL") is True

    assert fetcher._convert_stock_code("600519") == "600519.SH"
    assert fetcher._convert_stock_code("159919") == "159919.SZ"
    assert fetcher._convert_stock_code("920001") == "920001.BJ"

    with pytest.raises(module.DataFetchError):
        fetcher._convert_stock_code("AAPL")


@pytest.mark.unit
def test_yfinance_fetcher_code_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_fetcher_module(monkeypatch, "ai_stock.stock_data.yfinance_fetcher")

    fetcher = module.YfinanceFetcher()
    assert fetcher._is_jp_kr_suffix_stock("7203.T") is True
    assert fetcher._is_jp_kr_suffix_stock("005930.KS") is True

    assert fetcher._convert_stock_code("600519") == "600519.SS"
    assert fetcher._convert_stock_code("000001") == "000001.SZ"
    assert fetcher._convert_stock_code("hk00700") == "0700.HK"
    assert fetcher._convert_stock_code("AAPL") == "AAPL"
    assert fetcher._convert_stock_code("830001") == "830001.BJ"


@pytest.mark.api
def test_stock_data_fetchers_live_smoke_optional() -> None:
    if os.getenv("RUN_LIVE_STOCK_DATA_FETCHER_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_STOCK_DATA_FETCHER_TESTS=1 to run live stock_data fetcher checks")

    pytest.skip("Live smoke tests are opt-in and should be enabled per provider credentials")
