from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, expect, sync_playwright


class PlaywrightHookDemoPlugin:
	"""Runtime plugin showing how pytest hooks can work with Playwright tests."""

	def __init__(self, item: pytest.Item, page: Page, screenshot_path: Path) -> None:
		self.item = item
		self.page = page
		self.screenshot_path = screenshot_path

	def pytest_runtest_call(self, item: pytest.Item) -> None:
		if item is self.item:
			item.user_properties.append(("hook_call", "ran"))

	@pytest.hookimpl(hookwrapper=True)
	def pytest_runtest_makereport(self, item: pytest.Item, call: pytest.CallInfo[None]):
		outcome = yield
		report = outcome.get_result()

		if item is self.item and report.when == "call":
			setattr(item, "rep_call", report)
			item.user_properties.append(("hook_call_outcome", report.outcome))
			if report.failed:
				self.page.screenshot(path=str(self.screenshot_path), full_page=True)


@pytest.fixture
def hooked_page(request: pytest.FixtureRequest, tmp_path: Path):
	"""Create a Playwright page and register a local pytest hook plugin."""
	screenshot_path = tmp_path / "hook_failure.png"

	with sync_playwright() as p:
		try:
			browser = p.chromium.launch(headless=True)
		except PlaywrightError as exc:
			pytest.skip(f"Playwright browser is not installed: {exc}")

		context = browser.new_context()
		page = context.new_page()

		plugin = PlaywrightHookDemoPlugin(request.node, page, screenshot_path)
		request.config.pluginmanager.register(plugin, name=f"hook-demo-{request.node.nodeid}")

		yield page, screenshot_path

		request.config.pluginmanager.unregister(plugin)
		rep_call = getattr(request.node, "rep_call", None)
		assert rep_call is not None, "pytest_runtest_makereport did not run for call phase"
		assert rep_call.outcome == "passed"

		context.close()
		browser.close()


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_pytest_hook_demo(hooked_page, request: pytest.FixtureRequest) -> None:
	"""Demo test: verify hook metadata while running a simple Playwright check."""
	page, screenshot_path = hooked_page

	page.set_content("<h1 id='title'>Hook Demo</h1>")
	expect(page.locator("#title")).to_have_text("Hook Demo")

	properties = dict(request.node.user_properties)
	assert properties.get("hook_call") == "ran"
	assert not screenshot_path.exists()
