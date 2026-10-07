"""API tests for the intelligence source and item endpoints."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


def valid_source_payload(**overrides: Any) -> dict[str, Any]:
    """Return a schema-valid intelligence source payload."""
    payload: dict[str, Any] = {
        "name": "财联社电报",
        "url": "https://feeds.example.test/feed.xml",
        "source_type": "rss",
        "enabled": True,
        "scope_type": "market",
        "market": "cn",
        "description": "API suite fixture source",
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def create_source(api_client: TestClient) -> Callable[..., dict[str, Any]]:
    """Create an intelligence source and return the stored item."""

    def _create(**overrides: Any) -> dict[str, Any]:
        response = api_client.post(
            "/api/v1/intelligence/sources", json=valid_source_payload(**overrides)
        )
        assert response.status_code == 200, response.text
        return response.json()

    return _create


class TestCreateIntelligenceSource(BaseAPITest):
    """``POST /api/v1/intelligence/sources``."""

    ENDPOINT = "/api/v1/intelligence/sources"
    METHOD = "post"

    def test_creates_source(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A valid payload is persisted and echoed back with an id."""
        response = api_client.post(self.ENDPOINT, json=valid_source_payload())

        body = self.assert_matches_spec(api_spec, response)
        assert body["id"] > 0
        assert body["name"] == "财联社电报"
        assert body["source_type"] == "rss"
        assert body["enabled"] is True

    def test_applies_documented_defaults(self, api_client: TestClient) -> None:
        """Omitted optional fields fall back to the documented defaults."""
        body = self.assert_ok(
            api_client.post(
                self.ENDPOINT, json={"name": "默认源", "url": "https://feeds.example.test/a.xml"}
            )
        )

        assert body["source_type"] == "rss"
        assert body["scope_type"] == "market"
        assert body["market"] == "cn"
        assert body["enabled"] is True

    def test_rejects_missing_required_fields(self, api_client: TestClient) -> None:
        """``name`` and ``url`` are required."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_validation_error(response)
        missing = {entry["loc"][-1] for entry in body["detail"]}
        assert {"name", "url"} <= missing

    @pytest.mark.parametrize(
        ("overrides", "field"),
        [
            ({"source_type": "json"}, "source_type"),
            ({"scope_type": "industry"}, "scope_type"),
            ({"market": "eu"}, "market"),
            ({"name": ""}, "name"),
            ({"url": ""}, "url"),
            ({"name": "x" * 101}, "name"),
        ],
    )
    def test_rejects_values_outside_the_schema(
        self, api_client: TestClient, overrides: dict[str, Any], field: str
    ) -> None:
        """Enumerations and length limits documented in api_spec.json are enforced."""
        response = api_client.post(self.ENDPOINT, json=valid_source_payload(**overrides))

        self.assert_validation_error(response, field=field)

    @pytest.mark.parametrize(
        "url",
        [
            "ftp://feeds.example.test/feed.xml",
            "not-a-url",
            "https://user:pass@feeds.example.test/feed.xml",
            "http://127.0.0.1/feed.xml",
            "http://localhost/feed.xml",
            "http://192.168.1.10/feed.xml",
            "http://internal.local/feed.xml",
        ],
    )
    def test_rejects_unsafe_source_urls(self, api_client: TestClient, url: str) -> None:
        """The SSRF guard rejects non-http(s), credentialed and private-network URLs."""
        response = api_client.post(self.ENDPOINT, json=valid_source_payload(url=url))

        self.assert_error(response, 400, "validation_error")


class TestListIntelligenceSources(BaseAPITest):
    """``GET /api/v1/intelligence/sources``."""

    ENDPOINT = "/api/v1/intelligence/sources"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """No configured sources yields an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["page_size"] == 50

    def test_lists_created_sources(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_source: Callable[..., dict[str, Any]],
    ) -> None:
        """Created sources appear in the listing."""
        source = create_source()

        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 1
        assert body["items"][0]["id"] == source["id"]

    def test_filters_by_enabled_flag(
        self, api_client: TestClient, create_source: Callable[..., dict[str, Any]]
    ) -> None:
        """``enabled`` selects only sources in the requested state."""
        create_source(name="启用源", url="https://feeds.example.test/on.xml")
        create_source(name="停用源", url="https://feeds.example.test/off.xml", enabled=False)

        enabled = self.assert_ok(api_client.get(self.ENDPOINT, params={"enabled": "true"}))
        disabled = self.assert_ok(api_client.get(self.ENDPOINT, params={"enabled": "false"}))

        assert [item["name"] for item in enabled["items"]] == ["启用源"]
        assert [item["name"] for item in disabled["items"]] == ["停用源"]

    def test_filters_by_market(
        self, api_client: TestClient, create_source: Callable[..., dict[str, Any]]
    ) -> None:
        """``market`` narrows the listing."""
        create_source(market="cn")
        create_source(name="US feed", url="https://feeds.example.test/us.xml", market="us")

        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"market": "us"}))

        assert body["total"] == 1
        assert body["items"][0]["market"] == "us"

    @pytest.mark.parametrize(
        ("field", "value"), [("page", 0), ("page_size", 0), ("page_size", 101)]
    )
    def test_rejects_invalid_pagination(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Pagination bounds documented in api_spec.json are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestIntelligenceSourceTemplates(BaseAPITest):
    """``GET /api/v1/intelligence/sources/templates``."""

    ENDPOINT = "/api/v1/intelligence/sources/templates"
    METHOD = "get"

    def test_returns_builtin_templates(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """The built-in catalogue is always available."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == len(body["items"]) > 0
        for template in body["items"]:
            assert template["template_id"]
            assert template["url"]

    def test_filters_by_market(self, api_client: TestClient) -> None:
        """``market`` narrows the catalogue to one market."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"market": "cn"}))

        assert {template["market"] for template in body["items"]} <= {"cn"}

    def test_unknown_filter_returns_empty_catalogue(self, api_client: TestClient) -> None:
        """A filter without matches returns an empty list rather than an error."""
        body = self.assert_ok(
            api_client.get(self.ENDPOINT, params={"source_type": "carrier-pigeon"})
        )

        assert body == {"items": [], "total": 0}


class TestCreateSourceFromTemplate(BaseAPITest):
    """``POST /api/v1/intelligence/sources/templates/{template_id}``."""

    ENDPOINT = "/api/v1/intelligence/sources/templates/{template_id}"
    METHOD = "post"

    def test_creates_source_from_template(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A catalogue entry can be materialized into a stored source."""
        template = self.assert_ok(api_client.get("/api/v1/intelligence/sources/templates"))[
            "items"
        ][0]

        response = api_client.post(
            f"/api/v1/intelligence/sources/templates/{template['template_id']}", json={}
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["id"] > 0
        assert body["url"] == template["url"]

    def test_overrides_template_fields(self, api_client: TestClient) -> None:
        """Supplied overrides win over the template defaults."""
        template = self.assert_ok(api_client.get("/api/v1/intelligence/sources/templates"))[
            "items"
        ][0]

        body = self.assert_ok(
            api_client.post(
                f"/api/v1/intelligence/sources/templates/{template['template_id']}",
                json={"name": "自定义名称", "enabled": False},
            )
        )

        assert body["name"] == "自定义名称"
        assert body["enabled"] is False

    def test_returns_404_for_unknown_template(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An unknown template id reports a documented ``404``."""
        response = api_client.post(
            "/api/v1/intelligence/sources/templates/no-such-template", json={}
        )

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestCreateDefaultSources(BaseAPITest):
    """``POST /api/v1/intelligence/sources/defaults``."""

    ENDPOINT = "/api/v1/intelligence/sources/defaults"
    METHOD = "post"

    def test_creates_builtin_defaults(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """The first call materializes every built-in default source."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == len(body["items"]) > 0
        assert body["created_count"] == body["total"]
        assert all(result["created"] is True for result in body["items"])

    def test_is_idempotent(self, api_client: TestClient) -> None:
        """A repeated call creates nothing new."""
        first = self.assert_ok(api_client.post(self.ENDPOINT, json={}))

        second = self.assert_ok(api_client.post(self.ENDPOINT, json={}))

        assert second["total"] == first["total"]
        assert second["created_count"] == 0

    def test_enabled_override_is_applied(self, api_client: TestClient) -> None:
        """``enabled`` overrides the per-template default state."""
        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"enabled": False}))

        assert all(result["source"]["enabled"] is False for result in body["items"])


class TestFetchIntelligenceSource(BaseAPITest):
    """``POST /api/v1/intelligence/sources/{source_id}/fetch``."""

    ENDPOINT = "/api/v1/intelligence/sources/{source_id}/fetch"
    METHOD = "post"

    def test_returns_404_for_unknown_source(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A missing source is rejected before any network call is attempted."""
        response = api_client.post("/api/v1/intelligence/sources/999999/fetch")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_non_integer_source_id(self, api_client: TestClient) -> None:
        """``source_id`` must be an integer path parameter."""
        response = api_client.post("/api/v1/intelligence/sources/not-a-number/fetch")

        self.assert_validation_error(response, field="source_id")


class TestFetchEnabledSources(BaseAPITest):
    """``POST /api/v1/intelligence/sources/fetch-enabled``."""

    ENDPOINT = "/api/v1/intelligence/sources/fetch-enabled"
    METHOD = "post"

    def test_no_enabled_sources_is_a_successful_no_op(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """With nothing enabled the fail-open fetch reports zero work."""
        response = api_client.post(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["ok"] is True
        assert body["source_count"] == 0
        assert body["saved_count"] == 0

    def test_disabled_sources_are_skipped(
        self, api_client: TestClient, create_source: Callable[..., dict[str, Any]]
    ) -> None:
        """Disabled sources never participate in the batch fetch."""
        create_source(enabled=False)

        body = self.assert_ok(api_client.post(self.ENDPOINT))

        assert body["ok"] is True
        assert body["source_count"] == 0


class TestTestIntelligenceSourcePayload(BaseAPITest):
    """``POST /api/v1/intelligence/sources/test``."""

    ENDPOINT = "/api/v1/intelligence/sources/test"
    METHOD = "post"

    def test_rejects_missing_required_fields(self, api_client: TestClient) -> None:
        """The dry run validates the payload before contacting the source."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_validation_error(response)
        missing = {entry["loc"][-1] for entry in body["detail"]}
        assert {"name", "url"} <= missing

    @pytest.mark.parametrize(
        ("overrides", "field"),
        [
            ({"source_type": "json"}, "source_type"),
            ({"scope_type": "industry"}, "scope_type"),
            ({"market": "eu"}, "market"),
            ({"url": ""}, "url"),
        ],
    )
    def test_rejects_values_outside_the_schema(
        self, api_client: TestClient, overrides: dict[str, Any], field: str
    ) -> None:
        """Enumerations are enforced before the dry run starts."""
        response = api_client.post(self.ENDPOINT, json=valid_source_payload(**overrides))

        self.assert_validation_error(response, field=field)


class TestListIntelligenceItems(BaseAPITest):
    """``GET /api/v1/intelligence/items``."""

    ENDPOINT = "/api/v1/intelligence/items"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Without collected intelligence the listing is an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["page_size"] == 50

    @pytest.mark.parametrize(
        "params",
        [
            {"scope_type": "market"},
            {"scope_value": "cn"},
            {"market": "cn"},
            {"query": "茅台"},
            {"days": 7},
        ],
    )
    def test_accepts_documented_filters(
        self, api_client: TestClient, api_spec: dict[str, Any], params: dict[str, Any]
    ) -> None:
        """Every documented filter is accepted."""
        response = api_client.get(self.ENDPOINT, params=params)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0

    @pytest.mark.parametrize(
        ("field", "value"), [("page", 0), ("page_size", 0), ("page_size", 101), ("days", 0)]
    )
    def test_rejects_invalid_query_parameters(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Documented query bounds are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)
