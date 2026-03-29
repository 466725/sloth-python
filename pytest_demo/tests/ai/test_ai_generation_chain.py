from __future__ import annotations

import os
from pathlib import Path

import pytest

from pytest_demo.ai_generation.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from pytest_demo.ai_generation.generator import ScriptClient, _normalize_generated_code
from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.paths import resolve_output_path
from pytest_demo.ai_generation.prompt_builder import SYSTEM_PROMPT, build_generation_prompt


class _StepClient(ScriptClient):
    def __init__(self, response: str):
        self.response = response
        self.calls: list[tuple[str, str]] = []

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:  # type: ignore[override]
        self.calls.append((system_prompt, user_prompt))
        return self.response


def _snapshot() -> BrowserSnapshot:
    return BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine",
        dom="<html><body><a id='login'>Log in</a><a id='menu_signup'>Sign me up</a></body></html>",
        element_tree="<body><a id='login'>Log in</a><a id='menu_signup'>Sign me up</a></body>",
        screenshot_base64="abc123",
        network_events=[
            {"method": "GET", "url": "https://www.tangerine.ca/en/personal", "status": "200"},
        ],
    )


def _build_planner_user_prompt(goal: str) -> str:
    return (
        "Create a concise numbered UI test plan.\\n"
        "Include navigation, stable locator ideas, and assertion points.\\n"
        f"Goal: {goal}"
    )


def _build_coder_user_prompt(*, snapshot: BrowserSnapshot, goal: str, test_name: str, plan: str) -> str:
    base_prompt = build_generation_prompt(snapshot=snapshot, goal=goal, test_name=test_name)
    return f"{base_prompt}\\n\\nExecution plan:\\n{plan}"


def _build_reviewer_user_prompt(*, goal: str, plan: str, code: str) -> str:
    return (
        "Review this generated pytest + Playwright code for selector stability,"
        " assertion quality, and likely flakiness.\\n"
        "Return PASS or FAIL with short bullet points and concrete fixes.\\n\\n"
        f"Goal:\\n{goal}\\n\\nPlan:\\n{plan}\\n\\nCode:\\n{code}"
    )


@pytest.mark.unit
def test_chain_prompts_flow_and_output_normalization(tmp_path: Path):
    goal = "verify login and signup links are visible"
    test_name = "test_chain_generated"
    snapshot = _snapshot()

    planner = _StepClient("1. Open page\n2. Verify login link\n3. Verify signup link")
    coder = _StepClient(
        """```
        python
        from playwright.sync_api import Page
        
        def test_temp_name(page: Page):
            page.goto(\"https://www.tangerine.ca/en/personal\")
            assert page.locator(\"#login\").is_visible()
            assert page.locator(\"#menu_signup\").is_visible()
        ```"""
    )
    reviewer = _StepClient("PASS\n- Selectors are stable\n- Assertions are meaningful")

    plan = planner.generate(
        system_prompt="You are a QA planner.",
        user_prompt=_build_planner_user_prompt(goal),
    )
    raw_code = coder.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=_build_coder_user_prompt(snapshot=snapshot, goal=goal, test_name=test_name, plan=plan),
    )
    normalized = _normalize_generated_code(raw_code, test_name=test_name, url=snapshot.url)
    review = reviewer.generate(
        system_prompt="You are a strict QA code reviewer.",
        user_prompt=_build_reviewer_user_prompt(goal=goal, plan=plan, code=normalized),
    )

    output_path = tmp_path / "test_chain_generated.py"
    output_path.write_text(normalized, encoding="utf-8")

    assert "Goal:" in planner.calls[0][1]
    assert "Execution plan:" in coder.calls[0][1]
    assert plan in coder.calls[0][1]
    assert f"def {test_name}(" in normalized
    assert "PASS" in review
    assert output_path.exists()


@pytest.mark.ai
def test_real_ai_chain_generation_writes_script_and_review_notes():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("AI_GEN_BASE_URL", "").strip()
    default_model = os.getenv("AI_GEN_MODEL", "").strip()
    planner_model = os.getenv("AI_PLAN_MODEL", default_model).strip()
    coder_model = os.getenv("AI_CODE_MODEL", default_model).strip()
    reviewer_model = os.getenv("AI_REVIEW_MODEL", default_model).strip()

    if not all([api_key, base_url, planner_model, coder_model, reviewer_model]):
        pytest.skip(
            "Requires OPENAI_API_KEY, AI_GEN_BASE_URL, and AI_GEN_MODEL "
            "(or AI_PLAN_MODEL/AI_CODE_MODEL/AI_REVIEW_MODEL)."
        )

    goal = "verify the Tangerine homepage shows visible iOS and Android 'Get Our App' links"
    test_name = "test_tangerine_get_our_app_chain"
    snapshot = BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine",
        dom=(
            "<html><body><footer>"
            "<a href='https://apps.apple.com/ca/app/tangerine-mobile-banking/id611430670'>Get Our App iOS</a>"
            "<a href='https://play.google.com/store/apps/details?id=ca.tangerine.clients.banking.mobile'>"
            "Get Our App Android</a></footer></body></html>"
        ),
        element_tree=(
            "<body><footer>"
            "<a>Get Our App iOS</a><a>Get Our App Android</a>"
            "</footer></body>"
        ),
        screenshot_base64="abc123",
        network_events=[
            {"method": "GET", "url": "https://www.tangerine.ca/en/personal", "status": "200"},
        ],
    )

    planner_client = OpenAIChatScriptClient(
        OpenAIClientConfig(api_key=api_key, model=planner_model, base_url=base_url)
    )
    coder_client = OpenAIChatScriptClient(
        OpenAIClientConfig(api_key=api_key, model=coder_model, base_url=base_url)
    )
    reviewer_client = OpenAIChatScriptClient(
        OpenAIClientConfig(api_key=api_key, model=reviewer_model, base_url=base_url)
    )

    plan = planner_client.generate(
        system_prompt="You are a QA planning assistant. Output only a concise numbered plan.",
        user_prompt=_build_planner_user_prompt(goal),
    )

    raw_code = coder_client.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=_build_coder_user_prompt(snapshot=snapshot, goal=goal, test_name=test_name, plan=plan),
    )
    normalized_code = _normalize_generated_code(raw_code, test_name=test_name, url=snapshot.url)

    review = reviewer_client.generate(
        system_prompt="You are a strict QA reviewer. Return PASS or FAIL first, then short bullets.",
        user_prompt=_build_reviewer_user_prompt(goal=goal, plan=plan, code=normalized_code),
    )

    output_path = resolve_output_path(f"pytest_demo/tests/AI/generated_playwright/{test_name}.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_code, encoding="utf-8")

    notes_path = output_path.with_suffix(".review.txt")
    notes_path.write_text(
        f"PLAN:\n{plan}\n\nREVIEW:\n{review}\n",
        encoding="utf-8",
    )

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert notes_path.exists()
    assert f"def {test_name}(" in content
    assert "page.goto" in content
