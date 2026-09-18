import pytest


@pytest.mark.ddt
@pytest.mark.ui
@pytest.mark.playwright
def test_playwright_web_table_demo():
    pw_api = pytest.importorskip("playwright.sync_api")
    with pw_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except pw_api.Error as exc:
            pytest.skip(f"Playwright browser is not installed: {exc}")

        page = browser.new_page()
        page.set_content(
            """
            <table id="users">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Role</th>
                        <th>Active</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Alice</td>
                        <td>QA</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td>Bob</td>
                        <td>Developer</td>
                        <td>No</td>
                    </tr>
                </tbody>
            </table>
            """
        )

        headers = page.locator("#users thead th").all_inner_texts()
        first_row = page.locator("#users tbody tr").first.locator("td").all_inner_texts()

        assert headers == ["Name", "Role", "Active"]
        assert page.locator("#users tbody tr").count() == 2
        assert first_row == ["Alice", "QA", "Yes"]

        browser.close()
