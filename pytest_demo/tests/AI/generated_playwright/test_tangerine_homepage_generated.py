import re
from playwright.sync_api import Page, expect
import pytest

#@pytest.mark.ui
def test_tangerine_homepage_generated(page: Page):
    page.goto("https://www.tangerine.ca/en/personal", wait_until="domcontentloaded")
    
    # Verify page title contains brand name (full title can vary by locale/SEO copy)
    expect(page).to_have_title(re.compile(r".*Tangerine.*"))
    
    # Verify Sign In entry point is visible
    login_button = page.locator("#login")
    expect(login_button).to_be_visible()
    login_button.click()
    
    # Verify Sign Up entry point is visible after opening login menu
    signup_button = page.locator("#menu_signup")
    expect(signup_button).to_be_visible()
    
    # Verify a main heading is present
    heading = page.locator("h1")
    expect(heading.first).to_be_visible()
