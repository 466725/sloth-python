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


def _load_checkbox_demo_page(page) -> None:
		page.set_content(
				"""
				<html>
					<head><title>Checkbox Demo</title></head>
					<body>
						<label><input id="news" type="checkbox" /> Subscribe newsletter</label>
						<button id="save">Save</button>
						<p id="result">unchecked</p>

						<script>
							const checkbox = document.getElementById('news');
							const save = document.getElementById('save');
							const result = document.getElementById('result');
							save.addEventListener('click', () => {
								result.textContent = checkbox.checked ? 'checked' : 'unchecked';
							});
						</script>
					</body>
				</html>
				"""
		)


@pytest.mark.ui
@pytest.mark.playwright
def test_checkbox_check_and_save(page) -> None:
		"""Check the checkbox and verify saved state."""
		_load_checkbox_demo_page(page)

		checkbox = page.locator("#news")
		checkbox.check()
		expect(checkbox).to_be_checked()

		page.locator("#save").click()
		expect(page.locator("#result")).to_have_text("checked")


@pytest.mark.ui
@pytest.mark.playwright
def test_checkbox_uncheck_and_save(page) -> None:
		"""Check then uncheck the checkbox and verify saved state."""
		_load_checkbox_demo_page(page)

		checkbox = page.locator("#news")
		checkbox.check()
		checkbox.uncheck()
		expect(checkbox).not_to_be_checked()

		page.locator("#save").click()
		expect(page.locator("#result")).to_have_text("unchecked")
