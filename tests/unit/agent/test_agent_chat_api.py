# -*- coding: utf-8 -*-
"""Agent chat history API regressions."""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from ai_stock.config import Config
from ai_stock.storage import DatabaseManager
from api.app import create_app


def teardown_function() -> None:
    DatabaseManager.reset_instance()
    Config.reset_instance()


def test_chat_session_messages_api_does_not_expose_provider_trace(tmp_path: Path) -> None:
    DatabaseManager.reset_instance()
    Config.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'trace.db'}")
    session_id = "api-trace-hidden"
    user_id = db.save_conversation_message(session_id, "user", "visible question")
    assistant_id = db.save_conversation_message(session_id, "assistant", "visible answer")
    db.save_agent_provider_turn(
        session_id=session_id,
        run_id="run-hidden",
        provider="deepseek",
        model="deepseek/deepseek-chat",
        anchor_user_message_id=user_id,
        anchor_assistant_message_id=assistant_id,
        messages=[
            {
                "role": "assistant",
                "content": "checking",
                "reasoning_content": "SECRET_REASONING",
                "tool_calls": [{"id": "call_1", "name": "echo", "arguments": {}}],
            },
            {"role": "tool", "tool_call_id": "call_1", "content": "SECRET_TOOL_RESULT"},
        ],
        contains_reasoning=True,
        contains_tool_calls=True,
        contains_thinking_blocks=False,
        must_roundtrip=True,
        estimated_tokens=10,
    )

    client = TestClient(create_app(static_dir=tmp_path / "static"))
    response = client.get(f"/api/v1/agent/chat/sessions/{session_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == session_id
    assert [(msg["role"], msg["content"]) for msg in payload["messages"]] == [
        ("user", "visible question"),
        ("assistant", "visible answer"),
    ]
    assert "SECRET_REASONING" not in response.text
    assert "SECRET_TOOL_RESULT" not in response.text
    assert "tool_calls" not in response.text


def test_agent_chat_forwards_stock_context_to_executor(tmp_path: Path) -> None:
    executor = MagicMock()
    executor.chat.return_value = SimpleNamespace(
        success=True,
        content="ok",
        error=None,
    )
    config = SimpleNamespace(is_agent_available=lambda: True)

    with patch("api.v1.endpoints.agent.get_config", return_value=config):
        with patch("api.v1.endpoints.agent._build_executor", return_value=executor):
            client = TestClient(create_app(static_dir=tmp_path / "static"))
            response = client.post(
                "/api/v1/agent/chat",
                json={
                    "message": "如果不考虑 TTM 呢",
                    "session_id": "s1",
                    "context": {
                        "stock_code": "600519",
                        "stock_name": "匿名标的",
                    },
                },
            )

    assert response.status_code == 200
    kwargs = executor.chat.call_args.kwargs
    assert kwargs["message"] == "如果不考虑 TTM 呢"
    assert kwargs["session_id"] == "s1"
    assert kwargs["context"]["stock_code"] == "600519"
    assert kwargs["context"]["stock_name"] == "匿名标的"


def test_agent_chat_stream_forwards_stock_context_to_executor(tmp_path: Path) -> None:
    executor = MagicMock()
    executor.chat.return_value = SimpleNamespace(
        success=True,
        content="ok",
        error=None,
        total_steps=1,
    )
    config = SimpleNamespace(is_agent_available=lambda: True)

    with patch("api.v1.endpoints.agent.get_config", return_value=config):
        with patch("api.v1.endpoints.agent._build_executor", return_value=executor):
            client = TestClient(create_app(static_dir=tmp_path / "static"))
            response = client.post(
                "/api/v1/agent/chat/stream",
                json={
                    "message": "如果不考虑 TTM 呢",
                    "session_id": "s1",
                    "context": {
                        "stock_code": "600519",
                        "stock_name": "匿名标的",
                    },
                },
            )

    assert response.status_code == 200
    assert '"type": "done"' in response.text
    kwargs = executor.chat.call_args.kwargs
    assert kwargs["message"] == "如果不考虑 TTM 呢"
    assert kwargs["session_id"] == "s1"
    assert kwargs["context"]["stock_code"] == "600519"
    assert kwargs["context"]["stock_name"] == "匿名标的"


def test_analysis_session_reuses_only_single_topic_history(tmp_path: Path) -> None:
    DatabaseManager.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'topics.db'}")
    english = "Use strategy Bullish trend to analyze stock 600519"
    chinese = "使用策略 多头趋势 分析股票 600519"
    db.save_conversation_message("mixed", "user", english)
    db.save_conversation_message("mixed", "assistant", "old answer")
    db.save_conversation_message("mixed", "user", "analyze a different stock")
    db.save_conversation_message("single", "user", chinese)
    db.save_conversation_message("single", "assistant", "same topic answer")
    client = TestClient(create_app(static_dir=tmp_path / "static"))
    topic = {
        "stock_code": "600519",
        "strategy_id": "bull_trend",
        "prompt_variants": [english, chinese],
    }

    response = client.post("/api/v1/agent/chat/analysis-session", json=topic)
    assert response.status_code == 200
    assert response.json()["session_id"] == "single"
    assert len(response.json()["messages"]) == 2

    # The persisted topic identity, not the display language, selects the session.
    topic["prompt_variants"] = [english]
    assert (
        client.post("/api/v1/agent/chat/analysis-session", json=topic).json()["session_id"]
        == "single"
    )
    topic["stock_code"] = "300750"
    topic["prompt_variants"] = ["Use strategy Bullish trend to analyze stock 300750"]
    other = client.post("/api/v1/agent/chat/analysis-session", json=topic)
    assert other.status_code == 200
    assert other.json()["session_id"] not in {"single", "mixed"}
    assert other.json()["messages"] == []
    assert len(db.get_conversation_messages("mixed")) == 3

    sid = other.json()["session_id"]
    DatabaseManager.reset_instance()
    DatabaseManager(db_url=f"sqlite:///{tmp_path / 'topics.db'}")
    assert (
        client.post("/api/v1/agent/chat/analysis-session", json=topic).json()["session_id"] == sid
    )
    client.delete(f"/api/v1/agent/chat/sessions/{sid}")
    assert (
        client.post("/api/v1/agent/chat/analysis-session", json=topic).json()["session_id"] != sid
    )


