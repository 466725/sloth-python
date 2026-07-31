import pytest


@pytest.mark.ddt
@pytest.mark.ui
@pytest.mark.playwright
@pytest.mark.parametrize(
    "html, selector, expected_text",
    [
        ("<h1>Hello</h1>", "h1", "Hello"),
        ("<button>Submit</button>", "button", "Submit"),
    ],
)
def test_playwright_ddt_demo(html, selector, expected_text):
    pw_api = pytest.importorskip("playwright.sync_api")
    with pw_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except pw_api.Error as exc:
            pytest.skip(f"Playwright browser is not installed: {exc}")
        page = browser.new_page()
        page.set_content(html)
        assert page.locator(selector).inner_text() == expected_text
        browser.close()
