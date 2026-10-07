"""API tests for the stock import helpers (image extraction and file/text parsing)."""

from __future__ import annotations

import io
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6360000002000100ffff03000006000557bfabd400"
    "00000049454e44ae426082"
)


class TestExtractFromImage(BaseAPITest):
    """``POST /api/v1/stocks/extract-from-image``."""

    ENDPOINT = "/api/v1/stocks/extract-from-image"
    METHOD = "post"

    def test_rejects_missing_file(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A request without the ``file`` field never reaches the Vision model."""
        response = api_client.post(self.ENDPOINT)

        self.assert_error(response, 400, "bad_request")
        self.assert_documented_status(api_spec, response)

    @pytest.mark.parametrize(
        "content_type", ["text/plain", "application/pdf", "application/octet-stream"]
    )
    def test_rejects_unsupported_mime_types(
        self, api_client: TestClient, content_type: str
    ) -> None:
        """Only the documented image types are accepted."""
        files = {"file": ("upload.bin", io.BytesIO(b"not-an-image"), content_type)}

        response = api_client.post(self.ENDPOINT, files=files)

        self.assert_error(response, 400, "unsupported_type")

    def test_rejects_oversized_image(self, api_client: TestClient) -> None:
        """Images beyond the documented 5MB limit are rejected before inference."""
        oversized = io.BytesIO(b"\x00" * (5 * 1024 * 1024 + 1024))
        files = {"file": ("big.png", oversized, "image/png")}

        response = api_client.post(self.ENDPOINT, files=files)

        self.assert_error(response, 400, "file_too_large")

    def test_returns_extracted_codes(
        self, api_client: TestClient, api_spec: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A successful extraction is mapped onto the documented response."""
        import api.v1.endpoints.stocks as stocks_endpoint

        monkeypatch.setattr(
            stocks_endpoint,
            "extract_stock_codes_from_image",
            lambda data, content_type: ([("600519", "贵州茅台", "high")], "raw model output"),
        )
        files = {"file": ("shot.png", io.BytesIO(PNG_BYTES), "image/png")}

        response = api_client.post(self.ENDPOINT, files=files)

        body = self.assert_matches_spec(api_spec, response)
        assert body["codes"] == ["600519"]
        assert body["items"][0]["name"] == "贵州茅台"
        assert body["raw_text"] is None

    def test_include_raw_returns_model_output(
        self, api_client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``include_raw`` surfaces the raw model response."""
        import api.v1.endpoints.stocks as stocks_endpoint

        monkeypatch.setattr(
            stocks_endpoint,
            "extract_stock_codes_from_image",
            lambda data, content_type: ([("600519", None, "medium")], "raw model output"),
        )
        files = {"file": ("shot.png", io.BytesIO(PNG_BYTES), "image/png")}

        body = self.assert_ok(
            api_client.post(self.ENDPOINT, files=files, params={"include_raw": "true"})
        )

        assert body["raw_text"] == "raw model output"

    def test_extraction_failure_reports_400(
        self, api_client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A rejected image surfaces as a documented ``400``."""
        import api.v1.endpoints.stocks as stocks_endpoint

        def _raise(data: bytes, content_type: str) -> None:
            raise ValueError("无法识别图片内容")

        monkeypatch.setattr(stocks_endpoint, "extract_stock_codes_from_image", _raise)
        files = {"file": ("shot.png", io.BytesIO(PNG_BYTES), "image/png")}

        response = api_client.post(self.ENDPOINT, files=files)

        self.assert_error(response, 400, "extract_failed")


class TestParseImport(BaseAPITest):
    """``POST /api/v1/stocks/parse-import``."""

    ENDPOINT = "/api/v1/stocks/parse-import"
    METHOD = "post"

    def test_parses_pasted_text(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Pasted text yields the stock codes it contains."""
        response = api_client.post(self.ENDPOINT, json={"text": "600519 贵州茅台\n000858 五粮液"})

        body = self.assert_matches_spec(api_spec, response)
        assert "600519" in body["codes"]
        assert "000858" in body["codes"]

    def test_parses_uploaded_csv(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A CSV upload yields the stock codes it contains."""
        csv_bytes = "code,name\n600519,贵州茅台\n000858,五粮液\n".encode()
        files = {"file": ("watchlist.csv", io.BytesIO(csv_bytes), "text/csv")}

        response = api_client.post(self.ENDPOINT, files=files)

        body = self.assert_matches_spec(api_spec, response)
        assert "600519" in body["codes"]

    def test_rejects_missing_text(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A JSON body without ``text`` is rejected."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_error(response, 400, "bad_request")
        self.assert_documented_status(api_spec, response)

    def test_rejects_empty_text(self, api_client: TestClient) -> None:
        """An empty ``text`` value is treated as missing."""
        response = api_client.post(self.ENDPOINT, json={"text": ""})

        self.assert_error(response, 400, "bad_request")

    def test_rejects_non_string_text(self, api_client: TestClient) -> None:
        """``text`` must be a string."""
        response = api_client.post(self.ENDPOINT, json={"text": 600519})

        self.assert_error(response, 400, "bad_request")

    def test_rejects_unsupported_content_type(self, api_client: TestClient) -> None:
        """Only JSON bodies and multipart uploads are supported."""
        response = api_client.post(
            self.ENDPOINT, content=b"600519", headers={"content-type": "text/plain"}
        )

        self.assert_error(response, 400, "bad_request")

    def test_rejects_oversized_file(self, api_client: TestClient) -> None:
        """Uploads beyond the documented 2MB limit are rejected before parsing."""
        oversized = io.BytesIO(b"600519\n" * 400_000)
        files = {"file": ("huge.csv", oversized, "text/csv")}

        response = api_client.post(self.ENDPOINT, files=files)

        self.assert_error(response, 400, "file_too_large")
