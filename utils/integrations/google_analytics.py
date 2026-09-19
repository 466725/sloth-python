"""Google Analytics event capture for Playwright network requests."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qsl


class GoogleAnalyticsTracker:
    """Capture and validate GA4 events emitted by a Playwright page."""

    GA_ENDPOINTS = (
        "https://www.google-analytics.com/g/collect",
        "https://www.google-analytics.com/mp/collect",
        "https://analytics.google.com/g/collect",
    )

    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def attach_listener(self, page):
        page.on("request", self._capture_request)

    def _capture_request(self, request):
        if not any(endpoint in request.url for endpoint in self.GA_ENDPOINTS):
            return

        payload: dict[str, Any] | list[Any]
        if request.method == "GET":
            payload = dict(parse_qsl(request.url.split("?", 1)[-1]))
        elif request.method == "POST":
            try:
                payload = json.loads(request.post_data or "{}")
            except Exception:
                payload = {"raw_body": request.post_data}
        else:
            payload = {}

        self.events.append(
            {"url": request.url, "method": request.method, "payload": payload}
        )

    def get_events(self) -> list[dict[str, Any]]:
        return self.events

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
