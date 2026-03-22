import pytest
from playwright.sync_api import Page


@pytest.mark.ai
@pytest.mark.ui
def test_tangerine_get_our_app_links(page: Page):
    """Verify that 'Get Our App' link is visible on the Tangerine homepage."""
    
    # Navigate to Tangerine homepage
    page.goto("https://www.tangerine.ca/en/personal", wait_until="domcontentloaded")
    
    # Verify page loads successfully
    assert page.title() != "", "Page title should not be empty"
    
    # Verify Get Our App link is visible
    get_app_link = page.locator("text=/Get.*App/i").first
    assert get_app_link.is_visible(), "Get Our App link should be visible"
    
    # Log the element info for verification
    link_text = get_app_link.text_content()
    print(f"✅ Test passed! Found visible 'Get Our App' element: '{link_text}'")

