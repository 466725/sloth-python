# -*- coding: utf-8 -*-
"""
===================================
服务层模块初始化
===================================

职责：
1. 声明可导出的服务类（延迟导入，避免启动时拉入 LLM 等重依赖）

使用方式：
    直接从子模块导入，例如:
    from src.services.history_service import HistoryService
"""


def __getattr__(name: str):
    """延迟导入：仅在通过 src.services.X 访问时才加载对应子模块。"""
    _lazy_map = {
        "AnalysisService": "ai_stock.services.analysis_service",
        "BacktestService": "ai_stock.services.backtest_service",
        "HistoryService": "ai_stock.services.history_service",
        "StockService": "ai_stock.services.stock_service",
    }
    if name in _lazy_map:
        import importlib
        module = importlib.import_module(_lazy_map[name])
        return getattr(module, name)
    raise AttributeError(f"module 'ai_stock.services' has no attribute {name!r}")


__all__ = [
    "AnalysisService",
    "BacktestService",
    "HistoryService",
    "StockService",
]
