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
def test_keyboard_actions(page) -> None:
	"""Simple keyboard actions: type, select all, replace, then press Enter."""
	page.set_content(
		"""
		<input id="name" placeholder="Type here" />
		<p id="result"></p>
		<script>
			const input = document.getElementById('name');
			const result = document.getElementById('result');
			input.addEventListener('keydown', (event) => {
				if (event.key === 'Enter') {
					result.textContent = input.value;
				}
			});
		</script>
		"""
	)

	name_input = page.locator("#name")
	name_input.click()
	name_input.type("hello")
	name_input.press("Control+A")
	name_input.type("Playwright")
	name_input.press("Enter")

	expect(page.locator("#result")).to_have_text("Playwright")


@pytest.mark.ui
@pytest.mark.playwright
def test_mouse_actions(page) -> None:
	"""Simple mouse actions: click, double-click, hover, and drag-and-drop."""
	page.set_content(
		"""
		<button id="action-btn">Click me</button>
		<p id="click-status">0</p>
		<p id="dbl-status">no</p>

		<div id="hover-box" style="width: 140px; height: 40px; background: #ddd;">
			Hover on me
		</div>
		<p id="hover-status">no</p>

		<div id="drag-item" draggable="true"
			 style="width: 80px; height: 30px; background: #9cf; margin-top: 8px;">
			Drag me
		</div>
		<div id="drop-zone"
			 style="width: 140px; height: 50px; background: #efe; margin-top: 8px;">
			Drop here
		</div>

		<script>
			const btn = document.getElementById('action-btn');
			const clickStatus = document.getElementById('click-status');
			const dblStatus = document.getElementById('dbl-status');
			const hoverBox = document.getElementById('hover-box');
			const hoverStatus = document.getElementById('hover-status');
			const dragItem = document.getElementById('drag-item');
			const dropZone = document.getElementById('drop-zone');

			let clickCount = 0;
			btn.addEventListener('click', () => {
				clickCount += 1;
				clickStatus.textContent = String(clickCount);
			});
			btn.addEventListener('dblclick', () => {
				dblStatus.textContent = 'yes';
			});

			hoverBox.addEventListener('mouseenter', () => {
				hoverStatus.textContent = 'yes';
			});

			dragItem.addEventListener('dragstart', (event) => {
				event.dataTransfer.setData('text/plain', 'dragged');
			});
			dropZone.addEventListener('dragover', (event) => {
				event.preventDefault();
			});
			dropZone.addEventListener('drop', (event) => {
				event.preventDefault();
				dropZone.textContent = 'Dropped!';
			});
		</script>
		"""
	)

	action_btn = page.locator("#action-btn")
	action_btn.click()
	expect(page.locator("#click-status")).to_have_text("1")

	action_btn.dblclick()
	expect(page.locator("#dbl-status")).to_have_text("yes")

	page.locator("#hover-box").hover()
	expect(page.locator("#hover-status")).to_have_text("yes")

	page.drag_and_drop("#drag-item", "#drop-zone")
	expect(page.locator("#drop-zone")).to_have_text("Dropped!")
