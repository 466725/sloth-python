from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def _as_selector(strategy: dict[str, str]) -> tuple[str, str]:
    by = strategy["by"].strip().lower()
    value = strategy["value"].strip()

    if by == "id":
        return "css", f"#{value}"
    if by == "css":
        return "css", value
    if by == "xpath":
        return "xpath", value
    if by == "text":
        return "text", value

    raise ValueError(f"Unsupported locator strategy: {by}")


def _has_match(page, strategy: dict[str, str], timeout_ms: int = 1500) -> bool:
    kind, value = _as_selector(strategy)
    try:
        if kind == "css":
            page.wait_for_selector(value, timeout=timeout_ms)
            return True
        if kind == "xpath":
            page.wait_for_selector(f"xpath={value}", timeout=timeout_ms)
            return True
        if kind == "text":
            locator = page.get_by_text(value, exact=False).first
            return locator.count() > 0
    except Exception:
        return False

    return False


def build_locator(page, strategy: dict[str, str]):
    kind, value = _as_selector(strategy)
    if kind == "css":
        return page.locator(value).first
    if kind == "xpath":
        return page.locator(f"xpath={value}").first
    return page.get_by_text(value, exact=False).first


def find_element_with_fallback(page, locator: dict[str, Any]):
    strategies = [locator["primary"]] + locator.get("fallbacks", [])
    last_exception: Exception | None = None

    for i, strategy in enumerate(strategies):
        label = "primary" if i == 0 else f"fallback#{i}"
        logger.info("Trying %s locator: %s=%s", label, strategy["by"], strategy["value"])

        try:
            if _has_match(page, strategy):
                return build_locator(page, strategy)
        except Exception as exc:  # pragma: no cover - defensive log path
            last_exception = exc
            logger.warning("Locator attempt raised an exception: %s", exc)
            continue

        logger.warning("Locator %s failed: %s=%s", label, strategy["by"], strategy["value"])

    raise LookupError("Element not found using primary/fallback strategies") from last_exception
