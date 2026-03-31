import pytest


@pytest.mark.ui
@pytest.mark.playwright
def test_example(tangerine_homepage) -> None:
    """Codegen-recorded flow: navigate Log In, Sign Me Up, back to Home."""
    page = tangerine_homepage

    page.get_by_role("link", name="Log In").click()
    page.get_by_role("link", name="Sign Me Up").click()
    page.get_by_role("link", name="Tangerine Home").click()
