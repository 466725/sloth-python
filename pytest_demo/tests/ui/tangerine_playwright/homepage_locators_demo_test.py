from __future__ import annotations

import pytest


def _first_visible_attr(page, css_selector: str, attribute_name: str) -> str:
    value = page.eval_on_selector_all(
        css_selector,
        """
        (els, attr) => {
            const visible = (el) => {
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style && style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
            };
            const el = els.find((candidate) => visible(candidate) && candidate.getAttribute(attr));
            return el ? el.getAttribute(attr) : null;
        }
        """,
        attribute_name,
    )
    assert value, f"No visible element with attribute '{attribute_name}' matched selector '{css_selector}'"
    return value


def _first_attr(page, css_selector: str, attribute_name: str) -> str:
    value = page.eval_on_selector_all(
        css_selector,
        """
        (els, attr) => {
            const el = els.find((candidate) => (candidate.getAttribute(attr) || '').trim().length > 0);
            return el ? el.getAttribute(attr) : null;
        }
        """,
        attribute_name,
    )
    assert value, f"No element with attribute '{attribute_name}' matched selector '{css_selector}'"
    return value


def _first_label_name(page) -> str:
    label_candidates = page.eval_on_selector_all(
        "label",
        """
        (els) => {
            const visible = (el) => {
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style && style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
            };
            return els
                .filter((el) => visible(el))
                .map((el) => (el.textContent || '').trim())
                .filter((text) => text.length > 0);
        }
        """,
    )
    for candidate in label_candidates:
        if page.get_by_label(candidate).count() > 0:
            return candidate

    aria_label = page.eval_on_selector_all(
        "[aria-label]",
        """
        (els) => {
            const visible = (el) => {
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style && style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
            };
            const el = els.find((candidate) => visible(candidate) && (candidate.getAttribute('aria-label') || '').trim());
            return el ? el.getAttribute('aria-label') : null;
        }
        """,
    )
    assert aria_label, "Expected a visible label-associated control (label text or aria-label) on Tangerine homepage"
    return aria_label


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_all_builtin_locators(tangerine_homepage):
    page = tangerine_homepage

    # 1) Role locator
    page.get_by_role("link", name="Personal").first.wait_for(state="visible")

    # 2) Text locator
    page.get_by_text("Personal", exact=True).first.wait_for(state="visible")

    # 3) Label locator
    label_name = _first_label_name(page)
    page.get_by_label(label_name).first.wait_for(state="visible")

    # 4) Alt text locator
    alt_text = _first_visible_attr(page, "img[alt]", "alt")
    page.get_by_alt_text(alt_text).first.wait_for(state="visible")

    # 5) Title locator
    title_text = _first_visible_attr(page, "[title]", "title")
    title_locator = page.get_by_title(title_text).first
    title_locator.wait_for(state="visible")
    title_locator.click()

    # 6) Placeholder locator
    placeholder_text = _first_attr(page, "input[placeholder], textarea[placeholder]", "placeholder")
    assert page.get_by_placeholder(placeholder_text).count() > 0

    # 7) Test id locator
    page.evaluate(
        """
        () => {
            const target = document.querySelector('[title], a, button, input, img');
            if (!target) {
                throw new Error('Unable to find element to set data-testid for locator demo');
            }
            target.setAttribute('data-testid', 'tangerine-home-demo-testid');
        }
        """
    )
    page.get_by_test_id("tangerine-home-demo-testid").first.wait_for(state="visible")


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


@pytest.mark.ui
@pytest.mark.playwright
def test_tangerine_homepage_locator_test_id_hard_coded(tangerine_homepage):
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
    test_id_locator = page.get_by_test_id("nav-personal-link")
    assert test_id_locator.count() > 0
    test_id_locator.first.wait_for(state="visible")
