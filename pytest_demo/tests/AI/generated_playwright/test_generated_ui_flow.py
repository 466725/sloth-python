import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.ai
def test_tangerine_get_our_app_links(browser):
    page = browser.new_page()
    page.goto("https://www.tangerine.ca/en/personal")
    assert page.title() == "Personal Online Banking: Digital Banking in Canada | Tangerine | Tangerine"
    ios_link = page.locator('text=Get Our App (iOS)')
    android_link = page.locator('text=Get Our App (Android)')
    assert ios_link.is_visible()
    assert android_link.is_visible()