def test_analysis_session_does_not_reuse_a_mixed_matching_history(tmp_path: Path) -> None:
    DatabaseManager.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'mixed.db'}")
    prompt = "Use strategy Bullish trend to analyze stock 600519"
    db.save_conversation_message("mixed", "user", prompt)
    db.save_conversation_message("mixed", "assistant", "old answer")
    db.save_conversation_message(
        "mixed", "user", "Use strategy Volume breakout to analyze stock 300750"
    )
    client = TestClient(create_app(static_dir=tmp_path / "static"))
    topic = {"stock_code": "600519", "strategy_id": "bull_trend", "prompt_variants": [prompt]}

    response = client.post("/api/v1/agent/chat/analysis-session", json=topic)
    assert response.status_code == 200
    assert response.json()["session_id"] != "mixed"
    assert response.json()["messages"] == []
    topic["strategy_id"] = "volume_breakout"
    topic["prompt_variants"] = ["Use strategy Volume breakout to analyze stock 600519"]
    other = client.post("/api/v1/agent/chat/analysis-session", json=topic)
    assert other.json()["session_id"] != response.json()["session_id"]


@pytest.mark.parametrize("endpoint", ["/chat", "/chat/stream"])
def test_analysis_chat_keeps_latest_five_complete_turns(tmp_path: Path, endpoint: str) -> None:
    DatabaseManager.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'retention.db'}")
    client = TestClient(create_app(static_dir=tmp_path / "static"))
    prompt = "Use strategy Bullish trend to analyze stock 600519"
    topic = {"stock_code": "600519", "strategy_id": "bull_trend", "prompt_variants": [prompt]}
    sid = client.post("/api/v1/agent/chat/analysis-session", json=topic).json()["session_id"]
    replies = iter(range(7))

    def chat(**kwargs):
        session_id = kwargs["session_id"]
        turn = next(replies)
        user_id = db.save_conversation_message(session_id, "user", kwargs["message"])
        assistant_id = db.save_conversation_message(session_id, "assistant", f"answer {turn}")
        assert (
            len([m for m in db.get_conversation_messages(session_id) if m["role"] == "assistant"])
            <= 5
        )
        db.save_agent_provider_turn(
            session_id=session_id,
            run_id=f"run-{turn}",
            provider="deepseek",
            model="deepseek/deepseek-chat",
            anchor_user_message_id=user_id,
            anchor_assistant_message_id=assistant_id,
            messages=[{"role": "assistant", "content": f"answer {turn}"}],
            contains_reasoning=False,
            contains_tool_calls=False,
            contains_thinking_blocks=False,
            must_roundtrip=False,
            estimated_tokens=10,
        )
        if turn == 4:
            db.upsert_conversation_summary(
                session_id, "old summarized answers", assistant_id, 10, 10
            )
        return SimpleNamespace(success=True, content=f"answer {turn}", error=None, total_steps=1)

    executor = MagicMock()
    executor.chat.side_effect = chat
    with patch(
        "api.v1.endpoints.agent.get_config",
        return_value=SimpleNamespace(is_agent_available=lambda: True),
    ):
        with patch("api.v1.endpoints.agent._build_executor", return_value=executor):
            for turn in range(7):
                # A currently selected, unrelated history must not receive this prompt.
                response = client.post(
                    f"/api/v1/agent{endpoint}",
                    json={
                        "message": prompt,
                        "session_id": "unrelated",
                        "skills": ["bull_trend"],
                        "context": {"stock_code": "600519"},
                        "analysis_topic": topic,
                    },
                )
                assert response.status_code == 200
                if endpoint == "/chat/stream":
                    done = json.loads(response.text.strip().removeprefix("data: "))
                    assert done["type"] == "done"
                    assert len(done["messages"]) == min(turn + 1, 5) * 2
                else:
                    assert response.json()["session_id"] == sid
                assert executor.chat.call_args.kwargs["session_id"] == sid
                saved = db.get_conversation_messages(sid)
                assert len([m for m in saved if m["role"] == "assistant"]) == min(turn + 1, 5)

    assert [(m["role"], m["content"]) for m in db.get_conversation_messages(sid)] == [
        item for turn in range(2, 7) for item in [("user", prompt), ("assistant", f"answer {turn}")]
    ]
    assert db.get_conversation_messages("unrelated") == []
    assert db.get_conversation_summary(sid) is None
    assert [
        trace["run_id"] for trace in db.get_agent_provider_turns(sid, must_roundtrip_only=False)
    ] == [f"run-{turn}" for turn in range(2, 7)]
    DatabaseManager.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'retention.db'}")
    assert len(db.get_conversation_messages(sid)) == 10


