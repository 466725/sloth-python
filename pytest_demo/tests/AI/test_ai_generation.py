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

