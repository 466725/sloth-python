from __future__ import annotations

import pytest


def _assert_xpath_found_and_visible(page, xpath: str, *, wait_visible: bool = True) -> None:
    locator = page.locator(xpath)
    assert locator.count() > 0, f"No element found for XPath: {xpath}"
    if wait_visible:
        locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_role_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(page, "//a[normalize-space()='Personal']")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_text_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(page, "//*[normalize-space()='Personal']")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_label_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(page, "//*[@aria-label='Search, opens dialogue']")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_alt_text_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(page, "//img[@alt='Tangerine']")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_title_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(page, "//*[@title='Search, opens dialogue']")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_placeholder_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    _assert_xpath_found_and_visible(
        page,
        "//input[@placeholder='Search…'] | //textarea[@placeholder='Search…']",
        wait_visible=False,
    )


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_xpath_test_id_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    page.evaluate(
        """
        () => {
            const personalLink = [...document.querySelectorAll('a')].find(
                (el) => (el.textContent || '').trim() === 'Personal'
            );
            if (!personalLink) {
                throw new Error('Unable to find Personal link for test id locator demo');
            }
            personalLink.setAttribute('data-testid', 'nav-personal-link');
        }
        """
    )
    _assert_xpath_found_and_visible(page, "//*[@data-testid='nav-personal-link']")

