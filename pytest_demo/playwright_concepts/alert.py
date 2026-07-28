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


def _load_popup_demo_page(page) -> None:
	page.set_content(
		"""
		<button id="alert-btn" onclick="alert('Hello Alert')">Open Alert</button>
		<button id="confirm-btn" onclick="window.__confirmResult = confirm('Do you agree?')">Open Confirm</button>
		<button id="prompt-btn" onclick="window.__promptValue = prompt('What is your name?', '')">Open Prompt</button>

		<p id="confirm-result">none</p>
		<p id="prompt-result">none</p>

		<script>
			setInterval(() => {
				const confirmText = window.__confirmResult === undefined ? 'none' : String(window.__confirmResult);
				const promptText = window.__promptValue === undefined || window.__promptValue === null
					? 'none'
					: window.__promptValue;
				document.getElementById('confirm-result').textContent = confirmText;
				document.getElementById('prompt-result').textContent = promptText;
			}, 20);
		</script>
		"""
	)


@pytest.mark.ui
@pytest.mark.playwright
def test_alert_popup_accept(page) -> None:
	"""Handle a basic alert popup by accepting it."""
	_load_popup_demo_page(page)

	dialog_message = {"value": ""}

	def on_dialog(dialog):
		dialog_message["value"] = dialog.message
		dialog.accept()

	page.once("dialog", on_dialog)
	page.locator("#alert-btn").click()

	assert dialog_message["value"] == "Hello Alert"


@pytest.mark.ui
@pytest.mark.playwright
def test_confirm_popup_dismiss(page) -> None:
	"""Handle a confirm popup by dismissing it."""
	_load_popup_demo_page(page)

	page.once("dialog", lambda dialog: dialog.dismiss())
	page.locator("#confirm-btn").click()

	expect(page.locator("#confirm-result")).to_have_text("False")


@pytest.mark.ui
@pytest.mark.playwright
def test_prompt_popup_fill_text(page) -> None:
	"""Handle a prompt popup by entering text and accepting."""
	_load_popup_demo_page(page)

	page.once("dialog", lambda dialog: dialog.accept("Alice"))
	page.locator("#prompt-btn").click()

	expect(page.locator("#prompt-result")).to_have_text("Alice")
