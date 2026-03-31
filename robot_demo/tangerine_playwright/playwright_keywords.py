from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    # Ensure local imports resolve when Robot runs this suite directly.
    sys.path.insert(0, str(PROJECT_ROOT))

from robot.libraries.BuiltIn import BuiltIn
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import click as self_healing_click
from utils.config import settings

ROBOT_LIBRARY_SCOPE = "GLOBAL"

_pw: Playwright | None = None
_browser: Browser | None = None
_context: BrowserContext | None = None
_page: Page | None = None

# Keep Robot self-healing read-only by default to avoid silent locator store writes.
SELF_HEAL_AUTO_UPDATE = True


def open_browser_session() -> None:
    global _pw, _browser, _context, _page
    if _page is not None:
        return

    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch(headless=settings.playwright.headless)


def close_browser_session() -> None:
    global _pw, _browser, _context, _page
    _close_test_context()
    if _browser is not None:
        _browser.close()
    if _pw is not None:
        _pw.stop()

    _pw = None
    _browser = None
    _context = None
    _page = None


def open_tangerine_homepage() -> None:
    _start_test_context()
    page = _require_page()
    page.goto(settings.ui.base_url, wait_until="domcontentloaded")
    accept_cookies_if_present()


def attach_failure_artifacts() -> None:
    """On failure, attach screenshot and video links to Robot's default report."""
    page = _page
    context = _context
    if page is None or context is None:
        return

    # Gets Robot’s output directory (or defaults to temps) and turns it into a filesystem path object.
    built_in = BuiltIn()
    output_dir = Path(_variable_as_str(built_in, "${OUTPUT DIR}", "temps"))
    artifacts_dir = output_dir / "artifacts" / "playwright"
    screenshot_dir = artifacts_dir / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    status = built_in.get_variable_value("${TEST STATUS}", "")
    failed = status == "FAIL"
    if failed:
        test_name = _variable_as_str(built_in, "${TEST NAME}", "test")
        safe_name = _safe_file_name(test_name)
        screenshot_name = f"{safe_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        screenshot_path = screenshot_dir / screenshot_name
        page.screenshot(path=str(screenshot_path), full_page=True)
        _log_file_link(output_dir, screenshot_path, "Failure screenshot")

    video_path: Path | None = None
    if page.video is not None:
        try:
            # Path is known after context/page is closed.
            context.close()
            video_path = Path(page.video.path())
        except Exception:
            video_path = None
    else:
        try:
            context.close()
        except Exception:
            pass

    if failed and video_path is not None and video_path.exists():
        _log_file_link(output_dir, video_path, "Failure video")
    elif not failed and video_path is not None and video_path.exists():
        video_path.unlink()

    _reset_page_context_refs()


def accept_cookies_if_present() -> None:
    page = _require_page()
    button = page.locator("#onetrust-accept-btn-handler").first
    if button.count() == 0:
        return
    if button.is_visible():
        button.click(timeout=5000)


def go_to_sign_in_page() -> None:
    _click_with_self_healing("tangerine.login")


def go_to_sign_up_page() -> None:
    _click_with_self_healing("tangerine.login")
    _click_with_self_healing("tangerine.signup")


def page_title_should_contain(expected: str) -> None:
    page = _require_page()
    title = page.title()
    if expected not in title:
        raise AssertionError(f"Expected '{expected}' to be in page title, but got '{title}'.")


def _require_page() -> Page:
    if _page is None:
        raise RuntimeError("Browser session is not started. Call 'Open Browser Session' first.")
    return _page


def _click_with_self_healing(locator_key: str) -> None:
    page = _require_page()
    locator = get_locator(locator_key)
    self_healing_click(
        page,
        key=locator_key,
        locator=locator,
        auto_update=SELF_HEAL_AUTO_UPDATE,
    )


def _start_test_context() -> None:
    global _context, _page
    browser = _browser
    if browser is None:
        raise RuntimeError("Browser session is not started. Call 'Open Browser Session' first.")

    _close_test_context()
    video_dir = _video_dir_from_output_dir()
    _context = browser.new_context(locale=settings.ui.locale, record_video_dir=str(video_dir))
    _page = _context.new_page()


def _close_test_context() -> None:
    if _context is not None:
        try:
            _context.close()
        except Exception:
            pass
    _reset_page_context_refs()


def _reset_page_context_refs() -> None:
    global _context, _page
    _context = None
    _page = None


def _video_dir_from_output_dir() -> Path:
    output_dir = Path(_variable_as_str(BuiltIn(), "${OUTPUT DIR}", "temps"))
    video_dir = output_dir / "artifacts" / "playwright" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    return video_dir


def _log_file_link(output_dir: Path, file_path: Path, label: str) -> None:
    relative_path = file_path.relative_to(output_dir).as_posix()
    BuiltIn().log(f'{label}: <a href="{relative_path}">{relative_path}</a>', html=True)


def _safe_file_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "test"


def _variable_as_str(built_in: BuiltIn, name: str, default: str) -> str:
    value = built_in.get_variable_value(name, default)
    if isinstance(value, str):
        return value
    return str(value)
