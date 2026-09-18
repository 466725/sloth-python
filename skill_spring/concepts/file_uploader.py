from pathlib import Path

import pytest


@pytest.mark.ui
@pytest.mark.playwright
def test_file_upload_from_windows_folder(tmp_path: Path) -> None:
    pw_api = pytest.importorskip("playwright.sync_api")

    upload_file = tmp_path / "upload-demo.txt"
    upload_file.write_text("hello from windows temp folder", encoding="utf-8")

    with pw_api.sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(
            """
            <html>
                <body>
                    <input id="file-upload" type="file" />
                </body>
            </html>
            """
        )

        # set_input_files simulates selecting a file from the OS file picker.
        page.locator("#file-upload").set_input_files(str(upload_file))

        selected_name = page.eval_on_selector(
            "#file-upload",
            "input => input.files && input.files.length ? input.files[0].name : ''",
        )
        assert selected_name == upload_file.name

        browser.close()
