from __future__ import annotations

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect, sync_playwright


@pytest.fixture
def page():
    """Create a fresh Playwright page for each test."""
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except PlaywrightError as exc:
            pytest.skip(f"Playwright browser is not installed: {exc}")
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_shadow_dom_demo(page) -> None:
    """Simple demo for interacting with open shadow DOM using Playwright locators."""
    page.set_content(
        """
        <html>
          <head><title>Shadow DOM Demo</title></head>
          <body>
            <demo-shadow></demo-shadow>
            <script>
              class DemoShadow extends HTMLElement {
                constructor() {
                  super();
                  const root = this.attachShadow({ mode: "open" });
                  root.innerHTML = `
                    <button id="shadow-btn">Click me</button>
                    <span id="result">Not clicked</span>
                  `;
                  root.querySelector("#shadow-btn").addEventListener("click", () => {
                    root.querySelector("#result").textContent = "Clicked";
                  });
                }
              }
              customElements.define("demo-shadow", DemoShadow);
            </script>
          </body>
        </html>
        """
    )

    shadow_host = page.locator("demo-shadow")
    shadow_host.locator("#shadow-btn").click()
    expect(shadow_host.locator("#result")).to_have_text("Clicked")