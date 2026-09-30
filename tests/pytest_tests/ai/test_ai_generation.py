import os

import pytest

from ai_gen.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from ai_gen.generator import _normalize_generated_code
from ai_gen.mcp_context import BrowserSnapshot
from ai_gen.paths import resolve_path
from ai_gen.prompt_builder import SYSTEM_PROMPT, build_generation_prompt


@pytest.mark.ai
def test_real_ai_generation_without_cli_from_explicit_prompts():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("AI_GEN_BASE_URL", "").strip()
    model = os.getenv("AI_GEN_MODEL", "").strip()
    if not all([api_key, base_url, model]):
        pytest.skip("Requires OPENAI_API_KEY, AI_GEN_BASE_URL and AI_GEN_MODEL for a real ai call.")

    dom = """
    <div class="container">
      <a id="login" href="/app/#/login">Log In</a>
      <a id="get-started" href="/app/#/visitor-enroll/instructions">Become a Client</a>
    </div>
    """
    snapshot = BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine Sign In",
        dom=dom,
        element_tree=dom,
        screenshot_base64="iVBORw0KGgoAAAANSUhEUgAAAAUA",
        network_events=[],
    )
    goal = "verify the Log In and the Become a Client buttons are visible"
    test_name = "test_tangerine_homepage"

    user_prompt = build_generation_prompt(snapshot=snapshot, goal=goal, test_name=test_name)
    client = OpenAIChatScriptClient(
        OpenAIClientConfig(api_key=api_key, model=model, base_url=base_url)
    )
    raw_code = client.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    normalized_code = _normalize_generated_code(raw_code, test_name=test_name, url=snapshot.url)

    output_path = resolve_path(f"temps/ai/generated_playwright/{test_name}.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_code, encoding="utf-8")

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert f"def {test_name}(" in content
    assert "page.goto" in content
