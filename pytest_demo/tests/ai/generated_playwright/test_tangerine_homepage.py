import pytest
from playwright.sync_api import Page

def test_tangerine_homepage(page: Page):
    page.goto("https://www.tangerine.ca/en/personal")
    assert page.get_by_text("Log In").is_visible()
    assert page.get_by_text("Become a Client").is_visible()
