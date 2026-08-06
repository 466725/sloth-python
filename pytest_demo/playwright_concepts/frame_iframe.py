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


def _load_iframe_demo_page(page) -> None:
    page.set_content(
        """
        <html>
            <head><title>Iframe Demo</title></head>
            <body>
                <h1>Host Page</h1>
                <iframe
                    id="demo-iframe"
                    srcdoc="
                        <html>
                            <body>
                                <button id='run-action'>Run Action</button>
                                <p id='result'>waiting</p>
                                <script>
                                    document.getElementById('run-action').addEventListener('click', () => {
                                        document.getElementById('result').textContent = 'done';
                                    });
                                </script>
                            </body>
                        </html>
                    "
                ></iframe>
            </body>
        </html>
        """
    )


@pytest.mark.ui
@pytest.mark.playwright
def test_iframe_interaction_with_frame_locator(page) -> None:
    """Interact with elements inside iframe using frame_locator."""
    _load_iframe_demo_page(page)

    iframe = page.frame_locator("#demo-iframe")
    iframe.locator("#run-action").click()
    expect(iframe.locator("#result")).to_have_text("done")