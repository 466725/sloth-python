# -*- coding: utf-8 -*-
"""
Agent module for stock analysis system.

Provides LLM-based agent with tool-calling capabilities,
pluggable trading strategies, and multi-turn conversation support.

Enabled via AGENT_MODE=true environment variable.

Use explicit imports to avoid pulling in heavy dependencies (e.g. json_repair)
when only lightweight sub-modules like tools.registry are needed::

    from ai_stock.agent.executor import AgentExecutor, AgentResult
    from ai_stock.agent.runner import run_agent_loop, RunLoopResult
    from ai_stock.agent.protocols import AgentContext, AgentOpinion, StageResult, AgentRunStats
    from ai_stock.agent.orchestrator import AgentOrchestrator
"""


def __getattr__(name):
    """Lazy import to avoid triggering json_repair etc. on package access."""
    if name == "AgentExecutor":
        from ai_stock.agent.executor import AgentExecutor
        return AgentExecutor
    if name == "AgentResult":
        from ai_stock.agent.executor import AgentResult
        return AgentResult
    if name == "RunLoopResult":
        from ai_stock.agent.runner import RunLoopResult
        return RunLoopResult
    if name in ("AgentContext", "AgentOpinion", "StageResult", "AgentRunStats"):
        from ai_stock.agent import protocols
        return getattr(protocols, name)
    if name == "AgentOrchestrator":
        from ai_stock.agent.orchestrator import AgentOrchestrator
        return AgentOrchestrator
    if name == "AgentMemory":
        from ai_stock.agent.memory import AgentMemory
        return AgentMemory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AgentExecutor",
    "AgentResult",
    "RunLoopResult",
    "AgentContext",
    "AgentOpinion",
    "StageResult",
    "AgentRunStats",
    "AgentOrchestrator",
    "AgentMemory",
]
