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


def _load_text_demo_page(page) -> None:
	page.set_content(
		"""
		<!doctype html>
		<html lang="en">
			<head>
				<meta charset="utf-8" />
				<title>Playwright Text Verification Demo</title>
			</head>
			<body>
				<h1 id="heading">Account Overview</h1>
				<p id="welcome">Welcome back, Alice.</p>
				<ul id="features">
					<li>Realtime alerts</li>
					<li>Secure transfer</li>
					<li>Export reports</li>
				</ul>
				<button id="refresh" type="button">Refresh status</button>
				<p id="status" aria-live="polite">Status: Pending</p>

				<script>
					document.getElementById('refresh').addEventListener('click', () => {
						document.getElementById('status').textContent = 'Status: Synced';
					});
				</script>
			</body>
		</html>
		"""
	)


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_text_verification_demo(page) -> None:
	"""Demonstrate common text assertions with Playwright and pytest."""
	_load_text_demo_page(page)

	expect(page).to_have_title("Playwright Text Verification Demo")
	expect(page.locator("#heading")).to_have_text("Account Overview")
	expect(page.locator("#welcome")).to_contain_text("Alice")
	expect(page.locator("#features li")).to_have_text(
		["Realtime alerts", "Secure transfer", "Export reports"]
	)
	expect(page.locator("#status")).to_have_text("Status: Pending")

	page.locator("#refresh").click()
	expect(page.locator("#status")).to_have_text("Status: Synced")

