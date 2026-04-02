import pytest
from playwright.sync_api import Page

def test_tangerine_homepage(page: Page):
    page.goto("https://www.tangerine.ca/en/personal")
    assert page.title() == "Personal Online Banking: Digital Banking in Canada | Tangerine | Tangerine"
    assert page.get_by_role("button", name="Sign In").is_visible()
