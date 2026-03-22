from playwright.sync_api import Page
import pytest

@pytest.mark.ai
def test_tangerine_homepage_generated(page: Page):
    page.goto("https://www.tangerine.ca/en/personal", wait_until="domcontentloaded")
    
    # Verify page loads with correct title
    assert page.title() == "Tangerine"
    
    # Verify Sign In button is visible
    login_button = page.locator("#login")
    assert login_button.is_visible()
    
    # Verify Sign Up button is visible
    signup_button = page.locator("#menu_signup")
    assert signup_button.is_visible()
    
    # Verify main heading is present
    heading = page.locator("h1")
    assert heading.is_visible()
    assert "Welcome to Tangerine" in heading.text_content()
