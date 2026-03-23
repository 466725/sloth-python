from pathlib import Path
import os
from typing import cast

import pytest

from pytest_demo.ai_generation.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from pytest_demo.ai_generation.generator import PlaywrightTestScriptGenerator, ScriptClient
from pytest_demo.ai_generation.generator import _normalize_generated_code
from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.paths import resolve_output_path
from pytest_demo.ai_generation.prompt_builder import SYSTEM_PROMPT, build_generation_prompt


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


@pytest.mark.ai
def test_real_ai_generation_without_cli_from_explicit_prompts():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("AI_GEN_BASE_URL", "").strip()
    model = os.getenv("AI_GEN_MODEL", "").strip()
    if not all([api_key, base_url, model]):
        pytest.skip("Requires OPENAI_API_KEY, AI_GEN_BASE_URL and AI_GEN_MODEL for a real AI call.")

    dom = """
        <html>
            <body>
                <form id='login-form'>
                  <input id='username' name='username' type='text' />
                  <input id='password' name='password' type='password' />
                  <button type='submit'>Sign in</button>
                </form>
            </body>
        </html>
    """
    element_tree = """
    <body>
        <form id='login-form'>
            <input id='username'/>
            <input id='password'/>
            <button>Sign in</button>
        </form>
    </body>
    """
    screenshot_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAUA"
    network_events = [
        {"method": "GET", "url": "https://www.tangerine.ca/app#/login", "status": "200"},
    ]
    goal = "verify the sign-in form has username and password fields and a submit button"
    test_name = "test_tangerine_signin_form"

    snapshot = BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine Sign In",
        dom=dom,
        element_tree=element_tree,
        screenshot_base64=screenshot_base64,
        network_events=network_events,
    )

    # Explicit prompt variables for direct AI invocation without using CLI.
    system_prompt = SYSTEM_PROMPT
    user_prompt = build_generation_prompt(snapshot=snapshot, goal=goal, test_name=test_name)

    client = OpenAIChatScriptClient(
        OpenAIClientConfig(
            api_key=api_key,
            model=model,
            base_url=base_url,
        )
    )
    raw_code = client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    normalized_code = _normalize_generated_code(raw_code, test_name=test_name, url=snapshot.url)

    output_path = resolve_output_path(f"pytest_demo/tests/AI/generated_playwright/{test_name}.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_code, encoding="utf-8")

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert f"def {test_name}(" in content
    assert "page.goto" in content

