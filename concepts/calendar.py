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


def _load_calendar_demo_page(page) -> None:
		page.set_content(
				"""
				<html>
					<head><title>Calendar Demo</title></head>
					<body>
						<label for="checkin">Check-in date</label>
						<input id="checkin" type="date" />
						<button id="save">Save</button>
						<p id="result">none</p>

						<script>
							const save = document.getElementById('save');
							const checkin = document.getElementById('checkin');
							const result = document.getElementById('result');
							save.addEventListener('click', () => {
								result.textContent = checkin.value || 'none';
							});
						</script>
					</body>
				</html>
				"""
		)


@pytest.mark.ui
@pytest.mark.playwright
def test_calendar_select_date_and_save(page) -> None:
		"""Select a date from the calendar input and verify saved value."""
		_load_calendar_demo_page(page)

		page.locator("#checkin").fill("2026-12-25")
		page.locator("#save").click()

		expect(page.locator("#result")).to_have_text("2026-12-25")


@pytest.mark.ui
@pytest.mark.playwright
def test_calendar_default_when_no_date_selected(page) -> None:
		"""When no date is selected, keep a clear default result."""
		_load_calendar_demo_page(page)

		page.locator("#save").click()

		expect(page.locator("#result")).to_have_text("none")
