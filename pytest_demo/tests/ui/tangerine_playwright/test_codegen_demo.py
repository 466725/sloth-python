import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.playwright
def test_example(page: Page) -> None:
    page.goto("https://www.tangerine.ca/en/personal")
    expect(page.get_by_role("region", name="Cookie banner")).to_be_visible()
    page.get_by_role("button", name="Accept All").click()

    page.get_by_role("link", name="Log In").click()
    page.get_by_role("link", name="Sign Me Up").click()
    page.get_by_role("link", name="Tangerine Home").click()
