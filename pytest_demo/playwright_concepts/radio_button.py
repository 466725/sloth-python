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


def _load_radio_button_demo_page(page) -> None:
    page.set_content(
        """
        <html>
            <head><title>Radio Button Demo</title></head>
            <body>
                <label><input id="small"  type="radio" name="size" value="small"  /> Small</label>
                <label><input id="medium" type="radio" name="size" value="medium" /> Medium</label>
                <label><input id="large"  type="radio" name="size" value="large"  /> Large</label>
                <button id="save">Save</button>
                <p id="result">none</p>

                <script>
                    document.getElementById('save').addEventListener('click', () => {
                        const selected = document.querySelector('input[name="size"]:checked');
                        document.getElementById('result').textContent = selected ? selected.value : 'none';
                    });
                </script>
            </body>
        </html>
        """
    )


@pytest.mark.ui
@pytest.mark.playwright
def test_radio_button_select_and_save(page) -> None:
    """Select a radio button and verify the saved result."""
    _load_radio_button_demo_page(page)

    page.locator("#medium").check()
    expect(page.locator("#medium")).to_be_checked()
    expect(page.locator("#small")).not_to_be_checked()
    expect(page.locator("#large")).not_to_be_checked()

    page.locator("#save").click()
    expect(page.locator("#result")).to_have_text("medium")


@pytest.mark.ui
@pytest.mark.playwright
def test_radio_button_switch_selection(page) -> None:
    """Switch from one radio button to another and verify only the new one is checked."""
    _load_radio_button_demo_page(page)

    page.locator("#small").check()
    expect(page.locator("#small")).to_be_checked()

    # Switch selection — only the new choice should be checked
    page.locator("#large").check()
    expect(page.locator("#large")).to_be_checked()
    expect(page.locator("#small")).not_to_be_checked()

    page.locator("#save").click()
    expect(page.locator("#result")).to_have_text("large")
