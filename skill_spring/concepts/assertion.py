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


def _load_assertion_demo_page(page) -> None:
		page.set_content(
				"""
				<html>
					<head>
						<title>Playwright Assertion Demo</title>
					</head>
					<body>
						<h1 id="title">Welcome</h1>
						<button id="submit-btn">Submit</button>
						<input id="name-input" value="Alice" />
						<input id="agree" type="checkbox" checked />
						<p id="status" style="display: none;">Saved</p>
					</body>
				</html>
				"""
		)


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_assertions_demo(page) -> None:
		"""Straight-forward examples of common Playwright assertions."""
		_load_assertion_demo_page(page)

		expect(page).to_have_title("Playwright Assertion Demo")
		expect(page.locator("#title")).to_have_text("Welcome")
		expect(page.locator("#submit-btn")).to_be_visible()
		expect(page.locator("#name-input")).to_have_value("Alice")
		expect(page.locator("#agree")).to_be_checked()
		expect(page.locator("#status")).to_be_hidden()

