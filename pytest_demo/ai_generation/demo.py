from pathlib import Path

from pytest_demo.ai_generation.generator import PlaywrightTestScriptGenerator, ScriptClient
from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.paths import resolve_output_path


def demo_generate_tangerine_homepage_test():
    """Demo: Generate a test script from a snapshot without live browser."""

    snapshot = BrowserSnapshot(
        url="https://www.tangerine.ca/en/personal",
        title="Tangerine",
        dom="""<html>
<head><title>Tangerine</title></head>
<body>
  <header>
    <nav>
      <a id="login" href="/app#/login">Log in</a>
      <a id="menu_signup" href="/app#/signup">Sign me up</a>
    </nav>
  </header>
  <main>
    <h1>Welcome to Tangerine</h1>
    <p>Your trusted online banking partner</p>
  </main>
</body>
</html>""",
        element_tree="""<body>
  <header>
    <nav>
      <a id="login" href="/app#/login">Log in</a>
      <a id="menu_signup" href="/app#/signup">Sign me up</a>
    </nav>
  </header>
  <main>
    <h1>Welcome to Tangerine</h1>
    <p>Your trusted online banking partner</p>
  </main>
</body>""",
        screenshot_base64="iVBORw0KGgoAAAANSUhEUgAAAAUA...",
        network_events=[
            {"method": "GET", "url": "https://www.tangerine.ca/en/personal", "status": "200"},
            {"method": "GET", "url": "https://cdn.tangerine.ca/styles.css", "status": "200"},
        ],
    )

    class MockClient:
        def generate(self, *, system_prompt: str, user_prompt: str) -> str:
            return """```python
from playwright.sync_api import Page
import pytest

@pytest.mark.ui
def test_tangerine_homepage_generated(page: Page):
    page.goto("https://www.tangerine.ca/en/personal", wait_until="domcontentloaded")
    
    # Verify page loads with correct title
    assert page.title() == "Tangerine"
    
    # Verify Sign In button is visible
    login_button = page.locator("#login")
    assert login_button.is_visible()
    
    # Verify Sign Up button is visible
    signup_button = page.locator("#menu_signup")
    assert signup_button.is_visible()
    
    # Verify main heading is present
    heading = page.locator("h1")
    assert heading.is_visible()
    assert "Welcome to Tangerine" in heading.text_content()
```"""

    client: ScriptClient = MockClient()
    generator = PlaywrightTestScriptGenerator(client)

    output_path = resolve_output_path(
        Path("pytest_demo/tests/AI/generated_playwright/test_tangerine_homepage_generated.py")
    )
    result = generator.generate(
        snapshot=snapshot,
        goal="Verify the Tangerine homepage loads, displays the Sign In and Sign Up buttons",
        test_name="test_tangerine_homepage_generated",
        output_path=output_path,
    )

    print("\n" + "=" * 80)
    print("GENERATED TEST SCRIPT")
    print("=" * 80)
    print(f"\nOutput file: {result.output_path}")
    print(f"File exists: {result.output_path.exists()}")
    print("\nGenerated code:\n")
    print(result.code)
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo_generate_tangerine_homepage_test()

