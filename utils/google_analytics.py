import json
from typing import List, Dict, Any

class GoogleAnalyticsTracker:
    """
    Utility class to capture and validate Google Analytics (GA4) events
    from Playwright network logs.

    Usage:
    import pytest
    from utils.google_analytics import GoogleAnalyticsTracker

    Add fixture in conftest.py
    @pytest.fixture
    def ga_tracker(page):
        tracker = GoogleAnalyticsTracker()
        tracker.attach_listener(page)
        return tracker

    Use in a test
    def test_ga_event_on_login(page, ga_tracker):
        page.goto("https://your-app.com/login")
        page.fill("#username", "test")
        page.fill("#password", "password")
        page.click("#login-btn")

        # Example: assert GA event fired
        ga_tracker.assert_event("login_success")

        # Example: assert parameter
        ga_tracker.assert_event_param("login_success", "method", "password")
    """

    GA_ENDPOINTS = [
        "https://www.google-analytics.com/g/collect",
        "https://www.google-analytics.com/mp/collect",
        "https://analytics.google.com/g/collect",
    ]

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def attach_listener(self, page):
        """
        Attach a Playwright network listener to capture GA events.
        """
        page.on("request", self._capture_request)

    def _capture_request(self, request):
        """
        Internal: capture GA requests and extract event data.
        """
        url = request.url

        if not any(endpoint in url for endpoint in self.GA_ENDPOINTS):
            return

        payload = {}

        # GA4 sends data via query params OR POST body
        if request.method == "GET":
            payload = request.url.split("?")[-1]
            payload = dict(item.split("=") for item in payload.split("&") if "=" in item)

        elif request.method == "POST":
            try:
                body = request.post_data
                payload = json.loads(body) if body else {}
            except Exception:
                payload = {"raw_body": request.post_data}

        self.events.append({
            "url": url,
            "method": request.method,
            "payload": payload
        })

    def get_events(self) -> List[Dict[str, Any]]:
        """
        Return all captured GA events.
        """
        return self.events

    def find_event(self, event_name: str) -> List[Dict[str, Any]]:
        """
        Return all GA events matching a specific event name.
        GA4 event name is usually in parameter 'en' or 'event_name'.
        """
        results = []
        for event in self.events:
            payload = event["payload"]
            if payload.get("en") == event_name or payload.get("event_name") == event_name:
                results.append(event)
        return results

    def assert_event(self, event_name: str):
        """
        Assert that a GA event was fired.
        """
        events = self.find_event(event_name)
        assert events, f"Google Analytics event '{event_name}' was NOT fired"
        return events

    def assert_event_param(self, event_name: str, param: str, expected_value: str):
        """
        Assert that a GA event contains a specific parameter.
        """
        events = self.find_event(event_name)
        assert events, f"Event '{event_name}' not found"

        for event in events:
            payload = event["payload"]
            if payload.get(param) == expected_value:
                return True

        raise AssertionError(
            f"Event '{event_name}' does not contain param '{param}' "
            f"with value '{expected_value}'"
        )
