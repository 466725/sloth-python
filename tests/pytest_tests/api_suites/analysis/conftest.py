"""Fixtures for the analysis suite.

Analysis submissions normally hand work to a background task queue that calls
live market data providers and an LLM. The suite replaces that queue with an
in-memory stub so the HTTP contract can be exercised without running any
analysis.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

import pytest


@dataclass
class StubTask:
    """Minimal stand-in for a queued analysis task."""

    task_id: str
    stock_code: str
    analysis_phase: str = "auto"
    trace_id: str | None = None


@dataclass
class StubTaskQueue:
    """Records submissions instead of executing them."""

    batch_submissions: list[dict[str, Any]] = field(default_factory=list)
    background_submissions: list[dict[str, Any]] = field(default_factory=list)
    duplicates: list[Any] = field(default_factory=list)

    def submit_tasks_batch(self, **kwargs: Any) -> tuple[list[StubTask], list[Any]]:
        """Accept every submitted code and return stub tasks."""
        self.batch_submissions.append(kwargs)
        tasks = [
            StubTask(task_id=f"stub-task-{index}", stock_code=code)
            for index, code in enumerate(kwargs["stock_codes"])
        ]
        return tasks, list(self.duplicates)

    def submit_background_task(self, _callable: Any, **kwargs: Any) -> StubTask:
        """Record a background submission without scheduling it."""
        self.background_submissions.append(kwargs)
        return StubTask(
            task_id=kwargs.get("task_id", "stub-background-task"),
            stock_code=kwargs.get("stock_code", "market_review"),
        )


@pytest.fixture
def stub_task_queue(monkeypatch: pytest.MonkeyPatch) -> Iterator[StubTaskQueue]:
    """Replace the analysis task queue with a recording stub."""
    queue = StubTaskQueue()
    monkeypatch.setattr("api.v1.endpoints.analysis.get_task_queue", lambda: queue)
    yield queue