def test_analysis_topic_must_match_selected_stock_and_strategy(tmp_path: Path) -> None:
    DatabaseManager.reset_instance()
    DatabaseManager(db_url=f"sqlite:///{tmp_path / 'validation.db'}")
    client = TestClient(create_app(static_dir=tmp_path / "static"))
    with patch(
        "api.v1.endpoints.agent.get_config",
        return_value=SimpleNamespace(is_agent_available=lambda: True),
    ):
        response = client.post(
            "/api/v1/agent/chat/stream",
            json={
                "message": "generated prompt",
                "skills": ["volume_breakout"],
                "context": {"stock_code": "300750"},
                "analysis_topic": {
                    "stock_code": "600519",
                    "strategy_id": "bull_trend",
                    "prompt_variants": ["generated prompt"],
                },
            },
        )
    assert response.status_code == 422


def test_parallel_topic_resolution_creates_only_one_mapping(tmp_path: Path) -> None:
    DatabaseManager.reset_instance()
    db = DatabaseManager(db_url=f"sqlite:///{tmp_path / 'parallel.db'}")
    with ThreadPoolExecutor(max_workers=4) as pool:
        ids = list(
            pool.map(
                lambda _: db.resolve_analysis_conversation(
                    "600519", "bull_trend", ["Use strategy Bullish trend to analyze stock 600519"]
                ),
                range(8),
            )
        )
    assert len(set(ids)) == 1
    assert db.get_chat_sessions() == []
