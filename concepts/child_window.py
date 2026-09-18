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
def test_open_child_window_and_verify_content(page) -> None:
	"""Open a child window and verify content in the new page."""
	child_url = "data:text/html,<title>Child Window</title><h1 id='child-title'>Hello Child</h1>"

	page.set_content(
		f"""
		<h1 id="parent-title">Parent Window</h1>
		<button id="open-child" onclick="window.open('{child_url}', '_blank')">
			Open Child Window
		</button>
		"""
	)

	with page.context.expect_page() as child_event:
		page.locator("#open-child").click()

	child_page = child_event.value
	child_page.wait_for_load_state("domcontentloaded")

	expect(child_page).to_have_title("Child Window")
	expect(child_page.locator("#child-title")).to_have_text("Hello Child")


@pytest.mark.ui
@pytest.mark.playwright
def test_parent_window_stays_unchanged_after_child_opens(page) -> None:
	"""Opening a child window should keep parent page content unchanged."""
	page.set_content(
		"""
		<h1 id="parent-title">Parent Window</h1>
		<a id="open-child-link" target="_blank"
		   href="data:text/html,<title>Child</title><p>child tab</p>">
		   Open child tab
		</a>
		"""
	)

	with page.context.expect_page() as child_event:
		page.locator("#open-child-link").click()

	child_page = child_event.value
	child_page.wait_for_load_state("domcontentloaded")

	expect(page.locator("#parent-title")).to_have_text("Parent Window")
	expect(child_page).to_have_title("Child")
