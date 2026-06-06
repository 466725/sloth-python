import time
from functools import wraps
import functools
import asyncio
from typing import Callable, Union
from playwright.async_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


def wait_for_visible(
        selector: str,
        timeout: float = 30000,
        poll_interval: float = 500,
        raise_on_timeout: bool = True,
):
    """
    Decorator that waits for a Playwright page element to be visible
    before executing the decorated function.

    Args:
        selector:         CSS / XPath / text selector for the target element.
        timeout:          Maximum time to wait in milliseconds (default 30 000 ms).
        poll_interval:    How often to poll visibility in milliseconds (default 500 ms).
        raise_on_timeout: Re-raise PlaywrightTimeoutError when True (default);
                          silently continue when False.

    Requirements:
        - The decorated function must be async.
        - Its first positional argument must be a Playwright `Page` instance.

    Usage:
        @wait_for_visible("#submit-btn", timeout=10_000)
        async def click_submit(page: Page):
            await page.click("#submit-btn")

        @wait_for_visible(".modal", timeout=5_000, raise_on_timeout=False)
        async def handle_modal(page: Page, extra_arg: str):
            ...
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Resolve the Page object — accept it as the first positional arg
            # or via a 'page' keyword argument.
            page: Page = kwargs.get("page") or next(
                (a for a in args if isinstance(a, Page)), None
            )
            if page is None:
                raise ValueError(
                    "wait_for_visible: could not find a Playwright `Page` instance "
                    "in the decorated function's arguments."
                )

            locator: Locator = page.locator(selector)

            try:
                await locator.wait_for(
                    state="visible",
                    timeout=timeout,
                )
            except PlaywrightTimeoutError as exc:
                if raise_on_timeout:
                    raise TimeoutError(
                        f"wait_for_visible: element '{selector}' was not visible "
                        f"within {timeout} ms."
                    ) from exc
                # Otherwise fall through and let the wrapped function decide.

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Synchronous variant (uses Playwright's sync API)
# ---------------------------------------------------------------------------
def wait_for_visible_sync(
        selector: str,
        timeout: float = 30000,
        raise_on_timeout: bool = True,
):
    """
    Synchronous version of wait_for_visible for use with
    playwright.sync_api.Page.

    Usage:
        @wait_for_visible_sync("#submit-btn", timeout=10_000)
        def click_submit(page):
            page.click("#submit-btn")
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from playwright.sync_api import Page as SyncPage
            from playwright.sync_api import TimeoutError as SyncTimeoutError

            page: SyncPage = kwargs.get("page") or next(
                (a for a in args if isinstance(a, SyncPage)), None
            )
            if page is None:
                raise ValueError(
                    "wait_for_visible_sync: could not find a Playwright `Page` "
                    "instance in the decorated function's arguments."
                )

            locator = page.locator(selector)

            try:
                locator.wait_for(state="visible", timeout=timeout)
            except SyncTimeoutError as exc:
                if raise_on_timeout:
                    raise TimeoutError(
                        f"wait_for_visible_sync: element '{selector}' was not "
                        f"visible within {timeout} ms."
                    ) from exc

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_call(func):
    """
    A simple decorator that logs when a function is called.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def measure_time(func):
    """
    A decorator that measures how long a function takes to run.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[TIMER] {func.__name__} executed in {duration:.4f} seconds")
        return result

    return wrapper


def repeat(times):
    """
    A decorator factory that repeats a function call N times.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                print(f"[REPEAT] Run {i + 1}/{times}")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


# -------------------------
# Example usage
# -------------------------

@log_call
def greet(name):
    print(f"Hello, {name}!")


@measure_time
def slow_add(a, b):
    time.sleep(0.5)
    return a + b


@repeat(3)
def say_hi():
    print("Hi!")


# ---------------------------------------------------------------------------
# Example usage (requires a running browser / server to execute for real)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    greet("Weipeng")
    print(slow_add(3, 5))
    say_hi()

    from playwright.async_api import async_playwright


    # --- Async example ---
    @wait_for_visible("#hero-heading", timeout=10_000)
    async def scrape_heading(page: Page) -> str:
        return await page.inner_text("#hero-heading")


    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("https://example.com")
            heading = await scrape_heading(page)
            print("Heading:", heading)
            await browser.close()


    asyncio.run(main())
