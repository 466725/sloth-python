from __future__ import annotations

import pytest


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_role_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    locator = page.get_by_role("link", name="Personal")
    assert locator.count() > 0
    locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_text_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    locator = page.get_by_text("Personal", exact=True)
    assert locator.count() > 0
    locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_label_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    locator = page.get_by_label("Search, opens dialogue")
    assert locator.count() > 0
    locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_alt_text_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    locator = page.get_by_alt_text("Tangerine")
    assert locator.count() > 0
    locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_title_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    title_locator = page.get_by_title("Search, opens dialogue")
    assert title_locator.count() > 0
    title_locator.first.wait_for(state="visible")


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_placeholder_hard_coded(tangerine_homepage):
    page = tangerine_homepage
    placeholder_locator = page.get_by_placeholder("Search…")
    assert placeholder_locator.count() > 0