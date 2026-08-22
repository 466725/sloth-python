import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, expect, sync_playwright


@pytest.fixture
def page():
	"""Create a fresh Playwright page for each test."""
	with sync_playwright() as playwright:
		try:
			browser = playwright.chromium.launch(headless=True)
		except PlaywrightError as exc:
			pytest.skip(f"Playwright browser is not installed: {exc}")

		context = browser.new_context()
		page = context.new_page()
		yield page
		context.close()
		browser.close()


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_plugin_demo(page: Page) -> None:
	"""Use the page fixture supplied by the pytest-playwright plugin."""
	page.set_content("<button id='hello'>Say hello</button><p id='message'></p>")
	page.locator("#hello").click()
	page.locator("#message").evaluate("element => element.textContent = 'Hello, Playwright!'")

	expect(page.locator("#message")).to_have_text("Hello, Playwright!")
