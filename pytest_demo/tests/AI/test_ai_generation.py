from pathlib import Path
from typing import cast

import pytest

from pytest_demo.ai_generation.generator import PlaywrightTestScriptGenerator, ScriptClient
from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.paths import resolve_output_path
from pytest_demo.ai_generation.prompt_builder import build_generation_prompt


class _FakeClient:
    def __init__(self, response: str):
        self.response = response

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        assert "pytest" in system_prompt
        assert "Goal:" in user_prompt
        return self.response


def _script_client(response: str) -> ScriptClient:
    return cast(ScriptClient, cast(object, _FakeClient(response)))


def _snapshot(*, dom: str, element_tree: str, network_events: list[dict[str, str]] | None = None) -> BrowserSnapshot:
    return BrowserSnapshot(
        url="https://www.tangerine.ca/en",
        title="Tangerine",
        dom=dom,
        element_tree=element_tree,
        screenshot_base64="abc123",
        network_events=network_events or [],
    )


@pytest.mark.unit
def test_prompt_builder_includes_goal_and_mcp_context():
    snapshot = _snapshot(
        dom="<html><body><a id='login'>Log in</a></body></html>",
        element_tree="<body><a id='login'>Log in</a></body>",
        network_events=[{"method": "GET", "url": "https://www.tangerine.ca/en", "status": "200"}],
    )

    prompt = build_generation_prompt(snapshot=snapshot, goal="verify login button", test_name="test_login")
    assert "verify login button" in prompt
    assert "mcp_payload" in prompt
    assert "test_login" in prompt


@pytest.mark.unit
def test_generator_writes_code_from_fenced_response(tmp_path: Path):
    snapshot = _snapshot(dom="<html></html>", element_tree="<body></body>")
    client = _script_client(
        """```python
from playwright.sync_api import Page

def test_smoke(page: Page):
    page.goto(\"https://www.tangerine.ca/en\")
    assert \"Tangerine\" in page.title()
```"""
    )
    generator = PlaywrightTestScriptGenerator(client)

    output_path = tmp_path / "test_generated.py"
    result = generator.generate(
        snapshot=snapshot,
        goal="verify home page title",
        test_name="test_generated_ui_flow",
        output_path=output_path,
    )

    content = result.output_path.read_text(encoding="utf-8")
    assert "def test_generated_ui_flow" in content
    assert "page.goto" in content


@pytest.mark.unit
def test_generator_fallback_template_when_ai_response_is_not_code(tmp_path: Path):
    snapshot = _snapshot(dom="<html></html>", element_tree="<body></body>")
    client = _script_client("I cannot help with this")
    generator = PlaywrightTestScriptGenerator(client)

    output_path = tmp_path / "test_generated.py"
    result = generator.generate(
        snapshot=snapshot,
        goal="verify home page title",
        test_name="test_generated_ui_flow",
        output_path=output_path,
    )

    content = result.output_path.read_text(encoding="utf-8")
    assert "def test_generated_ui_flow" in content
    assert "assert page.title()" in content


@pytest.mark.unit
def test_resolve_output_path_anchors_relative_path_to_project_root():
    relative_output = Path("pytest_demo/tests/AI/generated_playwright/test_generated_ui_flow.py")

    resolved = resolve_output_path(relative_output)

    expected_root = Path(__file__).resolve().parents[3]
    assert resolved == (expected_root / relative_output).resolve()


@pytest.mark.unit
def test_resolve_output_path_keeps_absolute_path_unchanged(tmp_path: Path):
    absolute_output = tmp_path / "test_generated_ui_flow.py"

    resolved = resolve_output_path(absolute_output)

    assert resolved == absolute_output

