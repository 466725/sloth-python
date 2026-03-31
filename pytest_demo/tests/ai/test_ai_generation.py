import os

import pytest

from pytest_demo.ai_generation.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from pytest_demo.ai_generation.generator import _normalize_generated_code
from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.paths import resolve_output_path
from pytest_demo.ai_generation.prompt_builder import SYSTEM_PROMPT, build_generation_prompt


@pytest.mark.ai
def test_real_ai_generation_without_cli_from_explicit_prompts():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("AI_GEN_BASE_URL", "").strip()
    model = os.getenv("AI_GEN_MODEL", "").strip()
    if not all([api_key, base_url, model]):
        pytest.skip("Requires OPENAI_API_KEY, AI_GEN_BASE_URL and AI_GEN_MODEL for a real ai call.")

    dom = """
        <div class="container responsivegrid">
           <div id="search-actions" class="cmp-container">
              <div class="button cmp-button--icon">
                 <button type="button" id="search-btn" class="cmp-button" aria-label="Search, opens dialogue" title="Search, opens dialogue" data-cmp-clickable="" data-cmp-data-layer="{&quot;search-btn&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2023-12-07T18:42:24Z&quot;}}">
                 </button>
              </div>
              <div class="button cmp-button--primary-inverse-outline cmp-all-showVisitor">
                 <a id="login" class="cmp-button" data-cmp-clickable="" data-cmp-data-layer="{&quot;login&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2024-01-16T14:39:17Z&quot;,&quot;dc:title&quot;:&quot;Log In&quot;,&quot;xdm:linkURL&quot;:&quot;/app/#/login/login-id?locale=en_CA&quot;}}" href="/app/#/login/login-id?locale=en_CA">
                 <span class="cmp-button__text">Log In</span>
                 </a>
              </div>
              <div class="button cmp-button--primary-inverse-outline cmp-all-showClient cmp-all-showBusiness">
                 <button type="button" id="logout" class="cmp-button" data-cmp-clickable="" data-cmp-data-layer="{&quot;logout&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2024-01-19T21:51:21Z&quot;,&quot;dc:title&quot;:&quot;Log Out&quot;}}">
                 <span class="cmp-button__text">Log Out</span>
                 </button>
              </div>
              <div class="button cmp-all-showVisitor cmp-button--header-primary-visitor">
                 <a id="get-started" class="cmp-button" data-cmp-clickable="" data-cmp-data-layer="{&quot;get-started&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2024-03-11T17:48:16Z&quot;,&quot;dc:title&quot;:&quot;Become a Client&quot;,&quot;xdm:linkURL&quot;:&quot;/app/#/visitor-enroll/instructions?locale=en_CA&amp;products=4000&quot;}}" href="/app/#/visitor-enroll/instructions?locale=en_CA&amp;products=4000">
                 <span class="cmp-button__text">Become a Client</span>
                 </a>
              </div>
              <div class="button cmp-all-showClient cmp-button--header-primary-client">
                 <a id="mytangerine" class="cmp-button" data-cmp-clickable="" data-cmp-data-layer="{&quot;mytangerine&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2024-03-11T17:48:36Z&quot;,&quot;dc:title&quot;:&quot;My Tangerine&quot;,&quot;xdm:linkURL&quot;:&quot;/app/#/accounts?locale=en_CA&quot;}}" href="/app/#/accounts?locale=en_CA">
                 <span class="cmp-button__text">My Tangerine</span>
                 </a>
              </div>
              <div class="button cmp-all-showBusiness cmp-button--header-primary-business">
                 <a id="mytangerinebiz" class="cmp-button" data-cmp-clickable="" data-cmp-data-layer="{&quot;mytangerinebiz&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2024-03-11T17:49:06Z&quot;,&quot;dc:title&quot;:&quot;My Tangerine&quot;,&quot;xdm:linkURL&quot;:&quot;/app/#/accounts?locale=en_CA&quot;}}" href="/app/#/accounts?locale=en_CA">
                 <span class="cmp-button__text">My Tangerine</span>
                 </a>
              </div>
              <div class="button cmp-button--icon">
                 <button type="button" id="hamburger-menu" class="cmp-button" aria-label="Menu opens dialog" title="Menu opens dialog" data-cmp-clickable="" data-cmp-data-layer="{&quot;hamburger-menu&quot;:{&quot;@type&quot;:&quot;tangerine/components/button&quot;,&quot;repo:modifyDate&quot;:&quot;2023-10-18T16:11:34Z&quot;}}">
                 <span class="cmp-button__icon cmp-button__icon--menu-light" aria-hidden="true"></span>
                 </button>
              </div>
           </div>
        </div>
    """
    element_tree = dom
    screenshot_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAUA"
    network_events = []
    goal = "verify the Log In and the Become a Client buttons are visible"
    test_name = "test_tangerine_homepage"

    snapshot = BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine Sign In",
        dom=dom,
        element_tree=element_tree,
        screenshot_base64=screenshot_base64,
        network_events=network_events,
    )

    # Explicit prompt variables for direct ai invocation without using CLI.
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

    output_path = resolve_output_path(f"pytest_demo/tests/ai/generated_playwright/{test_name}.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_code, encoding="utf-8")

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert f"def {test_name}(" in content
    assert "page.goto" in content
