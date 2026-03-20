from __future__ import annotations

import logging
import os
from pathlib import Path
import re

import allure
import pytest

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pytest_demo.tests.ui.tangerine_support import (
    open_tangerine_homepage_playwright,
    open_tangerine_homepage_selenium,
)
from utils.config import settings
from utils.screenshot_handler import ScreenshotHandler

logger = logging.getLogger(__name__)

_VIDEO_MODE_FAILED = "failed"
_VIDEO_MODE_ALL = "all"
_VIDEO_MODE_OFF = "off"
_VALID_VIDEO_MODES = {_VIDEO_MODE_FAILED, _VIDEO_MODE_ALL, _VIDEO_MODE_OFF}


def _playwright_video_mode() -> str:
    # mode = os.getenv("PLAYWRIGHT_VIDEO_MODE", _VIDEO_MODE_FAILED).strip().lower()
    mode = _VIDEO_MODE_ALL
    if mode in _VALID_VIDEO_MODES:
        return mode
    logger.warning(
        "Invalid PLAYWRIGHT_VIDEO_MODE=%s. Falling back to '%s'.",
        mode,
        _VIDEO_MODE_FAILED,
    )
    return _VIDEO_MODE_ALL


def _slugify_nodeid(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", nodeid)


def _tangerine_playwright_video_dir() -> Path:
    project_root = Path(__file__).resolve().parents[3]
    video_dir = project_root / "temps" / "playwright-videos" / "tangerine_playwright"
    video_dir.mkdir(parents=True, exist_ok=True)
    return video_dir


def _attach_video_if_present(video_path: Path, name: str) -> None:
    if not video_path.exists():
        return
    attachment_type = getattr(allure.attachment_type, "WEBM", None)
    if attachment_type is None:
        allure.attach.file(str(video_path), name=name)
        return
    allure.attach.file(str(video_path), name=name, attachment_type=attachment_type, extension="webm")


def _attach_page_screenshot(page, name: str) -> None:
    allure.attach(
        page.screenshot(full_page=True),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="function")
def tangerine_homepage(request: pytest.FixtureRequest):
    pw = pytest.importorskip("playwright.sync_api")
    video_mode = _playwright_video_mode()
    video_dir = _tangerine_playwright_video_dir()
    with pw.sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.playwright.headless)
        context_options = {"locale": settings.ui.locale}
        if video_mode != _VIDEO_MODE_OFF:
            context_options["record_video_dir"] = str(video_dir)

        context = browser.new_context(**context_options)
        page = context.new_page()
        open_tangerine_homepage_playwright(page)
        yield page

        rep = getattr(request.node, "rep_call", None)
        failed = bool(rep and rep.failed)
        keep_video = (video_mode == _VIDEO_MODE_ALL) or (
            video_mode == _VIDEO_MODE_FAILED and failed
        )
        video = page.video

        _attach_page_screenshot(page, f"{request.node.name}-playwright")
        context.close()

        if video is not None:
            video_path = Path(video.path())
            if keep_video:
                _attach_video_if_present(
                    video_path,
                    f"{_slugify_nodeid(request.node.nodeid)}-playwright-video",
                )
            elif video_path.exists():
                video_path.unlink()

        browser.close()


@pytest.fixture(scope="function")
def open_tangerine_homepage(request: pytest.FixtureRequest):
    options = Options()
    for argument in settings.selenium.common_arguments:
        options.add_argument(argument)

    selenium_url = settings.selenium.remote_url
    if selenium_url:
        driver = webdriver.Remote(command_executor=selenium_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(settings.selenium.implicit_wait)
    open_tangerine_homepage_selenium(driver)
    sleep(settings.ui.sleep_time)

    yield driver

    # Attach screenshot only if the test failed
    # rep = getattr(request.node, "rep_call", None)
    # if rep is not None and rep.failed:
    #     handler = ScreenshotHandler(driver)
    #     handler.attach_screenshot(name=f"{request.node.name}-failure")

    # Attach a screenshot regardless of the test outcome
    handler = ScreenshotHandler(driver)
    handler.attach_screenshot(name=f"{request.node.name}")

    driver.quit()
