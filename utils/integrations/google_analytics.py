"""Google Analytics event capture for Playwright network requests."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qsl, urlsplit


class GoogleAnalyticsTracker:
    """Capture and validate GA4 events emitted by a Playwright page."""

    GA_ENDPOINTS = (
        "https://www.google-analytics.com/g/collect",
        "https://www.google-analytics.com/mp/collect",
        "https://analytics.google.com/g/collect",
    )

    def __init__(self, page: Any | None = None):
        self.events: list[dict[str, Any]] = []
        if page is not None:
            self.attach(page)

    def attach(self, page: Any) -> None:
        """Start capturing requests from a Playwright-compatible page."""

        page.on("request", self.capture_request)

    def attach_listener(self, page: Any) -> None:
        """Backward-compatible alias for :meth:`attach`."""

        self.attach(page)

    def capture_request(self, request: Any) -> None:
        """Capture one Playwright-compatible request when it is a GA request."""

        if not any(endpoint in request.url for endpoint in self.GA_ENDPOINTS):
            return

        payload: dict[str, Any]
        if request.method == "GET":
            payload = dict(parse_qsl(urlsplit(request.url).query, keep_blank_values=True))
        elif request.method == "POST":
            try:
                decoded_payload = json.loads(request.post_data or "{}")
                payload = decoded_payload if isinstance(decoded_payload, dict) else {"data": decoded_payload}
            except Exception:
                payload = {"raw_body": request.post_data or ""}
        else:
            payload = {}

        self.events.append(
            {"url": request.url, "method": request.method, "payload": payload}
        )

    def get_events(self) -> list[dict[str, Any]]:
        return list(self.events)

    def clear_events(self) -> None:
        """Discard captured events so the tracker can be reused."""

        self.events.clear()

    def find_event(self, event_name: str) -> list[dict[str, Any]]:
        return [
            event
            for event in self.events
            if event["payload"].get("en") == event_name
            or event["payload"].get("event_name") == event_name
        ]

    def assert_event(self, event_name: str) -> list[dict[str, Any]]:
        events = self.find_event(event_name)
        assert events, f"Google Analytics event '{event_name}' was NOT fired"
        return events

    def assert_event_param(self, event_name: str, param: str, expected_value: str) -> bool:
        events = self.find_event(event_name)
        assert events, f"Event '{event_name}' not found"
        if any(event["payload"].get(param) == expected_value for event in events):
            return True
        raise AssertionError(
            f"Event '{event_name}' does not contain param '{param}' with value '{expected_value}'"
        )
