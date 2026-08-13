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
		context = browser.new_context(viewport={"width": 960, "height": 640}, color_scheme="light")
		page = context.new_page()
		yield page
		context.close()
		browser.close()


def _load_visual_demo_page(page) -> None:
	page.set_content(
		"""
		<!doctype html>
		<html lang="en">
			<head>
				<meta charset="utf-8" />
				<title>Playwright Visual Demo</title>
				<style>
					:root {
						color-scheme: light;
						font-family: Arial, Helvetica, sans-serif;
					}
					body {
						margin: 0;
						min-height: 100vh;
						display: grid;
						place-items: center;
						background: linear-gradient(135deg, #f5efe6 0%, #eef4ff 100%);
					}
					.card {
						width: 420px;
						padding: 28px;
						border-radius: 24px;
						background: rgba(255, 255, 255, 0.92);
						box-shadow: 0 24px 60px rgba(29, 41, 62, 0.16);
						border: 1px solid rgba(255, 255, 255, 0.85);
					}
					.badge {
						display: inline-block;
						padding: 6px 12px;
						border-radius: 999px;
						background: #19324d;
						color: white;
						font-size: 12px;
						letter-spacing: 0.08em;
						text-transform: uppercase;
					}
					h1 {
						margin: 18px 0 10px;
						font-size: 32px;
						line-height: 1.1;
						color: #142033;
					}
					p {
						margin: 0;
						color: #526077;
						font-size: 15px;
						line-height: 1.55;
					}
					.metrics {
						display: grid;
						grid-template-columns: repeat(3, 1fr);
						gap: 12px;
						margin-top: 22px;
					}
					.metric {
						padding: 14px;
						border-radius: 16px;
						background: #f4f7fb;
					}
					.metric .value {
						display: block;
						font-size: 22px;
						font-weight: 700;
						color: #19324d;
					}
					.metric .label {
						display: block;
						margin-top: 4px;
						font-size: 12px;
						text-transform: uppercase;
						letter-spacing: 0.08em;
						color: #76859a;
					}
				</style>
			</head>
			<body>
				<main class="card" aria-label="visual demo card">
					<span class="badge">Visual check</span>
					<h1>Stable layout</h1>
					<p>This demo shows how to verify a rendered page with a Playwright screenshot assertion.</p>
					<section class="metrics" aria-label="summary metrics">
						<div class="metric"><span class="value">12</span><span class="label">tests</span></div>
						<div class="metric"><span class="value">98%</span><span class="label">pass rate</span></div>
						<div class="metric"><span class="value">1.2s</span><span class="label">runtime</span></div>
					</section>
				</main>
			</body>
		</html>
		"""
	)


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_visual_verification_demo(page) -> None:
	"""Demonstrate a basic Playwright visual regression check."""
	_load_visual_demo_page(page)

	expect(page.locator("main[aria-label='visual demo card']")).to_have_screenshot(
		name="visual-demo-card.png",
		animations="disabled",
		caret="hide",
	)
