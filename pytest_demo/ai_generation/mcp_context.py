from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BrowserSnapshot:
    """Normalized browser context used by the AI script generator."""

    url: str
    title: str
    dom: str
    element_tree: str
    screenshot_base64: str
    network_events: list[dict[str, str]]

    def to_mcp_payload(self) -> dict[str, Any]:
        """Expose snapshot data in an MCP-friendly resources/tools envelope."""
        return {
            "resources": {
                "page.url": self.url,
                "page.title": self.title,
                "page.dom": self.dom,
                "page.element_tree": self.element_tree,
                "page.screenshot_base64": self.screenshot_base64,
                "page.network_events": self.network_events,
            },
            "tools": [
                "get_dom",
                "get_element_tree",
                "get_screenshot",
                "get_network_events",
            ],
        }


class PlaywrightMCPContextCollector:
    """Collect page context from Playwright and shape it for AI generation."""

    def __init__(self, max_dom_chars: int = 12000):
        self.max_dom_chars = max_dom_chars
        self._network_events: list[dict[str, str]] = []

    def attach_network_listeners(self, page) -> None:
        def _on_request_finished(request) -> None:
            try:
                response = request.response()
                status = str(response.status) if response is not None else ""
            except Exception:
                status = ""

            self._network_events.append(
                {
                    "method": request.method,
                    "url": request.url,
                    "status": status,
                }
            )

        page.on("requestfinished", _on_request_finished)

    def collect(self, page) -> BrowserSnapshot:
        dom = (page.content() or "")[: self.max_dom_chars]
        element_tree = (
            page.evaluate("() => document.body ? document.body.innerHTML : ''") or ""
        )[: self.max_dom_chars]
        screenshot = page.screenshot(full_page=True)
        screenshot_base64 = base64.b64encode(screenshot).decode("ascii")

        return BrowserSnapshot(
            url=page.url,
            title=page.title(),
            dom=dom,
            element_tree=element_tree,
            screenshot_base64=screenshot_base64,
            network_events=self._network_events[-25:],
        )

