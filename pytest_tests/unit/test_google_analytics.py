import json

import pytest

from utils.integrations.google_analytics import GoogleAnalyticsTracker


class FakePage:
    def __init__(self):
        self.listeners = {}

    def on(self, event_name, callback):
        self.listeners[event_name] = callback


class FakeRequest:
    def __init__(self, url, method="GET", post_data=None):
        self.url = url
        self.method = method
        self.post_data = post_data


@pytest.mark.unit
def test_tracker_can_attach_during_construction():
    page = FakePage()

    tracker = GoogleAnalyticsTracker(page)

    assert page.listeners["request"] == tracker.capture_request


@pytest.mark.unit
def test_tracker_captures_get_event_and_finds_it():
    tracker = GoogleAnalyticsTracker()
    request = FakeRequest(
        "https://www.google-analytics.com/g/collect?en=purchase&ep.value=42"
    )

    tracker.capture_request(request)

    assert tracker.find_event("purchase")[0]["payload"] == {
        "en": "purchase",
        "ep.value": "42",
    }


@pytest.mark.unit
def test_tracker_captures_post_event_and_asserts_parameter():
    tracker = GoogleAnalyticsTracker()
    request = FakeRequest(
        "https://www.google-analytics.com/mp/collect",
        method="POST",
        post_data=json.dumps({"event_name": "login", "method": "email"}),
    )

    tracker.capture_request(request)

    assert tracker.assert_event_param("login", "method", "email") is True


@pytest.mark.unit
def test_tracker_ignores_non_analytics_and_handles_invalid_post_payload():
    tracker = GoogleAnalyticsTracker()

    tracker.capture_request(FakeRequest("https://example.com/page"))
    tracker.capture_request(
        FakeRequest(
            "https://analytics.google.com/g/collect",
            method="POST",
            post_data="not-json",
        )
    )

    assert len(tracker.get_events()) == 1
    assert tracker.get_events()[0]["payload"] == {"raw_body": "not-json"}


@pytest.mark.unit
def test_tracker_assert_event_reports_missing_event():
    tracker = GoogleAnalyticsTracker()

    with pytest.raises(AssertionError, match="'purchase' was NOT fired"):
        tracker.assert_event("purchase")