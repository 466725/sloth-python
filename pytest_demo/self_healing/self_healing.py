from __future__ import annotations

import logging
from typing import Any

from pytest_demo.self_healing.dom_similarity import (
    find_similar_element,
    suggest_locator_from_candidate,
)
from pytest_demo.self_healing.element_finder import build_locator, find_element_with_fallback
from pytest_demo.self_healing.locator_store import update_primary_locator

logger = logging.getLogger(__name__)


def find_element(page, key: str, locator: dict[str, Any], auto_update: bool = True):
    try:
        return find_element_with_fallback(page, locator)
    except Exception as first_error:
        logger.warning(
            "Primary/fallback strategies failed for key=%s. Running DOM similarity scan.", key
        )

        expected = locator.get("expected") or {
            "text": locator.get("primary", {}).get("value", ""),
            "id": (
                locator.get("primary", {}).get("value", "")
                if locator.get("primary", {}).get("by") == "id"
                else ""
            ),
        }
        candidate, score = find_similar_element(page.content(), expected)

        if candidate is None or score < 0.45:
            logger.error("Self-healing failed for key=%s (score=%.2f).", key, score)
            raise first_error

        healed_locator = suggest_locator_from_candidate(candidate)
        logger.info(
            "Self-healing activated for key=%s. New locator: %s=%s (score=%.2f)",
            key,
            healed_locator["by"],
            healed_locator["value"],
            score,
        )

        if auto_update:
            update_primary_locator(key, healed_locator)
            logger.info("Updated locator store for key=%s", key)

        return build_locator(page, healed_locator)


def click(page, key: str, locator: dict[str, Any], auto_update: bool = True) -> None:
    element = find_element(page, key=key, locator=locator, auto_update=auto_update)
    try:
        element.click(timeout=8000)
    except Exception:
        logger.warning("Normal click failed for key=%s. Retrying with overlay-safe strategy.", key)
        try:
            page.keyboard.press("Escape")
        except Exception:  # pragma: no cover - defensive
            pass
        element.click(force=True, timeout=5000)
