from __future__ import annotations

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect, sync_playwright


@pytest.fixture
def browser():
	"""Launch a browser once per test and close it afterward."""
	with sync_playwright() as p:
		try:
			browser = p.chromium.launch(headless=True)
		except PlaywrightError as exc:
			pytest.skip(f"Playwright browser is not installed: {exc}")
		yield browser
		browser.close()


@pytest.mark.ui
@pytest.mark.playwright
def test_browser_context_basic_usage(browser) -> None:
	"""Create a browser context and verify simple page content."""
	context = browser.new_context(locale="en-US")
	page = context.new_page()

	page.set_content("<h1 id='message'>Hello Context</h1>")
	expect(page.locator("#message")).to_have_text("Hello Context")

	context.close()


@pytest.mark.ui
@pytest.mark.playwright
def test_browser_context_isolation(browser) -> None:
	"""Different contexts should not share localStorage data."""
	context_a = browser.new_context()
	page_a = context_a.new_page()
	page_a.set_content("<p>Context A</p>")
	page_a.evaluate("localStorage.setItem('token', 'abc123')")
	stored_a = page_a.evaluate("localStorage.getItem('token')")
	assert stored_a == "abc123"

	context_b = browser.new_context()
	page_b = context_b.new_page()
	page_b.set_content("<p>Context B</p>")
	stored_b = page_b.evaluate("localStorage.getItem('token')")
	assert stored_b is None

	context_a.close()
	context_b.close()
