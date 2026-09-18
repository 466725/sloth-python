import pytest


@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_dropdown_demo():
    pw_api = pytest.importorskip("playwright.sync_api")
    with pw_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except pw_api.Error as exc:
            pytest.skip(f"Playwright browser is not installed: {exc}")

        page = browser.new_page()
        page.set_content(
            """
            <select id="cars">
                <option value="volvo">Volvo</option>
                <option value="saab">Saab</option>
            </select>
            """
        )
        page.locator("#cars").select_option("saab")
        assert page.locator("#cars").input_value() == "saab"
        browser.close()