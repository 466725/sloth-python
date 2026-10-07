"""API tests for the watchlist endpoints.

The suite environment seeds ``STOCK_LIST`` with ``600519,000858`` (see the
package ``conftest``), so every assertion here starts from that known baseline.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

SEEDED_CODES = ["600519", "000858"]
MALFORMED_CODES = ["   ", "12345678", "600519!", "600 519", "-600519"]


class TestGetWatchlist(BaseAPITest):
    """``GET /api/v1/stocks/watchlist``."""

    ENDPOINT = "/api/v1/stocks/watchlist"
    METHOD = "get"

    def test_returns_configured_codes(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """The watchlist mirrors the ``STOCK_LIST`` configuration."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["stock_codes"] == SEEDED_CODES
        assert str(len(SEEDED_CODES)) in body["message"]

    def test_reflects_subsequent_additions(self, api_client: TestClient) -> None:
        """A newly added code is visible on the next read."""
        self.assert_ok(
            api_client.post("/api/v1/stocks/watchlist/add", json={"stock_code": "601318"})
        )

        body = self.assert_ok(api_client.get(self.ENDPOINT))

        assert body["stock_codes"] == [*SEEDED_CODES, "601318"]


class TestAddToWatchlist(BaseAPITest):
    """``POST /api/v1/stocks/watchlist/add``."""

    ENDPOINT = "/api/v1/stocks/watchlist/add"
    METHOD = "post"

    def test_adds_new_code(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A valid code is appended to the watchlist."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": "601318"})

        body = self.assert_matches_spec(api_spec, response)
        assert body["stock_codes"] == [*SEEDED_CODES, "601318"]
        assert "601318" in body["message"]

    def test_adding_twice_does_not_duplicate(self, api_client: TestClient) -> None:
        """Re-adding an existing code keeps a single entry."""
        self.assert_ok(api_client.post(self.ENDPOINT, json={"stock_code": "601318"}))

        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"stock_code": "601318"}))

        assert body["stock_codes"].count("601318") == 1

    def test_adding_a_seeded_code_is_a_no_op(self, api_client: TestClient) -> None:
        """Codes already present are matched and left untouched."""
        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"stock_code": "600519"}))

        assert body["stock_codes"] == SEEDED_CODES

    def test_trims_surrounding_whitespace(self, api_client: TestClient) -> None:
        """Codes are stored without surrounding whitespace."""
        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"stock_code": "  601318  "}))

        assert "601318" in body["stock_codes"]

    @pytest.mark.parametrize("stock_code", MALFORMED_CODES)
    def test_rejects_malformed_codes(
        self, api_client: TestClient, api_spec: dict[str, Any], stock_code: str
    ) -> None:
        """Codes that do not match a supported market format are rejected."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": stock_code})

        self.assert_error(response, 400, "invalid_stock_code")
        self.assert_documented_status(api_spec, response)

    def test_rejects_empty_stock_code(self, api_client: TestClient) -> None:
        """``stock_code`` has a documented minimum length of one character."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": ""})

        self.assert_validation_error(response, field="stock_code")

    def test_rejects_missing_stock_code(self, api_client: TestClient) -> None:
        """``stock_code`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_validation_error(response, field="stock_code")


class TestRemoveFromWatchlist(BaseAPITest):
    """``POST /api/v1/stocks/watchlist/remove``."""

    ENDPOINT = "/api/v1/stocks/watchlist/remove"
    METHOD = "post"

    def test_removes_existing_code(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A watched code is removed from the list."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": "600519"})

        body = self.assert_matches_spec(api_spec, response)
        assert body["stock_codes"] == ["000858"]
        watchlist = self.assert_ok(api_client.get("/api/v1/stocks/watchlist"))
        assert watchlist["stock_codes"] == ["000858"]

    def test_removing_absent_code_is_a_no_op(self, api_client: TestClient) -> None:
        """Removing a code that is not watched succeeds without changing the list."""
        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"stock_code": "601318"}))

        assert body["stock_codes"] == SEEDED_CODES

    @pytest.mark.parametrize("stock_code", MALFORMED_CODES)
    def test_rejects_malformed_codes(self, api_client: TestClient, stock_code: str) -> None:
        """Removal validates the code format the same way as addition."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": stock_code})

        self.assert_error(response, 400, "invalid_stock_code")

    def test_rejects_empty_stock_code(self, api_client: TestClient) -> None:
        """``stock_code`` has a documented minimum length of one character."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": ""})

        self.assert_validation_error(response, field="stock_code")

    def test_rejects_missing_stock_code(self, api_client: TestClient) -> None:
        """``stock_code`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_validation_error(response, field="stock_code")
